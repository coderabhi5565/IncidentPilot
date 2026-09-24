from app.agent.state import InvestigationState


def reporter_node(state: InvestigationState) -> dict:
    report = {
        "incident": state["goal"],
        "investigation_summary": (
            "The incident was investigated using the available "
            "observability tools."
        ),
        "key_findings": state["evidence"],
        "hypotheses": state["hypotheses"],
        "tools_used": [
            execution["tool"]
            for execution in state["tool_executions"]
        ],
        "failures_and_recovery": [],
        "recommended_actions": [],
        "unresolved_questions": [],
    }

    return {
        "final_report": report,
        "events": state["events"] + ["REPORT_GENERATED"],
    }