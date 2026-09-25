from typing import TypedDict


class InvestigationState(TypedDict):
    goal: str
    plan: list[dict]
    current_step: int
    tool_executions: list[dict]
    evidence: list[dict]
    hypotheses: list[str]
    validated_hypotheses: list[str]
    evaluation_decision: str | None
    scenario: str

    recovery_action: str | None
    recovery_attempts: int
    failures: list[dict]
    fallback_tool: str | None
    failure_config: dict[str, int]

    events: list[str]
    final_report: dict | None