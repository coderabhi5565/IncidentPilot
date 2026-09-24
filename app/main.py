from app.agent.graph import graph


if __name__ == "__main__":
    initial_state = {
        "goal": (
            "Checkout service ka error rate last 30 minutes mein "
            "increase hua hai. Investigate the incident."
        ),
        "plan": [],
        "current_step": 0,
        "tool_executions": [],
        "evidence": [],
        "hypotheses": [],
        "evaluation_decision": None,
        "events": [],
        "final_report": None,
    }

    result = graph.invoke(initial_state)

    print("\n=== EVENTS ===")
    for event in result["events"]:
        print(event)

    print("\n=== PLAN ===")
    for step in result["plan"]:
        print(step)

    print("\n=== EVIDENCE ===")
    for item in result["evidence"]:
        print(item)

    print("\n=== HYPOTHESES ===")
    for hypothesis in result["hypotheses"]:
        print(hypothesis)

    print("\n=== FINAL REPORT ===")
    print(result["final_report"])