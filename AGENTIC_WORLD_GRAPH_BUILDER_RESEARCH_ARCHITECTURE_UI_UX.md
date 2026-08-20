# Agentic World Graph Builder: Research, Architecture and UI/UX Recommendations

## Research verdict

Many existing systems are not necessarily dishonest, but they are often research prototypes or demonstrations built to produce believable behaviour, rather than validated simulations of physical reality, human society, or future outcomes.

The recurring mistake is treating:

> Fluent agent dialogue + a map + long-term memory

as equivalent to:

> A physically grounded, causally consistent, empirically calibrated world simulation.

They are not the same thing.

The foundational rule for this project should be:

> **An LLM may propose an intention, plan, interpretation, or utterance. Only the deterministic simulation kernel may decide what actually happened.**

Games have spent decades making restricted agents appear intelligent inside reliable worlds. Many recent AI simulations instead make unrestricted text appear to be a world. This platform needs the engineering discipline of the first approach and the language flexibility of the second.

This review covers influential papers, official engine documentation, established simulation systems, and active open-source projects available through August 20, 2026. It is not a claim to include every paper or repository ever published.

---

## 1. What the current research really demonstrates

### Generative Agents and “Smallville”

The original Generative Agents work demonstrated 25 agents with a memory stream, retrieval based on relevance, recency and importance, reflection, planning, and social interaction. Those mechanisms are useful, particularly as an early design for episodic memory and reflection. However, the evaluation primarily concerned whether behaviour appeared believable—not whether the world was physically correct, empirically calibrated, causally valid, or suitable for forecasting.

Source: *Generative Agents: Interactive Simulacra of Human Behavior*

**Reuse:**

- Episodic memory records.
- Memory retrieval ranking.
- Periodic reflection rather than reflection after every event.
- Daily and hierarchical planning.
- Natural-language expression over structured internal state.

**Do not reuse as:**

- The world simulation kernel.
- The physical movement system.
- The source of objective truth.
- Evidence that generated populations accurately predict people.
- A justification for giving agents unrestricted access to world state.

### Interview-grounded simulations of 1,052 people

The Stanford study of 1,052 interview-grounded agents is substantially stronger than generating personas from a few demographic attributes. Its reported comparison against participants’ own two-week retest performance is a useful evaluation model. It demonstrates that rich grounding material can produce better persona-conditioned responses. It does not establish that those agents can accurately predict complex real-world behaviour under novel social, geographic, or crisis conditions.

Source: *Generative Agent Simulations of 1,000 People*

**Reuse:**

- Ground agents in evidence, interviews, records, roles and lived history.
- Compare simulated answers with human baselines.
- Measure model performance relative to human self-consistency.
- Maintain provenance for every profile attribute.

**Never infer:**

- A convincing persona equals a validated human model.
- Survey-answer similarity proves valid physical or social behaviour.
- One interview creates a complete psychological model.

### Evidence against trusting LLM simulations at face value

Several evaluations expose why believable output cannot be the main validation criterion:

- In **360CityArena**, the strongest tested model achieved only 17.1%, compared with 77.3% for humans, on grounded urban tasks involving streets, locations and navigation. This is direct evidence that language-capable models should not control authoritative urban movement or spatial truth.
- **SOTOPIA** found substantial gaps between strong language models and humans in difficult social interaction scenarios. It is useful as an evaluation framework, not as evidence that LLMs already possess reliable social intelligence.
- **Lost in Simulation** found material outcome variation across simulated-user models, including miscalibration and disparities across demographic and language groups.
- **Utopian Illusion** identified overly idealized and socially desirable behaviour in simulated societies.
- **Too Human to Model** argues that increasingly expressive agents can obscure causal mechanisms, time abstractions and model assumptions rather than improving scientific validity.
- Research on social-desirability effects shows that LLM-generated survey responses can inherit systematic response biases.

**Sources:**

- 360CityArena
- SOTOPIA
- Lost in Simulation
- Utopian Illusion
- Too Human to Model
- Social Desirability Bias in LLM-Generated Survey Responses

The correct conclusion is not that LLM agents are useless. It is that they must be bounded, measured, replaceable and prevented from becoming the authority over world truth.

---

## 2. What should be reused directly

### Geospatial foundation

| Requirement | Recommended foundation | Correct role |
| --- | --- | --- |
| Canonical OSM ingestion | **osm2pgsql** | Transform OSM extracts into a queryable, versioned schema |
| Spatial database | **PostgreSQL + PostGIS** | Authoritative geometry, spatial relationships and spatial indexes |
| Offline map display | **PMTiles + MapLibre/Protomaps** | Render and distribute offline vector tiles |
| Gazetteer | **Nominatim** | Resolve names, addresses and places |
| Regional routing | **Valhalla** | Walking, cycling, driving and multimodal route calculation |
| Microscopic traffic | **SUMO** | Detailed vehicles, public transport, junctions and road behaviour |
| Building/local navigation | **Recast/Detour** | Navmesh generation, local pathfinding and crowds |
| Large-scale activity mobility | **MATSim patterns or adapter** | Plans, activities, legs, scoring, replanning and mobility events |

### PostGIS and osm2pgsql should hold spatial truth

Use osm2pgsql to construct an explicit OSM-derived database model in PostGIS. Preserve:

- OSM node, way and relation identifiers.
- Dataset timestamp.
- Source extract.
- Object version.
- Tags and classification.
- Original and derived geometry.
- Transformation version.
- Access and routing interpretation.
- Synthetic-versus-observed provenance.

PostGIS provides spatial types, queries and indexes; osm2pgsql provides a controlled OSM import and transformation path. The osm2pgsql documentation also cautions against starting with the entire planet before establishing a working regional process.

**Sources:**

- osm2pgsql documentation
- PostGIS

### PMTiles is not the world

PMTiles is an excellent offline packaging and presentation technology. It stores tiled map pyramids in a single archive and supports local or range-request-based serving. That makes it ideal for offline visualization and distribution. It should not become the authoritative source of exact geometry, topology, entrances, route connectivity or simulation state.

Use this separation:

```text
PostGIS / OSM source data
        │
        ├── Routing graph
        ├── Gazetteer
        ├── Simulation spatial model
        └── PMTiles render projection
```

Never attempt to reconstruct authoritative world topology from generalized display tiles.

Source: Protomaps and PMTiles documentation

### Nominatim is a gazetteer, not physical truth

Nominatim should resolve:

- Place names.
- Addresses.
- Administrative areas.
- Named buildings.
- Named streets.
- Search and reverse-geocoding queries.

It should not decide whether an agent can physically enter, cross or traverse something. Nominatim’s reverse-geocoding documentation explains that it returns the closest suitable indexed OSM object, which can produce a different street or object from the exact coordinate.

Source: Nominatim documentation

### Layer movement engines by scale

No single navigation engine should control every spatial scale.

```text
Planet / regional route
    Valhalla

City-scale activity and transport demand
    MATSim-style plans and replanning

Detailed roads, junctions and vehicles
    SUMO

Local pedestrian and building navigation
    Recast / Detour or equivalent navmesh

Immediate movement and collision
    Local movement controller / physics
```

Valhalla supports tiled hierarchical routing, dynamic costing, map matching and multimodal route calculation. SUMO provides OSM import, microscopic transport simulation, remote control through TraCI, and state save/load. Recast and Detour provide navmesh construction, path queries, tiled navigation and crowd support.

**Sources:**

- Valhalla
- SUMO
- Recast Navigation
- MATSim

---

## 3. What established games already solved

### The central comparison

| Established game/ABM pattern | Weak LLM reinvention | Required hybrid approach |
| --- | --- | --- |
| Sensor and perception system | Put the entire world into the prompt | Generate only observations physically or informationally available to the agent |
| Blackboard or typed working memory | Dump vector-search results into context | Maintain typed beliefs, observations, uncertainties and source provenance |
| Behaviour trees, StateTree and utility selection | Ask “What do you do next?” every tick | Deterministic selector chooses routine behaviour; LLM handles exceptional ambiguity |
| GOAP/HTN with preconditions and effects | Let the model invent a prose plan | LLM may suggest typed goals; planner validates feasible action sequences |
| State machine/action executor | Model narrates that an action succeeded | Kernel executes, rejects, delays or partially completes actions |
| Navgraph/navmesh and movement controller | Model invents coordinates and travel times | Routing and physics calculate path, duration, occupancy and arrival |
| Smart objects and reservations | Agent says “I use the chair” | Object exposes affordances, slots, capacity, ownership and reservation rules |
| Contextual dialogue rules | Model is told everything and improvises | Eligible knowledge is selected from epistemic state; LLM realizes wording |
| Director and scenario controller | Hidden narrator forces a desired result | Explicit interventions are logged; agents independently react |
| Entity/data-oriented LOD | Every agent runs the same prompt loop | Aggregate, archetype, scheduled and high-fidelity modes |
| Debugger and event trace | Keep only chat transcripts | Record commands, decisions, causes, validators, state changes and model calls |

### F.E.A.R.: GOAP and reliable action execution

The published F.E.A.R. architecture used planning actions with preconditions, effects and costs, while a smaller execution layer carried out the selected actions. It allowed dynamic replanning without asking a free-form language model to invent and enforce the world simultaneously.

Source: GDC Vault: *Three States and a Plan — The AI of F.E.A.R.*

A suitable action contract for this system would look like:

```text
Action: TravelToPlace

Preconditions:
- actor is alive
- destination exists
- destination is reachable
- transport mode is available
- actor is allowed to use selected route

Effects:
- journey is created
- actor enters travelling state
- time and resources begin accumulating

Execution:
- mobility engine advances actor along route

Completion:
- actor reaches valid destination entrance

Failure possibilities:
- route closed
- vehicle unavailable
- capacity reached
- actor interrupted
- physical condition changed
```

The LLM can propose `TravelToPlace(destination_id, reason)`. It cannot declare the agent has arrived.

### Unreal Engine: perception, blackboards, StateTree, EQS and Smart Objects

Unreal’s documented AI systems embody several mature patterns:

- Behaviour Trees connected to blackboards.
- Event-driven decision updates rather than constant polling.
- Environment Query System generators, tests and weighting.
- Smart Objects with explicit interactions and claims.
- StateTree combining hierarchical states and selectors.
- MassEntity for data-oriented large populations.
- Crowd avoidance and navigation integration.
- Debugging and trace tooling for decisions.

**Sources:**

- Unreal Engine Behavior Trees
- Unreal Engine Environment Query System
- Unreal Engine Smart Objects
- Unreal Engine StateTree
- Unreal Engine MassEntity

These patterns should influence the core architecture even if Unreal itself is not used.

For example, a café should not simply be a place name. It exposes affordances:

