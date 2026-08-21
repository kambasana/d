# Agentic World Graph Builder: Research Review and Architecture Recommendations

## Research verdict

Many existing systems are not necessarily dishonest, but they are often **research prototypes or demonstrations built to produce believable behaviour**, rather than validated simulations of physical reality, human society, or future outcomes.

The recurring mistake is treating:

> Fluent agent dialogue + a map + long-term memory

as equivalent to:

> A physically grounded, causally consistent, empirically calibrated world simulation.

They are not the same thing.

The foundational rule for this project should be:

> **An LLM may propose an intention, plan, interpretation, or utterance. Only the deterministic simulation kernel may decide what actually happened.**

Games have spent decades making **restricted agents appear intelligent inside reliable worlds**. Many recent AI simulations instead make **unrestricted text appear to be a world**. This platform needs the engineering discipline of the first approach and the language flexibility of the second.

This review covers influential papers, official engine documentation, established simulation systems, and active open-source projects available through August 20, 2026. It is not a claim to include every paper or repository ever published.

---

## 1. What the current research really demonstrates

### Generative Agents and “Smallville”

The original Generative Agents work demonstrated 25 agents with a memory stream, retrieval based on relevance, recency and importance, reflection, planning, and social interaction. Those mechanisms are useful, particularly as an early design for episodic memory and reflection. However, the evaluation primarily concerned whether behaviour appeared believable—not whether the world was physically correct, empirically calibrated, causally valid, or suitable for forecasting.

Source: [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)

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

