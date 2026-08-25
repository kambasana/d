---
title: Storage, Indexing, and Projection Architecture
document_id: AWG-PLAT-004
status: draft
version: 0.2.0
last_updated: '2026-08-20'
normative: true
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on:
- AWG-DOM-001
- AWG-PLAT-002
linear_issue: null
supersedes: []
---

# Storage, Indexing, and Projection Architecture

## Purpose

Define fit-for-purpose persistence for authoritative state, spatial data, events, analytics, graph projections, search, embeddings, media, and caches.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define fit-for-purpose persistence for authoritative state, spatial data, events, analytics, graph projections, search, embeddings, media, and caches.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for storage, indexing, and projection architecture.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Principle

The world graph is semantic, not a mandate for one database.

## Workload-oriented stores

Candidate separation:

- PostGIS: authoritative geometry/spatial queries.
- Relational transactional store: ownership, resources, organizations, structured current state.
- Append-only event store/object files: firehose/event history.
- Columnar analytical store (for example Parquet/DuckDB-style workflows): experiment analysis and replay queries.
- Graph projection/index: relationships, provenance, diffusion paths.
- Search index: text/entity retrieval.
- Vector index: semantic memory/search acceleration only.
- Blob/object storage: media, snapshots, large exports.

## Current state vs history

Current-state tables/read models are projections over validated transitions. Event history remains immutable except for retention policies that are explicitly governed.

## Index requirements

Support efficient queries by:

- world/scenario/branch/time;
- agent/place/organization;
- event/command type;
- claim/source/lineage;
- spatial bounding region;
- journey;
- social post/message;
- model/plugin version.

## Projection rebuild

Derived UI/analytics projections should be rebuildable from authoritative state/event sources where practical. Projection corruption must not rewrite world truth.

## Vector databases

Embedding indexes may retrieve memories/documents but do not own timestamp, identity, source provenance, contradiction status, or causal truth.

## Failure modes

- Silent divergence between authoritative state and projections.
- A plugin or model bypasses validation or provenance controls.
- A dependency failure produces fabricated success rather than an explicit degraded or failed state.
- A schema or terminology change is introduced without versioning and migration notes.

## Security and privacy considerations

- Apply least privilege to plugins, model providers, data stores, and operator actions.
- Treat model output, imported data, agent messages, and social content as untrusted input.
- Record audit events for privileged changes and protect sensitive data according to classification.

## Performance and scale considerations

- Use event-driven activation, batching, caching, and level-of-detail policies before increasing hardware cost.
- Measure latency, throughput, memory, storage growth, and degradation behaviour under representative load.
- Do not trade away correctness, causality, or provenance to improve benchmark numbers.

## Acceptance criteria

- The defined inputs, outputs, states, and failure paths are testable.
- Normative requirements are linked to stable requirement IDs and acceptance-test IDs.
- At least one valid example and one invalid example are documented or represented in executable fixtures.
- Offline and degraded-mode behaviour is explicit.
- No LLM or visualization component can override authoritative state.

## Related documents

- AWG-DOM-001
- AWG-PLAT-002