```text
Café
├── enter through entrance
├── queue
├── order food
├── claim seat
├── eat
├── speak to nearby people
├── use toilet
├── work
└── leave
```

Each affordance has:

- Preconditions.
- Capacity.
- Location.
- Duration.
- Cost.
- Ownership or access.
- Resource locks.
- Possible interruption.
- Observable consequences.

### The Sims: interactions, constraints and concurrency

The Sims 4’s published architecture emphasizes data-defined interactions, compatibility constraints, location selection and concurrent activities. A character can, where valid, eat, watch and converse because different action channels and resource constraints are explicitly represented.

Source: GDC Vault: *Concurrent Interactions in The Sims 4*

Agents should therefore have action channels such as:

```text
Locomotion
Posture
Hands
Attention
Speech
Digital activity
Long-running obligation
```

This prevents absurd states:

- Driving two cars simultaneously.
- Sleeping while walking down a street.
- Holding six incompatible objects.
- Having ten full-attention conversations at once.
- Occupying the same exclusive seat as another agent.

### Left 4 Dead: scenario direction without controlling agents

Valve’s published Left 4 Dead material covers AI systems, replayable cooperative design and rule databases for contextual dialogue and game logic. The important reusable principle is separation between:

- What the scenario controller introduces.
- What the environment permits.
- What individual agents decide.
- How dialogue is selected from context.

Source: Valve publications

The scenario engine may create an explicit exogenous event:

```text
08:20 — Bridge B is closed because of structural damage
```

It must not silently force:

```text
All residents panic and travel north
```

Residents should react according to perception, knowledge, trust, plans, available alternatives and personal constraints.

### The Last of Us: dialogue based on knowledge state

The Last of Us contextual-dialogue presentation describes the use of individual knowledge, collective knowledge, global state and environmental context. That is much closer to the information-provenance requirement than giving an LLM the entire transcript and asking it to improvise.

Source: GDC Vault: *A Context-Aware Character Dialog System in The Last of Us*

The dialogue model should receive only:

- Facts the speaker currently believes.
- Confidence and uncertainty.
- Relevant relationship information.
- Recent context.
- Communication goal.
- Emotional and physical constraints.
- Permitted disclosure level.

The model realizes language. It does not create previously unknown facts merely to make the conversation interesting.

---

## 4. Promising agent-simulation systems and what to take from them

### Concordia

Concordia separates entities, components and an engine, and uses a Game Master to resolve natural-language intended actions in physical, social or digital environments. Its component and prefab architecture is valuable.

**Sources:**

- Concordia GitHub repository
- Concordia technical report

**Reuse:**

- Entity/component composition.
- Prefabricated agent and environment recipes.
- Replaceable memory and reasoning components.
- Explicit separation between entities and environment.
- Provider-neutral language-model integration.

**Modify:**

The Game Master must not be the final physical authority. Replace soft LLM resolution with:

```text
Natural-language intention
        ↓
Typed command
        ↓
Schema validation
        ↓
Rules / physics / topology / ownership checks
        ↓
Deterministic result
        ↓
Optional LLM narration
```

Concordia is Apache-2.0, but dependency and component-level licensing still require review.

### AgentSociety

AgentSociety 2 provides hot-pluggable environment components, multiple reasoning patterns, Ray-based execution, a unified service proxy, replay, JSONL traces, DuckDB-powered reads and distributed tracing. Its earlier version included urban mobility, economic and social modules.

**Sources:**

- AgentSociety GitHub repository
- AgentSociety paper
- AgentSociety 2 paper

**Reuse or adapt:**

- Experiment lifecycle management.
- Distributed task execution.
- Agent workspace isolation.
- Replay catalogue.
- Research experiment configuration.
- Service-proxy boundary.
- Benchmark package structure.
- Trace collection.

**Do not assume:**

- “LLM-native” means physically valid.
- A distributed prompt system is a distributed world simulator.
- Ray should become part of every core plugin contract.

Treat AgentSociety as a possible orchestration and experimentation layer—not automatically as the world kernel.

### OASIS

OASIS is one of the most directly relevant projects for a virtual social-media environment. It represents typed social actions, dynamic graphs, recommendations, messaging and platforms modelled after Twitter/Reddit-style interaction. Its repository advertises simulations of up to one million user records and defines actions including following, posting, commenting, liking, muting and searching.

**Sources:**

- OASIS GitHub repository
- OASIS paper

**Reuse or adapt:**

- Typed platform actions.
- Follow and social graphs.
- Post/comment/repost relationships.
- Feed and recommendation adapters.
- Activation scheduling.
- PettingZoo-style environment interface.
- Platform database schemas.
- Social-network metrics.

**Critical warning:**

OASIS’s published token-consumption example reports 335,600 input tokens for 100 agents in one fully activated step. That is direct evidence that per-agent, per-step LLM calls cannot be the basis of a planetary system.

Also, a like, repost or comment must not automatically mean belief:

```text
Observed action: repost
Possible motives:
- endorsement
- criticism
- mockery
- alerting others
- bookmarking
- coordinated amplification
- accidental interaction
```

Store the observable action separately from the inferred motive.

### AgentTorch and large-population models

AgentTorch and related Large Population Model research are relevant for large-scale, lower-fidelity population dynamics. Their strongest idea is not “give every person a language model.” It is using archetypes, shared policies, vectorized computation and differentiable or calibratable population simulation to reduce inference cost.

**Sources:**

- AgentTorch GitHub repository
- Large Population Models

**Reuse:**

- Archetype policies for low-detail populations.
- Batched and vectorized updates.
- Calibration against observed aggregate outcomes.
- Policy compilation.
- Differentiable parameters where appropriate.
- Promotion from aggregate to individual fidelity.

**Risk:**

Archetypes can erase meaningful individual variation. They should be a level-of-detail representation, not a claim that everyone in a demographic group behaves identically.

### CityBehavEx

CityBehavEx is particularly aligned with this philosophy because it describes itself as LLM-assisted, combines established urban-behaviour mechanisms with learned components, and emphasizes empirical validation, replay and comparison against mobility, time-use, transport and social-network patterns. Its paper reports large synthetic mobility runs without using an LLM for every agent decision.

**Sources:**

- CityBehavEx GitHub repository
- CityBehavEx paper

This is a stronger direction than prompt-only simulation:

```text
Established mobility mechanism
        +
Calibrated behavioural model
        +
Bounded learned component
        +
Replay and evaluation
```

The repository is new research software and uses AGPL-3.0, so it should be inspected carefully before code reuse in a commercial modular platform.

### MATSim

MATSim has mature concepts that should be adopted even without embedding the full Java system:

- Daily plans.
- Activities and travel legs.
- Plan execution.
- Scoring.
- Replanning.
- Mobility events.
- Sparse/event-driven execution.
- Co-location duration and intensity for exposure models.

**Sources:**

- MATSim
- *The Multi-Agent Transport Simulation MATSim*

This structure is preferable to prompting:

> “Describe what this person does today.”

Instead, the agent owns an executable plan:

```text
07:30 Wake
08:10 Leave home
08:10–08:42 Travel by bus
08:45–12:00 Work
12:00–12:40 Lunch
...
```

When a road closes, the replanning system updates affected legs and activities. The language model may explain the reaction or help select among unfamiliar alternatives, but routing and time remain authoritative.

### AI Town

AI Town is a useful starter for:

- Real-time presentation.
- Shared state.
- Agent visualisation.
- Ollama or OpenAI-compatible model switching.
- A simple town UI.

It is not a suitable planetary simulation kernel. Treat it as a reference for interactive presentation and developer experience, not as the model of physics, geography or society.

Source: AI Town GitHub repository

### Project Sid

Project Sid is useful as a source of ideas about large Minecraft populations, roles, institutions and civilization-like emergence. It should be treated as experimental inspiration and benchmarking material rather than a validated reusable world operating system.

Source: Project Sid GitHub repository

---

## 5. Components to reuse only as benchmarks

Some systems are more useful for testing the architecture than implementing it.

| System | Useful benchmark |
| --- | --- |
| Generative Agents | Memory, reflection and perceived believability |
| Stanford 1,052-person agents | Persona grounding and human-response comparison |
| SOTOPIA | Difficult social situations and goal completion |
| 360CityArena | Spatial reasoning, route understanding and street-level grounding |
| OASIS | Social-network propagation and platform mechanics |
| AI Town | Interactive developer experience |
| Project Sid | Larger-group narratives and institutional emergence |

A benchmark result should never be described as validation outside the domain it measured.

---

## 6. Things the architecture must never do

### 1. Never let the LLM mutate world state directly

Wrong:

```text
LLM: "I drove to London and arrived."
World: location = London
```

Correct:

```text
LLM proposes: Travel(destination=London, mode=car)

Kernel checks:
- vehicle access
- current position
- valid route
- road restrictions
- fuel
- travel time
- interruptions
- capacity

Kernel emits:
JourneyStarted
JourneyProgressed
JourneyRerouted
JourneyCompleted
```

### 2. Never use unrestricted free text as the action API

Every actionable output must become a typed command with:

- Schema.
- Preconditions.
- Permissions.
- Resource requirements.
- Duration.
- Effects.
- Failure conditions.
- Cancellation rules.

Invalid structured output must fail safely without changing state.

### 3. Never give agents global world state

An agent should receive an observation generated through:

- Physical senses.
- Devices.
- Messages.
- Media exposure.
- Records it can access.
- Previous memory.
- Explicit inference.

The simulator’s truth must remain distinct from what the agent believes.

### 4. Never call an LLM for every agent on every tick

That is economically and computationally unsuitable, creates latency coupling, and amplifies nondeterminism. OASIS’s published token example illustrates the cost even at 100 fully activated agents.

Most agents should spend most of their time executing:

- Schedules.
- Existing plans.
- Utility policies.
- State machines.
- Cached responses.
- Aggregate population transitions.

LLMs should be invoked at novelty boundaries, not simulation-clock boundaries.

### 5. Never treat a vector database as memory or truth

Embeddings are a retrieval index. They are not:

- Authoritative records.
- Exact timestamps.
- Source provenance.
- Contradiction tracking.
- Identity resolution.
- Causal history.

Maintain canonical typed memories and claims. Build vector indexes over them as a secondary access method.

### 6. Never use PMTiles as route or world authority

Tiles are for visual projection and distribution. Use OSM-derived topology, PostGIS and routing graphs for authoritative spatial behaviour.

### 7. Never permit unexplained position changes

Every physical relocation requires one of:

- Valid movement.
- Valid vehicle transport.
- Explicit emergency transfer.
- Explicit administrative intervention.
- Scenario initialization before simulation starts.

Even exceptional relocation must be a logged event with reason and authority.

