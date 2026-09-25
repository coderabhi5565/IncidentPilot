from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agent.graph import graph


app = FastAPI(
    title="IncidentPilot",
    description="Autonomous Production Incident Investigation Agent",
    version="1.0.0",
)


class InvestigationRequest(BaseModel):
    goal: str = Field(
        min_length=10,
        description="Natural-language production incident to investigate",
    )
    failure_config: dict[str, int] = Field(
        default_factory=dict,
        description="Optional deterministic tool failures for testing recovery",
    )


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "incidentpilot",
    }


@app.post("/api/v1/incidents/investigate")
def investigate_incident(
    request: InvestigationRequest,
) -> dict:
    initial_state = {
        "goal": request.goal,
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
        "failure_config": request.failure_config,
        "events": [],
        "final_report": None,
    }

    result = graph.invoke(initial_state)

    return {
        "status": "completed",
        "report": result["final_report"],
        "trace": result["events"],
    }