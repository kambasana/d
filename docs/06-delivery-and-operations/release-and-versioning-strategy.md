---
title: Release and Versioning Strategy
document_id: AWG-OPS-005
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
- AWG-PLAT-003
- AWG-PLAT-002
linear_issue: null
supersedes: []
---

# Release and Versioning Strategy

## Purpose

Define document, schema, plugin, scenario, data, and model versioning plus release manifests, checksums, migrations, and deprecation.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define document, schema, plugin, scenario, data, and model versioning plus release manifests, checksums, migrations, and deprecation.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for release and versioning strategy.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Versioned artifacts

Version independently where useful:

- application/runtime;
- domain/event schemas;
- plugin interfaces;
- individual plugins;
- scenario packages;
- data packages;
- model/prompt policies;
- documentation pack.

## Compatibility

Breaking schema/interface changes require migration notes and compatibility decision. Replays should record the schema/runtime version they require.

## Release evidence

A release candidate should include:

- changelog;
- migrations;
- SBOM/licence review;
- invariant/contract/integration test results;
- performance benchmark profile;
- known limitations;
- offline smoke test where supported;
- scenario/replay compatibility notes.

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

- AWG-PLAT-003
- AWG-PLAT-002
