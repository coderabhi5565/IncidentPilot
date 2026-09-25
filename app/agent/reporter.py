from app.agent.state import InvestigationState

def reporter_node(state: InvestigationState) -> dict:
    evidence = state["evidence"]
    hypotheses = state["hypotheses"]
    failures = state["failures"]
    executions = state["tool_executions"]

    likely_root_cause = (
        hypotheses[-1]
        if hypotheses
        else "No root cause could be established from the available evidence."
    )

    recommended_actions = []

    for item in evidence:
        observation = item["observation"].lower()

        if "database" in observation or "postgres" in observation:
            recommended_actions.append(
                "Investigate database health, connection capacity, and query latency."
            )

        if "deployment" in observation:
            recommended_actions.append(
                "Review the recent deployment and compare its behavior with the previous version."
            )

        if "redis" in observation and "degraded" in observation:
            recommended_actions.append(
                "Investigate Redis availability and latency."
            )

    if not recommended_actions:
        recommended_actions.append(
            "Collect additional observability data before taking corrective action."
        )

    report = {
        "incident": state["goal"],
        "investigation_summary": (
            f"The investigation executed {len(executions)} tool operations "
            f"and collected {len(evidence)} evidence items."
        ),
        "key_findings": evidence,
        "likely_root_cause": likely_root_cause,
        "hypotheses": hypotheses,
        "tools_used": list(dict.fromkeys(
            execution["tool"]
            for execution in executions
        )),
        "failures_and_recovery": failures,
        "recommended_actions": list(dict.fromkeys(recommended_actions)),
        "unresolved_questions": [],
    }

    return {
        "final_report": report,
        "events": state["events"] + ["REPORT_GENERATED"],
    }