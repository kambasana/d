---
title: Information, Trust, Provenance, and Social Diffusion Model
document_id: AWG-DOM-004
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
- AWG-DOM-001
- AWG-DOM-003
linear_issue: ELE-140
supersedes: []
---

# Information, Trust, Provenance, and Social Diffusion Model

## Purpose

Define claims, observations, beliefs, evidence, contextual trust, information mutation, bad actors, fact-checking, and virtual social-media diffusion.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define claims, observations, beliefs, evidence, contextual trust, information mutation, bad actors, fact-checking, and virtual social-media diffusion.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for information, trust, provenance, and social diffusion model.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Purpose

Information is a first-class simulation substrate. Agents are not omniscient. Facts and claims move through physical, interpersonal, institutional, broadcast, and digital networks.

## Knowledge hierarchy

An agent distinguishes at least:

```text
direct experience
personal observation
trusted first-hand report
second-hand report
accessible record/news
public social post
repost/comment/reaction
unattributed rumor
inference
```

These are not equivalent evidence states.

## World truth vs belief

Example:

```text
World truth: electrical transformer failure

Agent A belief: transformer exploded
Agent B belief: building explosion
Agent C belief: terror attack
Agent D belief: unknown cause
Agent E belief: gas explosion
```

Agents act on their available beliefs, not on simulator-only truth.

## Claim object

A claim should support:

```text
claim_id
proposition
subject/entity references
asserted_by
original_source
source_chain
channel
created_at / received_at
location context
evidence references
confidence
trust assessment
corroboration
contradictions
dispute/retraction status
mutation parent/version
agent disposition
```

## Provenance chain example

```text
Physical event
  -> A directly observes event
  -> A tells B
  -> B tells C
  -> C creates public post
  -> D views and likes
  -> E reposts
  -> F comments and messages A for verification
  -> A may reply, ignore, clarify, contradict, or deceive
```

Every step is represented separately. A later analyst should be able to ask why F believed something and trace the answer back through C, B, A, and the original observation.

## Information mutation

Claims may change as they propagate:

```text
A: "I heard a bang and saw smoke."
B: "A said there may have been an explosion."
C: "Explosion reported downtown."
D: "Major explosion downtown."
E: "Attack happening downtown."
```

Lineage must be retained so mutation is inspectable.

## Trust

Trust is contextual:

```text
Trust(observer, source, domain, channel, situation, history)
```

An agent may trust another person about engineering and distrust them about politics. Trust can be influenced by prior accuracy, relationship, expertise, incentives, deception history, institutional role, and corroboration.

## Bad actors

Agents may be mistaken, biased, unreliable, manipulative, deceptive, malicious, coordinated, compromised, or opportunistic. Receiving agents are not automatically told that a claim is false. They evaluate it using their own evidence and trust mechanisms.

## Fact-checking as an action

Verification is not global magic. Agents may:

- contact witnesses;
- search accessible records;
- compare independent sources;
- ask specialists;
- visit a location if feasible;
- wait for official communication;
- ignore or challenge a claim.

Each action has time, access, cost, and possible failure.

## Information spaces

Physical and information spaces interact bidirectionally:

```text
PHYSICAL WORLD
  -> observations
INFORMATION WORLD
  -> beliefs/actions
PHYSICAL WORLD
```

Information can produce physical feedback loops such as panic buying, travel changes, crowd formation, or organizational response.

## MVP 4 bounded reference

The `awg_mvp4` reference records an observation-to-message-to-post-to-repost
chain, keeps likes distinct from belief, preserves original posts under
correction, and withholds unexposed claims from participant projections.
Feed eligibility uses recorded ranking configuration. Information-only
actors declare `embodiment: none`. This is synthetic offline evidence, not
an empirically validated social model.


The platform supports simulated social systems with typed actions such as:

- create post/comment/reply;
- like/dislike/reaction;
- repost/quote-post;
- follow/unfollow;
- mention;
- direct message;
- group chat;
- block/mute/report;
- search;
- fact-check/contact source.

Social platform mechanics must model follow graphs, privacy, visibility, feed ranking, recommendation eligibility, recency, topic affinity, group membership, blocking, moderation, and platform-specific rules through adapters.

Do not ask an LLM to decide all feed exposure directly.

## Social action semantics

```text
viewed != understood
understood != believed
believed != endorsed
endorsed != liked
liked != reposted
reposted != motive known
```

Observable actions and inferred motives are stored separately.

## Information-space-only actors

The architecture may represent news organizations, bots, remote analysts, institutional accounts, automated alerts, and external commentators that primarily act in information space. Their identity/capability model must state whether they also have physical embodiment.

## Firehose events

Examples:

```text
ObservationCreated
ClaimAsserted
ClaimReceived
ClaimCorroborated
ClaimContradicted
BeliefUpdated
MessageSent
MessageDelivered
PostCreated
PostViewed
PostLiked
PostReposted
CommentCreated
FactCheckRequested
SourceContacted
ClaimCorrected
ClaimRetracted
```

Each event references time, actors, channel, claim/message/post IDs, causal parents, visibility/audience, and relevant location/provenance.

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
- AWG-DOM-001
- AWG-DOM-003
