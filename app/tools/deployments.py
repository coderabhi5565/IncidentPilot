from langchain_core.tools import tool


@tool
def get_recent_deployments(service: str) -> dict:
    """
    Get recent deployments for a service.
    """
    return {
        "service": service,
        "deployments": [
            {
                "version": "checkout-v42",
                "timestamp": "10:35",
                "status": "success"
            }
        ]
    }