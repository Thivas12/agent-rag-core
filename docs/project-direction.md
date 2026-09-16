# Project direction

## Current work

AgentRAG Core currently defines strict records for events, retrieved evidence, agent actions, and
evaluation runs. The immediate goal is to keep those contracts small, testable, and useful without
claiming that unfinished runtime components already exist.

The released code provides:

- immutable Pydantic models that reject unknown fields;
- timezone-aware event and action timestamps;
- stable event deduplication keys;
- evidence hashes and URI provenance;
- explicit action lifecycle validation;
- reproducible evaluation metadata; and
- automated formatting, linting, typing, tests, and coverage checks.

## Engineering approach

- Add a component only when there is a concrete use for it.
- Keep provenance and failure states visible in public contracts.
- Prefer a small measured implementation over an untested architecture diagram.
- Describe planned features as plans until working code and tests exist.
- Avoid claims such as autonomous, production-ready, or real-time without supporting evidence.

## Planned next

1. Define typed retrieval requests, results, and citation records.
2. Add a deterministic evaluation harness for retrieval and bounded agent behaviour.
3. Add OpenTelemetry-compatible trace context to cross-service records.
4. Introduce explicit approval and policy records before enabling tool execution.

AtlasPulse is being developed separately. Reusable patterns may be moved into AgentRAG Core after
they have been exercised in a real integration and shown to be stable.

## Constraints

- Use public data and free or open-source tooling.
- Keep secrets, private evaluation data, and generated evidence out of Git.
- Preserve deterministic replay and content-addressed provenance where practical.
- Do not hide manual steps or publish unverifiable metrics.
