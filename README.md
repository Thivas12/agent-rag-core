# AgentRAG Core

[![CI](https://github.com/Thivas12/agent-rag-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Thivas12/agent-rag-core/actions/workflows/ci.yml)

Typed contracts and evaluation primitives for auditable, real-time agentic RAG systems.

This repository is the shared foundation for three six-month portfolio flagships:

- **AtlasPulse** — real-time disruption intelligence from public hazard and infrastructure feeds.
- **RepairMesh** — observable multi-agent diagnosis and repair for software and data failures.
- **TransitTwin** — a multi-city transit digital twin using official GTFS-Realtime feeds.

## Why this repository exists

The three systems need the same language for events, retrieved evidence, agent actions, and
evaluation results. Defining that language once prevents incompatible payloads and makes every
decision traceable across service boundaries.

## Contracts

| Contract | Purpose |
|---|---|
| `Event` | Validated, source-neutral real-time event with a stable deduplication key. |
| `Evidence` | Retrieved content with URI provenance and automatic SHA-256 integrity checking. |
| `AgentAction` | Immutable audit record for a tool call or reasoning action. |
| `EvaluationRun` | Reproducible model, retrieval, or agent evaluation tied to data and code versions. |

All models reject unknown fields, require timezone-aware timestamps, and are immutable after
validation.

## Local development

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest --cov=agent_rag_core --cov-report=term-missing
```

Python 3.12 and dependency versions are pinned through `.python-version` and `uv.lock`.

## Current scope

Version `0.1.0` establishes the shared contracts and quality gate. The next vertical slice connects
AtlasPulse to the live USGS earthquake feed, passes validated events through a stream, persists the
raw source response, and exposes the result through FastAPI with OpenTelemetry traces.

See [`docs/portfolio-contract.md`](docs/portfolio-contract.md) for the hypotheses, constraints, and
definition of done governing the full programme.
