# AgentRAG Core

[![CI](https://github.com/Thivas12/agent-rag-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Thivas12/agent-rag-core/actions/workflows/ci.yml)

Typed contracts and evaluation primitives for auditable retrieval and agent systems.

AgentRAG Core is a self-directed engineering project focused on the small, stable building blocks
that retrieval and agent applications repeatedly need. The repository currently concentrates on
validated data contracts, provenance, immutability, and reproducible evaluation records.

## Why this repository exists

Retrieval and agent systems pass evidence and decisions across several boundaries. A shared,
strictly validated language for those records makes failures easier to inspect and experiments
easier to reproduce.

## What exists today

Version `0.1.0` provides four immutable Pydantic contracts with strict validation:

- stable event identities and deduplication keys;
- evidence records with URI provenance and SHA-256 integrity checks;
- auditable agent-action lifecycle records; and
- evaluation records tied to data, model, configuration, and code versions.

The repository also has pinned Python dependencies, strict typing, linting, automated tests, and a
GitHub Actions quality gate.

## Contracts

| Contract | Purpose |
|---|---|
| `Event` | Validated, source-neutral real-time event with a stable deduplication key. |
| `Evidence` | Retrieved content with URI provenance and automatic SHA-256 integrity checking. |
| `AgentAction` | Immutable audit record for a tool call or reasoning action. |
| `EvaluationRun` | Reproducible model, retrieval, or agent evaluation tied to data and code versions. |

All models reject unknown fields, require timezone-aware timestamps, and are immutable after
validation.

## Planned next

The next work is to add typed retrieval interfaces and a small evaluation harness around the
existing contracts. Telemetry and bounded tool execution are later plans, not released features.
Reusable patterns proven in AtlasPulse may move here when they are stable enough to share.

See [`docs/project-direction.md`](docs/project-direction.md) for the current boundaries and planned
order of work.

## Local development

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest --cov=agent_rag_core --cov-report=term-missing
```

Python 3.12 and dependency versions are pinned through `.python-version` and `uv.lock`.
