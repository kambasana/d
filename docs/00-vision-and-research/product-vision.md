---
title: Product Vision
document_id: AWG-VIS-001
status: draft
version: 0.2.0
last_updated: '2026-08-20'
normative: false
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on: []
linear_issue: null
supersedes: []
---

# Product Vision

## Vision

Build a persistent world and scenario engine in which agentic people, groups, organizations, infrastructure, objects, information, and events exist inside coherent real or synthetic geography.

The platform must feel like a world, not a chat room placed on a map.

## Core proposition

AWG combines:

- real OSM-based or synthetic OSM-like geography;
- planet/regional/city/building spatial hierarchy;
- proven game NPC systems such as perception, blackboards, utility AI, behavior trees, GOAP/HTN, smart objects, action concurrency, navigation, and event-driven updates;
- agent-based modelling and empirical calibration;
- bounded AI components through Ollama, OpenRouter, and future adapters;
- humanistic systems grounded in explicit models rather than invented prompt stereotypes;
- groups, households, organizations, institutions, economies, resources, and ownership;
- agent-specific knowledge, belief, trust, memory, misinformation, and information diffusion;
- virtual social media and information-space actors;
- event sourcing, firehose output, replay, inspection, and counterfactual branching;
- semantic zoom and multi-resolution simulation so the system can scale beyond toy populations.

## World creation

Users can build:

- a real city today;
- a historical scenario;
- a crisis or infrastructure failure;
- a synthetic town/country with coherent roads, places, buildings, topology, and routes;
- a social/economic ecosystem;
- a humanitarian, policy, migration, transport, or organizational scenario.

A scenario is not a prompt. It is a versioned state package with geography, populations, institutions, resources, networks, assumptions, interventions, and measurements.

## Spatial grounding

Agents must understand the space they occupy. A place is not merely a string. It has geometry, entrances, containment, nearby features, traversable connections, access conditions, and time/distance relationships.

Agents cannot randomly spawn elsewhere after initialization, travel impossible distances instantly, cross inaccessible barriers, enter buildings without valid access, or know distant events without an information path.

## Information grounding

Information also has paths. Agents distinguish direct experience, observation, trusted report, second-hand report, public post, repost, comment, rumor, inference, and disputed claims.

A may witness an event; B may see A there; B may tell C; C may post; D may repost; E may fact-check by contacting A. The firehose records the complete causal and informational chain.

## Modular architecture

AI providers, maps, routing, storage, event buses, physics, social platforms, analytics, and visualization are adapters around stable core contracts. Replacing Ollama with OpenRouter or one routing engine with another must not require rewriting agent semantics.

## Serious simulation posture

AWG must not claim that plausible dialogue equals human validity. Realism claims require calibration, benchmarks, sensitivity analysis, and explicit uncertainty.
