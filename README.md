# IncidentPilot 🚨

> Autonomous Production Incident Investigation Agent

IncidentPilot is an AI-powered agent designed to investigate software
production incidents autonomously.

Given a high-level incident description, IncidentPilot decomposes the
problem into investigation steps, selects and executes relevant tools,
observes their results, handles tool failures, re-plans when necessary,
validates its findings, and generates a structured incident report.

The project focuses on practical Agentic AI engineering:
planning, tool orchestration, stateful workflows, failure recovery,
evidence-based reasoning, and agent evaluation.

---

## 🎯 Problem

When a production incident occurs, engineers usually have to manually
inspect multiple sources such as:

- Service metrics
- Application logs
- Deployment history
- Dependency health
- Infrastructure events

The investigation process can involve many steps and may require changing
the investigation strategy when information is missing or a diagnostic
source becomes unavailable.

IncidentPilot aims to automate this investigation workflow while keeping
the execution process visible and traceable.

---

## 💡 What IncidentPilot Does

A user provides a high-level incident goal such as:

> "Checkout service error rate has increased significantly during the
> last 30 minutes. Investigate the incident and identify the likely
> root cause."

IncidentPilot then:

1. Understands the investigation goal
2. Creates an explicit investigation plan
3. Executes investigation steps
4. Uses multiple diagnostic tools
5. Observes and stores tool results
6. Collects supporting evidence
7. Handles tool failures through recovery strategies
8. Re-plans when the available evidence is insufficient
9. Evaluates whether the investigation is complete
10. Generates an evidence-backed incident report

---

## 🏗️ High-Level Architecture

