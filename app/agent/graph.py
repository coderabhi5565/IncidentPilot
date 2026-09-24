from langgraph.graph import StateGraph, START, END

from app.agent.state import InvestigationState
from app.agent.planner import planner_node
from app.agent.investigator import investigator_node


def should_continue(state: InvestigationState) -> str:
    if state["current_step"] < len(state["plan"]):
        return "investigator"

    return "end"


graph_builder = StateGraph(InvestigationState)

graph_builder.add_node("planner", planner_node)
graph_builder.add_node("investigator", investigator_node)

graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "investigator")

graph_builder.add_conditional_edges(
    "investigator",
    should_continue,
    {
        "investigator": "investigator",
        "end": END,
    }
)

graph = graph_builder.compile()