### 8. Never equate reposting, liking or commenting with belief

Exposure, belief, endorsement and propagation are separate states.

```text
Viewed post ≠ understood claim
Understood claim ≠ believed claim
Believed claim ≠ endorsed claim
Endorsed claim ≠ reposted claim
Reposted claim ≠ original motive known
```

### 9. Never reduce trust to one universal number

Trust should be contextual:

```text
Trust(
    observer,
    source,
    domain,
    channel,
    situation,
    history
)
```

A person may trust a mechanic about cars and distrust the same person about medicine.

### 10. Never let a hidden scenario director force outcomes

The scenario engine can introduce declared events and interventions. It cannot covertly modify agents to produce the researcher’s desired conclusion.

### 11. Never run every agent at identical fidelity

A planetary world cannot model everyone with full cognition, physics and LLM inference simultaneously.

Use adaptive fidelity:

```text
L0 Aggregate population
L1 Archetype policy
L2 Scheduled individual
L3 Cognitive individual
L4 Fully embodied local agent
```

### 12. Never poll dormant agents continuously

Use:

- Event-driven activation.
- Scheduled wake-up times.
- Dependency triggers.
- Spatial triggers.
- Stochastic activation where scientifically justified.

### 13. Never judge quality from transcripts alone

A compelling conversation proves that the system produced compelling text.

It does not prove:

- Correct geography.
- Correct mobility.
- Human validity.
- Correct information diffusion.
- Causal correctness.
- Forecasting accuracy.
- Reproducibility.

### 14. Never use an LLM judge as the only evaluator

Use deterministic checks, domain metrics, human baselines, observed datasets and blinded evaluation. An LLM judge may be one supplementary signal.

### 15. Never overwrite history

Corrections and retractions must be new events:

```text
ClaimCreated
ClaimShared
ClaimCorrected
ClaimRetracted
```

Do not silently replace the original claim, because that destroys provenance.

### 16. Never silently change models during an experiment

Record:

- Provider.
- Model identifier.
- Exact version where available.
- Quantization.
- Prompt-policy version.
- System prompt hash.
- Tool definitions.
- Temperature.
- Seed where supported.
- Adapter version.
- Retry and fallback path.
- Input/output tokens.
- Latency.
- Raw output reference.

### 17. Never generate populations from stereotypes alone

Demographic categories must not become personality templates. Population synthesis should distinguish:

- Statistically sampled attributes.
- Observed individual data.
- Derived attributes.
- Scenario assumptions.
- Randomly generated details.
- Model-generated interpretation.

Each needs provenance and uncertainty.

### 18. Never pretend aggregate agents have individual histories

When an aggregate population is promoted to individual fidelity, do not silently invent detailed backstories and present them as historical facts.

Generated details must be marked as:

- Newly instantiated.
- Constrained by aggregate history.
- Unobserved.
- Synthetic.
- Uncertain.

### 19. Never force the entire system into one graph database

The “world graph” should be a semantic model and API, not necessarily a single physical database.

Use fit-for-purpose storage:

- PostGIS for space.
- Append-only event storage for history.
- Relational tables for transactions and ownership.
- Columnar storage for analysis.
- Graph projections for relationships and provenance.
- Search indexes for retrieval.
- Blob storage for media.

Trying to put every position update, message, route point, relationship and analytic aggregate into one graph database will create performance and maintenance problems.

### 20. Never ignore license boundaries

Architecture patterns can be studied broadly, but direct code reuse must be gated by:

- License compatibility.
- Copyleft implications.
- Commercial restrictions.
- Dataset terms.
- Model licences.
- OSM attribution and database obligations.
- Dependency SBOM.
- Security review.

CityBehavEx, for example, is AGPL-3.0, while Concordia and OASIS are Apache-2.0. Component-level and dependency-level review is still required.

---

## 7. Recommended architecture

### Four separate data planes

This separation is essential.

#### 1. World-truth plane

Contains what objectively happened inside the simulation:

- Authoritative positions.
- Ownership.
- Physical events.
- Transactions.
- Infrastructure state.
- Ground-truth scenario cause.
- Validated actions.
- Simulation clock.

#### 2. Agent-epistemic plane

Contains what each agent believes:

- Observations.
- Claims.
- Sources.
- Confidence.
- Contradictions.
- Memories.
- Inferences.
- Trust.
- Uncertainty.
- Forgotten or inaccessible information.

#### 3. Projection plane

Contains views built for:

- Maps.
- Dashboards.
- Social feeds.
- Timelines.
- Graph displays.
- Analytics.
- Search.
- PMTiles.

A projection is never automatically authoritative truth.

#### 4. Software-telemetry plane

Contains:

- CPU/GPU usage.
- Model latency.
- Queue depth.
- Errors.
- Token usage.
- Service health.
- Traces.

Do not mix software telemetry with simulation events. OpenTelemetry-style traces can monitor the platform, but the simulation firehose remains a separate domain record.

### Command and event flow

```text
Agent / Scenario / Operator
          │
          ▼
     Typed Command
          │
          ▼
 Command Validation
          │
          ├── rejected ──► CommandRejected event
          │
          ▼
 Deterministic Resolver
          │
          ▼
   Domain Event(s)
          │
          ▼
 State Reducers / Systems
          │
          ├── World state
          ├── Agent observations
          ├── Social exposure
          ├── Analytics projections
          └── Firehose
```

The model never receives direct database write access.

### Recommended agent stack

```text
Agent
├── Identity and provenance
├── Body and physical condition
├── Roles and obligations
├── Needs and drives
├── Schedule
├── Perception filters
├── Working memory / blackboard
├── Episodic memory
├── Semantic knowledge
├── Claim and evidence graph
├── Relationship models
├── Trust models
├── Utility evaluation
├── Goal manager
├── GOAP / HTN / StateTree planner
├── Action executor
├── Dialogue policy
└── LLM adapter
```

### Decision hierarchy

Use the cheapest reliable mechanism first:

```text
1. Hard rule or safety invariant
2. Existing action execution
3. Schedule
4. State machine
5. Utility selection
6. GOAP or HTN planning
7. Cached learned policy
8. Small-model bounded decision
9. Larger-model novel reasoning
10. Human/operator escalation where configured
```

An LLM call should not be the default merely because it is available.

### Restricted roles for LLMs

Appropriate interfaces include:

```text
propose_intent(observation, goals, allowed_actions)

rank_bounded_options(options, agent_state)

realize_dialogue(communicative_intent, permitted_facts)

summarize_memories(memory_ids)

extract_claims(message)

generate_scenario_draft(user_description)

suggest_plan(goal, action_catalog)
```

In every case:

- Inputs are bounded.
- Outputs are schema-constrained.
- Proposed actions are validated.
- Model failure cannot corrupt state.
- Provider replacement does not alter core contracts.

Ollama and OpenRouter become implementations of an `AIProviderAdapter`, not dependencies inside the world model.

---

## 8. Information-provenance architecture

### Use claim objects, not boolean knowledge

```text
Claim
├── claim_id
├── proposition
├── subject references
├── asserted_by
├── original_source
├── source chain
├── evidence references
├── acquisition channel
├── acquired_at
├── valid-time interval
├── location context
├── confidence
├── source trust
├── corroboration status
├── contradiction links
├── mutation parent
└── current agent disposition
```

Use W3C PROV concepts—Entity, Activity, Agent, derivation and attribution—as a conceptual provenance basis. Use ActivityStreams-style Actor–Activity–Object structures for social actions such as Create, Like, Follow, Announce and Undo. These standards provide useful vocabularies without requiring that every runtime event be stored as RDF.

**Sources:**

- W3C PROV-O
- W3C ActivityStreams 2.0

### Separate social graphs

Do not maintain one generic “network.” Maintain distinct relationships:

- Knows.
- Follows.
- Communicates with.
- Works with.
- Lives with.
- Trusts in domain.
- Has blocked.
- Has recently seen.
- Receives recommendations from.
- Belongs to group.
- Can physically contact.
- Can digitally contact.

These networks overlap, but they are not interchangeable.

### Information transmission sequence

```text
World event occurs
        ↓
Perception system determines who can observe it
        ↓
Observation records are created
        ↓
Agents interpret observations into claims
        ↓
Communication actions transmit claims
        ↓
Platform ranking determines exposure
        ↓
Recipients evaluate claims
        ↓
Beliefs may change
        ↓
Behaviour may change
        ↓
New physical and information events occur
```

Nothing informationally teleports.

---

## 9. Firehose and replay design

Every accepted command and state transition should emit immutable events.

A practical envelope could contain:

```text
event_id
schema_version
world_id
scenario_id
branch_id
simulation_time
wall_clock_time
tick_or_sequence
event_type
actor_id
target_ids
command_id
location_reference
parent_event_ids
caused_by_event_ids
observation_scope
payload
result
uncertainty
data_provenance
plugin_id
plugin_version
rng_stream
rng_seed_or_position
model_provenance
created_at
```

### Event families

```text
world.*
agent.*
movement.*
perception.*
memory.*
belief.*
claim.*
communication.*
social.*
relationship.*
organization.*
economy.*
resource.*
infrastructure.*
scenario.*
model.*
validation.*
system.*
```

### Replay requirements

The platform should support:

- Replay without rerunning LLMs by using recorded model outputs.
- Deterministic non-LLM replay from the same data, versions and random streams.
- Branching at any snapshot.
- Counterfactual intervention after the branch point.
- Causal tracing from an action back to observations, beliefs, goals and commands.
- Comparison between branches.
- Corrections and retractions without deleting history.

---

## 10. Multi-resolution population simulation

A viable planetary system should use explicit fidelity levels.

### L0 — Aggregate

Population counts and flows:

- Births.
- Deaths.
- Migration.
- Employment.
- Demand.
- Aggregate opinion distributions.
- Disease or exposure states.

No individual LLM agents.

### L1 — Archetype or policy cohort

Groups share calibrated policies but retain distributions and uncertainty.

Example:

```text
Urban commuters with:
- employment distribution
- household constraints
- transport access
- schedule distributions
- response policy
```

### L2 — Scheduled individuals

Persistent individuals with:

- Home.
- Work.
- Household.
- Schedule.
- Resources.
- Relationships.
- Utility-based decisions.

Mostly deterministic or probabilistic classical simulation.

### L3 — Cognitive individuals

Focused agents receive:

- Detailed memory.
- Beliefs.
- Goals.
- Planning.
- Communication.
- Occasional model reasoning.

### L4 — Embodied local agents

Agents in an immediate region receive:

- Exact routes.
- Local navigation.
- Collision avoidance.
- Object affordances.
- Perception cones or ranges.
- Fine-grained action timing.