Source: [Generative Agent Simulations of 1,000 People](https://arxiv.org/abs/2411.10109)

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

- In 360CityArena, the strongest tested model achieved only **17.1%**, compared with **77.3% for humans**, on grounded urban tasks involving streets, locations and navigation. This is direct evidence that language-capable models should not control authoritative urban movement or spatial truth.
- SOTOPIA found substantial gaps between strong language models and humans in difficult social interaction scenarios. It is useful as an evaluation framework, not as evidence that LLMs already possess reliable social intelligence.
- “Lost in Simulation” found material outcome variation across simulated-user models, including miscalibration and disparities across demographic and language groups.
- “Utopian Illusion” identified overly idealized and socially desirable behaviour in simulated societies.
- “Too Human to Model” argues that increasingly expressive agents can obscure causal mechanisms, time abstractions and model assumptions rather than improving scientific validity.
- Research on social-desirability effects shows that LLM-generated survey responses can inherit systematic response biases.

Sources:

- [360CityArena](https://arxiv.org/abs/2608.08814)
- [SOTOPIA](https://arxiv.org/abs/2310.11667)
- [Lost in Simulation](https://arxiv.org/abs/2601.17087)
- [Utopian Illusion](https://arxiv.org/abs/2510.21180)
- [Too Human to Model](https://arxiv.org/abs/2507.06310)
- [Social Desirability Bias in LLM-Generated Survey Responses](https://arxiv.org/abs/2405.06058)

The correct conclusion is not that LLM agents are useless. It is that **they must be bounded, measured, replaceable and prevented from becoming the authority over world truth**.

---

## 2. What should be reused directly

### Geospatial foundation

| Requirement | Recommended foundation | Correct role |
|---|---|---|
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

Sources:

- [osm2pgsql documentation](https://osm2pgsql.org/doc/manual.html)
- [PostGIS](https://postgis.net/)

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

Source: [Protomaps and PMTiles documentation](https://docs.protomaps.com/)

### Nominatim is a gazetteer, not physical truth

Nominatim should resolve:

- Place names.
- Addresses.
- Administrative areas.
- Named buildings.
- Named streets.
- Search and reverse-geocoding queries.

It should not decide whether an agent can physically enter, cross or traverse something. Nominatim’s reverse-geocoding documentation explains that it returns the closest suitable indexed OSM object, which can produce a different street or object from the exact coordinate.

Source: [Nominatim documentation](https://nominatim.org/)

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

Sources:

- [Valhalla](https://valhalla.github.io/valhalla/)
- [SUMO](https://sumo.dlr.de/docs/)
- [Recast Navigation](https://github.com/recastnavigation/recastnavigation)
- [MATSim](https://matsim.org/)

---

## 3. What established games already solved

### The central comparison

| Established game/ABM pattern | Weak LLM reinvention | Required hybrid approach |
|---|---|---|
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

Source: [GDC Vault: Three States and a Plan — The AI of F.E.A.R.](https://www.gdcvault.com/play/1013459/Three-States-and-a-Plan)

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

Sources:

- [Unreal Engine Behavior Trees](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-trees-in-unreal-engine)
- [Unreal Engine Environment Query System](https://dev.epicgames.com/documentation/en-us/unreal-engine/environment-query-system-in-unreal-engine)
- [Unreal Engine Smart Objects](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine)
- [Unreal Engine StateTree](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine)
- [Unreal Engine MassEntity](https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-entity-in-unreal-engine)

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

Source: [GDC Vault: Concurrent Interactions in The Sims 4](https://www.gdcvault.com/play/1020190/Concurrent-Interactions-in-The-Sims)

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

Source: [Valve publications](https://www.valvesoftware.com/en/publications)

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

Source: [GDC Vault: A Context-Aware Character Dialog System in The Last of Us](https://www.gdcvault.com/play/1020951/A-Context-Aware-Character-Dialog)

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

Sources:

- [Concordia GitHub repository](https://github.com/google-deepmind/concordia)
- [Concordia technical report](https://arxiv.org/abs/2312.03664)

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

Sources:

- [AgentSociety GitHub repository](https://github.com/tsinghua-fib-lab/AgentSociety)
- [AgentSociety paper](https://arxiv.org/abs/2502.08691)
- [AgentSociety 2 paper](https://arxiv.org/abs/2607.11895)

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

Sources:

- [OASIS GitHub repository](https://github.com/camel-ai/oasis)
- [OASIS paper](https://arxiv.org/abs/2411.11581)

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

OASIS’s published token-consumption example reports **335,600 input tokens for 100 agents in one fully activated step**. That is direct evidence that per-agent, per-step LLM calls cannot be the basis of a planetary system.

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

Sources:

- [AgentTorch GitHub repository](https://github.com/agenttorch/agenttorch)
- [Large Population Models](https://arxiv.org/abs/2507.09901)

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

CityBehavEx is particularly aligned with this philosophy because it describes itself as **LLM-assisted**, combines established urban-behaviour mechanisms with learned components, and emphasizes empirical validation, replay and comparison against mobility, time-use, transport and social-network patterns. Its paper reports large synthetic mobility runs without using an LLM for every agent decision.

Sources:

- [CityBehavEx GitHub repository](https://github.com/gefgu/citybehavex)
- [CityBehavEx paper](https://arxiv.org/abs/2607.12086)

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

Sources:

- [MATSim](https://matsim.org/)
- [The Multi-Agent Transport Simulation MATSim](https://matsim.org/the-book/)

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

Source: [AI Town GitHub repository](https://github.com/a16z-infra/ai-town)

### Project Sid

Project Sid is useful as a source of ideas about large Minecraft populations, roles, institutions and civilization-like emergence. It should be treated as experimental inspiration and benchmarking material rather than a validated reusable world operating system.

Source: [Project Sid GitHub repository](https://github.com/altera-al/project-sid)

---

## 5. Components to reuse only as benchmarks

Some systems are more useful for testing the architecture than implementing it.

| System | Useful benchmark |
|---|---|
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

LLMs should be invoked at **novelty boundaries**, not simulation-clock boundaries.

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

Sources:

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [W3C ActivityStreams 2.0](https://www.w3.org/TR/activitystreams-core/)

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

Every world and scenario should have a machine-readable **ODD-style model specification** covering:

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

Source: [ODD Protocol for Describing Agent-Based and Other Simulation Models](https://www.usgs.gov/publications/odd-protocol-describing-agent-based-and-other-simulation-models-a-second-update)

### Minimum validation layers

#### Structural verification

Does the software implement the declared rules?

#### Invariant testing

Can an agent teleport, duplicate ownership or know inaccessible information?

#### Empirical calibration

Do mobility, schedules, communication, networks and resource use resemble relevant observed data?

#### Sensitivity analysis

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

#### Out-of-sample tests

Can the model reproduce withheld scenarios or time periods?

#### Human comparison

Where human behaviour is claimed, compare against actual human data rather than another LLM’s judgment.

#### Uncertainty reporting

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

## Final recommendation

Do **not** build another “LLM society.”

Build a **deterministic, event-sourced simulation operating system** in which:

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
