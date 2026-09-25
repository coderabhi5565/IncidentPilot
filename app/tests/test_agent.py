from unittest.mock import MagicMock, patch

from app.agent.graph import graph


class MockPlanStep:
    def __init__(self, tool: str, purpose: str):
        self.tool = tool
        self.purpose = purpose


class MockPlan:
    steps = [
        MockPlanStep(
            "get_service_metrics",
            "Check whether the service error rate and latency increased.",
        ),
        MockPlanStep(
            "search_logs",
            "Inspect recent errors and timeouts.",
        ),
        MockPlanStep(
            "get_recent_deployments",
            "Check whether a recent deployment may be related to the incident.",
        ),
        MockPlanStep(
            "get_dependency_health",
            "Check whether a downstream dependency is degraded.",
        ),
    ]


class MockHypothesisItem:
    explanation = (
        "A degraded dependency is contributing to the checkout errors."
    )


class MockHypothesis:
    hypotheses = [MockHypothesisItem()]


def run_investigation(
    goal: str,
    scenario: str,
    failure_config: dict[str, int] | None = None,
) -> dict:
    initial_state = {
        "goal": goal,
        "scenario": scenario,
        "plan": [],
        "current_step": 0,
        "tool_executions": [],
        "evidence": [],
        "hypotheses": [],
        "validated_hypotheses": [],
        "evaluation_decision": None,
        "recovery_action": "none",
        "recovery_attempts": 0,
        "failures": [],
        "fallback_tool": None,
        "failure_config": failure_config or {},
        "events": [],
        "final_report": None,
    }

    planner_mock = MagicMock()
    planner_mock.invoke.return_value = MockPlan()

    hypothesis_mock = MagicMock()
    hypothesis_mock.invoke.return_value = MockHypothesis()

    evaluator_mock = MagicMock()

    evaluation_calls = 0

    def evaluator_side_effect(prompt):
        nonlocal evaluation_calls

        evaluation_calls += 1

        result = MagicMock()

        if evaluation_calls <= 4:
            result.decision = "continue"
        else:
            result.decision = "report"

        result.reason = (
            "The collected evidence is sufficient for the investigation."
        )

        result.validated_hypotheses = [
            "A degraded dependency is contributing to the checkout errors."
        ]

        return result

    evaluator_mock.invoke.side_effect = evaluator_side_effect

    with patch(
        "app.agent.planner.structured_llm",
        planner_mock,
    ), patch(
        "app.agent.hypothesis.structured_llm",
        hypothesis_mock,
    ), patch(
        "app.agent.evaluator.structured_llm",
        evaluator_mock,
    ):
        return graph.invoke(initial_state)


def test_database_degradation():
    result = run_investigation(
        goal="Investigate checkout error rate increase",
        scenario="database_degradation",
    )

    report = result["final_report"]

    assert report is not None
    assert len(report["key_findings"]) > 0
    assert len(report["execution_trace"]) > 0


def test_retry_and_fallback():
    result = run_investigation(
        goal="Investigate checkout error rate increase",
        scenario="database_degradation",
        failure_config={
            "get_service_metrics": 2,
        },
    )

    trace = result["final_report"]["execution_trace"]

    assert any(
        execution["status"] == "failed"
        for execution in trace
    )

    assert any(
        execution.get("recovery_action") == "retry"
        for execution in trace
    )

    assert any(
        execution.get("recovery_action") == "fallback"
        for execution in trace
    )


def test_ambiguous_incident_does_not_force_root_cause():
    result = run_investigation(
        goal="Investigate an unexplained checkout error increase",
        scenario="ambiguous_incident",
    )

    report = result["final_report"]

    assert report is not None
    assert len(report["key_findings"]) > 0
    assert "likely_root_cause" in report
    assert "unresolved_questions" in report


def test_bad_deployment():
    result = run_investigation(
        goal="Investigate checkout failures after a recent deployment",
        scenario="bad_deployment",
    )

    report = result["final_report"]

    assert report is not None
    assert len(report["key_findings"]) > 0
    assert "get_recent_deployments" in report["tools_used"]


def test_redis_outage():
    result = run_investigation(
        goal="Investigate checkout failures caused by Redis issues",
        scenario="redis_outage",
    )

    report = result["final_report"]

    assert report is not None
    assert len(report["key_findings"]) > 0


def test_payment_timeout():
    result = run_investigation(
        goal="Investigate checkout payment timeouts",
        scenario="payment_timeout",
    )

    report = result["final_report"]

    assert report is not None
    assert len(report["key_findings"]) > 0


def test_replan_after_repeated_failure():
    result = run_investigation(
        goal="Investigate checkout error rate increase",
        scenario="database_degradation",
        failure_config={
            "get_service_metrics": 2,
            "search_logs": 1,
        },
    )

    events = result["events"]

    assert "RECOVERY:REPLAN" in events
    assert "PLAN_CREATED" in events