from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import InvestigationState


load_dotenv()


class PlanStep(BaseModel):
    tool: Literal[
        "get_service_metrics",
        "search_logs",
        "get_recent_deployments",
        "get_dependency_health",
    ]
    purpose: str = Field(
        description="Why this tool should be used during the investigation"
    )


class InvestigationPlan(BaseModel):
    steps: list[PlanStep] = Field(
        description="Ordered investigation steps"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(
    InvestigationPlan
)


def planner_node(state: InvestigationState) -> dict:
    evidence_text = "\n".join(
        f"- {item['observation']}"
        for item in state["evidence"]
    )

    failure_text = "\n".join(
        f"- {failure['tool']}: {failure['error']}"
        for failure in state["failures"]
    )

    previous_plan_text = "\n".join(
        f"- {step['tool']}: {step['purpose']}"
        for step in state["plan"]
    )

    prompt = f"""
You are a production incident investigation planner.

Create an ordered investigation plan for this incident:

{state["goal"]}

Available tools:
- get_service_metrics
- search_logs
- get_recent_deployments
- get_dependency_health

Previous investigation plan:
{previous_plan_text or "No previous plan exists."}

Evidence already collected:
{evidence_text or "No evidence collected yet."}

Tool failures:
{failure_text or "No tool failures yet."}

Rules:
- Use only the available tools.
- Focus on gathering missing evidence.
- Do not diagnose the root cause yet.
- Do not unnecessarily repeat already completed investigation steps.
- If the previous investigation was blocked by a tool failure, choose an alternative evidence source when possible.
- Order the investigation logically.
- Return the investigation steps.
"""

    plan = structured_llm.invoke(prompt)

    return {
        "plan": [
            {
                "tool": step.tool,
                "purpose": step.purpose
            }
            for step in plan.steps
        ],
        "current_step": 0,
        "recovery_action": "none",
        "recovery_attempts": 0,
        "fallback_tool": None,
        "events": state["events"] + ["PLAN_CREATED"],
    }