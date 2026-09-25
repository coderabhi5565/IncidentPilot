from app.agent.state import InvestigationState
from app.tools.failure_injector import failure_injector
from app.tools.scenarios import set_current_scenario

def initialize_node(state: InvestigationState) -> dict:
    set_current_scenario(
        state["scenario"]
    )

    failure_injector.configure(
        state["failure_config"]
    )

    return {
        "events": state["events"] + [
            "SCENARIO_CONFIGURED",
            "FAILURE_INJECTOR_CONFIGURED",
        ]
    }