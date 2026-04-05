# MergeMind

## Pydantic Models

- agent input/output
- graph state
- API responses
- DB schema

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
