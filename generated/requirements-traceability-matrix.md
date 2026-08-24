# Requirements Traceability Matrix

| Requirement | Statement | Source documents | Implemented by | Verified by | Status |
| --- | --- | --- | --- | --- | --- |
| AWG-REQ-VIS-001 | Build complete worlds and scenarios, not isolated chat agents. | AWG-VIS-001, AWG-SCN-001 | AWG-VIS-001, AWG-SCN-001 | AWG-TEST-COV-001 | draft |
| AWG-REQ-GEO-001 | Ground real worlds in OpenStreetMap geography and topology. | AWG-DOM-002 | AWG-DOM-002 | AWG-TEST-COV-002 | draft |
| AWG-REQ-GEO-002 | Support planet and regional tile views while keeping tiles separate from authoritative world state. | AWG-DOM-002, AWG-UX-003 | AWG-DOM-002, AWG-UX-003 | AWG-TEST-COV-003 | draft |
| AWG-REQ-GEO-003 | Use Nominatim-compatible gazetteer semantics for places, streets, and addresses. | AWG-DOM-002 | AWG-DOM-002 | AWG-TEST-COV-004 | draft |
| AWG-REQ-GEO-004 | Use Protomaps and PMTiles for offline map presentation. | AWG-DOM-002, AWG-PLAT-006 | AWG-DOM-002, AWG-PLAT-006 | AWG-TEST-COV-005 | draft |
| AWG-REQ-PLG-001 | Support Ollama as a local AI provider. | AWG-PLAT-003, AWG-PLAT-006 | AWG-PLAT-003, AWG-PLAT-006 | AWG-TEST-COV-006 | draft |
| AWG-REQ-PLG-002 | Support OpenRouter as a remote AI provider. | AWG-PLAT-003 | AWG-PLAT-003 | AWG-TEST-COV-007 | draft |
| AWG-REQ-PLG-003 | Use modular plugin and adapter architecture so components can be swapped without breaking core functionality. | AWG-PLAT-003 | AWG-PLAT-003 | AWG-TEST-COV-008 | draft |
| AWG-REQ-GOV-001 | Treat the system as a serious simulation platform rather than a toy agent demo. | AWG-GOV-001, AWG-VIS-002 | AWG-GOV-001, AWG-VIS-002 | AWG-TEST-COV-009 | draft |
| AWG-REQ-EVT-001 | Expose a structured firehose for each agent and world. | AWG-PLAT-002 | AWG-PLAT-002 | AWG-TEST-COV-010 | draft |
| AWG-REQ-SCN-001 | Allow scenarios and live changes so agents and groups react and communicate. | AWG-SCN-001, AWG-DOM-003, AWG-DOM-013 | AWG-SCN-001, AWG-DOM-003, AWG-DOM-013 | AWG-TEST-COV-011 | draft |
| AWG-REQ-AGT-001 | Build humanistic systems from established NPC, ABM, cognitive, social, and behavioural patterns rather than unconstrained invention. | AWG-DOM-003, AWG-DOM-011, AWG-VIS-006 | AWG-DOM-003, AWG-DOM-011, AWG-VIS-006 | AWG-TEST-COV-012 | draft |
| AWG-REQ-GEO-005 | Agents must understand the space they occupy. | AWG-DOM-002, AWG-DOM-009 | AWG-DOM-002, AWG-DOM-009 | AWG-TEST-COV-013 | draft |
| AWG-REQ-GEO-006 | Synthetic worlds must use coherent OSM-like places, geometry, access, and traversal. | AWG-DOM-002 | AWG-DOM-002 | AWG-TEST-COV-014 | draft |
| AWG-REQ-GEO-007 | Movement must consume plausible time and obey route, mode, and speed constraints. | AWG-DOM-002, AWG-DOM-008 | AWG-DOM-002, AWG-DOM-008 | AWG-TEST-COV-015 | draft |
| AWG-REQ-GEO-008 | Agents cannot randomly spawn at destinations or teleport. | AWG-GOV-001, AWG-DOM-002 | AWG-GOV-001, AWG-DOM-002 | AWG-TEST-COV-016 | draft |
| AWG-REQ-EPI-001 | Knowledge learned from another agent must retain source provenance. | AWG-DOM-004 | AWG-DOM-004 | AWG-TEST-COV-017 | draft |
| AWG-REQ-EPI-002 | Information sources may be reliable, mistaken, deceptive, malicious, or coordinated. | AWG-DOM-004 | AWG-DOM-004 | AWG-TEST-COV-018 | draft |
| AWG-REQ-EPI-003 | Relationship history and domain context affect trust. | AWG-DOM-004 | AWG-DOM-004 | AWG-TEST-COV-019 | draft |
| AWG-REQ-EPI-004 | Model witness, second-hand report, post, repost, comment, message, and fact-checking chains. | AWG-DOM-004, AWG-DOM-013 | AWG-DOM-004, AWG-DOM-013 | AWG-TEST-COV-020 | draft |
| AWG-REQ-EPI-005 | A contacted witness may reply, clarify, contradict, ignore, block, or remain uncertain. | AWG-DOM-004, AWG-DOM-013 | AWG-DOM-004, AWG-DOM-013 | AWG-TEST-COV-021 | draft |
| AWG-REQ-SOC-001 | Provide a virtual social-media site where agents can post, react, comment, repost, and message. | AWG-DOM-013, AWG-UX-010 | AWG-DOM-013, AWG-UX-010 | AWG-TEST-COV-022 | draft |
| AWG-REQ-SOC-002 | Support information-space actors that may not be fully embodied in the physical world. | AWG-DOM-013 | AWG-DOM-013 | AWG-TEST-COV-023 | draft |
| AWG-REQ-EVT-002 | Capture social and information actions in the firehose. | AWG-PLAT-002, AWG-DOM-004 | AWG-PLAT-002, AWG-DOM-004 | AWG-TEST-COV-024 | draft |
| AWG-REQ-RES-001 | Research papers, GitHub projects, systems, and proven game AI before designing replacements. | AWG-VIS-004, AWG-VIS-005 | AWG-VIS-004, AWG-VIS-005 | AWG-TEST-COV-025 | draft |
| AWG-REQ-RES-002 | Record useful reusable mechanisms and unsuitable mechanisms. | AWG-VIS-004, AWG-VIS-006 | AWG-VIS-004, AWG-VIS-006 | AWG-TEST-COV-026 | draft |
| AWG-REQ-GOV-002 | Maintain a never-do list for fake, invalid, or misleading simulation shortcuts. | AWG-GOV-001, AWG-VIS-002 | AWG-GOV-001, AWG-VIS-002 | AWG-TEST-COV-027 | draft |
| AWG-REQ-AGT-002 | Prefer established game NPC architecture over prompt-only reinvention. | AWG-DOM-003, AWG-VIS-006 | AWG-DOM-003, AWG-VIS-006 | AWG-TEST-COV-028 | draft |
| AWG-REQ-UX-001 | Balance agent markers with aggregate world views. | AWG-UX-007, AWG-UX-002 | AWG-UX-007, AWG-UX-002 | AWG-TEST-COV-029 | draft |
| AWG-REQ-UX-002 | Allow thousands of raw dots as an optional debug view without making it the only representation. | AWG-UX-007 | AWG-UX-007 | AWG-TEST-COV-030 | draft |
| AWG-REQ-UX-003 | Provide detailed building and interior world views. | AWG-UX-009 | AWG-UX-009 | AWG-TEST-COV-031 | draft |
| AWG-REQ-RND-001 | Use controlled randomness for variation, not arbitrary activity. | AWG-DOM-007 | AWG-DOM-007 | AWG-TEST-COV-032 | draft |
| AWG-REQ-SCL-001 | Keep simulation level of detail independent from visualization level of detail. | AWG-PLAT-005, AWG-UX-002 | AWG-PLAT-005, AWG-UX-002 | AWG-TEST-COV-033 | draft |
| AWG-REQ-UX-004 | Use semantic zoom where cluster totals progressively split into smaller clusters and individuals. | AWG-UX-002 | AWG-UX-002 | AWG-TEST-COV-034 | draft |
| AWG-REQ-UX-005 | Clicking a geographic cluster should normally zoom to member bounds. | AWG-UX-002 | AWG-UX-002 | AWG-TEST-COV-035 | draft |
| AWG-REQ-UX-006 | Use a radial circle of clickable agents for small true co-location overlaps. | AWG-UX-002 | AWG-UX-002 | AWG-TEST-COV-036 | draft |
| AWG-REQ-UX-007 | Use building, floor, room, or occupant browsers for large co-located populations. | AWG-UX-002, AWG-UX-009 | AWG-UX-002, AWG-UX-009 | AWG-TEST-COV-037 | draft |
| AWG-REQ-UX-008 | Distinguish geographic, co-location, and analytical clusters. | AWG-UX-002 | AWG-UX-002 | AWG-TEST-COV-038 | draft |
| AWG-REQ-UX-009 | Base UI/UX on research and proven visual analytics patterns. | AWG-UX-008, AWG-UX-001 | AWG-UX-008, AWG-UX-001 | AWG-TEST-COV-039 | draft |
| AWG-REQ-UX-010 | Provide a design system and frontend architecture. | AWG-UX-001, AWG-UX-013 | AWG-UX-001, AWG-UX-013 | AWG-TEST-COV-040 | draft |
| AWG-REQ-DOC-001 | Create a structured master Markdown documentation pack. | AWG-OPS-009, AWG-APP-003 | AWG-OPS-009, AWG-APP-003 | AWG-TEST-COV-041 | draft |
| AWG-REQ-DOC-002 | Put structure and AI-agent instructions first so future agents know how to work. | AWG-OPS-009 | AWG-OPS-009 | AWG-TEST-COV-042 | draft |
| AWG-REQ-OPS-001 | Map the work to the AWG Linear project while retaining a separate canonical source. | AWG-OPS-010 | AWG-OPS-010 | AWG-TEST-COV-043 | draft |
| AWG-REQ-OPS-002 | Generate the full pack on disk with CLI validation. | AWG-OPS-006, AWG-OPS-009 | AWG-OPS-006, AWG-OPS-009 | AWG-TEST-COV-044 | draft |
| AWG-REQ-OPS-003 | Provide a complete archive and downloadable logical parts. | AWG-OPS-005, AWG-APP-003 | AWG-OPS-005, AWG-APP-003 | AWG-TEST-COV-045 | draft |
| AWG-REQ-DOC-003 | Preserve all prior conversation-derived specifications and research. | AWG-VIS-004, AWG-UX-008, AWG-APP-003 | AWG-VIS-004, AWG-UX-008, AWG-APP-003 | AWG-TEST-COV-046 | draft |
| AWG-REQ-DOC-004 | Validate that no declared document, requirement, schema, example, register, or release file is missing. | AWG-OPS-009, AWG-APP-003 | AWG-OPS-009, AWG-APP-003 | AWG-TEST-COV-047 | draft |
| AWG-REQ-GOV-003 | Record risks, assumptions, data provenance, model versions, and open-source licensing. | AWG-GOV-003, AWG-GOV-007, AWG-OPS-011 | AWG-GOV-003, AWG-GOV-007, AWG-OPS-011 | AWG-TEST-COV-048 | draft |
| AWG-REQ-TIME-001 | Simulation time is separate from wall-clock time and is authoritative for causality. | AWG-DOM-008 | AWG-DOM-008 | AWG-TEST-TIME-001 | draft |
| AWG-REQ-PER-001 | Agents receive only observations available through valid sensing or communication paths. | AWG-DOM-009 | AWG-DOM-009 | AWG-TEST-PER-001 | draft |
| AWG-REQ-OBJ-001 | Object interactions enforce affordances, reservations, capacity, and concurrent-action constraints. | AWG-DOM-010 | AWG-DOM-010 | AWG-TEST-OBJ-001 | draft |
| AWG-REQ-KER-001 | The deterministic kernel is the sole authority for accepted state transitions. | AWG-PLAT-007 | AWG-PLAT-007 | AWG-TEST-KER-001 | draft |
| AWG-REQ-REP-001 | Recorded model outputs support replay without external model calls. | AWG-PLAT-002, AWG-SCN-006 | AWG-PLAT-002, AWG-SCN-006 | AWG-TEST-REP-001 | draft |
| AWG-REQ-SEC-001 | Untrusted plugins and model output cannot access secrets or bypass typed interfaces. | AWG-GOV-002, AWG-PLAT-003, AWG-OPS-011 | AWG-GOV-002, AWG-PLAT-003, AWG-OPS-011 | AWG-TEST-SEC-001 | draft |
| AWG-REQ-DATA-001 | Every external dataset records source, licence, coverage, version, transformations, uncertainty, and permitted use. | AWG-GOV-007, AWG-SCN-009 | AWG-GOV-007, AWG-SCN-009 | AWG-TEST-DATA-001 | draft |
| AWG-REQ-CMP-001 | Counterfactual branches remain identical before their declared divergence point. | AWG-SCN-004 | AWG-SCN-004 | AWG-TEST-CMP-001 | draft |
| AWG-REQ-A11Y-001 | Every map workflow has a keyboard-operable and non-map alternative. | AWG-UX-006, AWG-UX-014 | AWG-UX-006, AWG-UX-014 | AWG-TEST-A11Y-001 | draft |
| AWG-REQ-MIG-001 | Breaking schema changes preserve historical readability and provide migration or explicit rejection. | AWG-OPS-007 | AWG-OPS-007 | AWG-TEST-MIG-001 | draft |
| AWG-REQ-REL-001 | Every release includes a file manifest, checksums, validation report, and integrity-tested archives. | AWG-OPS-005, AWG-OPS-009 | AWG-OPS-005, AWG-OPS-009 | AWG-TEST-REL-001 | draft |
| AWG-REQ-COV-001 | The implementation and review process must conform to AWG-VIS-003: Design Principles. | AWG-VIS-003 | AWG-VIS-003 | AWG-TEST-DOC-001 | draft |
| AWG-REQ-COV-002 | The implementation and review process must conform to AWG-DOM-001: Canonical World Model and Ontology. | AWG-DOM-001 | AWG-DOM-001 | AWG-TEST-DOC-002 | draft |
| AWG-REQ-COV-003 | The implementation and review process must conform to AWG-DOM-005: Organization, Group, and Institution Model. | AWG-DOM-005 | AWG-DOM-005 | AWG-TEST-DOC-003 | draft |
| AWG-REQ-COV-004 | The implementation and review process must conform to AWG-DOM-006: Economy, Resource, and Ownership Model. | AWG-DOM-006 | AWG-DOM-006 | AWG-TEST-DOC-004 | draft |
| AWG-REQ-COV-005 | The implementation and review process must conform to AWG-PLAT-001: System Architecture. | AWG-PLAT-001 | AWG-PLAT-001 | AWG-TEST-DOC-005 | draft |
| AWG-REQ-COV-006 | The implementation and review process must conform to AWG-PLAT-004: Storage, Indexing, and Projection Architecture. | AWG-PLAT-004 | AWG-PLAT-004 | AWG-TEST-DOC-006 | draft |
| AWG-REQ-COV-007 | The implementation and review process must conform to AWG-SCN-002: Validation, Calibration, and Benchmark Framework. | AWG-SCN-002 | AWG-SCN-002 | AWG-TEST-DOC-007 | draft |
| AWG-REQ-COV-008 | The implementation and review process must conform to AWG-SCN-003: Uncertainty and Sensitivity Analysis. | AWG-SCN-003 | AWG-SCN-003 | AWG-TEST-DOC-008 | draft |
| AWG-REQ-COV-009 | The implementation and review process must conform to AWG-UX-004: Agent, Place, and Organization Inspectors. | AWG-UX-004 | AWG-UX-004 | AWG-TEST-DOC-009 | draft |
| AWG-REQ-COV-010 | The implementation and review process must conform to AWG-UX-005: Timeline, Replay, and Branch Comparison UX. | AWG-UX-005 | AWG-UX-005 | AWG-TEST-DOC-010 | draft |
| AWG-REQ-COV-011 | The implementation and review process must conform to AWG-OPS-001: MVP Roadmap and Definition of Done. | AWG-OPS-001 | AWG-OPS-001 | AWG-TEST-DOC-011 | draft |
| AWG-REQ-COV-012 | The implementation and review process must conform to AWG-OPS-002: Software Testing and Quality Strategy. | AWG-OPS-002 | AWG-OPS-002 | AWG-TEST-DOC-012 | draft |
| AWG-REQ-COV-013 | The implementation and review process must conform to AWG-OPS-003: Performance Budget and Capacity Plan. | AWG-OPS-003 | AWG-OPS-003 | AWG-TEST-DOC-013 | draft |
| AWG-REQ-COV-014 | The implementation and review process must conform to AWG-OPS-004: Observability, Reliability, and Recovery. | AWG-OPS-004 | AWG-OPS-004 | AWG-TEST-DOC-014 | draft |
| AWG-REQ-COV-015 | The implementation and review process must conform to AWG-GOV-004: Data Classification, Retention, and Deletion. | AWG-GOV-004 | AWG-GOV-004 | AWG-TEST-DOC-015 | draft |
| AWG-REQ-COV-016 | The implementation and review process must conform to AWG-GOV-005: Human Subjects and Real-Person Representation Policy. | AWG-GOV-005 | AWG-GOV-005 | AWG-TEST-DOC-016 | draft |
| AWG-REQ-COV-017 | The implementation and review process must conform to AWG-GOV-006: Claims, Communication, and Responsible Use Policy. | AWG-GOV-006 | AWG-GOV-006 | AWG-TEST-DOC-017 | draft |
| AWG-REQ-COV-018 | The implementation and review process must conform to AWG-DOM-012: Population Synthesis, Cohorts, and Individual Instantiation. | AWG-DOM-012 | AWG-DOM-012 | AWG-TEST-DOC-018 | draft |
| AWG-REQ-COV-019 | The implementation and review process must conform to AWG-PLAT-008: API, Service, and Boundary Contracts. | AWG-PLAT-008 | AWG-PLAT-008 | AWG-TEST-DOC-019 | draft |
| AWG-REQ-COV-020 | The implementation and review process must conform to AWG-PLAT-009: Configuration, Secrets, and Feature Flags. | AWG-PLAT-009 | AWG-PLAT-009 | AWG-TEST-DOC-020 | draft |
| AWG-REQ-COV-021 | The implementation and review process must conform to AWG-PLAT-010: Identity, Access, Tenancy, and Authorization. | AWG-PLAT-010 | AWG-PLAT-010 | AWG-TEST-DOC-021 | draft |
| AWG-REQ-COV-022 | The implementation and review process must conform to AWG-PLAT-011: World Partitioning, Region Ownership, and Handoff. | AWG-PLAT-011 | AWG-PLAT-011 | AWG-TEST-DOC-022 | draft |
| AWG-REQ-COV-023 | The implementation and review process must conform to AWG-SCN-007: Metrics, Measurements, and Outcome Catalog. | AWG-SCN-007 | AWG-SCN-007 | AWG-TEST-DOC-023 | draft |
| AWG-REQ-COV-024 | The implementation and review process must conform to AWG-SCN-008: Scenario Cards, Model Cards, and Limitations. | AWG-SCN-008 | AWG-SCN-008 | AWG-TEST-DOC-024 | draft |
| AWG-REQ-COV-025 | The implementation and review process must conform to AWG-UX-011: Scenario Studio UX. | AWG-UX-011 | AWG-UX-011 | AWG-TEST-DOC-025 | draft |
| AWG-REQ-COV-026 | The implementation and review process must conform to AWG-UX-012: Firehose and Causal Explorer UX. | AWG-UX-012 | AWG-UX-012 | AWG-TEST-DOC-026 | draft |
| AWG-REQ-COV-027 | The implementation and review process must conform to AWG-OPS-008: Backup, Restore, and Disaster Recovery. | AWG-OPS-008 | AWG-OPS-008 | AWG-TEST-DOC-027 | draft |
| AWG-REQ-COV-028 | The implementation and review process must conform to AWG-APP-001: Standards, Conventions, and Identifiers. | AWG-APP-001 | AWG-APP-001 | AWG-TEST-DOC-028 | draft |
| AWG-REQ-INV-001 | An LLM MUST NOT directly write authoritative positions, ownership, resources, event truth, physical state, or completed actions. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-001 | draft |
| AWG-REQ-INV-002 | After scenario initialization, every position change MUST require valid movement, transport, or an explicit logged intervention with authority and reason. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-002 | draft |
| AWG-REQ-INV-003 | Travel, actions, queues, communication, work, sleep, and other processes MUST consume simulation time according to their rules. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-003 | draft |
| AWG-REQ-INV-004 | Routes, barriers, entrances, access rights, modes, capacities, and topology MUST constrain movement. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-004 | draft |
| AWG-REQ-INV-005 | An agent MUST only know information through direct perception, communication, accessible records or media, prior memory, or explicit inference from available evidence. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-005 | draft |
| AWG-REQ-INV-006 | World truth and agent belief MUST remain separate data. Agents MAY hold uncertain, incorrect, manipulated, or contradictory beliefs. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-006 | draft |
| AWG-REQ-INV-007 | Viewing, understanding, believing, endorsing, liking, commenting, reposting, and forwarding MUST be distinct states or actions. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-007 | draft |
| AWG-REQ-INV-008 | Corrections, retractions, reversals, and updated beliefs MUST create new records or events. Causal history MUST NOT be silently erased. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-008 | draft |
| AWG-REQ-INV-009 | Important accepted commands and domain transitions MUST emit versioned machine-readable events to the world firehose. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-009 | draft |
| AWG-REQ-INV-010 | Stochastic behaviour MUST use named random streams or seeds and MUST be recorded sufficiently for experiment comparison and replay. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-010 | draft |
| AWG-REQ-INV-011 | Rendering an individual marker MUST NOT imply full cognition. Aggregating an individual into a map cluster MUST NOT remove their authoritative state. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-011 | draft |
| AWG-REQ-INV-012 | When promoting cohorts to individuals, generated detail MUST be marked synthetic or instantiated and constrained by aggregate history; it MUST NOT be presented as previously observed personal history. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-012 | draft |
| AWG-REQ-INV-013 | Interventions MUST change declared world conditions. Agents MUST react according to their own state, information, constraints, and decision systems. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-013 | draft |
| AWG-REQ-INV-014 | Every adapter MUST preserve validation, provenance, eventing, access, and safety boundaries. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-014 | draft |
| AWG-REQ-INV-015 | Model, provider, version, prompt-policy, and fallback changes MUST be recorded and MUST NOT silently alter a controlled run. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-015 | draft |
| AWG-REQ-INV-016 | PMTiles or Protomaps MAY present offline maps but MUST NOT replace OSM, PostGIS, or routing topology as simulation authority. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-016 | draft |
| AWG-REQ-INV-017 | Believable output, LLM judge scores, or visual plausibility alone MUST NOT be treated as sufficient validation. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-017 | draft |
| AWG-REQ-INV-018 | Observed, imported, inferred, statistically sampled, scenario-assumed, and AI-generated data MUST be distinguishable. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-018 | draft |
| AWG-REQ-INV-019 | Trust MUST be evaluated in context such as source, domain, channel, situation, and history rather than a universal number alone. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-019 | draft |
| AWG-REQ-INV-020 | Loss or failure of an AI provider MUST NOT corrupt authoritative simulation state. Systems MUST fail closed, use deterministic fallback where specified, or leave agents inactive or deferred. | AWG-GOV-001 | AWG-GOV-001 | AWG-TEST-INV-020 | draft |
| AWG-REQ-MVP1-001 | The MVP 1 reference scenario MUST package checksummed generated OSM, a PostGIS spatial model, a local gazetteer, a local routing graph, and a PMTiles presentation archive with explicit provenance. | AWG-OPS-001, AWG-DOM-002, AWG-PLAT-006 | AWG-DOM-002, AWG-PLAT-006 | AWG-TEST-MVP1-001 | draft |
| AWG-REQ-MVP1-002 | The MVP 1 kernel MUST reject teleportation and inaccessible modes, MUST use authoritative route topology, and MUST leave an agent at its origin until computed travel time has elapsed. | AWG-OPS-001, AWG-DOM-002, AWG-DOM-008 | AWG-DOM-002, AWG-DOM-008, AWG-PLAT-007 | AWG-TEST-MVP1-002 | draft |
| AWG-REQ-MVP1-003 | The MVP 1 kernel MUST terminate a building route at a declared entrance and MUST keep building and smart-object occupancy within capacity. | AWG-OPS-001, AWG-DOM-002, AWG-DOM-010 | AWG-DOM-002, AWG-DOM-010, AWG-PLAT-007 | AWG-TEST-MVP1-003 | draft |
| AWG-REQ-MVP1-004 | The MVP 1 event firehose MUST be append-only, snapshots MUST contain integrity checksums, and deterministic replay MUST reproduce the authoritative state checksum. | AWG-OPS-001, AWG-PLAT-002, AWG-PLAT-007 | AWG-PLAT-002, AWG-PLAT-007 | AWG-TEST-MVP1-004 | draft |
| AWG-REQ-MVP1-005 | Semantic clustering and building occupancy inspection MUST operate as deterministic read projections and MUST NOT change authoritative agent positions or state checksums. | AWG-OPS-001, AWG-UX-002, AWG-UX-009 | AWG-UX-002, AWG-UX-009 | AWG-TEST-MVP1-005 | draft |
| AWG-REQ-MVP1-006 | The MVP 1 reference scenario MUST complete with no external network dependency and MUST validate every packaged spatial asset against its recorded checksum. | AWG-OPS-001, AWG-PLAT-006 | AWG-PLAT-006, AWG-PLAT-007 | AWG-TEST-MVP1-006 | draft |
| AWG-REQ-MVP1-007 | The MVP 1 acceptance profile MUST simulate 100 scheduled agents for 24 hours and complete 200 journeys and 1,400 domain events with zero state-integrity failures within the declared test budget. | AWG-OPS-001, AWG-OPS-002, AWG-OPS-003 | AWG-OPS-001, AWG-OPS-002, AWG-OPS-003 | AWG-TEST-MVP1-007 | draft |
| AWG-REQ-MVP2-001 | The MVP 2 classical NPC kernel MUST produce 24-hour home and work activity from needs, utility, schedules, and planners without importing or calling an LLM. | AWG-OPS-001, AWG-DOM-003, AWG-DOM-011 | AWG-DOM-003, AWG-PLAT-007 | AWG-TEST-MVP2-001 | draft |
| AWG-REQ-MVP2-002 | The MVP 2 kernel MUST occupy explicit action channels and MUST reject combinations such as sleep with travel or eat with work. | AWG-OPS-001, AWG-DOM-003 | AWG-DOM-003, AWG-PLAT-007 | AWG-TEST-MVP2-002 | draft |
| AWG-REQ-MVP2-003 | Token and meal totals MUST be conserved across transfers, unique assets MUST have one owner, exclusive smart-object slots MUST NOT be double-reserved, and inventories MUST NOT go negative. | AWG-OPS-001, AWG-DOM-006, AWG-DOM-010 | AWG-DOM-006, AWG-DOM-010 | AWG-TEST-MVP2-003 | draft |
| AWG-REQ-MVP2-004 | An agent MUST know an event only as actor or via a valid co-located observation path and MUST NOT receive organization inventories or remote location changes automatically. | AWG-OPS-001, AWG-DOM-009, AWG-GOV-001 | AWG-DOM-009, AWG-PLAT-007 | AWG-TEST-MVP2-004 | draft |
| AWG-REQ-MVP3-001 | Ollama and OpenRouter candidates MUST implement one provider-neutral AIProviderAdapter boundary, and switching provider MUST NOT change domain proposal schemas. | AWG-OPS-001, AWG-PLAT-003 | AWG-PLAT-003 | AWG-TEST-MVP3-001 | draft |
| AWG-REQ-MVP3-002 | Malformed, timed-out, schema-invalid, or provider-error model output MUST NOT mutate WorldState, EventLog, occupancy, claims, or live memory. | AWG-OPS-001, AWG-PLAT-003, AWG-GOV-001 | AWG-PLAT-003, AWG-PLAT-002 | AWG-TEST-MVP3-002 | draft |
| AWG-REQ-MVP3-003 | Every accepted adapter output MUST be recordable and replayable into the same typed proposal without a provider call. | AWG-OPS-001, AWG-PLAT-003, AWG-PLAT-002 | AWG-PLAT-003, AWG-PLAT-002 | AWG-TEST-MVP3-003 | draft |
| AWG-REQ-MVP3-004 | Every adapter output artifact MUST record adapter, provider, model, prompt-policy, interface, and output-schema versions plus request correlation and outcome. | AWG-OPS-001, AWG-PLAT-003 | AWG-PLAT-003 | AWG-TEST-MVP3-004 | draft |
| AWG-REQ-MVP4-001 | An observation-to-message-to-post-to-repost chain MUST be reconstructable from parent event identifiers without deleting prior transmissions. | AWG-OPS-001, AWG-DOM-004, AWG-DOM-013 | AWG-DOM-004, AWG-PLAT-002 | AWG-TEST-MVP4-001 | draft |
| AWG-REQ-MVP4-002 | Belief MUST remain agent-specific and MUST NOT be implied by likes, views, follows, comments, or reposts, and MUST NOT equal simulator world truth. | AWG-OPS-001, AWG-DOM-004, AWG-GOV-001 | AWG-DOM-004, AWG-DOM-013 | AWG-TEST-MVP4-002 | draft |
| AWG-REQ-MVP4-003 | An agent MUST NOT know a claim, and a participant feed MUST NOT include a post, unless an explicit exposure or audience rule granted access. | AWG-OPS-001, AWG-DOM-004, AWG-DOM-009 | AWG-DOM-004, AWG-DOM-013 | AWG-TEST-MVP4-003 | draft |
| AWG-REQ-MVP4-004 | Corrections and retractions MUST be append-only events and MUST NOT overwrite or delete the original post, claim, or transmission. | AWG-OPS-001, AWG-DOM-004 | AWG-DOM-004, AWG-PLAT-002 | AWG-TEST-MVP4-004 | draft |
| AWG-REQ-MVP5-001 | Scale benchmarks MUST report population records and active cognition as separate counts across fidelity levels S0 through S4. | AWG-OPS-001, AWG-PLAT-005 | AWG-PLAT-005 | AWG-TEST-MVP5-001 | draft |
| AWG-REQ-MVP5-002 | Promotion and demotion MUST conserve tokens and beliefs for the affected record. | AWG-OPS-001, AWG-PLAT-005 | AWG-PLAT-005 | AWG-TEST-MVP5-002 | draft |
| AWG-REQ-MVP5-003 | Branch comparison with a shared seed MUST distinguish an intervention effect from seed-only variance. | AWG-OPS-001, AWG-SCN-002, AWG-SCN-004 | AWG-SCN-002, AWG-SCN-004 | AWG-TEST-MVP5-003 | draft |
| AWG-REQ-WFL-001 | Every roadmap stage MUST execute scope, traceability, implementation, contracts, verification, and closeout in order, and MUST NOT advance while required outputs, acceptance tests, evidence, or validation are incomplete. | AWG-OPS-012 | AWG-OPS-012, AWG-OPS-006, AWG-OPS-009 | AWG-TEST-WFL-001 | draft |
