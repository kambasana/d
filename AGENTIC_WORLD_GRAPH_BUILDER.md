# Agentic World Graph Builder

Build a serious, extensible, persistent agentic world-simulation platform capable of creating real-world, historical, hypothetical, or fully synthetic worlds and scenarios.

This must **not** be designed as a toy agent simulation or a collection of LLM characters placed on a map. It should be architected as a **simulation system first**, combining proven game-engine architecture, geospatial systems, NPC AI techniques, physics, social simulation, autonomous agents, and persistent world state.

The fundamental model is:

> Real or synthetic geography + game simulation + agentic AI + human systems + persistent temporal world graph = an emergent digital world.

---

## World and Scenario Builder

Users must be able to construct complete worlds, scenarios, populations, organizations, environments, events, constraints, and starting conditions.

A scenario might represent:

- A real city today.
- A historical environment.
- A geopolitical crisis.
- A disaster or infrastructure failure.
- A synthetic town or country.
- A business ecosystem.
- A military or humanitarian scenario.
- A migration scenario.
- A social or economic experiment.
- A completely fictional world built using realistic spatial rules.

A scenario is **not simply a prompt**. It is a configurable simulation state containing geography, population, infrastructure, organizations, resources, policies, environmental conditions, timelines, and behavioral constraints.

Users must then be able to change conditions while the world is running and observe how individuals, groups, institutions, infrastructure, and the wider world react.

For example:

```
Scenario state → Intervention → Agent perception → Individual reaction → Group reaction → World consequences → New state
```

Agents should be able to communicate about these events naturally, but their conversations must emerge from what they know, perceive, remember, and experience inside the simulation.

---

## Real Geographic Foundation

Every world should have a genuine understanding of geographic space.

Use **OpenStreetMap** as a primary spatial foundation, supporting:

- Roads
- Streets
- Paths
- Buildings
- Land parcels
- Administrative boundaries
- Natural features
- Transport infrastructure
- Points of interest
- Places
- Addresses
- Geographic relationships

Use a proper OSM gazetteer, including Nominatim-compatible place resolution, so agents and systems understand named locations and their relationship to physical geometry.

The system should understand the distinction between:

- **Place identity**
- **Place geometry**

For example, “Manchester Piccadilly Station” is not merely a string. It represents a geographic object with coordinates, entrances, roads, rail infrastructure, surrounding buildings, travel connections, and relationships with other places.

---

## Offline Maps

Support **Protomaps / PMTiles** as a first-class map architecture so complete geographic environments can operate locally or in disconnected environments.

A world should therefore be capable of running with:

- Local OSM extracts
- Local vector tiles
- PMTiles
- Local gazetteers
- Local routing graphs
- Local elevation data
- Local building geometry
- Local spatial databases

Internet access must **not** be a fundamental dependency.

This enables fully offline and controlled simulations.

---

## Synthetic Geography

Synthetic worlds must use the same spatial principles as real worlds.

A synthetic city should still contain meaningful:

- Roads
- Streets
- Buildings
- Addresses
- Districts
- Boundaries
- Paths
- Transport networks
- Geographic features
- Points of interest

Synthetic geography should therefore be generated into an **OSM-like spatial model**, rather than merely inventing place names.

Agents must be capable of reasoning about synthetic places exactly as they would reason about real places.

The simulation should understand:

> Where things are, how they connect, what separates them, and how an entity can physically move between them.

---

## Spatially Grounded Agents

Agents must always understand the physical space they occupy.

An agent should have concepts such as:

- Current location
- Previous location
- Destination
- Route
- Distance
- Travel time
- Movement speed
- Accessible paths
- Buildings
- Entrances
- Rooms
- Transport modes
- Geographic boundaries
- Nearby entities
- Visibility
- Physical obstacles

Agents must **never** behave as though geography does not exist.

For example, an agent cannot:

- Travel three miles in one second.
- Instantly appear at another location.
- Randomly spawn at a destination without travelling there.
- Walk through an inaccessible building.
- Cross a river without an appropriate crossing.
- Travel along a road that does not exist.
- Enter a building without an appropriate entrance.
- Know something happening miles away without an information source.

