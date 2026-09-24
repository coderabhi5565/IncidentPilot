from typing import Literal

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import InvestigationState
from dotenv import load_dotenv

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

structured_llm = llm.with_structured_output(InvestigationPlan)


def planner_node(state: InvestigationState) -> dict:
    prompt = f"""
You are a production incident investigation planner.

Create an ordered investigation plan for this incident:

{state["goal"]}

Available tools:
- get_service_metrics
- search_logs
- get_recent_deployments
- get_dependency_health

Rules:
- Use only the available tools.
- Focus on gathering evidence.
- Do not diagnose the root cause yet.
- Order the investigation logically.
- Return the investigation steps.
"""

    plan = structured_llm.invoke(prompt)

    return {
        "plan": [
            {
                "tool": step.tool,
                "purpose": step.purpose,
            }
            for step in plan.steps
        ],
        "current_step": 0,
        "events": ["PLAN_CREATED"],
    }