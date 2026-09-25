from typing import Literal

from fastapi import FastAPI, HTTPException
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
    scenario: Literal[
        "database_degradation",
        "bad_deployment",
        "redis_outage",
        "payment_timeout",
        "ambiguous_incident",
    ] = "database_degradation"
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
    allowed_tools = {
        "get_service_metrics",
        "search_logs",
        "get_recent_deployments",
        "get_dependency_health",
    }

    for tool_name, failures in request.failure_config.items():
        if tool_name not in allowed_tools:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown tool in failure_config: {tool_name}",
            )

        if failures < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Failure count cannot be negative: {tool_name}",
            )

    initial_state = {
        "goal": request.goal,
        "scenario": request.scenario,
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
    "plan": result["plan"],
    "report": result["final_report"],
    "trace": result["events"],
}