---
title: Multi-Resolution Simulation and Scaling Architecture
document_id: AWG-PLAT-005
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
- AWG-GOV-001
- AWG-PLAT-001
- AWG-PLAT-004
linear_issue: ELE-143
supersedes: []
---

# Multi-Resolution Simulation and Scaling Architecture

## Purpose

Define aggregate, cohort, scheduled, cognitive, and embodied simulation levels independently from visualization levels.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define aggregate, cohort, scheduled, cognitive, and embodied simulation levels independently from visualization levels.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for multi-resolution simulation and scaling architecture.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Principle

Planetary scope is achieved by simulating relevant entities at appropriate fidelity, not by running every person as a continuously reasoning LLM agent.

## Simulation fidelity levels

```text
S0 - Aggregate population
S1 - Cohort/archetype policy
S2 - Scheduled individual
S3 - Cognitive individual
S4 - Fully embodied local agent
```

The `awg_mvp5` reference keeps 1000 population records distinct from 50
active cognition records, conserves tokens and beliefs across promotion and
demotion, and compares a shared-seed control branch with a suppress-post
intervention. Counts are software evidence, not calibrated human behavior.


### S0 - Aggregate
Counts/flows/distributions for demographics, migration, employment, demand, exposure, disease/risk states, or other macro variables.

### S1 - Cohort/archetype
Shared calibrated policies with distributions and stochastic variation. Suitable for large-scale lower-detail behavior.

### S2 - Scheduled individual
Persistent identity, home/work/household, schedules, resources, relationships, and classical decision systems.

### S3 - Cognitive individual
Detailed memories, beliefs, goals, planning, information diffusion, and occasional AI reasoning.

### S4 - Fully embodied
High-detail local navigation, object interaction, perception, concurrency, collision/occupancy, and fine-grained timing.

## Visualization fidelity

Separate from simulation:

```text
V0 - hidden/aggregate
V1 - heatmap/density
V2 - cluster
V3 - individual map marker
V4 - detailed local/interior avatar/state
```

An S3 agent can appear as V2 when zoomed out. A V3 marker does not imply S3/S4 cognition.

## Promotion

Promoting a cohort/agent to higher fidelity must preserve constraints and provenance. Newly instantiated personal details are tagged synthetic/instantiated, not historical observations.

## Demotion

Compression preserves:

- identity where still required;
- unresolved obligations;
- exceptional state;
- key relationships;
- resource/ownership conservation;
- belief/claim summaries needed for future causality;
- links to full event history.

## Activation

Use event-driven wakeups, schedules, spatial triggers, message delivery, scenario events, and stochastic activation where modelled. Do not poll dormant agents continuously.

## Partitioning

Candidate partitions include spatial cells/regions, organizations/platform shards, or workload-specific services. Cross-partition movement/communication uses explicit handoff/correlation events.

## AI budget

AI usage is a managed resource. Budgets may limit:

- concurrent calls;
- calls per simulated hour;
- calls per agent/day;
- token/latency budgets;
- model class based on task importance/novelty.

Fallback policies preserve simulation integrity when budgets are exhausted.

## Determinism and scale

Distributed execution must distinguish deterministic domain transitions from nondeterministic AI/provider behavior. Record random streams, partition ordering rules, and model call outputs for replay.

## Performance objective style

Avoid vague "million agents" claims. Define benchmark profiles such as:

```text
1M population records
100k S1 cohort-equivalent active updates/hour
10k S2 scheduled individuals in region
1k S3 cognitively detailed agents under scenario load
100 S4 embodied agents in selected local area
```

These numbers are examples for benchmark definition, not committed targets until measured.

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

- AWG-GOV-001
- AWG-PLAT-001
- AWG-PLAT-004
