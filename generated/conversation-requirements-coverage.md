# Conversation Requirements Coverage

Every substantive requirement from the design session is mapped to a normative requirement and document set.

| Conversation ID | Request | Requirement | Covered by | Status |
| --- | --- | --- | --- | --- |
| AWG-CONV-001 | Build complete worlds and scenarios, not isolated chat agents. | AWG-REQ-VIS-001 | AWG-VIS-001, AWG-SCN-001 | covered |
| AWG-CONV-002 | Ground real worlds in OpenStreetMap geography and topology. | AWG-REQ-GEO-001 | AWG-DOM-002 | covered |
| AWG-CONV-003 | Support planet and regional tile views while keeping tiles separate from authoritative world state. | AWG-REQ-GEO-002 | AWG-DOM-002, AWG-UX-003 | covered |
| AWG-CONV-004 | Use Nominatim-compatible gazetteer semantics for places, streets, and addresses. | AWG-REQ-GEO-003 | AWG-DOM-002 | covered |
| AWG-CONV-005 | Use Protomaps and PMTiles for offline map presentation. | AWG-REQ-GEO-004 | AWG-DOM-002, AWG-PLAT-006 | covered |
| AWG-CONV-006 | Support Ollama as a local AI provider. | AWG-REQ-PLG-001 | AWG-PLAT-003, AWG-PLAT-006 | covered |
| AWG-CONV-007 | Support OpenRouter as a remote AI provider. | AWG-REQ-PLG-002 | AWG-PLAT-003 | covered |
| AWG-CONV-008 | Use modular plugin and adapter architecture so components can be swapped without breaking core functionality. | AWG-REQ-PLG-003 | AWG-PLAT-003 | covered |
| AWG-CONV-009 | Treat the system as a serious simulation platform rather than a toy agent demo. | AWG-REQ-GOV-001 | AWG-GOV-001, AWG-VIS-002 | covered |
| AWG-CONV-010 | Expose a structured firehose for each agent and world. | AWG-REQ-EVT-001 | AWG-PLAT-002 | covered |
| AWG-CONV-011 | Allow scenarios and live changes so agents and groups react and communicate. | AWG-REQ-SCN-001 | AWG-SCN-001, AWG-DOM-003, AWG-DOM-013 | covered |
| AWG-CONV-012 | Build humanistic systems from established NPC, ABM, cognitive, social, and behavioural patterns rather than unconstrained invention. | AWG-REQ-AGT-001 | AWG-DOM-003, AWG-DOM-011, AWG-VIS-006 | covered |
| AWG-CONV-013 | Agents must understand the space they occupy. | AWG-REQ-GEO-005 | AWG-DOM-002, AWG-DOM-009 | covered |
| AWG-CONV-014 | Synthetic worlds must use coherent OSM-like places, geometry, access, and traversal. | AWG-REQ-GEO-006 | AWG-DOM-002 | covered |
| AWG-CONV-015 | Movement must consume plausible time and obey route, mode, and speed constraints. | AWG-REQ-GEO-007 | AWG-DOM-002, AWG-DOM-008 | covered |
| AWG-CONV-016 | Agents cannot randomly spawn at destinations or teleport. | AWG-REQ-GEO-008 | AWG-GOV-001, AWG-DOM-002 | covered |
| AWG-CONV-017 | Knowledge learned from another agent must retain source provenance. | AWG-REQ-EPI-001 | AWG-DOM-004 | covered |
| AWG-CONV-018 | Information sources may be reliable, mistaken, deceptive, malicious, or coordinated. | AWG-REQ-EPI-002 | AWG-DOM-004 | covered |
| AWG-CONV-019 | Relationship history and domain context affect trust. | AWG-REQ-EPI-003 | AWG-DOM-004 | covered |
| AWG-CONV-020 | Model witness, second-hand report, post, repost, comment, message, and fact-checking chains. | AWG-REQ-EPI-004 | AWG-DOM-004, AWG-DOM-013 | covered |
| AWG-CONV-021 | A contacted witness may reply, clarify, contradict, ignore, block, or remain uncertain. | AWG-REQ-EPI-005 | AWG-DOM-004, AWG-DOM-013 | covered |
| AWG-CONV-022 | Provide a virtual social-media site where agents can post, react, comment, repost, and message. | AWG-REQ-SOC-001 | AWG-DOM-013, AWG-UX-010 | covered |
| AWG-CONV-023 | Support information-space actors that may not be fully embodied in the physical world. | AWG-REQ-SOC-002 | AWG-DOM-013 | covered |
| AWG-CONV-024 | Capture social and information actions in the firehose. | AWG-REQ-EVT-002 | AWG-PLAT-002, AWG-DOM-004 | covered |
| AWG-CONV-025 | Research papers, GitHub projects, systems, and proven game AI before designing replacements. | AWG-REQ-RES-001 | AWG-VIS-004, AWG-VIS-005 | covered |
| AWG-CONV-026 | Record useful reusable mechanisms and unsuitable mechanisms. | AWG-REQ-RES-002 | AWG-VIS-004, AWG-VIS-006 | covered |
| AWG-CONV-027 | Maintain a never-do list for fake, invalid, or misleading simulation shortcuts. | AWG-REQ-GOV-002 | AWG-GOV-001, AWG-VIS-002 | covered |
| AWG-CONV-028 | Prefer established game NPC architecture over prompt-only reinvention. | AWG-REQ-AGT-002 | AWG-DOM-003, AWG-VIS-006 | covered |
| AWG-CONV-029 | Balance agent markers with aggregate world views. | AWG-REQ-UX-001 | AWG-UX-007, AWG-UX-002 | covered |
| AWG-CONV-030 | Allow thousands of raw dots as an optional debug view without making it the only representation. | AWG-REQ-UX-002 | AWG-UX-007 | covered |
| AWG-CONV-031 | Provide detailed building and interior world views. | AWG-REQ-UX-003 | AWG-UX-009 | covered |
| AWG-CONV-032 | Use controlled randomness for variation, not arbitrary activity. | AWG-REQ-RND-001 | AWG-DOM-007 | covered |
| AWG-CONV-033 | Keep simulation level of detail independent from visualization level of detail. | AWG-REQ-SCL-001 | AWG-PLAT-005, AWG-UX-002 | covered |
| AWG-CONV-034 | Use semantic zoom where cluster totals progressively split into smaller clusters and individuals. | AWG-REQ-UX-004 | AWG-UX-002 | covered |
| AWG-CONV-035 | Clicking a geographic cluster should normally zoom to member bounds. | AWG-REQ-UX-005 | AWG-UX-002 | covered |
| AWG-CONV-036 | Use a radial circle of clickable agents for small true co-location overlaps. | AWG-REQ-UX-006 | AWG-UX-002 | covered |
| AWG-CONV-037 | Use building, floor, room, or occupant browsers for large co-located populations. | AWG-REQ-UX-007 | AWG-UX-002, AWG-UX-009 | covered |
| AWG-CONV-038 | Distinguish geographic, co-location, and analytical clusters. | AWG-REQ-UX-008 | AWG-UX-002 | covered |
| AWG-CONV-039 | Base UI/UX on research and proven visual analytics patterns. | AWG-REQ-UX-009 | AWG-UX-008, AWG-UX-001 | covered |
| AWG-CONV-040 | Provide a design system and frontend architecture. | AWG-REQ-UX-010 | AWG-UX-001, AWG-UX-013 | covered |
| AWG-CONV-041 | Create a structured master Markdown documentation pack. | AWG-REQ-DOC-001 | AWG-OPS-009, AWG-APP-003 | covered |
| AWG-CONV-042 | Put structure and AI-agent instructions first so future agents know how to work. | AWG-REQ-DOC-002 | AWG-OPS-009 | covered |
| AWG-CONV-043 | Map the work to the AWG Linear project while retaining a separate canonical source. | AWG-REQ-OPS-001 | AWG-OPS-010 | covered |
| AWG-CONV-044 | Generate the full pack on disk with CLI validation. | AWG-REQ-OPS-002 | AWG-OPS-006, AWG-OPS-009 | covered |
| AWG-CONV-045 | Provide a complete archive and downloadable logical parts. | AWG-REQ-OPS-003 | AWG-OPS-005, AWG-APP-003 | covered |
| AWG-CONV-046 | Preserve all prior conversation-derived specifications and research. | AWG-REQ-DOC-003 | AWG-VIS-004, AWG-UX-008, AWG-APP-003 | covered |
| AWG-CONV-047 | Validate that no declared document, requirement, schema, example, register, or release file is missing. | AWG-REQ-DOC-004 | AWG-OPS-009, AWG-APP-003 | covered |
| AWG-CONV-048 | Record risks, assumptions, data provenance, model versions, and open-source licensing. | AWG-REQ-GOV-003 | AWG-GOV-003, AWG-GOV-007, AWG-OPS-011 | covered |
