from typing import TypedDict


class InvestigationState(TypedDict):
    goal: str
    plan: list[dict]
    current_step: int
    tool_executions: list[dict]
    evidence: list[dict]
    hypotheses: list[str]
    events: list[str]
    final_report: dict | None