### Promotion and demotion

Promotion must preserve prior aggregate constraints. Demotion must compress state without erasing important commitments, relationships or causal history.

```text
Aggregate → Individual:
sample conditionally from recorded aggregate state

Individual → Aggregate:
retain summary, obligations, exceptional state and event references
```

---

## 11. Scientific and engineering validation

Every world and scenario should have a machine-readable ODD-style model specification covering:

- Purpose.
- Entities and state variables.
- Spatial and temporal scales.
- Process overview and scheduling.
- Design concepts.
- Initialization.
- Input data.
- Submodels.
- Stochastic processes.
- Calibration targets.
- Known limitations.

The ODD protocol was developed to make agent-based models more understandable, comparable and reproducible. Broader verification, validation and accreditation practices are necessary before using simulations for consequential conclusions.

Source: ODD Protocol for Describing Agent-Based and Other Simulation Models

### Minimum validation layers

**Structural verification**

Does the software implement the declared rules?

**Invariant testing**

Can an agent teleport, duplicate ownership or know inaccessible information?

**Empirical calibration**

Do mobility, schedules, communication, networks and resource use resemble relevant observed data?

**Sensitivity analysis**

How much do results change with:

- Random seed.
- Model provider.
- Model version.
- Prompt policy.
- Temperature.
- Trust parameters.
- Activation rate.
- Population synthesis assumptions.
- Routing assumptions.

**Out-of-sample tests**

Can the model reproduce withheld scenarios or time periods?

**Human comparison**

Where human behaviour is claimed, compare against actual human data rather than another LLM’s judgment.

**Uncertainty reporting**

Produce distributions and confidence intervals—not one authoritative generated future.

---

## 12. Non-negotiable acceptance tests

### Physical integrity

- Every location change has a valid path, mode and elapsed time.
- Agents cannot pass through inaccessible geometry.
- Object capacity and reservations are enforced.
- Travel interruption and rerouting work.

### Epistemic integrity

- No agent can reference an event without a valid observation or communication chain.
- Beliefs can differ from world truth.
- Contradictory claims coexist.
- Corrections do not erase original claims.

### Causal integrity

- “Why did the agent do this?” reconstructs:
  - observation,
  - belief,
  - goal,
  - selected plan,
  - command,
  - validator result,
  - resulting events.

### Replay integrity

- The same world snapshot, plugin versions and random streams reproduce deterministic core events.
- Recorded LLM responses can be replayed without calling the model provider.

### Provider independence

- Switching Ollama to OpenRouter changes adapter configuration, not world schemas or agent code.
- Model failure results in bounded fallback or inactivity, not corrupted state.

### Offline integrity

A city scenario must run with:

- Local OSM extract.
- Local PostGIS.
- Local Nominatim.
- Local routing tiles.
- Local PMTiles.
- Local models through Ollama.
- No required external analytics or telemetry.

### Counterfactual integrity

Two branches must remain identical before an intervention and diverge only through consequences after it.

### Scale integrity

A million population records must not imply a million simultaneously reasoning LLM agents.

### Social integrity

The system retains the complete lineage:

```text
event → witness → message → post → exposure → repost → reply → belief change
```

### Fault integrity

Malformed model output, timeouts, prompt injection or hostile content cannot obtain direct access to world-state mutation.

---

## 13. Recommended build order

### Phase 0 — Simulation constitution

Define before writing the main application:

- Invariants.
- Event schemas.
- Command schemas.
- Plugin contracts.
- Fidelity levels.
- ODD model template.
- Provenance rules.
- Replay contract.
- Model-call recording.
- Licensing gate.
- Acceptance tests.

### Phase 1 — One city, no LLM

Build a credible city simulation with:

- OSM/PostGIS.
- Nominatim.
- Valhalla.
- PMTiles.
- Simulation clock.
- Agent schedules.
- Valid routes and movement.
- Buildings and entrances.
- Smart-object affordances.
- Event firehose.
- Replay.

Do not begin with the entire planet.

### Phase 2 — Classical NPC cognition

Add:

- Perception.
- Blackboard.
- Needs.
- Utility selection.
- StateTree or behaviour tree.
- GOAP/HTN planning.
- Action channels.
- Reservations.
- Relationships.
- Organization membership.

Agents should already lead coherent lives before adding language models.

### Phase 3 — Bounded LLM capability

Add models only for:

- Dialogue realization.
- Claim extraction.
- Unfamiliar decision support.
- Long-horizon plan proposals.
- Memory compression.
- Scenario authoring assistance.

Keep deterministic fallbacks.

### Phase 4 — Information world

Add:

- Claims and evidence.
- Trust models.
- Direct messages.
- Group communication.
- Social posts.
- Feed algorithms.
- Reactions.
- Reposts.
- Fact-checking actions.
- Bad actors.
- Moderation.
- Information-space-only actors.

### Phase 5 — Multi-resolution scale

Add:

- Aggregate populations.
- Archetype policies.
- Promotion and demotion.
- Vectorized updates.
- Distributed partitions.
- Event-driven activation.
- Cached and compiled policies.

### Phase 6 — Empirical validation

Calibrate and test:

- Travel distributions.
- Time use.
- Household activity.
- Transport modes.
- Social networks.
- Information spread.
- Resource demand.
- Intervention response.
- Model and seed sensitivity.

Only after this phase should the platform make serious claims about scenario analysis.

---

## 14. Map, world and agent visualization strategy

### Verdict on the “thousands of dots” question

The instinct is correct, with one essential architectural separation:

> **The number of agents being simulated must not determine how many agents are rendered individually.**

Thousands of dots are useful in a raw operational or debugging view. They can reveal congestion, evacuation, crowd formation, migration, route choice and local activity. However, thousands of overlapping markers are usually poor as the default analytical interface because they hide density, overlap, uncertainty and movement patterns.

The system should therefore support both:

1. A raw individual-agent layer for debugging, inspection and demonstrations.
2. Scale-dependent aggregated representations for normal analysis.

The detailed “world” or embodied view is best used for a selected local area, street, building, floor, room or followed agent. A planet-scale 3D world containing every fully rendered person would be expensive, visually noisy and analytically weak.

### Separate simulation level of detail from visualization level of detail

These are independent systems.

**Simulation level of detail**

```text
S0 — Aggregate population
S1 — Statistical cohort or archetype
S2 — Persistent scheduled individual
S3 — Cognitive individual
S4 — Fully embodied local agent
```

**Visualization level of detail**

```text
V0 — Not individually rendered
V1 — Included in density, flow or aggregate cell
V2 — Included in a cluster
V3 — Rendered as an individual point or icon
V4 — Rendered as a detailed character or local embodied entity
```

An agent can be simulated as a persistent individual while being displayed only as part of an H3 cell or cluster. Conversely, a decorative point should never imply that a full LLM cognition loop is running behind it.

### Recommended spatial display hierarchy

| Geographic scale | Default visual representation | Optional detail |
| --- | --- | --- |
| Planet | Regional aggregates, major flows, event zones and scenario boundaries | Selected countries, organizations or global routes |
| Country or large region | H3/grid aggregates, migration and transport flows, major incidents | Cohorts, selected agents and administrative comparisons |
| City or district | Clusters, density surfaces, activity areas, selected routes and active incidents | Individual agents, vehicles and buildings where useful |
| Street or neighbourhood | Individual agents, vehicles, queues, routes, entrances and local events | Perception ranges, conversations and object interactions |
| Building exterior | Entrances, exits, occupancy, queues, access state and selected occupants | Floor selector and internal route preview |
| Building interior | Floors, rooms, doors, stairs, lifts, objects, occupants and affordances | Fully embodied movement and interaction |
| Selected agent | Continuous location, route, activity, knowledge, goals and history | Agent-perspective view and causal explanation |

The exact map zoom thresholds should be configurable by world type, display size and density. They should not be hard-coded into the simulation model.

### Raw-dot mode should remain available

A raw-dot layer is valuable for:

- Simulation debugging.
- Verifying movement continuity.
- Detecting teleportation or route errors.
- Inspecting crowd behaviour.
- Demonstrating exact population positions.
- Following selected cohorts.
- Comparing simulated and observed mobility.

It should clearly state whether points represent:

- Exact positions.
- Interpolated positions.
- Last-known positions.
- Sampled agents.
- Synthetic positions within an aggregate.
- Privacy-preserving or deliberately coarsened locations.

### Do not use random movement to make the map look alive

A quiet residential street at 03:00 may correctly contain little or no movement. Adding artificial movement for visual excitement damages realism.

The map should be allowed to look:

- Quiet.
- Uneven.
- Concentrated.
- Repetitive.
- Temporarily inactive.
- Highly active only around specific events.

A serious simulation should optimize for truthful state communication, not permanent visual spectacle.

### Recommended view modes

The product should offer explicit view modes rather than one overloaded map:

```text
Operational Map
    2D geographic analysis, layers, events, routes and density

Local World
    Detailed street, site or neighbourhood scene

Building / Indoor
    Floors, rooms, indoor topology, occupants and affordances

Agent Follow
    Continuous selected-agent journey and state

Information Space
    Posts, messages, claims, exposure and diffusion

Debug / Omniscient
    Ground truth, raw events, invariants and exact state
```

Changing mode must preserve:

- Selected world and scenario.
- Simulation time.
- Selected entities.
- Filters.
- Branch.
- Camera context where possible.

The user should feel that they are changing the lens on one world, not opening unrelated applications.

---

## 15. Randomness, noise and uncertainty

### Randomness is necessary, but arbitrary randomness is not

Human, environmental and social systems should not be perfectly deterministic. Similar agents can make different choices, travel times vary, attention is imperfect and messages can be missed. The correct implementation is bounded stochasticity inside explicit mechanisms.

**Bad randomness:**

```text
Agent randomly changes belief.
Agent randomly posts.
Agent randomly becomes angry.
Agent randomly walks to another city.
Agent randomly appears at a destination.
```

**Good randomness:**

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

Do not create one generic randomness slider. Model separate mechanisms.

| Noise type | Example | Required constraint |
| --- | --- | --- |
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

**Sources:**

- Hypothetical Outcome Plots Help Untrained Observers Judge Trends in Ambiguous Data
- Visual Reasoning Strategies for Effect Size Judgments and Decisions
- Visualizing Uncertainty in Probabilistic Graphs with NetHOPs

---

## 16. UI/UX research foundation

### Treat the product as a visual analytics environment

This is not primarily a chat application, a game HUD or a conventional business dashboard. It is a visual analytics and simulation-control environment combining:

- Geographic data.
- Temporal data.
- Networks and graphs.
- Event streams.
- Agent state.
- Scenario configuration.
- Uncertainty.
- Provenance.
- System operations.