Movement must have physical and temporal consequences.

If an agent moves from A to B, the simulation records:

```
origin → departure → route → transport mode → elapsed time → intermediate position → arrival
```

Physical presence is therefore a persistent fact of the world.

---

## Proven Game-Simulation Architecture

Humanistic behaviour should not be invented from scratch simply because LLMs are available.

The system should build on real, proven NPC and simulation architectures developed through games, artificial-life research, multi-agent systems, and simulation engineering.

Relevant mechanisms include:

- Entity Component Systems
- Utility AI
- Behaviour trees
- Goal-Oriented Action Planning
- Hierarchical task planning
- Blackboard systems
- State machines
- Needs systems
- Schedules
- Perception systems
- Memory systems
- Reputation
- Relationships
- Factions
- Inventories
- Ownership
- Resource systems
- Economies
- Navigation meshes
- Navigation graphs
- Pathfinding
- Collision systems
- Event systems
- Simulation ticks
- Deterministic systems
- Spatial partitioning
- Level-of-detail simulation
- Procedural generation
- Emergent AI
- Agent communication systems

LLMs should **complement** these mechanisms rather than replace them.

---

## Humanistic Systems

Human behaviour is a core part of the platform.

Agents should possess persistent internal and external state representing things such as:

- Needs
- Goals
- Responsibilities
- Social relationships
- Beliefs
- Knowledge
- Memories
- Skills
- Occupation
- Household
- Culture
- Reputation
- Wealth
- Resources
- Affiliations
- Commitments
- Preferences
- Current emotional state
- Physical state
- Location
- History

These systems should be based wherever possible on established models from:

- Game NPC architecture
- Agent-based modelling
- Cognitive architectures
- Behavioural science
- Sociology
- Economics
- Artificial life
- Multi-agent systems

The objective is not to claim that simulated people are perfect models of humans.

The objective is to build a **transparent and defensible computational model** where behaviour emerges from explicit systems rather than arbitrary LLM improvisation.

---

## Agent Lives

Agents should genuinely live inside the world.

They can:

- Sleep
- Work
- Travel
- Communicate
- Form relationships
- Join groups
- Leave groups
- Purchase goods
- Own property
- Exchange resources
- Cooperate
- Compete
- Learn
- Remember
- Forget
- Make plans
- Change plans
- React to events
- Experience consequences
- Develop histories

An agent should therefore have a **continuous life** rather than existing only when somebody sends it a prompt.

---

## Groups and Society

Agents must be able to form higher-order social entities.

For example:

```
Civilization → Government → Institution → Organization → Faction → Community → Household → Group → Individual
```

Groups themselves should have persistent state.

An organization might possess:

- Members
- Leadership
- Resources
- Property
- Policies
- Objectives
- Internal relationships
- External relationships
- Reputation
- Geographic territory
- Communication structures
- Decision-making mechanisms

This allows behaviour to emerge at both individual and collective scales.

---

## Dynamic World Graph

The underlying representation should be a **spatial-temporal world graph**.

Nodes may represent:

- People
- Groups
- Buildings
- Streets
- Vehicles
- Infrastructure
- Businesses
- Governments
- Resources
- Events
- Objects
- Documents
- Communications
- Geographic places

Edges represent relationships such as:

- Located at
- Owns
- Works for
- Member of
- Related to
- Knows
- Communicated with
- Travelled through
- Supplies
- Controls
- Neighbours
- Depends upon
- Observed
- Participated in

The graph changes continuously over simulated time.

This makes the system not simply a world database but a **living temporal graph**.

---

## World Firehose

Every world and every agent must expose a structured event firehose.

The simulation should make its internal activity observable rather than hiding everything inside agents.

Examples include:

- Agent movement
- Conversations
- Decisions
- Perceptions
- Actions
- Transactions
- Relationship changes
- Resource changes
- Group membership changes
- Economic activity
- Infrastructure events
- Environmental events
- World-state changes

Events should be machine-readable and consumable by external systems.

