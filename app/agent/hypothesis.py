from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import InvestigationState


class Hypothesis(BaseModel):
    explanation: str = Field(
        description="A possible explanation for the incident"
    )


class HypothesisResponse(BaseModel):
    hypotheses: list[Hypothesis]


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(HypothesisResponse)


def hypothesis_node(state: InvestigationState) -> dict:
    evidence = state["evidence"]

    if not evidence:
        return {}

    evidence_text = "\n".join(
        f"- {item['observation']}"
        for item in evidence
    )

    prompt = f"""
You are a production incident investigator.

Based ONLY on the following observed evidence,
generate possible hypotheses that could explain the incident.

Evidence:
{evidence_text}

Rules:
- Do not treat hypotheses as confirmed facts.
- Do not invent evidence.
- Keep hypotheses specific and technically plausible.
- Generate only hypotheses supported by the available evidence.
"""

    response = structured_llm.invoke(prompt)

    hypotheses = [
        hypothesis.explanation
        for hypothesis in response.hypotheses
    ]

    return {
        "hypotheses": state["hypotheses"] + hypotheses,
        "events": state["events"] + ["HYPOTHESES_CREATED"],
    }