The interface must help users move from overview to explanation without losing spatial, temporal or causal context.

### Apply the Visual Information-Seeking Mantra

Ben Shneiderman’s established pattern is directly applicable:

> **Overview first, zoom and filter, then details on demand.**

The original taxonomy also includes relating items, preserving history and extracting subsets. That maps closely to this product:

```text
Overview
    World, region, population and event state

Zoom
    Region → city → street → building → room → agent

Filter
    Time, entity type, event type, scenario, confidence and source

Details on demand
    Entity inspector, event record, claim provenance and route

Relate
    Who knew whom, which event caused what, and what occupied the same place

History
    Replay, undo, branches, saved views and investigation history

Extract
    Export a cohort, event chain, route, region or scenario result
```

Source: *The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations*

### Use Munzner’s nested model for design and validation

Visualization decisions should be evaluated at four separate levels:

1. **Domain problem:** What real task is the analyst, world builder or operator trying to complete?
2. **Data and task abstraction:** Which entities, attributes, relationships and actions represent that task?
3. **Visual encoding and interaction:** Which map, timeline, graph, table or control best supports it?
4. **Algorithm:** Can the interface calculate and render the result correctly and efficiently?

An attractive visualisation cannot repair the wrong task abstraction. A fast renderer cannot repair misleading encodings.

Source: *A Nested Model for Visualization Design and Validation*

### Use coordinated multiple views

Map, timeline, event table, charts and graph views should be linked through one selection model.

For example:

```text
Brush time range on timeline
        ↓
Map shows only matching movement and events
        ↓
Event table filters to the same interval
        ↓
Selecting a claim highlights its social path
        ↓
Agent inspector shows belief state at that exact time
```

Brushing and linking is an established visual-analysis interaction for exploring relationships across views.

Source: Vega brushing and linking example

### Use progressive disclosure, not feature removal

The platform will be inherently complex. The solution is not to hide all power or place every control on one screen.

Use three interface levels:

```text
Standard
    Common world exploration, agent inspection and scenario playback

Advanced
    Layer configuration, uncertainty, branches, parameter controls and provenance

Developer / Research
    Raw events, schemas, model calls, seeds, plugin state and invariants
```

Critical risk, uncertainty and assumptions must never be hidden merely to make the interface look simple.

### Preserve the user’s mental map

When users zoom, open a building, select an agent or switch to a graph, preserve orientation through:

- Stable selection.
- Breadcrumbs.
- Visible parent context.
- Consistent spatial anchors.
- Smooth but restrained transitions.
- Back and forward navigation.
- Saved investigation history.

The user should always be able to answer:

- Where am I?
- At what simulation time?
- In which scenario and branch?
- What filters are active?
- Am I seeing ground truth, an agent’s belief or an aggregate projection?

---

## 17. Product information architecture

### Primary user roles

The interface should be role-aware without creating separate incompatible products.

| Role | Primary tasks |
| --- | --- |
| World builder | Import or generate geography, define entities, configure systems and validate world structure |
| Scenario author | Establish conditions, interventions, variables, seeds, metrics and experiment branches |
| Analyst | Explore patterns, compare outcomes, inspect cohorts and explain anomalies |
| Investigator | Trace claims, actions, provenance, causality and bad-actor behaviour |
| Simulation operator | Start, pause, monitor, recover and manage long-running simulations |
| Researcher | Calibrate, validate, run ensembles and examine sensitivity |
| Developer | Inspect events, plugins, model calls, schemas, performance and invariants |

### Recommended workspaces

1. **World Explorer** — map, local world, layers, entities and live state.
2. **Scenario Studio** — scenario creation, assumptions, interventions and run configuration.
3. **Agent and Group Inspector** — lives, plans, state, relationships, knowledge and history.
4. **Information Space** — messages, claims, feeds, diffusion, trust and moderation.
5. **Timeline and Replay** — playback, branching, comparison and causal navigation.
6. **Event Firehose** — structured event investigation and export.
7. **Validation Lab** — calibration, metrics, ensembles, sensitivity and observed-data comparison.
8. **System Console** — plugins, adapters, model providers, queues, health and storage.

### Recommended desktop layout

This should be a desktop-first analysis environment. Mobile can support monitoring and lightweight inspection, but complex world authoring should not be forced into a phone-first layout.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ World / Scenario / Branch / Time       Search      Run state      Commands │
├──────────────┬───────────────────────────────────────┬──────────────────────┤
│ Workspace    │                                       │ Inspector            │
│ navigation   │              Main canvas              │                      │
│              │       Map / world / graph / chart     │ Entity / event /     │
│ Layers       │                                       │ claim / route /      │
│ Filters      │                                       │ configuration        │
│ Saved views  │                                       │                      │
├──────────────┴───────────────────────────────────────┴──────────────────────┤
│ Timeline / playback / event density / branch markers / annotations         │
└─────────────────────────────────────────────────────────────────────────────┘
```

Panels should be:

- Resizable.
- Dockable where practical.
- Collapsible.
- Restorable to a known layout.
- Saved by workspace.
- Keyboard reachable.

Map camera padding must respond to panel dimensions so opening the inspector does not hide the selected entity. MapLibre exposes viewport edge insets specifically to shift the apparent map centre around floating or resized UI.

Source: MapLibre EdgeInsets

### Global context strip

A persistent context strip should always show:

```text
World: London Baseline
Scenario: Transport Disruption
Branch: Intervention B
Simulation time: 2026-09-02 08:42:12
Playback: Paused
Truth mode: Analyst ground truth
Seed: 1042
Active filters: 4
```

This prevents screenshots, exports and decisions from losing essential context.

---

## 18. World Explorer and multiscale map UX

### Use semantic zoom

Zoom should change meaning, not simply make the same symbols larger.

An illustrative default policy is:

| View band | Display policy |
| --- | --- |
| Globe or planet | Regions, macro flows, major events and aggregate indicators |
| Continental or country | H3/grid aggregates, administrative comparisons and transport corridors |
| Regional or city | Density, clusters, origin-destination flows, buildings and selected individuals |
| Neighbourhood or street | Individual agents, vehicles, routes, entrances, queues and local events |
| Site or building | Access points, occupancy, floors, indoor links and selected activities |
| Room or immediate local area | Embodied agents, objects, affordances, perception and exact movement |

MapLibre’s own performance guidance recommends clustering large point sets, controlling zoom ranges and simplifying styles. deck.gl provides heatmap, grid, hexagon and cluster layers for aggregated views. H3 supplies a hierarchical spatial index that can move between parent and child resolutions efficiently, but its hierarchy has exact logical containment and approximate geometric containment, so exact boundary decisions still require proper geometry tests.

**Sources:**

- MapLibre guidance for large datasets
- deck.gl layer catalogue
- deck.gl aggregation layers
- H3 hierarchical indexing

### Recommended rendering split

```text
MapLibre GL JS
    Basemap, vector tiles, labels, roads, buildings, terrain and map camera

PMTiles / Protomaps
    Offline tile packaging and delivery

deck.gl
    Large agent layers, paths, trips, flows, grids, H3 cells and analytical overlays

DOM / accessible UI
    Controls, inspector, legends, textual summaries and keyboard alternatives
```

Do not render thousands of agents as individual DOM markers. Use GPU layers or tile-based projections.

### Layer manager

Every visual layer should declare:

- Name and purpose.
- Data source.
- Time coverage.
- Spatial resolution.
- Aggregation method.
- Whether it represents truth, belief, observation or estimate.
- Whether locations are exact, sampled or coarsened.
- Legend.
- Visible zoom range.
- Performance cost.
- Export rules.

Users should be able to reorder, hide, pin and save layer presets. However, the interface should limit simultaneous high-salience overlays so the map does not become an unreadable collection of colours and symbols.

### Default map presets

```text
Population
Mobility
Incidents
Information diffusion
Organizations and influence
Infrastructure
Resources and economy
Scenario interventions
Validation comparison
Debug geometry
```

A preset changes several coordinated layers and legends, not the underlying simulation.

### Selection patterns

Support more than clicking tiny points:

- Click to inspect.
- Hover for lightweight preview where pointer input exists.
- Lasso or box selection.
- Radius selection.
- Route corridor selection.
- Select all occupants of a building.
- Select all agents exposed to a claim.
- Select a cohort from a chart and highlight it on the map.
- Search by agent, organization, place, event or OSM identifier.

Every map selection should have a table or list equivalent.

### Selected-agent focus

Selecting an agent should create a persistent focus state rather than a temporary popup.

```text
Agent A-10482
Current location: Bus 22, segment 18
Destination: Workplace
Journey progress: 63%
Current action: Travelling
Next decision point: Stop 14
Known disruption: Neighbour report, medium confidence
Simulation fidelity: S3 Cognitive individual
Display fidelity: V3 Individual marker
```

The user can:

- Follow.
- Pin without following.
- Compare with another agent.
- Open agent perspective.
- Open history.
- Trace why the current plan was selected.

### Ground-truth and perspective modes

The product must visibly distinguish:

```text
Analyst truth mode
    Shows authoritative simulation state

Agent perspective mode
    Shows only what the selected agent can perceive, remember or infer

Public information mode
    Shows information available through public channels

Scenario author mode
    Shows interventions and hidden experimental configuration
```

When ground truth is visible, use a persistent mode label or watermark. Otherwise users may accidentally interpret privileged simulator state as something agents knew.

---

## 19. Building and interior world UX

### Use the map for orientation and the local world for embodiment

The recommended default is:

- 2D map for regional and operational work.
- Optional 3D city view for height, terrain and local context.
- Detailed local scene for selected sites and streets.
- Floor-based indoor view for buildings.

A global 3D globe should be a context view, not the primary analytical surface. Three-dimensional views introduce occlusion, orientation and performance problems. They are justified when vertical relationships, line of sight, floors, terrain or embodied movement matter.

### Indoor model

A building should expose:

```text
Building
├── Site boundary
├── Entrances and exits
├── Floors and levels
├── Rooms and zones
├── Corridors
├── Doors and access restrictions
├── Stairs, lifts and ramps
├── Indoor navigation graph
├── Objects and affordances
├── Occupancy and capacity
├── Utilities and hazards
└── Current events
```

OGC IndoorGML is specifically designed around indoor spaces, topology and navigation relationships. It is a useful conceptual model even if the runtime uses a different encoding.

Source: OGC IndoorGML

### Building interaction pattern

```text
Select building on map
        ↓
Inspector shows occupancy, access and active events
        ↓
Open building
        ↓
Choose floor or follow selected agent automatically
        ↓
Display rooms, routes, doors and occupants
        ↓
