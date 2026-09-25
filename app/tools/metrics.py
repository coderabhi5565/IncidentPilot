from langchain_core.tools import tool
from app.tools.scenarios import get_current_scenario


@tool
def get_service_metrics(service: str, time_range: str) -> dict:
    """Fetch service metrics for the requested time range."""
    scenario = get_current_scenario()
    metrics = scenario["metrics"]

    return {
        "service": service,
        "time_range": time_range,
        "error_rate": metrics["error_rate"],
        "baseline_error_rate": metrics["baseline_error_rate"],
        "request_rate": metrics["request_rate"],
        "latency_p95_ms": metrics["latency_p95_ms"],
    }