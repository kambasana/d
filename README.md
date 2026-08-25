# Agentic World Graph

**Version:** 0.2.0  
**Status:** complete architecture and documentation baseline; normative documents remain subject to formal review  
**Generated:** 2026-08-20

Agentic World Graph (AWG) is a serious, geographically grounded, event-sourced simulation platform for building real, historical, hypothetical, or synthetic worlds containing persistent people, groups, organizations, resources, information networks, and changing scenarios.

The platform combines established game/NPC architecture, agent-based modelling, OSM-derived geography, offline Protomaps/PMTiles visualization, deterministic movement and causality, modular AI providers such as Ollama and OpenRouter, information provenance, virtual social media, replay, counterfactual branching, empirical validation, and multi-resolution simulation.

> An AI model may propose an intention, interpretation, plan, or utterance. Only the validated simulation kernel may decide what happened.

## What this repository contains

- A manifest-controlled documentation pack with stable document IDs and required sections.
- The full research and prior-art review preserved from the design discussion.
- The simulation constitution and controlled vocabulary.
- Domain specifications for space, time, agents, perception, claims, trust, organizations, resources, synthetic populations, and social platforms.
- Platform specifications for the kernel, scheduler, commands, events, firehose, replay, plugins, storage, partitioning, security, and offline operation.
- Scenario, experiment, calibration, validation, uncertainty, and counterfactual protocols.
- UI/UX specifications for semantic zoom, clustering, radial co-location expansion, buildings, social information space, causal investigation, and the design system.
- JSON Schemas, valid and invalid fixtures for every executable contract family, acceptance-test catalogues, registers, validation scripts, Docker workflow, GitHub workflow templates, release tooling, and split distribution archives.

## Canonical reading order

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/01-governance-and-safety/simulation-constitution-and-invariants.md`](docs/01-governance-and-safety/simulation-constitution-and-invariants.md)
3. [`generated/glossary-and-controlled-vocabulary.md`](generated/glossary-and-controlled-vocabulary.md)
4. [`generated/document-map.md`](generated/document-map.md)
5. The relevant normative specification
6. Related requirements, schemas, tests, risks, evidence, and ADRs

## Repository structure

```text
agentic-world-graph/
├── docs/                 Authored narrative specifications
├── contracts/            Machine-readable JSON Schemas
├── registers/            Canonical YAML registries
├── generated/            Generated indexes and reports
├── examples/             Valid and invalid fixtures plus walkthroughs
├── tests/                Pack, contract, and acceptance-test tooling
├── scripts/              Validation, generation, and release commands
├── decisions/            Architecture Decision Records
├── archive/              Conversation-derived source material and v0.1 context
├── .github/              CI and review templates
├── pack-manifest.yaml    Completeness controller
└── dist/                 Generated release artefacts
```

## Validate

```bash
make validate
make test
```

Equivalent:

```bash
PYTHONPATH=scripts python3 scripts/validate_all.py
PYTHONPATH=scripts python3 -m pytest -q
```

Or with Docker:

```bash
docker compose run --rm docs validate
docker compose run --rm docs release
```

## Run the MVP 1 reference district

The dependency-free reference runtime loads the checksummed synthetic OSM, PostGIS model, gazetteer, routing graph, and PMTiles bundle, simulates 100 scheduled agents for 24 hours, and verifies replay:

```bash
make mvp1
```

This bounded fixture is implementation evidence, not a validated model of a real population or approval to redistribute candidate external components.

## Run the MVP 2 classical NPC profile

```bash
make mvp2
```

Agents use needs, utility scoring, action channels, households/organizations, resource conservation, and perception gating. No LLM is imported or required.

## Run the MVP 3 bounded adapter profile

```bash
make mvp3
```

The offline reference replays 20 recorded calls across intent proposal,
option ranking, dialogue realization, memory summarization, and claim
extraction. Ollama and OpenRouter remain unapproved candidate integrations;
model outputs are proposals and cannot mutate authoritative state.

## Run the MVP 4 information-world profile

```bash
make mvp4
```

Synthetic actors exchange a reconstructable claim chain. Likes are not
belief, unexposed claims stay unknown, and corrections keep original posts.

## Run the MVP 5 scale profile

```bash
make mvp5
```

Population records stay separate from active cognition. Promotion conserves
tokens and beliefs. Shared-seed branch comparison isolates an intervention.

## Run the World Explorer review service

```bash
make world-explorer
```

Serves read-only JSON projections from the MVP 1, MVP 4, and MVP 5 reference
kernels. Mutating HTTP methods are rejected. See
[`apps/world-explorer/README.md`](apps/world-explorer/README.md).

## Run the staged contributor workflow

```bash
make workflow-check
make workflow-status
make workflow-graph
make workflow-next
make workflow-run
make workflow-loop
```

The workflow emits the next role packet and blocks stage advancement until ordered outputs, validation, closeout evidence, limitations, and risks are complete. See [`AWG-OPS-012`](docs/06-delivery-and-operations/automated-contributor-stage-workflow.md).

## Completeness model

The pack is considered structurally complete only when the manifest, authored files, YAML registers, generated indexes, schemas, examples, tests, checksums, and release archives agree. A passed build does not mean that every draft normative decision has received human approval; document status is tracked separately from structural completeness.

## Source-of-truth rule

The authored files and canonical YAML registers in this repository are the source of truth. Linear tracks work, ownership, review, and delivery; exported ZIPs and generated reports are immutable projections of a release.
