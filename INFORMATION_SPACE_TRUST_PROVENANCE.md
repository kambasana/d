# Information Space, Trust, Provenance and Social Diffusion

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
