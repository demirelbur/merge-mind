# Agentic PR Review System

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

## 🎯 v1 Scope (MVP)

### Feature: PR Review Agent with PBI Alignment

#### Input

- Repository
- PR URL or PR number
- Optional PBI ID

#### Output

- PR summary
- PBI summary
- Alignment score
- Covered acceptance criteria
- Missing acceptance criteria
- Risks
- Missing tests
- Suggested review comments
- Confidence score
- Evidence trace

---

## 👤 Target Users

### Primary

- Software developers reviewing PRs

### Secondary

- Tech leads
- Engineering managers
- QA engineers

---

## 🤖 What Makes It Agentic

The system is **not just RAG**, but an **agentic workflow**:

- Decides what information is missing
- Retrieves additional context dynamically
- Uses tools (code search, doc search, PR history)
- Adapts based on findings
- Produces confidence-aware output

---

## 🧱 Technology Stack

### Backend

- Python 3.12+
- FastAPI
- Pydantic v2
- Pydantic Settings

### Agent System

- PydanticAI (reasoning + tools)
- Pydantic Graph (workflow orchestration)

### Frontend

- Next.js (App Router)
- TypeScript

### Database

- PostgreSQL
- pgvector (for embeddings)

### Infrastructure

- Docker
- GitHub Actions (CI)
- uv (Python package manager)

### Observability

- OpenTelemetry

---

## 🏗️ Architecture Overview

### 1. API Layer

- Receives requests (manual + webhook)
- Handles orchestration trigger

### 2. Graph Layer (Pydantic Graph)

Workflow nodes:

- Load PR
- Resolve PBI
- Retrieve evidence
- Run reviewer agent
- Validate output
- Finalize response

### 3. Agent Layer (PydanticAI)

- Performs reasoning
- Produces structured output (`ReviewReport`)

### 4. Retrieval Layer

Sources:

- PR metadata and diff
- PBIs
- Documentation
- Historical PRs
- Code context

### 5. Persistence Layer

- Stores metadata, embeddings, and review results

---

## 📦 Data Sources (v1)

- GitHub PR (title, body, diff, files)
- Jira / Azure DevOps PBIs
- Repo documentation:
  - README
  - CONTRIBUTING
  - Architecture docs
- Historical PRs (small subset)

---

## 🧾 Core Domain Models

- `PBI`
- `PullRequest`
- `ChangedFile`
- `RetrievedChunk`
- `ReviewIssue`
- `ReviewComment`
- `ReviewReport`
- `ReviewState`
- `AppSettings`

---

## 🔍 Retrieval Strategy

Use **source-aware hybrid retrieval**:

### Retrieve

- Exact PBI
- PR content
- Changed files
- Relevant docs
- Top 3 similar PRs

### Search methods

- Metadata filters
- Keyword search
- Vector similarity

---

## 🔄 Workflow (v1)

1. User submits PR URL
2. Parse repo + PR
3. Load PR data
4. Resolve linked PBI
5. Retrieve relevant context
6. Run reviewer agent
7. Validate output
8. Return structured report
9. Display in UI

---

## 🖥️ Frontend Features

- PR input form
- Review results:
  - Summary
  - Alignment
  - Risks
  - Missing tests
  - Comments
- Evidence trace
- Confidence score

---

## 🚫 Non-Goals (v1)

- Auto-writing code
- Auto-merging PRs
- Multi-agent systems
- Full repo indexing
- IDE plugins
- Slack/Teams integration
- Multi-platform support

---

## 📁 Repository Structure

agentic-pr-review/
frontend/
app/
components/
lib/
backend/
app/
api/
core/
models/
integrations/
retrieval/
agents/
graph/
services/
db/
tests/
infra/
docker/
migrations/
docs/

---

## 🔧 Backend Modules

- `core/config.py`
- `models/domain.py`
- `models/api.py`
- `integrations/github.py`
- `integrations/jira.py` / `azure_devops.py`
- `retrieval/docs.py`
- `retrieval/code_context.py`
- `retrieval/pr_history.py`
- `agents/reviewer.py`
- `graph/review_graph.py`
- `api/routes_reviews.py`
- `services/review_service.py`

---

## 🌐 API Endpoints

- `POST /reviews/run`
- `GET /reviews/{id}`
- `POST /ingest/repo-docs`
- `POST /ingest/pr-history`
- `GET /health`

---

## 🗄️ Database Schema (Minimal)

- `repositories`
- `pull_requests`
- `pbis`
- `documents`
- `document_chunks`
- `review_runs`
- `review_comments`

---

## 🔐 Trust & Safety Rules

- Never hallucinate PBIs
- Lower confidence when uncertain
- Separate evidence from inference
- Always show sources
- No automatic PR commenting (v1)

---

## 📊 Evaluation Plan

### Product Metrics

- Review usefulness
- Developer satisfaction
- Time saved

### ML/RAG Metrics

- Retrieval relevance
- PBI linking accuracy
- False positive rate

### Engineering Metrics

- Output validation success
- Observability coverage
- System reliability

---

## 🛠️ Development Phases

### Phase 0: Setup

- Repo structure
- Tech stack
- Core models

### Phase 1: Basic PR Review

- Fetch PR
- Generate report (no RAG)

### Phase 2: Add PBI

- Link PR to PBI
- Add alignment analysis

### Phase 3: Add RAG

- Index docs and PRs
- Retrieve context

### Phase 4: Agentic Workflow

- Conditional retrieval
- Confidence-based logic

### Phase 5: Polish

- UI improvements
- Evidence trace
- Demo-ready system

---

## 📌 Final Definition

> A typed Agentic RAG system for reviewing pull requests in the context of PBIs, using structured reasoning, retrieval, and workflow orchestration to produce reliable and explainable software review insights.

---

## ✅ Next Steps

1. Create repo + structure
2. Implement core Pydantic models
3. Set up FastAPI + uv + Docker
4. Build PR fetch + basic review agent
5. Add PBI integration
6. Add retrieval layer
7. Implement graph workflow