```
World
 ├─ Agent events
 ├─ Movement events
 ├─ Communication events
 ├─ Economic events
 ├─ Social events
 ├─ Geographic events
 ├─ Infrastructure events
 ├─ Scenario events
 └─ System events
        ↓
   Event Firehose
        ↓
 Analytics / AI / dashboards / databases / replay / external applications
```

The event stream should allow the simulation to be observed, analysed, replayed, queried, audited, and integrated with other systems.

---

## Scenario Intervention Engine

The platform must support deliberate interventions.

Examples:

- Close a road.
- Raise food prices.
- Remove electricity.
- Introduce a new law.
- Add a disease outbreak.
- Change public transport.
- Remove a bridge.
- Introduce a new employer.
- Trigger a natural disaster.
- Change weather.
- Increase unemployment.
- Introduce misinformation.
- Change an organization’s leadership.

Agents should **not** receive a scripted reaction.

Instead:

1. The world changes.
2. Agents perceive the portions of that change they could realistically discover.
3. Their existing goals, relationships, knowledge, location, resources, responsibilities, and behavioural systems determine what happens next.

This allows users to investigate:

> What happens if the world changes?

rather than merely:

> What does an LLM think would happen?

---

## Modular Plugin and Adapter Architecture

Every major subsystem must be replaceable through a well-defined plugin / adapter architecture.

Core simulation functionality must not be tightly coupled to a particular AI model, database, map provider, routing engine, vector store, physics engine, or user interface.

```
Core World Runtime
        │
        ├── AI Provider Adapter
        │     ├── Ollama
        │     ├── OpenRouter
        │     ├── Local models
        │     └── Future providers
        │
        ├── Map Adapter
        │     ├── OSM
        │     ├── Protomaps / PMTiles
        │     └── Synthetic maps
        │
        ├── Gazetteer Adapter
        │
        ├── Routing Adapter
        │
        ├── Simulation Adapter
        │
        ├── Physics Adapter
        │
        ├── Storage Adapter
        │
        ├── Event Adapter
        │
        └── Visualization Adapter
```

An implementation should be swappable without requiring changes to core world behaviour.

For example:

- Changing **Ollama → OpenRouter** should not require rewriting an agent.
- Changing **Routing Engine A → Routing Engine B** should not change the world model.
- Changing **PostgreSQL → another supported persistence layer** should not break simulation logic.

The interfaces remain stable while implementations change.

---

## AI Architecture

AI should therefore be **provider-neutral**.

First-class adapters can include:

- Ollama
- OpenRouter
- Local model runtimes
- Remote inference services
- Specialist models

Different models may be assigned to different functions.

For example:

- Dialogue model
- Planning model
- Memory model
- Perception model
- Summarization model
- World-generation model
- Scenario controller
- Organization-level reasoning model

However, deterministic simulation systems should remain **outside the LLM** whenever possible.

The AI should reason **within the rules of the world**, not redefine them.

---

## Multi-Resolution Planetary Simulation

The platform should support hierarchical spatial simulation:

```
Planet → Continent → Country → Region → City → District → Street → Building → Room → Object
```

Only relevant areas need maximum simulation fidelity.

| Level | Name | Description |
| --- | --- | --- |
| **Level 0** | Statistical | Millions of distant agents represented as aggregate populations. |
| **Level 1** | Macro Simulation | Cities, economies, migration, infrastructure and organizations. |
| **Level 2** | Agent Simulation | Relevant individuals receive persistent goals, relationships, schedules and activities. |
| **Level 3** | High-Fidelity Simulation | Nearby agents receive detailed navigation, perception, interaction and decision making. |
| **Level 4** | Immediate Physical Simulation | Fine-grained positioning, collision, object interaction and potentially physics. |

Entities can move between levels dynamically.

This makes planetary simulation possible without pretending every person on Earth can be run as a high-frequency LLM agent.

---

## Time Is Fundamental

Time should be a first-class world dimension.

Every important state change should have temporal context.

The platform should understand:

- Before
- After
- Duration
- Scheduled events
- Recurrence
- Travel time
- Working hours
- Sleeping hours
- Historical state
- Future plans
- Concurrent events

The world graph therefore becomes:

> Entity + relationship + geography + time.

---

## Persistent Causality

Actions should leave consequences.