Inspect object, activity or conversation
```

The transition should preserve the selected building and simulation time. Users must be able to return to the city view without losing their investigation.

### Floor and room controls

Provide:

- Floor stack with occupancy and alert counts.
- “Follow selected agent” floor switching.
- Ghosted adjacent-floor context where useful.
- Indoor route preview.
- Accessibility route option.
- Entrance and exit state.
- Capacity and reservation overlays.
- Hazard and visibility overlays.
- Textual room list as an accessible alternative.

### Exact versus aggregate indoor position

At lower fidelity, the system may know that an agent is “inside Building X” or “on Floor 2” without an exact room coordinate. The UI must not fabricate a precise dot.

Use explicit position quality:

```text
Exact
Route-interpolated
Room-level
Floor-level
Building-level
Area estimate
Unknown
```

---

## 20. Agent, group and organization inspector

### Inspector structure

The inspector should use stable tabs or sections:

```text
Overview
Current state
Location and movement
Schedule and plans
Needs and resources
Knowledge and beliefs
Memory
Relationships and trust
Groups and organizations
Communications
Actions and decisions
Timeline
Provenance and debug
```

The overview should remain compact. Advanced and developer details can be progressively disclosed.

### Structured “Why?” explanations

Do not expose or fabricate hidden chain-of-thought. Provide a structured causal explanation derived from recorded state and events.

Example:

```text
Why did A leave work early?

Observed:
- Message M-883 from school at 14:02
- Child pickup was required before 15:00

Believed:
- Normal route would be delayed by road closure
- Confidence: 0.81

Goal selected:
- Reach school before 15:00

Plan:
- Leave work → walk to station → take train → walk to school

Constraints:
- Car unavailable
- Bus route affected

Result:
- Departed at 14:08
```

Every row should link to the supporting event, claim, route or state record.

### Truth-versus-belief comparison

For analysts, provide a comparison view:

| Topic | World truth | Agent belief | Evidence available to agent |
| --- | --- | --- | --- |
| Bridge status | Closed | Probably closed | Neighbour message and delayed bus |
| Cause | Structural damage | Possible accident | No direct evidence |
| Reopening time | Unknown | Believes 17:00 | Unverified social post |

This makes epistemic differences understandable without merging them.

### Group and organization inspection

Groups should have their own state, not just a member list:

- Purpose.
- Membership and roles.
- Leadership.
- Rules and decision process.
- Resources and assets.
- Territory and locations.
- Internal communication channels.
- External relationships.
- Current objectives.
- Decisions and history.

Selecting an organization should highlight relevant sites, members, supply relationships and information channels across linked views.

---

## 21. Information-space and virtual social-media UX

### Separate participant experience from analyst experience

The virtual platform should support two distinct interfaces:

**Participant platform view**

What an in-world user or bot experiences:

- Feed.
- Search.
- Posts.
- Replies.
- Likes.
- Reposts.
- Messages.
- Groups.
- Moderation actions.

**Analyst information-space view**

What a researcher or investigator needs:

- Exposure graph.
- Claim lineage.
- Source provenance.
- Belief change.
- Trust context.
- Recommendation causes.
- Coordination patterns.
- Bot or bad-actor indicators.
- Ground-truth comparison.

Do not put privileged analytical overlays into the participant feed unless the scenario explicitly models such tools.

### Distinguish actions and interpretations

The interface must not equate:

```text
Viewed
Understood
Believed
Endorsed
Liked
Reposted
Commented
Acted upon
```

A repost may represent endorsement, criticism, mockery, warning, archiving or coordinated amplification. Store observable actions separately from inferred motives.

### Claim provenance view

A selected claim should show:

```text
World event E-142
    ↓ directly observed by A
Claim C-1 created by A
    ↓ told face-to-face to B
Claim C-2 paraphrased by B
    ↓ sent to C
Post P-9 created by C
    ├── viewed by D
    ├── reposted by E
    └── challenged by F
            ↓
        F messages A for verification
```

The user should be able to switch between:

- Timeline.
- Sankey/flow view.
- Ego network.
- Geographic diffusion.
- Claim version comparison.
- Tabular provenance.

Avoid displaying the entire social network as one node-link “hairball.” Default to a selected claim, actor, community or time window.

### Recommendation transparency

For a simulated platform, the analyst should be able to inspect why a post was eligible for a feed:

```text
Follow relationship
Community membership
Recency
Topic affinity
Engagement score
Paid or promoted status
Moderation state
Experiment treatment
```

The participant-facing platform does not necessarily expose all of this, but the simulation firehose should.

---

## 22. Scenario Studio UX

### Scenario creation workflow

A scenario should be assembled through a validated sequence:

```text
1. Choose or create world
2. Define geographic and temporal scope
3. Select population and fidelity policy
4. Configure systems and adapters
5. Define baseline conditions
6. Add interventions and triggers
7. Define uncertainty and seeds
8. Choose metrics and stopping conditions
9. Validate assumptions and invariants
10. Run baseline, branches or ensemble
```

### Scenario Studio layout

Use coordinated surfaces:

- Map for geographic scope and interventions.
- Timeline for scheduled events and triggers.
- Form/editor for parameters.
- Dependency panel for affected systems.
- Assumption register.
- Validation panel.
- Cost and performance estimate.
- Diff against previous version.

### Interventions should be typed

Examples:

```text
CloseRoad
ChangePrice
RemovePower
IssuePublicAlert
ChangePolicy
AddWeatherEvent
IntroduceClaim
ChangeLeadership
ModifyTransportSchedule
DisableCommunicationChannel
```

The interface should explain:

- Preconditions.
- Target scope.
- Start and end.
- Direct effects.
- Systems that may propagate consequences.
- Whether agents can know about it immediately.
- Whether it is a ground-truth event or information-only injection.

### Advanced authoring

Support three synchronized authoring modes:

1. Guided forms for common scenarios.
2. Visual timeline/map authoring.
3. Versioned JSON or YAML for advanced users.

All three must compile to the same typed scenario schema. Editing source should update the visual representation after validation, and visual edits should produce a reviewable source diff.

### Assumption register

Every scenario should display assumptions such as:

```text
Population generated from census distribution 2025-Q4
Public transport timetable source dated 2026-07-01
Weather model: synthetic baseline profile
Agent trust model: experimental v2
LLM provider: local Ollama model X
No mobile-network outage unless explicitly introduced
```

Assumptions are part of the scenario result, not hidden configuration.

### Pre-run validation

Block or warn on:

- Missing geography.
- Unreachable required locations.
- Invalid dates.
- Impossible capacities.
- Undefined plugins.
- Incompatible adapter versions.
- Missing seed policy.
- No recorded outcome metrics.
- Information injected without a channel.
- Intervention that silently reveals ground truth to agents.

---

## 23. Timeline, replay, branching and comparison UX

### Timeline is a first-class navigation surface

The timeline should show:

- Current simulation time.
- Playback state.
- Event density.
- Scenario interventions.
- Agent or group milestones.
- Claim propagation.
- Infrastructure incidents.
- Snapshots.
- Branch points.
- User annotations.

Users should be able to zoom from years to seconds while keeping the same selected entities and filters.

### Separate simulation time from rendering time

A simulation may run faster than the interface can animate. The UI should:

- Consume authoritative timestamps.
- Interpolate position only for presentation.
- Batch updates when necessary.
- Never imply that skipped visual frames were skipped simulation events.
- Clearly indicate live, buffered, paused and replay modes.

### Branching model

```text
Baseline
    ├── Branch A: Bridge remains open
    ├── Branch B: Bridge closes at 08:20
    │       └── Branch B2: Public alert at 08:24
    └── Branch C: Bus capacity increased
```

A branch comparison should show:

- Shared history before the branch point.
- Exact intervention difference.
- Divergence over time.
- Outcome metrics.
- Difference maps.
- Different affected cohorts.
- Causal paths leading to major divergence.

### Comparison patterns

Use the appropriate pattern for the task:

- Side-by-side small multiples for spatial comparison.
- Swipe or synchronized cameras for local map comparison.
- Difference layers for quantitative change.
- Aligned timelines for event sequence comparison.
- Distribution plots for ensembles.
- Cohort tables for who changed outcome.
- Causal explanation for why branches diverged.

Avoid rapidly toggling two maps as the only comparison method; it burdens memory and can conceal small differences.

### Investigation history

Shneiderman’s original taxonomy emphasizes history for undo, replay and progressive refinement. Preserve:

- Map extents.
- Filters.
- Selections.
- Queries.
- Opened entities.
- Branch changes.
- Annotations.

Users should be able to save an investigation as a shareable view without changing the world state.

---

## 24. Event firehose and causal explorer UX

### The firehose must not become an unreadable terminal

The underlying event stream can be enormous. The interface should provide:

- Live tail with pause.
- Virtualized event table.
- Time and sequence filters.
- Event-type facets.
- Actor, target, place and claim filters.
- Full-text and structured query.
- Saved queries.
- Sampling only for display, never for canonical storage.
- Aggregation by time, type, location or actor.
- Export of the exact matching event set.

### Event detail

Each event detail should include:

```text
Event identity and schema version
World, scenario and branch
Simulation time and sequence
Actor and targets
Location
Command that produced the event
Parent and causal events
Validation result
Plugin and version
Random stream reference
Model-call reference where applicable
Payload
State changes
Who could observe it
Derived projections
```

### Causal navigation

Users should be able to move both directions:

```text
Why did this happen?
    Event ← command ← selected plan ← goal ← belief ← observation ← source event

What did this cause?
    Event → observations → claims → actions → later world changes
```

### Raw and human-readable views

Provide:

- Human summary.
- Structured fields.
- Raw JSON or binary-decoded payload.
- Schema documentation.
- Related events.

The human summary is a projection. The structured record remains authoritative.

---

## 25. Design system

### Design principles

The design system should encode these principles:

1. **Evidence over spectacle.** Visual polish must not hide uncertainty or assumptions.
2. **Context is persistent.** World, scenario, branch, time and truth mode remain visible.
3. **Details on demand.** Do not expose every control at once.
4. **Truth, belief and claim are visually distinct.** Never merge their semantics.
5. **Actions are reversible where possible.** Exploration does not mutate the simulation.
6. **Writes are explicit.** Scenario or world changes require a clear command and validation result.
7. **State is never communicated by colour alone.** Use text, shape, icon or pattern as well.
8. **Dense does not mean chaotic.** Support compact expert workflows with hierarchy and alignment.
9. **Motion communicates state change, not decoration.**
10. **Every visualization has a table, summary or query alternative.**

### Token architecture

Use the Design Tokens Community Group format as the interchange format for design decisions. The 2025.10 format is the first stable community specification and supports vendor-neutral exchange across tools and platforms.

**Sources:**

- Design Tokens Community Group
- Design Tokens Format Module 2025.10

Recommended token layers:

```text
Primitive tokens
    Raw colour ramps, font families, type scales, spacing, radii and durations