```text
                         User
                           │
                           ▼
                      FastAPI API
                           │
                           ▼
                  Investigation Manager
                           │
                           ▼
                       LangGraph
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Planner        Investigator       Evaluator
                           │                │
                           ▼                │
                    Tool Orchestrator       │
                           │                │
             ┌─────────────┼────────────┐   │
             ▼             ▼            ▼   │
          Metrics         Logs      Deployment
             │             │            │   │
             └─────────────┼────────────┘   │
                           │                │
                           ▼                │
                       Evidence ────────────┘
                           │
                           ▼
                        Reporter
                           │
                           ▼
                   Incident Report
🔄 Investigation Workflow
User Goal
    │
    ▼
Create Investigation
    │
    ▼
Generate Plan
    │
    ▼
Execute Investigation
    │
    ▼
Call Diagnostic Tools
    │
    ▼
Observe Results
    │
    ▼
Evaluate Evidence
    │
    ├───────────────┐
    │               │
    ▼               ▼
 Sufficient      Insufficient
 Evidence?       Evidence?
    │               │
   YES              NO
    │               │
    ▼               ▼
 Reporter        Re-plan
    │               │
    ▼               └──────► Investigation
 Report
Failure Flow
Tool Execution
      │
      ▼
   Failure
      │
      ▼
Recovery Manager
      │
      ├──► Retry
      │
      ├──► Fallback
      │
      └──► Re-plan
🧰 Investigation Tools

IncidentPilot will operate through dedicated investigation tools.

Metrics Tool

Retrieves service health and performance metrics.

Examples:

Error rate
Latency
CPU usage
Memory usage
Request volume
Log Analysis Tool

Searches application logs for relevant errors and patterns.

Deployment Tool

Retrieves recent deployments and configuration changes.

Dependency Health Tool

Checks the health of dependencies such as:

Database
Redis
Payment services
External APIs
🧠 Agent Capabilities
1. Planning

The agent creates an explicit investigation plan before taking action.

2. Tool Orchestration

The agent selects and invokes appropriate diagnostic tools based on
the investigation objective and previous observations.

3. Dynamic Investigation

The investigation is not restricted to a fixed sequence.

The agent can change its approach based on newly discovered evidence.

4. Failure Recovery

Tool failures are treated as part of the investigation environment.

The agent can:

Retry failed operations
Use alternative tools
Continue with partial information
Re-plan the investigation
5. Evidence-Based Findings

Important conclusions are connected to evidence collected during the
investigation.

6. Self-Evaluation

Before generating the final report, the agent evaluates whether the
available evidence is sufficient to support its conclusions.

7. Execution Trace

The system maintains a visible investigation trace containing events
such as:

PLAN_CREATED
TOOL_STARTED
TOOL_COMPLETED
TOOL_FAILED
RETRY_STARTED
FALLBACK_TRIGGERED
FINDING_DISCOVERED
REPLAN_TRIGGERED
HYPOTHESIS_VALIDATED
REPORT_GENERATED
🧪 Synthetic Investigation Environment

The project uses a controlled synthetic observability environment for
development and evaluation.

Example data sources:

data/
├── metrics/
├── logs/
├── deployments/
└── dependencies/

This allows the agent to be tested against deterministic incident
scenarios and controlled tool failures.

Example scenarios include:

Database degradation
Bad deployment
Redis outage
Payment dependency failure
Memory pressure
Ambiguous evidence
Metrics tool failure
Log analysis failure
🛡️ Failure Injection

IncidentPilot intentionally introduces failures during testing to
evaluate the agent's recovery behavior.

Example:

failure_injection:
  metrics_timeout: true
  logs_failure: false
  deployment_failure: false

Example execution:

Metrics Tool
     │
     ▼
  Timeout
     │
     ▼
   Retry
     │
     ▼
  Timeout
     │
     ▼
  Fallback
     │
     ▼
  Logs Tool
     │
     ▼
Continue Investigation
🧩 Design & Engineering

The project is being designed with modularity and separation of
responsibilities in mind.

Potential design concepts include:

SOLID principles
Strategy Pattern
State-based workflow
Dependency Injection
Tool abstractions
Event-driven execution tracing
Structured domain models

Design patterns will only be introduced where they solve an actual
engineering problem.

🛠️ Technology Stack
Core
Python
LangGraph
LangChain
Pydantic
FastAPI
Testing & Engineering
Pytest
Structured logging
Docker
Git
Storage
PostgreSQL (planned)
Redis (optional)
AI
LLM provider abstraction
Tool calling
Structured LLM outputs
📊 Evaluation

The project will be evaluated using multiple controlled incident
scenarios.

Potential evaluation metrics include:

Planning completion rate
Tool selection success
Investigation completion rate
Recovery success rate
Root-cause identification accuracy
Unsupported-claim rate
Number of tool calls
Investigation latency

Evaluation results will only be reported after being measured through
actual experiments.

🗺️ Development Roadmap
Phase 1 — Core Agent
 Domain model
 Synthetic incident data
 Investigation tools
 LangGraph state
 Planner
 Investigator
 Reporter
Phase 2 — Agentic Behavior
 Tool calling
 Dynamic planning
 Evidence collection
 Hypothesis validation
 Self-evaluation
 Re-planning
Phase 3 — Reliability
 Failure injection
 Retry mechanism
 Fallback strategies
 Graceful degradation
 Recovery orchestration
 Execution trace
Phase 4 — Engineering
 FastAPI
 Persistence
 Unit tests
 Integration tests
 Evaluation framework
 Docker
Phase 5 — Extensions
 Advanced observability
 LLM provider abstraction
 Investigation replay
 Cost and latency tracking
 Human approval checkpoints
 MCP-based tool integration
📁 Project Structure
incident-pilot/
│
├── app/
│   ├── api/
│   ├── agent/
│   ├── domain/
│   ├── tools/
│   ├── recovery/
│   ├── evaluation/
│   ├── infrastructure/
│   └── main.py
│
├── data/
│   ├── metrics/
│   ├── logs/
│   ├── deployments/
│   └── dependencies/
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── docker-compose.yml
🚀 Development Philosophy

IncidentPilot is being developed using a learning-first engineering
approach.

For every major component:

Understand the Problem
        ↓
Identify Required Concepts
        ↓
Learn the Concepts
        ↓
Design
        ↓
Implement
        ↓
Test
        ↓
Break
        ↓
Debug
        ↓
Improve

The goal is not to add technologies for the sake of complexity, but to
build a system whose architectural decisions are understandable,
justifiable, and testable.

📌 Project Status

🚧 Active Development

The project is currently in the initial architecture and core-agent
development phase.
