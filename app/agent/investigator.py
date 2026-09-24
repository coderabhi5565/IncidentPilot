from app.agent.state import InvestigationState
from app.tools.metrics import get_service_metrics


def investigator_node(state: InvestigationState) -> dict:
    current_step = state["current_step"]
    plan = state["plan"]

    if current_step >= len(plan):
        return {}

    step = plan[current_step]

    if "metrics" in step.lower():
        result = get_service_metrics.invoke({
            "service": "checkout",
            "time_range": "last_30_minutes"
        })

        execution = {
            "tool": "get_service_metrics",
            "status": "success",
            "input": {
                "service": "checkout",
                "time_range": "last_30_minutes"
            },
            "result": result
        }

        return {
            "tool_executions": state["tool_executions"] + [execution],
            "current_step": current_step + 1,
            "events": state["events"] + ["METRICS_CHECKED"]
        }

    return {}