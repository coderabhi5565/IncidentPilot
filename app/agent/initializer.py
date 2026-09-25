from app.agent.state import InvestigationState
from app.tools.failure_injector import failure_injector


def initialize_node(state: InvestigationState) -> dict:
    failure_injector.configure(
        state["failure_config"]
    )

    return {
        "events": state["events"] + [
            "FAILURE_INJECTOR_CONFIGURED"
        ]
    }