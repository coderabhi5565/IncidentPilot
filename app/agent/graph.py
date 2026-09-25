from langgraph.graph import StateGraph, START, END

from app.agent.state import InvestigationState

from app.agent.planner import planner_node
from app.agent.investigator import investigator_node
from app.agent.evidence import evidence_node
from app.agent.hypothesis import hypothesis_node
from app.agent.evaluator import evaluator_node
from app.agent.reporter import reporter_node
from app.agent.initializer import initialize_node

def evaluation_router(state: InvestigationState) -> str:
    decision = state["evaluation_decision"]

    if (
        decision == "continue"
        and state["current_step"] >= len(state["plan"])
    ):
        return "report"

    return decision

def recovery_router(state: InvestigationState) -> str:
    return state["recovery_action"]

graph_builder = StateGraph(InvestigationState)


graph_builder.add_node("planner", planner_node)
graph_builder.add_node("investigator", investigator_node)
graph_builder.add_node("evidence", evidence_node)
graph_builder.add_node("hypothesis", hypothesis_node)
graph_builder.add_node("evaluator", evaluator_node)
graph_builder.add_node("reporter", reporter_node)
graph_builder.add_node("initialize", initialize_node)


graph_builder.add_edge(START, "initialize")
graph_builder.add_edge("initialize", "planner")

graph_builder.add_edge(
    "planner",
    "investigator",
)


graph_builder.add_conditional_edges(
    "investigator",
    recovery_router,
    {
        "none": "evidence",
        "retry": "investigator",
        "fallback": "investigator",
        "replan": "planner",
    },
)

graph_builder.add_edge(
    "evidence",
    "hypothesis",
)

graph_builder.add_edge(
    "hypothesis",
    "evaluator",
)

graph_builder.add_conditional_edges(
    "evaluator",
    evaluation_router,
    {
        "continue": "investigator",
        "replan": "planner",
        "report": "reporter",
    },
)

graph_builder.add_edge(
    "reporter",
    END,
)


graph = graph_builder.compile()