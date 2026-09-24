from typing import TypedDict


class InvestigationState(TypedDict):
    goal: str
    plan: list[dict]
    current_step: int
    tool_executions: list[dict]
    evidence: list[dict]
    hypotheses: list[str]
    evaluation_decision: str | None
    events: list[str]
    final_report: dict | None