If an agent leaves home at 08:10 and reaches work at 08:42, the system should be able to reconstruct that journey.

If a bridge closes at 08:20, the agent may need to reroute.

That increases journey time.

That may make the agent late.

Being late may affect a meeting.

The meeting may affect an organization.

The organization’s decision may affect other agents.

This creates:

```
Event → consequence → secondary consequence → emergent behaviour
```

rather than disconnected generated responses.

---

## Core Engine Separation

The architecture should separate at least these systems:

1. **World Graph Engine** — Persistent entities, relationships and state.
2. **Geospatial Engine** — OSM, geometry, tiles, gazetteers, spatial queries and coordinate systems.
3. **Navigation and Mobility Engine** — Routes, travel modes, movement constraints and travel time.
4. **Simulation and Physics Engine** — Time, movement, collisions, physical rules and deterministic systems.
5. **Agent Runtime** — Goals, planning, perception, memory and action selection.
6. **Human Systems Engine** — Needs, behaviour, relationships, households, culture and social systems.
7. **Society and Economy Engine** — Organizations, markets, resources, institutions and collective behaviour.
8. **Scenario Engine** — Initial conditions, interventions, constraints and experiments.
9. **Event and Firehose Engine** — Observable event streams, telemetry, replay and external integration.
10. **AI Adapter Layer** — Ollama, OpenRouter and interchangeable model providers.
11. **Storage Layer** — Persistent simulation state and historical records.
12. **Visualization and Control Layer** — World editor, map interface, scenario controls, inspection tools and analytics.

---

## Non-Negotiable Principle

An agent does not exist outside the simulation.

Every agent has:

- a place
- a history
- a clock
- a physical state
- knowledge
- relationships
- constraints
- consequences

If it travels, travel consumes time.

If it learns something, there must be a plausible information path.

If it owns something, ownership exists in world state.

If it joins a group, that relationship persists.

If the environment changes, agents experience that change according to where they are and what they can perceive.

If the world is synthetic, its geography must still be coherent and traversable.

**LLMs provide reasoning and language.**

They do **not** get to override physics, geography, causality, time, or world state.

The goal is therefore not another collection of AI NPCs.

The goal is a **general-purpose agentic world operating system** capable of creating persistent, geographically grounded, causally consistent simulated societies in which people, organizations and environments can evolve over time and respond realistically to changing scenarios.

---

## Information Space, Trust, Provenance and Social Diffusion

The simulation must treat information as something that **moves through the world**, rather than giving agents omniscient access to global state.

Agents should distinguish between:

- What they directly experienced.
- What they personally observed.
- What another agent told them.
- What they inferred.
- What they read.
- What they saw posted publicly.
- What was reposted by somebody they trust.
- What originated from an unknown source.
- What has been independently corroborated.
- What has been disputed.
- What is deliberately misleading.
- What they remember imperfectly.
- What they currently believe.

This creates a separate but connected **information space** layered over the physical world.

---

## Information Must Have Provenance

Every meaningful piece of information should have provenance.

For example:

```
EVENT
A observes an explosion at Location X
        ↓
A tells B
        ↓
B tells C
        ↓
C posts about it publicly
        ↓
D reposts C
        ↓
E comments with conflicting information
        ↓
F messages A directly to verify
        ↓
A replies / ignores / contradicts / clarifies
```

The system must preserve that chain.

An agent should therefore never simply contain:

```
knows_explosion = true
```

Instead, knowledge should contain something closer to:

```yaml
Claim:
  subject: Event-482
  assertion: "An explosion occurred at Location X"
  source: Agent-C
  original_source: Agent-A
  acquisition_channel: social_post
  received_at: 14:32:08
  confidence: 0.67
  trust_in_source: 0.82
  corroboration_count: 2
  direct_observation: false
  disputed: false
```

The precise implementation can vary, but **knowledge provenance must be first-class world state**.

---

## Knowing Someone Changes Interpretation

Social relationships must influence how information is interpreted.

If Agent A knows Agent B personally and has repeatedly observed B behaving in a particular way, that historical experience should affect how A evaluates future information about B.

For example, if A has personally observed that B:

- Frequently exaggerates.
- Usually tells the truth.
- Becomes aggressive under pressure.
- Routinely helps neighbours.
- Regularly shares unreliable information.
- Has specialist knowledge in a particular field.

then A can reasonably incorporate those observations when evaluating a new claim.

That is fundamentally different from an unrelated agent seeing:

- A like
- A repost
- A comment
- A viral post
- An anonymous message

Agents therefore require **relationship-specific epistemic models**.

An agent might trust another individual highly regarding engineering but distrust the same person regarding politics.

Trust should therefore not necessarily be represented by a single global number.

It can be:

```
Agent × Agent × Domain × Context × History → Trust
```

---

## Direct Experience Must Differ From Hearsay

The system should maintain an explicit evidence hierarchy.

For example:

```
DIRECT EXPERIENCE
"I was there."
        ↓
DIRECT OBSERVATION
"I saw A entering the building."
        ↓
TRUSTED FIRST-HAND REPORT
"A told me they were inside."
        ↓
SECOND-HAND REPORT
"B said A was inside."
        ↓
PUBLIC POST
"Someone posted that A was inside."
        ↓
REPOST / LIKE / COMMENT
        ↓
UNATTRIBUTED RUMOUR
"People are saying A was inside."
```

These are **not equivalent** information states.

Agents should understand the difference.

---

## Observation Must Be Spatially Grounded

Direct observation depends on physical position.

If Agent A is inside the direct area of an incident, A may perceive:

- Sound
- Movement
- People
- Smoke
- Damage
- Traffic
- Emergency response
- Nearby conversation

Agent B may be outside the direct area but physically see A at the location.

Agent C may be kilometres away and only learn about the event from B.

Agent D may be in another country and encounter C’s public post.

The resulting information graph might therefore look like:

```
Physical Event
      │
      ├──── perceived directly by A
      │
      └──── B sees A near event
                 │
                 ▼
             B tells C
                 │
                 ▼
           C publishes post
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
      D likes   E reposts  F comments
                  │
                  ▼
             wider network
```

Each agent has a different evidence relationship with the original event.

---

## Information Diffusion Engine

Introduce a dedicated **Information Diffusion Engine**.

It models how information propagates through:

- Face-to-face conversation
- Telephone calls
- Direct messages
- Group chats
- Email
- Workplace communication
- News
- Radio
- Television
- Public announcements
- Social media
- Forums
- Communities
- Rumour networks
- Organizational hierarchies
- Emergency alerts

Information propagation should depend upon the communication network that actually exists.

An agent cannot receive a message merely because the simulation needs them to know something.

There must be a valid:

```
Source → Channel → Transmission → Recipient
```

path.

---

## Information Can Mutate

Information should not necessarily remain identical as it passes between agents.

For example:

- **A:** “I heard a loud bang and saw smoke.”
- **B:** “A said there may have been an explosion.”
- **C:** “Explosion reported downtown.”
- **D:** “Major explosion downtown.”
- **E:** “Terror attack happening downtown.”

The final statement may be dramatically different from the original observation.

The system should preserve the lineage so researchers can determine exactly how the claim evolved.

This creates:

> **Claim lineage** rather than a single global fact string.

---

## Fact and Belief Must Be Separate

The simulation requires an important distinction between:

- **World truth**
- **Agent belief**

The world may contain an authoritative simulation fact:

> Actual Event: Electrical transformer failure

while agents believe:

- **A:** transformer exploded
- **B:** building explosion
- **C:** terrorist attack
- **D:** unknown
- **E:** gas explosion

Agents act according to the information available to them, **not** according to privileged simulator truth.

This distinction is critical for realistic behaviour.

---

## Bad Actors and Adversarial Information

Agents may be:

- Reliable
- Unreliable
- Mistaken
- Biased
- Manipulative
- Deceptive
- Malicious
- Coordinated
- Compromised
- Opportunistic

A bad actor might deliberately inject a false claim into the information network.

The simulation should **not** automatically mark this claim as false for receiving agents.

Instead, agents evaluate it using:

