from langchain_core.tools import tool
from app.tools.scenarios import get_current_scenario


@tool
def get_recent_deployments(service: str) -> dict:
    """Fetch recent deployments for a service."""
    scenario = get_current_scenario()

    return {
        "service": service,
        "deployments": scenario["deployments"],
    }