Semantic UI tokens
    Surface, text, border, focus, selected, disabled, warning and danger

Domain tokens
    World truth, observation, belief, inference, claim status, intervention and uncertainty

Visualization tokens
    Map layers, density, flow, route, comparison, selection and confidence

Component tokens
    Inspector, timeline, layer panel, event grid, scenario editor and map controls
```

Example conceptual token structure:

```json
{
  "domain": {
    "truth": {
      "observed": {
        "$type": "color",
        "$value": "{color.semantic.verified}"
      }
    },
    "claim": {
      "unverified": {
        "$type": "color",
        "$value": "{color.semantic.caution}"
      },
      "disputed": {
        "$type": "color",
        "$value": "{color.semantic.conflict}"
      }
    },
    "selection": {
      "primary": {
        "$type": "color",
        "$value": "{color.semantic.accent}"
      }
    }
  }
}
```

Do not hard-code map colours separately from the application design system. Compile the same token source into:

- CSS custom properties.
- TypeScript token definitions.
- MapLibre style fragments and expressions.
- deck.gl layer themes.
- Chart themes.
- Documentation examples.

### Domain visual language

The visual system needs explicit semantic roles for:

- Authoritative world truth.
- Direct observation.
- Reported claim.
- Agent belief.
- Inference.
- Unknown state.
- Disputed state.
- Corroborated state.
- Scenario intervention.
- Simulation warning.
- Validation failure.
- Selected entity.
- Followed entity.
- Comparison branch A and B.

Each role needs:

- Colour role.
- Icon or marker shape.
- Text label.
- Pattern or line style where relevant.
- Light, dark and high-contrast treatment.

For maps, use cartographic palette practices rather than arbitrary interface colours. ColorBrewer provides sequential, diverging and qualitative schemes with options for colour-blind, print and photocopy safety.

Source: ColorBrewer 2.0

### Typography

Use a highly readable interface family and a separate monospaced family for:

- Identifiers.
- Event types.
- Times.
- Coordinates.
- JSON.
- Queries.

Define at least:

- Display or workspace title.
- Section heading.
- Panel heading.
- Body.
- Dense table.
- Caption and metadata.
- Code and event payload.

Long prose should not dominate the main map workspace. Use short summaries with expandable evidence.

### Density modes

Support:

```text
Comfortable
    General use and onboarding

Compact
    Analyst and operator workflows

Presentation
    Larger text and simplified controls for shared screens
```

Density changes spacing and row height, not the amount of evidence available.

### Motion system

Define motion tokens by purpose:

- State transition.
- Spatial navigation.
- Selection confirmation.
- Live update.
- Alert.

Avoid constant pulsing and moving markers. Respect prefers-reduced-motion; provide dissolve, instant or static alternatives for camera fly-throughs, animated paths and uncertainty animations.

Source: MDN: prefers-reduced-motion

### Core component inventory

```text
AppShell
WorkspaceNavigation
ContextStrip
MapCanvas
LocalWorldCanvas
LayerManager
MapLegend
SimulationControls
Timeline
BranchTree
EntityInspector
AgentSummary
BeliefTruthComparison
ClaimProvenance
CausalTrail
EventGrid
EventDetail
ScenarioForm
InterventionEditor
AssumptionRegister
ValidationPanel
FilterBuilder
SavedView
CommandPalette
SearchOmnibox
StatusBadge
SplitPane
DockPanel
EmptyState
ErrorBoundary
OfflineStatus
```

### Design-system repository structure

```text
packages/
├── design-tokens/
│   ├── source/
│   ├── themes/
│   ├── map-themes/
│   └── build/
├── ui-primitives/
├── ui-components/
├── domain-components/
├── map-components/
├── chart-themes/
├── icons/
├── accessibility/
└── storybook/
```

Every domain component should have deterministic fixture stories based on recorded simulation events so design review does not depend on a live backend.

---

## 26. Frontend and application architecture

### Architectural principle

The interface is a client of the world. It must not become the world authority.

```text
User gesture
    ↓
Typed UI intent
    ↓
Command API
    ↓
Server validation and simulation kernel
    ↓
Authoritative event
    ↓
Read-model projection
    ↓
UI update
```

The UI must never mutate authoritative world state locally and then assume success.

### API boundaries

```text
World Query API
    Entity snapshots, relationships, read models and search

World Command API
    Explicit validated mutations and simulation controls

Event Stream API
    Ordered live or replayed domain events

Tile and Geometry API
    Vector tiles, PMTiles, terrain, indoor geometry and analytical tiles

Gazetteer API
    Place, street, address and OSM object search

Scenario API
    Versioned definitions, validation, branches and runs

Analytics API
    Aggregates, distributions, metrics and comparison results

Plugin Registry API
    Manifests, compatibility, capabilities and permissions
```

### Recommended data flow

```text
Authoritative event store
        ↓
Projection services
        ├── Entity read model
        ├── Spatial tiles and H3 aggregates
        ├── Timeline buckets
        ├── Social and claim graph projections
        ├── Metrics and validation projections
        └── Search indexes
                ↓
        Query and streaming gateway
                ↓
        Client caches and Web Workers
                ↓
        Map, timeline, graph, tables and inspector
```

The map should consume spatial projections designed for the current zoom and filters, not the entire event store.

### Client-state separation

Maintain separate stores for:

**Authoritative server state**

- Entity snapshots.
- Events.
- Scenario definitions.
- Branch state.
- Simulation run state.
- Read-model results.

**Ephemeral interaction state**

- Current viewport.
- Hover.
- Open panels.
- Unsaved filter edits.
- Selection rectangle.
- Inspector tab.

**Persisted user workspace state**

- Saved views.
- Panel layout.
- Layer presets.
- Query history.
- Density preference.
- Accessibility preferences.

**Draft mutation state**

- Scenario edits.
- World edits.
- Pending command.
- Validation errors.

Draft state must never be confused with accepted world state.

### Streaming architecture

The event gateway should support:

- Ordered sequence numbers.
- Resume after disconnect.
- Gap detection.
- Backpressure.
- Batch delivery.
- Subscription filters.
- Snapshot plus delta synchronization.
- Live and replay streams through the same envelope where practical.

The UI may batch visual updates, but it must retain the highest received sequence and clearly indicate when it is behind live time.

### Rendering pipeline

```text
Binary or tiled spatial data
        ↓
Web Worker decode and filter
        ↓
Typed arrays / GPU buffers
        ↓
MapLibre and deck.gl layers
        ↓
Accessible DOM summary and controls
```

Use workers for:

- Decoding.
- Aggregation.
- Filtering.
- Route interpolation.
- Geometry simplification.
- Event bucketing.

Avoid sending every raw event through the React component tree.

### UI plugin architecture

UI extensions should use versioned manifests and stable extension points.

```ts
interface WorldUiPluginManifest {
  id: string;
  version: string;
  compatibleCore: string;
  permissions: string[];
  routes?: UiRouteContribution[];
  panels?: PanelContribution[];
  mapLayers?: MapLayerContribution[];
  inspectors?: InspectorContribution[];
  eventRenderers?: EventRendererContribution[];
  scenarioEditors?: ScenarioEditorContribution[];
  commands?: CommandContribution[];
}
```

Rules:

- Plugins cannot write directly to the core store.
- World mutations go through typed commands.
- Plugins declare event schemas and permissions.
- UI contributions have lifecycle and disposal hooks.
- Compatibility is checked before loading.
- Untrusted plugins run in a restricted boundary where possible.
- One plugin failure cannot collapse the main world explorer.

### Suggested web stack

This is a candidate architecture, not a mandatory dependency list:

| Concern | Candidate |
| --- | --- |
| Application shell | React + TypeScript |
| Basemap and vector tiles | MapLibre GL JS |
| Offline tile archive | PMTiles / Protomaps |
| Large geospatial overlays | deck.gl |
| Spatial aggregation | Server projections plus H3 where suitable |
| Charts and linked views | Vega / Vega-Lite or another declarative chart layer |
| Accessible primitives | React Aria, Radix-style primitives or equivalent reviewed components |
| Event and data tables | Virtualized table/grid |
| Local processing | Web Workers and transferable typed arrays |
| Offline client storage | IndexedDB or Origin Private File System where supported |
| Component documentation | Storybook or equivalent |
| Token compilation | DTCG-compatible token pipeline |

The adapter architecture should allow the map, chart and component implementations to change without changing domain contracts.

### Offline architecture

Offline mode should package or locally serve:

- PMTiles.
- World and scenario metadata.
- Gazetteer.
- Routing data.
- Building and indoor geometry.
- Local model endpoints.
- Event and snapshot storage.
- Design-system assets.

The interface should display:

```text
Offline: fully available
Offline: map available, model unavailable
Offline: read-only replay
Online provider active
```

Never silently fall back from a local provider to a remote provider.

### AI assistant in the UI

A natural-language assistant can help users:

- Build a filter.
- Find an entity.
- Draft a scenario.
- Explain a selected event.
- Suggest a comparison.
- Translate a question into a query.

It must:

- Show the structured query or command it generated.
- Cite event and entity sources.
- Distinguish evidence from inference.
- Require explicit confirmation before mutation.
- Never directly alter scenario or world state.
- Remain optional; core tasks must be available through normal controls.

---

## 27. Performance architecture for the interface

### Use aggregation before sampling

For density and counts, aggregation generally preserves meaning better than arbitrary sampling. If sampling is used, the interface must state the method and sample size.

Recommended strategies:

- Server-generated vector tiles.
- H3 or grid aggregates.
- Zoom-dependent clustering.
- GPU aggregation.
- Time bucketing.
- Spatial and temporal query windows.
- Cohort summaries.
- Progressive loading.

### Avoid common rendering failures

Never:

- Render every agent as a DOM element.
- Send the whole world graph to the browser.
- Recalculate all aggregates on every pan.
- Let every event trigger a full application render.
- Keep invisible 3D building interiors loaded globally.
- Load full agent memories into list views.
- Animate at simulation-event frequency.

### Local fidelity activation

When a user enters a building or follows an agent, the UI can request a higher-detail projection for the local area.

```text
City projection
    ↓ select building
Building projection requested
    ↓ open floor
Indoor geometry and occupant state requested
    ↓ follow agent
