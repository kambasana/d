---
title: Uncertainty and Sensitivity Analysis
document_id: AWG-SCN-003
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
linear_issue: null
supersedes: []
---

# Uncertainty and Sensitivity Analysis

## Purpose

Define ensembles, seed variation, parameter sensitivity, model-provider sensitivity, confidence intervals, and reporting of unstable outcomes.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define ensembles, seed variation, parameter sensitivity, model-provider sensitivity, confidence intervals, and reporting of unstable outcomes.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for uncertainty and sensitivity analysis.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Types of uncertainty

- input/data uncertainty;
- population synthesis uncertainty;
- stochastic behavioral variation;
- model parameter uncertainty;
- structural/model-choice uncertainty;
- LLM/provider nondeterminism;
- measurement uncertainty;
- scenario-assumption uncertainty.

## Typed randomness

Do not use a generic "randomness" knob. Maintain named mechanisms such as:

```text
perception_noise
memory_decay
travel_time_variation
decision_tie_breaking
communication_failure
information_mutation
population_sampling
environmental_variation
```

Each has explicit distribution/rules and named random stream.

## Seed strategy

Use world/scenario/region/system/agent-level streams as appropriate. Record enough metadata to reproduce stochastic sequences without assuming one global RNG is sufficient.

## Repeated runs

A scenario conclusion should be tested across seeds when stochastic mechanisms materially affect outcomes. Report distributions, not only a favorable single run.

## Model sensitivity

Repeat controlled subsets with alternative AI providers/models/prompt policies when AI materially influences outcomes. If outcomes swing widely, report that as model sensitivity rather than hiding it.

## Intervention robustness

Compare effect size against baseline variance. An intervention whose observed effect is smaller than ordinary seed/model variance should not be described as robust without further evidence.

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
