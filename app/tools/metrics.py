from langchain_core.tools import tool


@tool
def get_service_metrics(service: str, time_range: str) -> dict:
    """
    Get service metrics for a given time range.
    """
    return {
        "service": service,
        "time_range": time_range,
        "error_rate": 18.2,
        "baseline_error_rate": 2.1,
        "request_rate": 1240,
        "latency_p95_ms": 840,
    }