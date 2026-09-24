from app.agent.state import InvestigationState

from app.tools.metrics import get_service_metrics
from app.tools.logs import search_logs
from app.tools.deployments import get_recent_deployments
from app.tools.dependencies import get_dependency_health


TOOL_REGISTRY = {
    "get_service_metrics": get_service_metrics,
    "search_logs": search_logs,
    "get_recent_deployments": get_recent_deployments,
    "get_dependency_health": get_dependency_health,
}


def investigator_node(state: InvestigationState) -> dict:
    current_step = state["current_step"]
    plan = state["plan"]

    if current_step >= len(plan):
        return {}

    step = plan[current_step]

    tool_name = step["tool"]
    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        execution = {
            "tool": tool_name,
            "status": "failed",
            "error": f"Unknown tool: {tool_name}",
        }

        return {
            "tool_executions": state["tool_executions"] + [execution],
            "current_step": current_step + 1,
            "events": state["events"] + ["TOOL_NOT_FOUND"],
        }

    service = "checkout"

    if tool_name == "get_service_metrics":
        result = tool.invoke({
            "service": service,
            "time_range": "last_30_minutes",
        })

    elif tool_name == "search_logs":
        result = tool.invoke({
            "service": service,
            "query": "error OR exception OR timeout",
            "time_range": "last_30_minutes",
        })

    elif tool_name == "get_recent_deployments":
        result = tool.invoke({
            "service": service,
        })

    elif tool_name == "get_dependency_health":
        result = tool.invoke({
            "service": service,
        })

    else:
        raise ValueError(f"Unsupported tool: {tool_name}")

    execution = {
        "tool": tool_name,
        "status": "success",
        "result": result,
    }

    return {
        "tool_executions": state["tool_executions"] + [execution],
        "current_step": current_step + 1,
        "events": state["events"] + [f"TOOL_EXECUTED:{tool_name}"],
    }