---
title: Deployment Topologies and Offline Operation
document_id: AWG-PLAT-006
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
- AWG-PLAT-001
- AWG-PLAT-003
- AWG-PLAT-004
linear_issue: null
supersedes: []
---

# Deployment Topologies and Offline Operation

## Purpose

Define developer, single-machine offline, LAN, air-gapped, hybrid, distributed, and read-only analyst deployment modes.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define developer, single-machine offline, LAN, air-gapped, hybrid, distributed, and read-only analyst deployment modes.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for deployment topologies and offline operation.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Supported topology classes

### Developer workstation
Single machine, local OSM/PMTiles, local services, Ollama optional. Fast setup and debugging.

### Single-machine offline
All required scenario dependencies installed locally: PostGIS, gazetteer, routing data, PMTiles, simulation runtime, local model if AI is required.

### LAN/private cluster
Distributed simulation/services within a controlled local network. No public internet required.

### Air-gapped
No external network dependency. Data/model/plugin packages are pre-approved and imported through controlled media/processes.

### Hybrid AI
World/geospatial/state remain local while an approved AI adapter may call a remote provider such as OpenRouter. The run records what data crosses the boundary.

### Distributed/cloud
Horizontally scaled regions/services, managed storage/event buses, optional remote model providers.

### Analyst/read-only
Consumes event/projection exports without permissions to mutate scenario/world state.

## Offline bundle

A reproducible offline scenario package should identify:

- OSM extract/version;
- PostGIS import/migrations;
- Nominatim data/build;
- routing tiles/graphs;
- PMTiles;
- local elevation/building supplements if needed;
- models/quantization/runtime;
- plugin binaries/packages;
- scenario definition;
- seeds;
- validation/reference data;
- checksums and licences.

## Network policy

Core services should declare network requirements. "Offline" means required functionality does not silently phone home for analytics, model downloads, fonts, maps, embeddings, or package metadata.

## Recovery

Each topology defines snapshot/backup location, event-log durability, RPO/RTO targets when productionized, and restore verification.

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

- AWG-PLAT-001
- AWG-PLAT-003
- AWG-PLAT-004
