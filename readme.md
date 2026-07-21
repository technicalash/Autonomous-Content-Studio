# Autonomous Content Studio

An autonomous multi-agent AI system that plans, researches, generates, and continuously improves short-form educational content for social media.

The project is being built sprint-by-sprint with a modular Agentic AI architecture.

---

## Vision

Autonomous Content Studio aims to function as a complete AI content production pipeline.

Instead of using a single LLM prompt, multiple specialized AI agents collaborate to:

- Plan content ideas
- Research topics
- Generate scenarios
- Create scripts
- Produce media
- Review quality
- Learn from previous content

The long-term goal is to build a self-improving AI content studio capable of generating high-quality social media videos with minimal human intervention.

---

## Current Progress

### ✅ Sprint 1 — Planner Agent

Completed features:

- FastAPI backend
- Modular project architecture
- Gemini AI integration
- Planner Agent
- Structured LLM outputs using Pydantic
- SQLite database
- SQLAlchemy ORM
- Project persistence
- Plan persistence
- Memory Service
- Orchestrator
- Project Service
- Context-aware prompt generation
- Category selection strategy
- Duplicate topic avoidance using previous projects
- Exception handling
- Project status management

---

## Tech Stack

- Python
- FastAPI
- Gemini 2.5 Flash
- Agno Framework
- SQLAlchemy
- SQLite
- Pydantic

---

## Project Structure

```
backend/
│
├── agents/
├── api/
├── config/
├── database/
├── models/
├── schemas/
├── services/
├── prompts/
├── utils/
└── main.py
```

---

## Current Workflow

```
API
    │
    ▼
Orchestrator
    │
    ▼
Planner Agent
    │
    ▼
Gemini
    │
    ▼
ProjectPlan
    │
    ▼
Memory Service
    │
    ▼
Database
```

---

## Upcoming Sprints

- Sprint 2 — Research Agent
- Sprint 3 — Scenario Agent
- Sprint 4 — Storyboard Agent
- Sprint 5 — Media Generation Agent
- Sprint 6 — Reviewer Agent
- Sprint 7 — Analytics & Continuous Learning

---

## Status

🚧 Active Development
