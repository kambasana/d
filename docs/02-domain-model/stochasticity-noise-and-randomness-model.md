---
title: Stochasticity, Noise, and Randomness Model
document_id: AWG-DOM-007
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
- AWG-DOM-003
- AWG-SCN-003
linear_issue: null
supersedes: []
---

# Stochasticity, Noise, and Randomness Model

## Purpose

Define bounded variation, typed uncertainty, random streams, reproducible seeds, perception noise, memory noise, travel variation, and ensemble analysis without using randomness to disguise missing mechanisms.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define bounded variation, typed uncertainty, random streams, reproducible seeds, perception noise, memory noise, travel variation, and ensemble analysis without using randomness to disguise missing mechanisms.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Randomness may select only among valid actions and states permitted by the deterministic model.
- Each random source must have a semantic type, stream identifier, seed or recorded stream position, and owning subsystem.
- Perception, memory, mobility, communication, environment, and population-sampling noise must be represented separately.
- A scenario run must be repeatable with the same inputs, versions, and random streams.
- Results must be reported as distributions when stochastic variation materially affects conclusions.

## Detailed specification

## 15. Randomness, noise and uncertainty

### Randomness is necessary, but arbitrary randomness is not

Human, environmental and social systems should not be perfectly deterministic. Similar agents can make different choices, travel times vary, attention is imperfect and messages can be missed. The correct implementation is **bounded stochasticity inside explicit mechanisms**.

Bad randomness:

```text
Agent randomly changes belief.
Agent randomly posts.
Agent randomly becomes angry.
Agent randomly walks to another city.
Agent randomly appears at a destination.
```

Good randomness:

```text
Agent becomes hungry.

Valid actions are generated from world state:
- Eat available food at home.
- Visit an open café within reachable distance.
- Buy food from an accessible shop.
- Delay eating because of another obligation.

A bounded policy selects among valid options using preferences,
cost, habit, time, social context and a controlled random stream.
```

### Use typed noise sources

Do not create one generic `randomness` slider. Model separate mechanisms.

| Noise type | Example | Required constraint |
|---|---|---|
| Perception noise | Agent fails to notice a weak signal | Signal must have been physically perceptible |
| Attention variation | Agent notices one nearby event but not another | Attention budget and salience rules |
| Memory noise | Detail becomes uncertain over time | Original memory remains in provenance history |
| Decision variation | Tie between similarly valued actions | Only valid actions may be selected |
| Travel-time variation | Congestion or dwell-time variation | Route and transport constraints remain valid |
| Communication failure | Delayed, missed or partial message | Valid communication channel must exist |
| Information mutation | Retelling changes wording or certainty | Claim lineage must preserve the source chain |
| Environmental variation | Weather or equipment failure | Defined distribution and world mechanism |
| Population sampling | Synthetic individual instantiated from a cohort | Conditional on aggregate state and provenance |
| Measurement uncertainty | Sensor or imported data is imprecise | Accuracy and confidence metadata retained |

### Separate two kinds of uncertainty

The interface should distinguish:

- **Aleatory uncertainty:** inherent variation in the simulated process, such as travel delay or who notices a weak signal.
- **Epistemic uncertainty:** uncertainty caused by incomplete data, uncertain parameters, weak evidence or an imperfect model.

These should not share one visual treatment. Aleatory uncertainty is usually explored through repeated runs and outcome distributions. Epistemic uncertainty needs provenance, confidence, sensitivity testing and explicit assumptions.

### Randomness must be reproducible

Use deterministic, named random streams:

```text
world_seed
scenario_seed
population_seed
mobility_seed
perception_seed
information_seed
economy_seed
environment_seed
agent_seed
```

Record the stream and draw position for consequential stochastic decisions. A user must be able to:

- Replay the same seed.
- Rerun with a new seed.
- Lock some streams while varying others.
- Compare an ensemble of runs.
- Determine whether an outcome is robust or seed-sensitive.

### UI controls for randomness

Scenario Studio should expose randomness through documented profiles rather than an unexplained global percentage.

Example:

```text
Variation profile: Urban weekday baseline

Mobility variation        Calibrated distribution v3
Perception variation      Medium
Communication delay       Observed-network profile v2
Memory decay              Enabled, long-term only
Information mutation      Low
Rare infrastructure fault 0.002 per simulated day
Seed policy               Locked for baseline comparison
```

Advanced users may inspect distributions and parameters, but the default interface should describe what the profile means in domain language.

### Show distributions, not one generated future

Scenario results should default to:

- Outcome ranges.
- Percentiles.
- Small multiples.
- Difference maps.
- Confidence or credible intervals where justified.
- Frequency of threshold crossings.
- Sensitivity to seed, model and parameter changes.

Animated hypothetical outcome plots can help users reason about uncertainty for some tasks, but they require a reduced-motion alternative and should not replace numeric summaries. Research has found that animated samples can improve some probability and trend judgments, while other uncertainty encodings involve task-dependent trade-offs.

Sources:

- [Hypothetical Outcome Plots Help Untrained Observers Judge Trends in Ambiguous Data](https://idl.uw.edu/papers/hops-trends)
- [Visual Reasoning Strategies for Effect Size Judgments and Decisions](https://arxiv.org/abs/2007.14516)
- [Visualizing Uncertainty in Probabilistic Graphs with NetHOPs](https://pubmed.ncbi.nlm.nih.gov/34587012/)

---

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
- AWG-DOM-003
- AWG-SCN-003