Fine movement stream requested
```

Leaving the area should release high-detail resources after a controlled cache period.

### Degradation policy

When device or stream capacity is limited, degrade in a defined order:

1. Reduce decorative motion.
2. Reduce update frequency while preserving timestamps.
3. Reduce geometry detail.
4. Replace individual points with clusters.
5. Replace clusters with aggregate cells.
6. Disable optional 3D.

Do not silently drop authoritative event categories.

### Performance instrumentation

Measure separately:

- Initial shell load.
- Time to first usable map.
- Pan and zoom frame rate.
- Selection response.
- Inspector load.
- Stream lag.
- Event-table filtering.
- Building transition.
- Memory and GPU use.
- Offline startup.

Performance telemetry belongs to the software-observability plane, not the simulation firehose.

---

## 28. Accessibility and inclusive design

### Standard

Target WCAG 2.2 AA for the web application, with selected AAA practices where feasible. WCAG 2.2 includes requirements concerning focus visibility, focus not being obscured, dragging alternatives and minimum target size.

**Sources:**

- WCAG 2.2
- What is new in WCAG 2.2

### The map cannot be the only interface

Provide equivalent access through:

- Search.
- Entity lists.
- Event tables.
- Place hierarchy.
- Route steps.
- Textual visible-area summaries.
- Keyboard selection.
- Saved queries.

A screen-reader user should be able to ask:

```text
Which incidents are visible in the current region?
Which selected agents are moving?
What building is selected?
What changed in this time range?
```

without interpreting a canvas.

### Keyboard interaction

MapLibre supports keyboard pan, zoom, rotation and pitch controls, but the application must also provide keyboard access to layers, visible entities and selections.

Source: MapLibre KeyboardHandler

Use established WAI-ARIA patterns for grids, treegrids, tabs, dialogs and menus. Dense event tables and hierarchical entity lists require predictable arrow-key and focus behaviour.

Source: WAI-ARIA Authoring Practices Guide

### Focus and target size

- Focus indicators must remain visible above maps and overlays.
- Docked panels must not cover the focused element.
- Controls should meet or exceed the WCAG minimum target-size rules or provide sufficient spacing.
- Drag-only operations need click, keyboard or form alternatives.

**Sources:**

- Understanding Focus Appearance
- Understanding Target Size Minimum

### Colour and graphics

Meaningful map features and UI components need sufficient non-text contrast. Never encode claim state, scenario branch or alert severity by colour alone.

Source: Understanding Non-text Contrast

### Motion and time

Provide:

- Reduced-motion mode.
- Pause for non-essential animation.
- Manual playback speed.
- Step-by-step replay.
- Static uncertainty alternatives.
- No flashing event markers.
- Ability to stop automatic camera following.

### Cognitive accessibility

- Keep world, branch and time visible.
- Use plain domain language alongside technical IDs.
- Preserve filters and explain why data disappeared.
- Make destructive or mutating actions explicit.
- Provide undo for workspace changes.
- Use consistent component placement.
- Avoid unexplained adaptive UI rearrangement.

---

## 29. UI/UX anti-patterns to avoid

1. **The wall of dots** — every person rendered individually at every scale.
2. **The impressive globe trap** — a cinematic 3D globe used where a 2D analytical map is clearer.
3. **Chat as the whole product** — forcing every task through a conversation instead of direct manipulation and structured controls.
4. **God mode without a warning** — showing simulator truth while implying it is participant knowledge.
5. **Map popups as inspectors** — placing complex agent state in transient tiny popups.
6. **One universal dashboard** — combining world building, live operation, validation and investigation into one overloaded screen.
7. **Colour-only truth states** — no textual or symbolic distinction between observed, believed and disputed.
8. **A single randomness slider** — concealing many distinct stochastic mechanisms.
9. **Animation as evidence** — assuming moving visuals prove simulation fidelity.
10. **Silent sampling** — dropping or sampling agents without labelling the projection.
11. **3D interiors with fabricated precision** — drawing an exact room position when only building-level location is known.
12. **Network hairballs** — rendering every social edge without a task-specific filter.
13. **Live/replay ambiguity** — users cannot tell whether they are watching current state or historical playback.
14. **Hidden filters** — screenshots and exports omit active filters or branch context.
15. **AI writes without review** — an assistant silently alters the world or scenario.
16. **Raw firehose only** — an infinite log without facets, lineage or causal navigation.
17. **UI state treated as world state** — optimistic local mutation becomes authoritative.
18. **Map tiles treated as exact topology** — presentation data used as simulation truth.
19. **Decorative agent emotion** — avatar animation presented as validated internal state.
20. **Uncertainty washed away** — displaying one run or one point estimate as the answer.

---

## 30. UI/UX validation and acceptance tests

### Research process

Use Munzner’s levels to structure evaluation:

| Level | Validation question | Method |
| --- | --- | --- |
| Domain problem | Does the workspace support real analyst, builder and operator tasks? | Interviews, observation and task analysis |
| Data/task abstraction | Are truth, belief, claim, event, time and branch represented correctly? | Domain expert review and scenario walkthroughs |
| Encoding/interaction | Can users perceive, select, compare and explain correctly? | Usability tests and controlled visualization studies |
| Algorithm/performance | Does it render and query correctly at required scale? | Benchmarks, profiling and correctness tests |

### Critical usability tasks

Test whether representative users can:

1. Locate an agent and determine their current physical state.
2. Follow the agent into and through a building.
3. Explain why the agent performed an action using evidence.
4. Distinguish world truth from the agent’s belief.
5. Trace a claim from witness to repost and later action.
6. Build a road-closure scenario without creating impossible travel.
7. Replay the scenario and create a counterfactual branch.
8. Compare outcomes across seeds and understand uncertainty.
9. Find all events affecting a selected building and time range.
10. Determine whether a displayed density layer is exact, aggregated or sampled.
11. Use the main workflows without a mouse.
12. Recover from a disconnected event stream without losing investigation context.

### Acceptance criteria

**Context integrity**

- World, scenario, branch and time are visible in every analytical workspace.
- Exports include context and active filters.
- Ground-truth mode is persistently labelled.

**Map integrity**

- Zooming changes representation according to the semantic-zoom policy.
- Individual markers do not appear where only aggregate positions are known.
- Selection remains stable during zoom and view-mode changes.
- Map and table selections stay synchronized.

**Causal integrity**

- Every “why” explanation links to recorded evidence.
- The interface distinguishes recorded fact from generated summary.
- Claim lineage can be traversed without reading raw logs.

**Randomness integrity**

- The active seed policy is visible.
- A run can be reproduced with the same seed and versions.
- Ensemble results are not presented as one deterministic forecast.

**Accessibility integrity**

- Core workflows are keyboard operable.
- Map information has list or table alternatives.
- Focus remains visible and unobscured.
- Reduced-motion mode removes non-essential camera and data animation.
- State is not encoded by colour alone.

**Performance integrity**

- Large populations aggregate rather than freezing the interface.
- Stream lag is visible.
- Reconnection detects missing sequence ranges.
- High-detail building data loads only when needed.

**Plugin integrity**

- UI plugins cannot mutate authoritative state directly.
- Incompatible plugins are blocked with an explanation.
- Plugin failure is isolated from the core workspace.

---

## 31. Recommended UI implementation sequence

### UI Phase 0 — Design and data contracts

Define:

- User roles and critical tasks.
- Truth/belief/claim visual semantics.
- Command and query contracts.
- Selection model.
- Timeline model.
- Semantic zoom policy.
- Design tokens.
- Accessibility baseline.
- Performance test datasets.

### UI Phase 1 — Read-only World Explorer

Build:

- Application shell.
- Offline MapLibre/PMTiles basemap.
- Layer manager.
- Agent clusters and aggregate cells.
- Entity search.
- Inspector.
- Timeline playback.
- Event table.
- Saved views.

Use recorded events before connecting live simulation.

### UI Phase 2 — Agent and causal investigation

Add:

- Agent follow.
- Route history.
- Belief/truth comparison.
- Structured “why” explanations.
- Claim provenance.
- Coordinated map, timeline and table selection.

### UI Phase 3 — Building and local world

Add:

- Building selection.
- Floors and rooms.
- Indoor graph.
- Occupancy.
- Local high-fidelity movement.
- Object affordance inspection.

### UI Phase 4 — Scenario Studio

Add:

- Typed interventions.
- Map/timeline authoring.
- Assumption register.
- Validation.
- Source editor.
- Version diff.
- Run configuration.

### UI Phase 5 — Branches, ensembles and validation

Add:

- Branch tree.
- Side-by-side and difference comparison.
- Seed ensembles.
- Uncertainty visualizations.
- Observed-data comparison.
- Calibration and sensitivity views.

### UI Phase 6 — Plugin SDK and operational hardening

Add:

- UI plugin manifest.
- Map-layer extension points.
- Event renderers.
- Custom inspectors.
- Permission model.
- Performance budgets.
- Accessibility regression testing.
- Offline packaging and recovery.

---

## 32. Consolidated UI/UX recommendation

The best balance is:

```text
Far away
    Simulate at appropriate fidelity, aggregate heavily, show patterns.

Nearby
    Increase spatial and behavioural detail, show individuals selectively.

Inside a selected building
    Show rooms, routes, objects, affordances and embodied agents.

Selected or followed
    Expose full state, history, knowledge and causal explanation.

Across all levels
    Preserve time, selection, provenance, uncertainty and branch context.
```

The map should be the geographic backbone, not a screen filled permanently with dots. The local world and building views should provide embodiment where it has analytical value. Randomness should create controlled variation inside valid mechanisms, not unexplained motion. The design system should make truth, belief, provenance and uncertainty visually explicit. The frontend should consume event-sourced read models through stable contracts and remain replaceable, offline-capable and independent of the simulation kernel.

The core UI rule is:

> **Show the world at the level needed for the current task, preserve the path to detail, and never imply more precision, certainty or knowledge than the simulation actually contains.**

---

## Final recommendation

Do not build another “LLM society.”

Build a deterministic, event-sourced simulation operating system in which:

- Geography is authoritative.
- Time is authoritative.
- Movement is authoritative.
- Ownership and resources are authoritative.
- Knowledge has provenance.
- Belief is separate from truth.
- Every consequence has a causal path.
- Every important action is replayable.
- Every AI component is replaceable.
- Every model call is observable.
- Every scenario declares its assumptions.
- Every claim of realism has a validation measure.

Then allow LLMs to contribute where they are genuinely strong:

- Expressing language.
- Interpreting ambiguous information.
- Proposing bounded plans.
- Compressing experience.
- Handling unusual situations.
- Generating scenario drafts.
- Producing human-readable explanations.

The best summary is:

> **Games provide the world, rules, perception, planning, execution, navigation, affordances, scheduling, debugging and scale architecture. Classical agent-based modelling provides calibration, population mechanisms and scientific discipline. LLMs provide bounded language and reasoning. None of those three should be allowed to impersonate the other two.**
