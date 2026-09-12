# Six-Month Portfolio Contract

## Mission

Build three public, continuously operating AI systems that demonstrate production engineering,
not isolated notebooks: **AtlasPulse**, **RepairMesh**, and **TransitTwin**. `agent-rag-core`
provides the contracts, retrieval, agent-audit, and evaluation primitives shared by all three.

## Product hypotheses

1. **AtlasPulse:** combining live public hazard and infrastructure feeds with provenance-aware
   retrieval can explain emerging disruptions earlier and more transparently than a static
   dashboard.
2. **RepairMesh:** a bounded multi-agent system with traces, evidence, replay, and approval gates
   can diagnose real software/data failures without hiding unsafe autonomous behaviour.
3. **TransitTwin:** a multi-city digital twin using official GTFS-Realtime data can quantify
   service reliability and test disruption-response policies using replayable evidence.

## Engineering contract

Every flagship must provide:

- A public HTTPS application and API using continuously refreshed public data.
- Schema validation, provenance, idempotency, retries, and late/missing-data handling.
- Deterministic replay from immutable raw snapshots.
- Automated tests, type checking, linting, CI/CD, and infrastructure as code.
- OpenTelemetry traces, service-health metrics, freshness monitoring, and documented failures.
- RAG and agent evaluations tied to versioned datasets, prompts, models, and Git commits.
- Backup, restore, rollback, degraded mode, and at least 30 days of operational evidence.

## Evidence bar

A feature is not complete because it works once. It is complete when its behaviour is tested,
observable, reproducible, documented, and demonstrated against real data. Each weekly release
must include a 60–120 second recording, updated metrics, one decision record, and one documented
failure or limitation.

## Constraints

- Six-month execution window: 14 September 2026 to 14 March 2027.
- Public data and free/open-source tools only; no required paid API or hosting dependency.
- Production starts with the smallest reliable architecture. Larger technologies are introduced
  in controlled lab comparisons and adopted only when measurements justify them.
- No inflated claims, unverifiable metrics, hidden manual steps, or notebook-only demos.
