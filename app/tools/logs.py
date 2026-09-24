from langchain_core.tools import tool


@tool
def search_logs(service: str, query: str, time_range: str) -> dict:
    """
    Search application logs for a service.
    """
    return {
        "service": service,
        "time_range": time_range,
        "query": query,
        "matches": [
            {
                "timestamp": "10:42:13",
                "level": "ERROR",
                "message": "Database connection timeout"
            },
            {
                "timestamp": "10:42:27",
                "level": "ERROR",
                "message": "Failed to acquire database connection"
            }
        ]
    }