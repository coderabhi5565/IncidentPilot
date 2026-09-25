from typing import Literal

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.state import InvestigationState

from dotenv import load_dotenv

load_dotenv()

class EvaluationResult(BaseModel):
    decision: Literal["continue", "replan", "report"]
    reason: str = Field(
        description="Explain why this decision was made based on the evidence"
    )
    validated_hypotheses: list[str] = Field(
        description="Hypotheses that are sufficiently supported by the available evidence"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
)

structured_llm = llm.with_structured_output(EvaluationResult)


def evaluator_node(state: InvestigationState) -> dict:
    evidence = state["evidence"]
    hypotheses = state["hypotheses"]

    if not evidence:
        return {
            "events": state["events"] + ["EVALUATION_FAILED_NO_EVIDENCE"]
        }

    evidence_text = "\n".join(
        f"- {item['observation']}"
        for item in evidence
    )

    hypothesis_text = "\n".join(
        f"- {hypothesis}"
        for hypothesis in hypotheses
    )

    prompt = f"""
You are evaluating a production incident investigation.

Observed evidence:
{evidence_text}

Current hypotheses:
{hypothesis_text}

Decide what should happen next.

Decision meanings:
The validated_hypotheses field must contain only hypotheses supported by the observed evidence.

continue:
More evidence should be gathered using the existing investigation plan.

replan:
The current investigation is insufficient, blocked, or needs a different
investigation strategy.

report:
There is sufficient evidence to produce a final incident report.

Rules:
- Do not claim a root cause without supporting evidence.
- Consider contradictions and missing evidence.
- Prefer additional investigation when evidence is insufficient.
- If all planned investigation steps have been executed and the available evidence is sufficient, choose report.
- Do not choose continue when there are no remaining investigation steps.
- Identify which hypotheses are sufficiently supported by the available evidence.
- Only include a hypothesis as validated when multiple pieces of evidence support it or the evidence directly supports it.
- Do not validate a hypothesis when important contradictory evidence exists.
- If no hypothesis is sufficiently supported, return an empty validated_hypotheses list.
"""

    result = structured_llm.invoke(prompt)

    return {
    "evaluation_decision": result.decision,
    "validated_hypotheses": result.validated_hypotheses,
    "events": state["events"] + [f"EVALUATION:{result.decision.upper()}"],
}