from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import InvestigationState


class InvestigationPlan(BaseModel):
    steps: list[str] = Field(
        description="Ordered investigation steps required to investigate the incident"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(InvestigationPlan)


def planner_node(state: InvestigationState) -> dict:
    prompt = f"""
You are a production incident investigation planner.

Create an ordered investigation plan for the following incident:

{state["goal"]}

Rules:
- Focus on gathering evidence.
- Prefer concrete observability checks.
- Do not diagnose the root cause yet.
- Return only the investigation steps.
"""

    plan = structured_llm.invoke(prompt)

    return {
        "plan": plan.steps,
        "current_step": 0,
        "events": ["PLAN_CREATED"]
    }