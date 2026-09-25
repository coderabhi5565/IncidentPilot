from langchain_core.tools import tool

from app.tools.scenarios import get_current_scenario


@tool
def get_dependency_health(service: str) -> dict:
    scenario = get_current_scenario()

    return {
        "service": service,
        "dependencies": scenario["dependencies"],
    }