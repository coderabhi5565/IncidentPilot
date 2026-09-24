from app.agent.state import InvestigationState


def evidence_node(state: InvestigationState) -> dict:
    executions = state["tool_executions"]

    if not executions:
        return {}

    latest_execution = executions[-1]

    if latest_execution["status"] != "success":
        return {}

    tool_name = latest_execution["tool"]
    result = latest_execution["result"]

    evidence = []

    if tool_name == "get_service_metrics":
        evidence.append({
            "source": tool_name,
            "observation": (
                f"Error rate is {result['error_rate']}%, "
                f"compared with a baseline of {result['baseline_error_rate']}%."
            )
        })

        evidence.append({
            "source": tool_name,
            "observation": (
                f"P95 latency is {result['latency_p95_ms']} ms."
            )
        })

    elif tool_name == "search_logs":
        for match in result["matches"]:
            evidence.append({
                "source": tool_name,
                "observation": match["message"],
                "timestamp": match["timestamp"],
            })

    elif tool_name == "get_recent_deployments":
        for deployment in result["deployments"]:
            evidence.append({
                "source": tool_name,
                "observation": (
                    f"Deployment {deployment['version']} was deployed "
                    f"at {deployment['timestamp']}."
                ),
            })

    elif tool_name == "get_dependency_health":
        for name, dependency in result["dependencies"].items():
            evidence.append({
                "source": tool_name,
                "observation": (
                    f"{name} dependency is {dependency['status']} "
                    f"with latency {dependency['latency_ms']} ms."
                ),
            })

    return {
        "evidence": state["evidence"] + evidence,
        "events": state["events"] + ["EVIDENCE_EXTRACTED"],
    }