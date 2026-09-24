from langchain_core.tools import tool


@tool
def get_dependency_health(service: str) -> dict:
    """
    Get health information for service dependencies.
    """
    return {
        "service": service,
        "dependencies": {
            "postgres": {
                "status": "degraded",
                "latency_ms": 920
            },
            "redis": {
                "status": "healthy",
                "latency_ms": 4
            }
        }
    }