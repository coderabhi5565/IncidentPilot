# IncidentPilot

**Autonomous Production Incident Investigation Agent**

IncidentPilot is an agentic AI system that investigates backend production incidents using a stateful LangGraph workflow. Given a natural-language incident, it creates an investigation plan, gathers evidence from observability tools, generates hypotheses, evaluates the available evidence, handles tool failures, and produces a structured incident report.

## What It Does

Example input:

> Investigate the checkout error rate increase in the last 30 minutes.

IncidentPilot can:

- Decompose the incident into investigation steps
- Query metrics, logs, deployments, and dependency health
- Build structured evidence from tool results
- Generate and evaluate possible hypotheses
- Retry failed tools
- Use fallback evidence sources when available
- Re-plan when the current investigation strategy is insufficient
- Preserve uncertainty when evidence is not enough to establish a root cause
- Produce a structured investigation report

## Architecture

```text
Natural Language Incident
          |
          v
      Initializer
          |
          v
        Planner
          |
          v
      Investigator
          |
          v
     Observability Tools
          |
          v
       Evidence
          |
          v
      Hypotheses
          |
          v
       Evaluator
       /    |    \
      /     |     \
 Continue  Re-plan  Report
    |        |        |
    |        v        v
    |      Planner  Reporter
    |                 |
    +---------------->+
                      |
                Final Report

The workflow is implemented using LangGraph shared state and conditional routing.

Investigation Tools

IncidentPilot currently uses four observability tools:

Tool	Purpose
get_service_metrics	Checks error rate, baseline and latency
search_logs	Searches recent service errors and timeouts
get_recent_deployments	Checks recent deployments
get_dependency_health	Checks downstream dependency health

The tools operate on a deterministic synthetic observability environment.

Recovery

Tool failures are deliberately testable through a failure injector.

Tool Failure
     |
     v
   Retry
     |
     v
  Fallback
     |
     v
  Re-plan

The recovery manager selects a recovery strategy based on the failure history. A fallback is only used when another suitable evidence source exists; otherwise the investigation is re-planned.

Synthetic Scenarios

The project includes deterministic scenarios for:

Database degradation
Bad deployment
Redis outage
Payment provider timeout
Ambiguous incident

An additional failure configuration can be used to reproduce tool failures and test recovery behavior.

Example:

{
  "scenario": "database_degradation",
  "failure_config": {
    "get_service_metrics": 2
  }
}

This can be used to test retry and fallback behavior.

Investigation Flow

The agent separates observations from conclusions:

Tool Output
    ↓
Evidence
    ↓
Hypothesis
    ↓
Evaluation
    ↓
Validated Finding / Further Investigation

This prevents an LLM-generated hypothesis from automatically being treated as the confirmed root cause.

API

Start the application:

uvicorn app.main:app --reload

The API provides:

GET  /health
POST /api/v1/incidents/investigate

Swagger documentation is available at:

http://127.0.0.1:8000/docs

Example request:

{
  "goal": "Investigate checkout error rate increase",
  "scenario": "database_degradation",
  "failure_config": {}
}

The response contains the generated investigation plan, structured report, and execution trace.

Testing

The project includes automated tests covering:

Normal database degradation investigation
Retry and fallback recovery
Ambiguous incidents
Bad deployments
Redis outages
Payment timeouts
Re-planning after repeated tool failures

Run:

python -m pytest -q
Project Structure
app/
├── agent/
│   ├── graph.py
│   ├── initializer.py
│   ├── planner.py
│   ├── investigator.py
│   ├── evidence.py
│   ├── hypothesis.py
│   ├── evaluator.py
│   ├── reporter.py
│   └── state.py
│
├── tools/
│   ├── metrics.py
│   ├── logs.py
│   ├── deployments.py
│   ├── dependencies.py
│   ├── scenarios.py
│   └── failure_injector.py
│
├── recovery/
│   ├── manager.py
│   └── strategy.py
│
├── tests/
└── main.py
Design Decisions

The implementation separates planning, investigation, evidence extraction, hypothesis generation, evaluation, and reporting so each component has a focused responsibility.

A small Strategy-based recovery layer keeps retry, fallback, and re-planning independent from the investigation logic. A tool registry decouples the investigator from individual tool implementations.

The synthetic observability environment was designed to make incident scenarios and failures deterministic and reproducible.

Limitations
Observability data is synthetic rather than from real production systems.
The evaluation dataset is relatively small.
Formal precision/recall metrics were not measured.
The current system is a prototype rather than a production remediation system.
Real deployment would require stronger security, monitoring, persistent state, broader evaluation, and human approval for high-impact remediation.
Future Improvements

With more time, I would:

Integrate real monitoring and logging systems
Add persistent investigation checkpoints
Build a larger labeled incident evaluation set
Add systematic agent evaluation
Introduce human approval before production remediation actions
Project Artifacts

The submission includes:

Architecture diagram
Synthetic/test traces
Sample investigation transcripts
Monitoring report
Design decisions and limitations write-up
