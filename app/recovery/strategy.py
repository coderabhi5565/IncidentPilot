from abc import ABC, abstractmethod
from typing import Any


class RecoveryStrategy(ABC):

    @abstractmethod
    def execute(
        self,
        tool_name: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        pass


class RetryStrategy(RecoveryStrategy):

    def execute(
        self,
        tool_name: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "action": "retry",
            "tool": tool_name,
            "reason": "Retrying the failed tool execution.",
        }


class FallbackStrategy(RecoveryStrategy):

    def execute(
        self,
        tool_name: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        fallback_tools = {
            "get_service_metrics": "search_logs",
            "search_logs": "get_service_metrics",
            "get_dependency_health": "search_logs",
        }

        fallback_tool = fallback_tools.get(tool_name)

        return {
            "action": "fallback",
            "tool": fallback_tool,
            "reason": f"Using {fallback_tool} as an alternative evidence source.",
        }


class ReplanStrategy(RecoveryStrategy):

    def execute(
        self,
        tool_name: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "action": "replan",
            "tool": tool_name,
            "reason": "Current investigation path is insufficient; requesting a new plan.",
        }