from app.agent.state import InvestigationState

from app.tools.metrics import get_service_metrics
from app.tools.logs import search_logs
from app.tools.deployments import get_recent_deployments
from app.tools.dependencies import get_dependency_health
from app.tools.failure_injector import failure_injector

from app.recovery.manager import RecoveryManager


TOOL_REGISTRY = {
    "get_service_metrics": get_service_metrics,
    "search_logs": search_logs,
    "get_recent_deployments": get_recent_deployments,
    "get_dependency_health": get_dependency_health,
}


recovery_manager = RecoveryManager()


def build_tool_input(tool_name: str) -> dict:
    if tool_name == "get_service_metrics":
        return {
            "service": "checkout",
            "time_range": "last_30_minutes",
        }

    if tool_name == "search_logs":
        return {
            "service": "checkout",
            "query": "error OR exception OR timeout",
            "time_range": "last_30_minutes",
        }

    if tool_name == "get_recent_deployments":
        return {
            "service": "checkout",
        }

    if tool_name == "get_dependency_health":
        return {
            "service": "checkout",
        }

    raise ValueError(
        f"Unsupported tool: {tool_name}"
    )


def investigator_node(state: InvestigationState) -> dict:
    current_step = state["current_step"]
    plan = state["plan"]

    if current_step >= len(plan):
        return {}

    step = plan[current_step]
    purpose = step["purpose"]

    fallback_tool = state["fallback_tool"]

    if fallback_tool:
        tool_name = fallback_tool
    else:
        tool_name = step["tool"]

    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        failure = {
            "tool": tool_name,
            "error": f"Unknown tool: {tool_name}",
            "attempt": state["recovery_attempts"] + 1,
        }

        execution = {
            "tool": tool_name,
            "purpose": purpose,
            "status": "failed",
            "attempt": state["recovery_attempts"] + 1,
            "error": f"Unknown tool: {tool_name}",
            "recovery_action": "replan",
        }

        return {
            "tool_executions": state["tool_executions"] + [
                execution
            ],
            "failures": state["failures"] + [
                failure
            ],
            "recovery_action": "replan",
            "fallback_tool": None,
            "recovery_attempts": state["recovery_attempts"] + 1,
            "events": state["events"] + [
                "TOOL_NOT_FOUND",
                "RECOVERY:REPLAN",
            ],
        }

    try:
        failure_injector.check(tool_name)

        tool_input = build_tool_input(tool_name)

        result = tool.invoke(tool_input)

        execution = {
            "tool": tool_name,
            "purpose": purpose,
            "status": "success",
            "attempt": state["recovery_attempts"] + 1,
            "result": result,
        }

        return {
            "tool_executions": state["tool_executions"] + [
                execution
            ],
            "current_step": current_step + 1,
            "recovery_action": "none",
            "recovery_attempts": 0,
            "fallback_tool": None,
            "events": state["events"] + [
                f"TOOL_EXECUTED:{tool_name}"
            ],
        }

    except Exception as exc:
        attempts = state["recovery_attempts"]

        failure = {
            "tool": tool_name,
            "error": str(exc),
            "attempt": attempts + 1,
        }

        recovery = recovery_manager.recover(
            tool_name,
            {
                "attempts": attempts,
                "error": str(exc),
            },
        )

        recovery_action = recovery["action"]

        execution = {
            "tool": tool_name,
            "purpose": purpose,
            "status": "failed",
            "attempt": attempts + 1,
            "error": str(exc),
            "recovery_action": recovery_action,
        }

        return {
            "tool_executions": state["tool_executions"] + [
                execution
            ],
            "failures": state["failures"] + [
                failure
            ],
            "recovery_action": recovery_action,
            "recovery_attempts": attempts + 1,
            "fallback_tool": (
                recovery.get("tool")
                if recovery_action == "fallback"
                else None
            ),
            "events": state["events"] + [
                f"TOOL_FAILED:{tool_name}",
                f"RECOVERY:{recovery_action.upper()}",
            ],
        }