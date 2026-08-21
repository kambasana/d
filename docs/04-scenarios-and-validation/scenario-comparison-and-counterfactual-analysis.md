---
title: Scenario Comparison and Counterfactual Analysis
document_id: AWG-SCN-004
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
- AWG-SCN-001
- AWG-SCN-002
- AWG-SCN-003
linear_issue: null
supersedes: []
---

# Scenario Comparison and Counterfactual Analysis

## Purpose

Define baseline alignment, branch inheritance, divergence analysis, causal comparison, and safeguards against false counterfactual claims.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define baseline alignment, branch inheritance, divergence analysis, causal comparison, and safeguards against false counterfactual claims.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for scenario comparison and counterfactual analysis.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Goal

Compare branches without pretending that one simulation run proves causality in the real world.

## Comparison requirements

- same pre-branch history;
- declared intervention differences;
- matched or deliberately varied seeds;
- matched software/plugin/model versions unless the comparison is explicitly about those versions;
- common measurement definitions;
- confidence/uncertainty reporting.

## Views

Compare:

- world-state trajectories;
- population aggregates;
- selected agents;
- journeys/mobility;
- organizations/economy;
- information cascades;
- claims/beliefs;
- resource/infrastructure states;
- model-call usage/cost;
- validation metrics.

## Causal language

Use cautious wording such as "within this model, under these assumptions, the branch produced..." unless external validation justifies stronger claims.

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

- AWG-SCN-001
- AWG-SCN-002
- AWG-SCN-003