- Source reputation
- Existing relationships
- Previous accuracy
- Corroboration
- Contradictory evidence
- Domain expertise
- Social pressure
- Institutional trust
- Their own observations
- Existing beliefs
- Available fact-checking mechanisms

This enables simulation of misinformation, disinformation and contested information without requiring the simulation itself to become confused about ground truth.

---

## Information-Seeking Behaviour

Agents should not only receive information passively.

They can attempt to investigate.

For example:

```
F sees C's post
    ↓
F distrusts C
    ↓
F sees that A may be original witness
    ↓
F messages A
    ↓
A may:
    ├── reply
    ├── ignore
    ├── block F
    ├── clarify
    ├── contradict C
    ├── lie
    └── say they are unsure
```

Fact-checking should therefore be an **agent action**, not a global simulator function that instantly corrects everybody.

---

## Virtual Social Media

The architecture should support a native virtual information ecosystem, including simulated social-media platforms.

Agents may:

- Create posts
- Reply
- Comment
- Like
- Dislike
- Repost
- Quote-post
- Follow
- Unfollow
- Mention
- Direct-message
- Join groups
- Share media
- Search
- Report content
- Block accounts

The social network exists within the simulated information space and interacts with the physical world.

An agent physically witnessing an event can post about it.

Another agent on the other side of the world can encounter the post without being anywhere near the event.

The simulation therefore contains at least two interconnected spaces:

```
PHYSICAL WORLD
Places
People
Buildings
Movement
Events
Infrastructure
Objects
        │
        │ observations create information
        ▼
INFORMATION WORLD
Messages
Posts
Claims
Media
Rumours
News
Comments
Communities
Networks
        │
        │ information changes behaviour
        ▼
PHYSICAL WORLD
```

The relationship is **bidirectional**.

---

## Agents Outside the Physical World

The architecture should also allow participants or agents that exist primarily in the information space rather than being fully simulated physical-world inhabitants.

Examples might include:

- External commentators
- News organizations
- Bots
- Remote analysts
- Institutional accounts
- Automated alert systems
- Virtual communities

They can interact with world inhabitants through information channels while following explicitly defined simulation rules.

---

## Social Platform Mechanics Must Be Real Systems

A simulated social network should not simply ask an LLM:

> “Who would like this post?”

It should model actual mechanics such as:

- Follow graphs
- Friendship graphs
- Communities
- Recommendation eligibility
- Feed ranking
- Recency
- Engagement
- Network proximity
- Content propagation
- Reposting
- Topic affinity
- Account reputation
- Moderation
- Visibility
- Blocking
- Privacy
- Group membership

The exact algorithm should be plugin-based so different platform behaviours can be simulated.

For example:

```
InformationPlatformAdapter
        │
        ├── ChronologicalFeed
        ├── EngagementRankedFeed
        ├── CommunityFeed
        ├── MessagingNetwork
        ├── NewsNetwork
        └── CustomExperimentalAlgorithm
```

---

## Firehose Must Capture the Complete Information Chain

The world firehose becomes especially important here.

It should record events such as:

```
14:30:02  EVENT_OCCURRED
14:30:04  AGENT_A_PERCEIVED_EVENT
14:30:08  AGENT_B_OBSERVED_AGENT_A
14:31:12  A_TOLD_B
14:31:44  B_TOLD_C
14:32:08  C_CREATED_POST
14:32:14  D_VIEWED_POST
14:32:18  D_LIKED_POST
14:32:32  E_REPOSTED_POST
14:33:02  F_COMMENTED
14:33:20  F_MESSAGED_A
14:35:09  A_REPLIED_TO_F
```

Each event can reference:

- World time
- Agent
- Location
- Channel
- Claim
- Source
- Parent event
- Original event
- Confidence
- Visibility
- Audience
- Relationship context
- Resulting belief change

This creates a complete machine-readable **information provenance graph**.

---

## Event Sourcing and Replay

The firehose should make it possible to reconstruct:

- Who knew what.
- When they knew it.
- Where they learned it.
- Who told them.
- What version they received.
- What they believed.
- What they passed onward.
- Whether they modified it.
- What action it caused.

A simulation could therefore be rewound and inspected:

> At 14:33, why did Agent F believe there had been an attack?

