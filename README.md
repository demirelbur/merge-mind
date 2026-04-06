# MergeMind: Agentic PR Review System

## 🚀 Project Goal

Build a **typed Agentic RAG system** for software development workflows that:

- Takes a **Pull Request (PR)** and its related **Product Backlog Item (PBI)**
- Retrieves relevant context from code, documentation, and historical PRs
- Produces a **structured review report** with:
  - Requirement alignment
  - Risks
  - Missing tests
  - Suggested review comments

---

## 🧠 One-Sentence Vision

> A developer submits a PR, the system links it to the PBI, gathers relevant evidence, reasons over it, and produces a trustworthy, structured review with traceable justification.

---

## Tree Structure

```text
merge-mind/
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── mergemind/
│       ├── __init__.py
│
│       # Entry points
│       ├── main.py              # FastAPI app
│       ├── cli.py               # CLI entry (optional but good)
│
│       # Core (config, settings, shared types)
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── constants.py
│
│       # Domain models (Pydantic)
│       ├── models/
│       │   ├── domain.py        # PBI, PR, ReviewReport
│       │   ├── api.py           # request/response schemas
│       │   └── state.py         # graph state
│
│       # Integrations (external systems)
│       ├── integrations/
│       │   ├── github.py
│       │   ├── jira.py          # or azure_devops.py
│       │   └── base.py
│
│       # Retrieval (RAG layer)
│       ├── retrieval/
│       │   ├── base.py
│       │   ├── docs.py
│       │   ├── code.py
│       │   ├── pr_history.py
│       │   └── orchestrator.py
│
│       # Agents (PydanticAI)
│       ├── agents/
│       │   ├── reviewer.py
│       │   ├── repairer.py
│       │   └── prompts.py
│
│       # Graph workflow (Pydantic Graph)
│       ├── graph/
│       │   ├── review_graph.py
│       │   └── nodes/
│       │       ├── load_pr.py
│       │       ├── resolve_pbi.py
│       │       ├── retrieve.py
│       │       ├── review.py
│       │       └── finalize.py
│
│       # Business logic layer
│       ├── services/
│       │   └── review_service.py
│
│       # API routes
│       ├── api/
│       │   ├── routes_reviews.py
│       │   └── deps.py
│
│       # Persistence layer
│       ├── db/
│       │   ├── session.py
│       │   ├── models.py
│       │   └── repositories/
│       │       ├── review_repo.py
│       │       └── document_repo.py
│
│       # Utilities
│       ├── utils/
│       │   └── text.py
│
├── tests/
│   ├── test_api.py
│   ├── test_agent.py
│   └── test_graph.py
│
└── docs/
```
