from langchain_core.tools import tool
from app.tools.scenarios import get_current_scenario


@tool
def search_logs(
    service: str,
    query: str,
    time_range: str,
) -> dict:
    """Search service logs for the requested time range."""
    scenario = get_current_scenario()

    return {
        "service": service,
        "time_range": time_range,
        "query": query,
        "matches": scenario["logs"],
    }