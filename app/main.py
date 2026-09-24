from app.agent.graph import graph


initial_state = {
    "goal": "Investigate increased error rate in checkout service",
    "plan": [],
    "current_step": 0,
    "tool_executions": [],
    "evidence": [],
    "hypotheses": [],
    "events": [],
    "final_report": None
}


result = graph.invoke(initial_state)

print("Final State:")
print(result)