The system could reconstruct:

> F believed Claim-887 because F read Post-229 from C, which was derived from Message-114 from B, which originated from Observation-72 by A.

That level of traceability should be a fundamental property of the architecture.

---

## Information Has Reach, Not Telepathy

The same principle used for physical travel applies to information.

An agent cannot physically teleport.

Likewise, information cannot informationally teleport.

A claim needs a valid path through:

- Human conversation
- Communication infrastructure
- Broadcast infrastructure
- Organizational structure
- Digital networks
- Social platforms

The simulation therefore enforces two related forms of causality:

**Physical causality**

Agent must travel through space.

**Informational causality**

Knowledge must travel through a communication network.

---

## Agent Epistemic State

Every agent should have an explicit epistemic state representing what that individual currently thinks they know.

Conceptually:

```
Agent Knowledge
 ├── Direct experiences
 ├── Observations
 ├── Memories
 ├── Beliefs
 ├── Claims received
 ├── Sources
 ├── Source trust
 ├── Confidence
 ├── Contradictions
 ├── Uncertainty
 ├── Rumours
 └── Verified information
```

This state influences planning and behaviour.

Two agents standing next to each other may therefore react differently because they possess different histories and information.

---

## Information Can Drive Physical Consequences

Information itself becomes a causal mechanism.

For example:

```
Rumour posted
      ↓
Residents believe fuel shortage imminent
      ↓
More people travel to petrol stations
      ↓
Queues increase
      ↓
Actual shortage begins
      ↓
News organizations report shortage
      ↓
More people respond
```

The simulation can therefore produce feedback loops between:

```
Information → Human behaviour → Physical world → New information
```

This is essential for meaningful scenario simulation.

---

## Updated Core Architecture

The platform should therefore contain an additional group of first-class engines:

1. **World Graph Engine** — Persistent entities, relationships and state.
2. **Geospatial Engine** — OSM, geometry, PMTiles, gazetteers and spatial relationships.
3. **Navigation and Mobility Engine** — Physically plausible movement through geographic space.
4. **Simulation and Physics Engine** — Time, rules, constraints and deterministic world mechanics.
5. **Agent Runtime** — Goals, planning, action selection and autonomous behaviour.
6. **Human Systems Engine** — Needs, relationships, identity, schedules and social behaviour.
7. **Agent Epistemic Engine** — Knowledge, beliefs, uncertainty, memories and evidence.
8. **Trust and Reputation Engine** — Relationship-specific and domain-specific assessments of other actors.
9. **Information Diffusion Engine** — Transmission of claims and messages through communication networks.
10. **Information Provenance Graph** — Complete lineage from events to observations to claims to redistribution.
11. **Virtual Social Platform Engine** — Posts, feeds, messaging, reactions, networks and recommendation mechanics.
12. **Society and Economy Engine** — Organizations, institutions, markets and collective behaviour.
13. **Scenario and Intervention Engine** — World construction, experiments, shocks and changing conditions.
14. **Event Firehose and Replay Engine** — Complete observable record of actions and information propagation.
15. **AI Adapter Layer** — Ollama, OpenRouter and interchangeable reasoning systems.
16. **Storage and Temporal State Layer** — Persistent state, historical state and event sourcing.
17. **Visualization, Investigation and Control Layer** — Maps, timelines, graph exploration, social networks, analytics and scenario control.

---

## Expanded Non-Negotiable Principle

An agent must never know something merely because the simulation knows it.

An agent can only know something through a plausible chain of:

```
experience → perception → communication → memory → reasoning
```

Likewise, an agent’s beliefs should not automatically become identical to objective world state.

Agents can be informed, uninformed, mistaken, uncertain, manipulated, deceptive, contradictory or correct.

Every significant piece of knowledge should therefore answer:

- What does this agent believe?
- Why do they believe it?
- Where did the information originate?
- How did it reach them?
- Who else received it?
- How did it change while travelling?
- What did they do because of it?

Combined with spatial grounding, this produces a stronger foundational rule for the entire platform:

> **Nothing teleports — not people, objects, consequences or information. Everything has a path through space, time, relationships or communication networks.**
