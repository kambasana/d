from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import textwrap
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path('/mnt/data/agentic-world-graph')
SOURCE_ROOT = Path('/mnt/data/agentic-world-graph-docs')
TODAY = '2026-08-20'
VERSION = '0.2.0'

if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + '\n'


def write(path: str | Path, content: str, executable: bool = False) -> Path:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + '\n', encoding='utf-8')
    if executable:
        p.chmod(0o755)
    return p


def first_h1(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return None


def strip_front_matter_text(text: str) -> str:
    """Remove one leading YAML front-matter block from imported Markdown."""
    return re.sub(r'\A---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.DOTALL)


def strip_first_h1(text: str) -> str:
    text = strip_front_matter_text(text)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('# '):
            del lines[i]
            break
    while lines and not lines[0].strip():
        lines.pop(0)
    return '\n'.join(lines).rstrip() + '\n'


def fm(meta: dict[str, Any]) -> str:
    data = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    return f'---\n{data}\n---\n\n'


@dataclass
class DocSpec:
    path: str
    document_id: str
    title: str
    summary: str
    normative: bool = True
    status: str = 'draft'
    owners: list[str] = field(default_factory=lambda: ['AWG architecture'])
    audience: list[str] = field(default_factory=lambda: ['engineering', 'research', 'product'])
    depends_on: list[str] = field(default_factory=list)
    linear_issue: str | None = None
    required_sections: list[str] = field(default_factory=list)
    source_path: Path | None = None
    body: str | None = None
    scope: list[str] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    security: list[str] = field(default_factory=list)
    performance: list[str] = field(default_factory=list)
    acceptance: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)


DOCS: list[DocSpec] = []


def default_required_sections(normative: bool) -> list[str]:
    if not normative:
        return []
    return [
        'Purpose', 'Scope', 'Non-goals', 'Normative requirements',
        'Failure modes', 'Security and privacy considerations',
        'Performance and scale considerations', 'Acceptance criteria',
        'Related documents'
    ]


def render_list(items: list[str]) -> str:
    return '\n'.join(f'- {item}' for item in items) if items else '- None beyond the stated scope.'


def standard_body(spec: DocSpec, detailed: str = '') -> str:
    scope = spec.scope or [spec.summary]
    reqs = spec.requirements or [
        f'The implementation must conform to the rules defined in this specification for {spec.title.lower()}.',
        'All state-changing operations must use typed commands, validation, and append-only domain events where applicable.',
        'Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.',
        'Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.'
    ]
    failures = spec.failure_modes or [
        'Silent divergence between authoritative state and projections.',
        'A plugin or model bypasses validation or provenance controls.',
        'A dependency failure produces fabricated success rather than an explicit degraded or failed state.',
        'A schema or terminology change is introduced without versioning and migration notes.'
    ]
    security = spec.security or [
        'Apply least privilege to plugins, model providers, data stores, and operator actions.',
        'Treat model output, imported data, agent messages, and social content as untrusted input.',
        'Record audit events for privileged changes and protect sensitive data according to classification.'
    ]
    performance = spec.performance or [
        'Use event-driven activation, batching, caching, and level-of-detail policies before increasing hardware cost.',
        'Measure latency, throughput, memory, storage growth, and degradation behaviour under representative load.',
        'Do not trade away correctness, causality, or provenance to improve benchmark numbers.'
    ]
    acceptance = spec.acceptance or [
        'The defined inputs, outputs, states, and failure paths are testable.',
        'Normative requirements are linked to stable requirement IDs and acceptance-test IDs.',
        'At least one valid example and one invalid example are documented or represented in executable fixtures.',
        'Offline and degraded-mode behaviour is explicit.',
        'No LLM or visualization component can override authoritative state.'
    ]
    related = spec.related or spec.depends_on

    parts = [
        f'# {spec.title}',
        '## Purpose', spec.summary,
        '## Status and authority',
        f"This document is {'normative' if spec.normative else 'informative'}. Its current status is **{spec.status}**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.",
        '## Scope', render_list(scope),
        '## Non-goals',
        '- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.\n'
        '- It does not claim that a plausible simulation output is an empirically validated forecast.\n'
        '- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.',
        '## Normative requirements', render_list(reqs),
    ]
    if detailed.strip():
        parts.extend(['## Detailed specification', strip_front_matter_text(detailed).strip()])
    parts.extend([
        '## Failure modes', render_list(failures),
        '## Security and privacy considerations', render_list(security),
        '## Performance and scale considerations', render_list(performance),
        '## Acceptance criteria', render_list(acceptance),
        '## Related documents', render_list(related),
    ])
    return '\n\n'.join(parts).strip() + '\n'


def add_doc(spec: DocSpec) -> None:
    if not spec.required_sections:
        spec.required_sections = default_required_sections(spec.normative)
    if spec.source_path:
        src = spec.source_path.read_text(encoding='utf-8')
        detailed = strip_first_h1(src)
        content = standard_body(spec, detailed) if spec.normative else clean(f'# {spec.title}\n\n{detailed}')
    elif spec.body is not None:
        content = spec.body
        if spec.normative and not all(f'## {s}' in content for s in spec.required_sections):
            content = standard_body(spec, content)
    else:
        content = standard_body(spec)
    meta: dict[str, Any] = {
        'title': spec.title,
        'document_id': spec.document_id,
        'status': spec.status,
        'version': VERSION,
        'last_updated': TODAY,
        'normative': spec.normative,
        'owners': spec.owners,
        'audience': spec.audience,
        'depends_on': spec.depends_on,
        'linear_issue': spec.linear_issue,
        'supersedes': [],
    }
    write(spec.path, fm(meta) + content)
    DOCS.append(spec)


def src(rel: str) -> Path:
    return SOURCE_ROOT / rel


# Existing high-value documents, preserved and normalized.
existing_specs = [
    DocSpec('docs/00-vision-and-research/product-vision.md', 'AWG-VIS-001', 'Product Vision',
            'Define the product vision for a geographically grounded, persistent, modular agentic world operating system.',
            source_path=src('00-vision-and-research/product-vision.md'), normative=False),
    DocSpec('docs/00-vision-and-research/product-scope-and-non-goals.md', 'AWG-VIS-002', 'Product Scope and Non-Goals',
            'Bound the platform so that it is not mistaken for a chatbot village, omniscient digital twin, or guaranteed prediction engine.',
            source_path=src('00-vision-and-research/product-scope-and-non-goals.md'), depends_on=['AWG-VIS-001', 'AWG-GOV-001']),
    DocSpec('docs/00-vision-and-research/design-principles.md', 'AWG-VIS-003', 'Design Principles',
            'Set the cross-cutting design principles used by architecture, product, simulation, research, and UI work.',
            source_path=src('00-vision-and-research/design-principles.md'), depends_on=['AWG-VIS-001', 'AWG-GOV-001']),
    DocSpec('docs/00-vision-and-research/research-and-prior-art.md', 'AWG-VIS-004', 'Research and Prior Art',
            'Preserve the research review of agent simulations, game AI, agent-based modelling, geospatial systems, and reusable open-source components.',
            source_path=src('00-vision-and-research/research-and-prior-art.md'), normative=False,
            owners=['AWG research'], audience=['research', 'architecture', 'engineering']),

    DocSpec('docs/01-governance-and-safety/simulation-constitution-and-invariants.md', 'AWG-GOV-001', 'Simulation Constitution and Invariants',
            'Define the non-negotiable laws that no model, plugin, scenario, operator, projection, or user interface may bypass.',
            source_path=src('01-governance-and-safety/simulation-constitution-and-invariants.md'), linear_issue='ELE-136',
            requirements=['Authoritative state is owned by deterministic simulation systems, not by LLM output.',
                          'People, objects, consequences, and information must have valid paths through space, time, ownership, or communication networks.',
                          'World truth, agent belief, and user-interface projections must remain separate data planes.',
                          'History is append-preserving; corrections and retractions are new events.',
                          'Randomness is typed, seeded, recorded, and replayable.',
                          'Every plugin must obey validation, provenance, security, and event-recording boundaries.'],
            acceptance=['Invariant tests prove that agents cannot teleport, become omniscient, duplicate exclusive resources, or bypass command validation.',
                        'A recorded run can be replayed without re-calling external model providers.',
                        'All normative documents declare dependency on this Constitution or inherit it through another normative document.',
                        'The requirements registry contains a stable requirement ID for every constitutional rule.']),
    DocSpec('docs/01-governance-and-safety/security-safety-privacy-and-misuse-model.md', 'AWG-GOV-002', 'Security, Safety, Privacy, and Misuse Model',
            'Define threat boundaries, privacy controls, misuse protections, access rules, and high-consequence scenario restrictions.',
            source_path=src('01-governance-and-safety/security-safety-privacy-and-misuse-model.md'), depends_on=['AWG-GOV-001']),

    DocSpec('docs/02-domain-model/canonical-world-model-and-ontology.md', 'AWG-DOM-001', 'Canonical World Model and Ontology',
            'Define stable identities, entities, relationships, lifecycles, temporal semantics, spatial semantics, and provenance classes.',
            source_path=src('02-domain-model/canonical-world-model-and-ontology.md'), linear_issue='ELE-137', depends_on=['AWG-GOV-001']),
    DocSpec('docs/02-domain-model/spatial-world-mobility-and-building-specification.md', 'AWG-DOM-002', 'Spatial World, Mobility, and Building Specification',
            'Define authoritative geography, OSM-derived topology, gazetteer semantics, routing, journeys, buildings, interiors, occupancy, and synthetic-world spatial rules.',
            source_path=src('02-domain-model/spatial-world-mobility-and-building-specification.md'), linear_issue='ELE-138', depends_on=['AWG-GOV-001', 'AWG-DOM-001']),
    DocSpec('docs/02-domain-model/agent-runtime-cognition-and-action-model.md', 'AWG-DOM-003', 'Agent Runtime, Cognition, and Action Model',
            'Define a proven NPC-style agent stack using perception, blackboards, needs, schedules, utility systems, planners, action executors, and bounded language models.',
            source_path=src('02-domain-model/agent-runtime-cognition-and-action-model.md'), linear_issue='ELE-139', depends_on=['AWG-GOV-001', 'AWG-DOM-001', 'AWG-DOM-002']),
    DocSpec('docs/02-domain-model/information-trust-and-provenance-model.md', 'AWG-DOM-004', 'Information, Trust, Provenance, and Social Diffusion Model',
            'Define claims, observations, beliefs, evidence, contextual trust, information mutation, bad actors, fact-checking, and virtual social-media diffusion.',
            source_path=src('02-domain-model/information-trust-and-provenance-model.md'), linear_issue='ELE-140', depends_on=['AWG-GOV-001', 'AWG-DOM-001', 'AWG-DOM-003']),
    DocSpec('docs/02-domain-model/organization-group-and-institution-model.md', 'AWG-DOM-005', 'Organization, Group, and Institution Model',
            'Define persistent households, teams, communities, factions, organizations, institutions, governments, membership, authority, and collective action.',
            source_path=src('02-domain-model/organization-group-and-institution-model.md'), depends_on=['AWG-DOM-001', 'AWG-DOM-003']),
    DocSpec('docs/02-domain-model/economy-resource-and-ownership-model.md', 'AWG-DOM-006', 'Economy, Resource, and Ownership Model',
            'Define resources, inventories, transactions, assets, ownership, scarcity, markets, obligations, and economic event provenance.',
            source_path=src('02-domain-model/economy-resource-and-ownership-model.md'), depends_on=['AWG-DOM-001', 'AWG-DOM-003', 'AWG-DOM-005']),

    DocSpec('docs/03-platform-architecture/system-architecture.md', 'AWG-PLAT-001', 'System Architecture',
            'Define the service boundaries and data planes for the world kernel, geospatial systems, agents, information space, scenarios, event history, AI adapters, and projections.',
            source_path=src('03-platform-architecture/system-architecture.md'), depends_on=['AWG-GOV-001', 'AWG-DOM-001']),
    DocSpec('docs/03-platform-architecture/command-event-firehose-and-replay-specification.md', 'AWG-PLAT-002', 'Command, Event, Firehose, and Replay Specification',
            'Define typed intentions and commands, validation, immutable domain events, causal links, snapshots, replay, branches, subscriptions, and model-call provenance.',
            source_path=src('03-platform-architecture/command-event-firehose-and-replay-specification.md'), linear_issue='ELE-141', depends_on=['AWG-GOV-001', 'AWG-DOM-001', 'AWG-PLAT-001']),
    DocSpec('docs/03-platform-architecture/plugin-adapter-sdk-and-compatibility-contracts.md', 'AWG-PLAT-003', 'Plugin and Adapter SDK Compatibility Contracts',
            'Define swappable adapters for AI providers, embeddings, maps, gazetteers, routing, mobility, physics, storage, social platforms, analytics, and visualization.',
            source_path=src('03-platform-architecture/plugin-adapter-sdk-and-compatibility-contracts.md'), linear_issue='ELE-142', depends_on=['AWG-GOV-001', 'AWG-PLAT-001', 'AWG-PLAT-002']),
    DocSpec('docs/03-platform-architecture/storage-indexing-and-projection-architecture.md', 'AWG-PLAT-004', 'Storage, Indexing, and Projection Architecture',
            'Define fit-for-purpose persistence for authoritative state, spatial data, events, analytics, graph projections, search, embeddings, media, and caches.',
            source_path=src('03-platform-architecture/storage-indexing-and-projection-architecture.md'), depends_on=['AWG-DOM-001', 'AWG-PLAT-002']),
    DocSpec('docs/03-platform-architecture/multi-resolution-simulation-and-scaling-architecture.md', 'AWG-PLAT-005', 'Multi-Resolution Simulation and Scaling Architecture',
            'Define aggregate, cohort, scheduled, cognitive, and embodied simulation levels independently from visualization levels.',
            source_path=src('03-platform-architecture/multi-resolution-simulation-and-scaling-architecture.md'), linear_issue='ELE-143', depends_on=['AWG-GOV-001', 'AWG-PLAT-001', 'AWG-PLAT-004']),
    DocSpec('docs/03-platform-architecture/deployment-topologies-and-offline-operation.md', 'AWG-PLAT-006', 'Deployment Topologies and Offline Operation',
            'Define developer, single-machine offline, LAN, air-gapped, hybrid, distributed, and read-only analyst deployment modes.',
            source_path=src('03-platform-architecture/deployment-topologies-and-offline-operation.md'), depends_on=['AWG-PLAT-001', 'AWG-PLAT-003', 'AWG-PLAT-004']),

    DocSpec('docs/04-scenarios-and-validation/scenario-definition-and-experiment-protocol.md', 'AWG-SCN-001', 'Scenario Definition and Experiment Protocol',
            'Define versioned scenario packages, initial state, seeds, interventions, measurements, stop conditions, run records, and reproducible branches.',
            source_path=src('04-scenarios-and-validation/scenario-definition-and-experiment-protocol.md'), linear_issue='ELE-144', depends_on=['AWG-GOV-001', 'AWG-DOM-001', 'AWG-PLAT-002']),
    DocSpec('docs/04-scenarios-and-validation/validation-calibration-and-benchmark-framework.md', 'AWG-SCN-002', 'Validation, Calibration, and Benchmark Framework',
            'Separate software verification, model validation, empirical calibration, human comparison, uncertainty analysis, and use-specific accreditation.',
            source_path=src('04-scenarios-and-validation/validation-calibration-and-benchmark-framework.md'), linear_issue='ELE-145', depends_on=['AWG-GOV-001', 'AWG-SCN-001']),
    DocSpec('docs/04-scenarios-and-validation/uncertainty-and-sensitivity-analysis.md', 'AWG-SCN-003', 'Uncertainty and Sensitivity Analysis',
            'Define ensembles, seed variation, parameter sensitivity, model-provider sensitivity, confidence intervals, and reporting of unstable outcomes.',
            source_path=src('04-scenarios-and-validation/uncertainty-and-sensitivity-analysis.md'), depends_on=['AWG-SCN-001', 'AWG-SCN-002']),
    DocSpec('docs/04-scenarios-and-validation/scenario-comparison-and-counterfactual-analysis.md', 'AWG-SCN-004', 'Scenario Comparison and Counterfactual Analysis',
            'Define baseline alignment, branch inheritance, divergence analysis, causal comparison, and safeguards against false counterfactual claims.',
            source_path=src('04-scenarios-and-validation/scenario-comparison-and-counterfactual-analysis.md'), depends_on=['AWG-SCN-001', 'AWG-SCN-002', 'AWG-SCN-003']),
    DocSpec('docs/04-scenarios-and-validation/example-scenario-package.md', 'AWG-SCN-005', 'Example Scenario Package',
            'Provide an informative example showing how a bounded, reproducible scenario package should be assembled.',
            source_path=src('04-scenarios-and-validation/example-scenario-package.md'), normative=False, depends_on=['AWG-SCN-001']),

    DocSpec('docs/05-ui-ux/ui-application-architecture-and-design-system.md', 'AWG-UX-001', 'UI Application Architecture and Design System',
            'Define the World Explorer, Scenario Studio, inspectors, information space, timeline, firehose, design system, offline client state, and rendering boundaries.',
            source_path=src('05-ui-ux/ui-application-architecture-and-design-system.md'), linear_issue='ELE-146', depends_on=['AWG-GOV-001', 'AWG-PLAT-001']),
    DocSpec('docs/05-ui-ux/agent-map-clustering-and-semantic-zoom.md', 'AWG-UX-002', 'Agent Map Clustering, Semantic Zoom, and Co-Location Interaction',
            'Define count clusters, geographic versus co-location versus analytical clusters, zoom-to-bounds, radial expansion, building drill-down, and selected-agent persistence.',
            source_path=src('05-ui-ux/agent-map-clustering-and-semantic-zoom.md'), linear_issue='ELE-146', depends_on=['AWG-DOM-002', 'AWG-PLAT-005', 'AWG-UX-001']),
    DocSpec('docs/05-ui-ux/map-layer-and-visualization-semantics.md', 'AWG-UX-003', 'Map Layer and Visualization Semantics',
            'Define the meaning, precedence, legends, uncertainty encoding, and truth-versus-projection boundaries of map layers.',
            source_path=src('05-ui-ux/map-layer-and-visualization-semantics.md'), depends_on=['AWG-DOM-002', 'AWG-UX-001', 'AWG-UX-002']),
    DocSpec('docs/05-ui-ux/agent-place-and-organization-inspectors.md', 'AWG-UX-004', 'Agent, Place, and Organization Inspectors',
            'Define structured inspection of current state, history, beliefs, provenance, relationships, occupancy, ownership, and causal explanations.',
            source_path=src('05-ui-ux/agent-place-and-organization-inspectors.md'), depends_on=['AWG-DOM-001', 'AWG-DOM-003', 'AWG-DOM-005', 'AWG-UX-001']),
    DocSpec('docs/05-ui-ux/timeline-replay-and-branch-comparison-ux.md', 'AWG-UX-005', 'Timeline, Replay, and Branch Comparison UX',
            'Define time navigation, causal event inspection, replay controls, branch creation, synchronized comparison, and investigation history.',
            source_path=src('05-ui-ux/timeline-replay-and-branch-comparison-ux.md'), depends_on=['AWG-PLAT-002', 'AWG-SCN-004', 'AWG-UX-001']),
    DocSpec('docs/05-ui-ux/accessibility-and-inclusive-design.md', 'AWG-UX-006', 'Accessibility and Inclusive Design',
            'Ensure maps, graphs, timelines, clusters, alerts, and controls remain operable without relying only on colour, motion, pointer input, or visual maps.',
            source_path=src('05-ui-ux/accessibility-and-inclusive-design.md'), depends_on=['AWG-UX-001']),

    DocSpec('docs/06-delivery-and-operations/mvp-roadmap-and-definition-of-done.md', 'AWG-OPS-001', 'MVP Roadmap and Definition of Done',
            'Define a phased path from one offline district and deterministic movement through bounded AI, information space, validation, and multi-resolution scale.',
            source_path=src('06-delivery-and-operations/mvp-roadmap-and-definition-of-done.md'), linear_issue='ELE-147', depends_on=['AWG-GOV-001', 'AWG-PLAT-001', 'AWG-SCN-002']),
    DocSpec('docs/06-delivery-and-operations/software-testing-and-quality-strategy.md', 'AWG-OPS-002', 'Software Testing and Quality Strategy',
            'Define unit, property, invariant, contract, integration, replay, performance, security, offline, migration, and accessibility testing.',
            source_path=src('06-delivery-and-operations/software-testing-and-quality-strategy.md'), depends_on=['AWG-GOV-001', 'AWG-PLAT-002']),
    DocSpec('docs/06-delivery-and-operations/performance-budget-and-capacity-plan.md', 'AWG-OPS-003', 'Performance Budget and Capacity Plan',
            'Define measurable budgets for agents, events, AI calls, map rendering, storage, replay, snapshots, recovery, and offline hardware profiles.',
            source_path=src('06-delivery-and-operations/performance-budget-and-capacity-plan.md'), depends_on=['AWG-PLAT-005', 'AWG-UX-001']),
    DocSpec('docs/06-delivery-and-operations/observability-reliability-and-recovery.md', 'AWG-OPS-004', 'Observability, Reliability, and Recovery',
            'Define service telemetry separately from simulation events, health indicators, failure isolation, degraded modes, recovery, and auditability.',
            source_path=src('06-delivery-and-operations/observability-reliability-and-recovery.md'), depends_on=['AWG-PLAT-001', 'AWG-PLAT-002']),
    DocSpec('docs/06-delivery-and-operations/release-and-versioning-strategy.md', 'AWG-OPS-005', 'Release and Versioning Strategy',
            'Define document, schema, plugin, scenario, data, and model versioning plus release manifests, checksums, migrations, and deprecation.',
            source_path=src('06-delivery-and-operations/release-and-versioning-strategy.md'), depends_on=['AWG-PLAT-003', 'AWG-PLAT-002']),
]

for spec in existing_specs:
    add_doc(spec)

# Extract detailed conversation-derived sections that were not fully represented in v0.1.0.
ui_source = Path('/mnt/data/agentic-world-graph-research-ui-ux.md').read_text(encoding='utf-8').splitlines()
map_strategy = '\n'.join(ui_source[1521:1651])
randomness = '\n'.join(ui_source[1651:1774])
ui_research = '\n'.join(ui_source[1774:])

add_doc(DocSpec(
    'docs/02-domain-model/stochasticity-noise-and-randomness-model.md', 'AWG-DOM-007',
    'Stochasticity, Noise, and Randomness Model',
    'Define bounded variation, typed uncertainty, random streams, reproducible seeds, perception noise, memory noise, travel variation, and ensemble analysis without using randomness to disguise missing mechanisms.',
    depends_on=['AWG-GOV-001', 'AWG-DOM-003', 'AWG-SCN-003'],
    body=standard_body(DocSpec('', 'AWG-DOM-007', 'Stochasticity, Noise, and Randomness Model',
        'Define bounded variation, typed uncertainty, random streams, reproducible seeds, perception noise, memory noise, travel variation, and ensemble analysis without using randomness to disguise missing mechanisms.',
        depends_on=['AWG-GOV-001', 'AWG-DOM-003', 'AWG-SCN-003'],
        requirements=['Randomness may select only among valid actions and states permitted by the deterministic model.',
                      'Each random source must have a semantic type, stream identifier, seed or recorded stream position, and owning subsystem.',
                      'Perception, memory, mobility, communication, environment, and population-sampling noise must be represented separately.',
                      'A scenario run must be repeatable with the same inputs, versions, and random streams.',
                      'Results must be reported as distributions when stochastic variation materially affects conclusions.']), randomness)
))

add_doc(DocSpec(
    'docs/05-ui-ux/map-world-and-agent-visualization-strategy.md', 'AWG-UX-007',
    'Map, World, and Agent Visualization Strategy',
    'Define the balance between aggregate world views, thousands of agent dots, clusters, flows, building occupancy, local embodied views, and selected-agent continuity.',
    depends_on=['AWG-DOM-002', 'AWG-PLAT-005', 'AWG-UX-001', 'AWG-UX-002'],
    body=standard_body(DocSpec('', 'AWG-UX-007', 'Map, World, and Agent Visualization Strategy',
        'Define the balance between aggregate world views, thousands of agent dots, clusters, flows, building occupancy, local embodied views, and selected-agent continuity.',
        depends_on=['AWG-DOM-002', 'AWG-PLAT-005', 'AWG-UX-001', 'AWG-UX-002']), map_strategy)
))

add_doc(DocSpec(
    'docs/05-ui-ux/ui-ux-research-and-patterns.md', 'AWG-UX-008',
    'UI/UX Research and Proven Interaction Patterns',
    'Preserve the detailed UI/UX research covering visual analytics, semantic zoom, coordinated views, scenario authoring, causal investigation, information-space analysis, design tokens, accessibility, and performance.',
    normative=False, owners=['AWG design research'], audience=['design', 'research', 'engineering'],
    body=fm({}) + '' if False else clean('# UI/UX Research and Proven Interaction Patterns\n\n' + ui_research)
))

print(f'Created {len(DOCS)} normalized documents before new specifications.')

# Additional specifications required for end-to-end completeness.
new_specs: list[DocSpec] = [
    DocSpec('docs/00-vision-and-research/research-method-and-evidence-quality.md', 'AWG-VIS-005',
            'Research Method and Evidence Quality',
            'Define how papers, repositories, game-AI patterns, standards, datasets, and empirical claims are collected, graded, cited, and revisited.',
            normative=True, depends_on=['AWG-VIS-004', 'AWG-GOV-001'],
            scope=['Evidence intake and source classification.', 'Distinguishing architectural inspiration from validated mechanisms.', 'Recording dates, versions, licences, limitations, and conflicting evidence.', 'Rules for claims about human realism, prediction, and scale.'],
            requirements=['Primary sources and official repositories are preferred for technical claims.',
                          'A repository demonstration is not treated as scientific validation.',
                          'Claims about human behaviour must identify the population, task, benchmark, and uncertainty.',
                          'Evidence entries record retrieval date, source type, quality level, relevance, and limitations.',
                          'Contradictory evidence is retained rather than silently resolved.'],
            acceptance=['Every cited reusable component has an evidence entry and licensing review status.',
                        'Every major design principle identifies its evidence basis or is explicitly marked as a design choice.',
                        'The pack does not use star counts, demos, or fluent transcripts as substitutes for validation.']),
    DocSpec('docs/00-vision-and-research/architecture-pattern-reuse-policy.md', 'AWG-VIS-006',
            'Architecture Pattern Reuse Policy',
            'Define how established game, simulation, geospatial, distributed-systems, and AI patterns are adopted without copying unsuitable implementations.',
            depends_on=['AWG-VIS-004', 'AWG-GOV-001'],
            requirements=['Reuse proven concepts such as perception systems, blackboards, utility AI, behaviour trees, StateTree, GOAP/HTN, smart objects, reservations, event sourcing, and adaptive level of detail.',
                          'Do not replace deterministic navigation, physics, ownership, or action execution with natural-language narration.',
                          'Separate pattern reuse from source-code reuse and record licence implications independently.',
                          'Prototype integrations behind adapters and require contract tests before adoption.']),

    DocSpec('docs/01-governance-and-safety/governance-change-control-and-approvals.md', 'AWG-GOV-003',
            'Governance, Change Control, and Approvals',
            'Define document authority, decision ownership, change classes, reviews, approvals, emergency changes, and audit records.',
            depends_on=['AWG-GOV-001'],
            requirements=['Breaking changes to constitutional rules, canonical entities, event envelopes, or plugin contracts require an ADR and explicit approval.',
                          'Generated indexes and reports are never edited directly.',
                          'Emergency changes are time-bounded and followed by retrospective review.',
                          'Every normative change identifies affected requirements, tests, risks, schemas, migrations, and Linear work items.']),
    DocSpec('docs/01-governance-and-safety/data-classification-retention-and-deletion.md', 'AWG-GOV-004',
            'Data Classification, Retention, and Deletion',
            'Define data classes, retention rules, deletion semantics, archival boundaries, backups, and treatment of immutable simulation history.',
            depends_on=['AWG-GOV-001', 'AWG-GOV-002'],
            requirements=['Classify public, internal, confidential, sensitive personal, restricted geospatial, and secret material.',
                          'Separate deletion of personal source material from preservation of non-identifying simulation audit records.',
                          'Retention periods are scenario- and deployment-specific but always explicit.',
                          'Backups, caches, indexes, exports, and model traces follow the same classification rules as source data.']),
    DocSpec('docs/01-governance-and-safety/human-subjects-and-real-person-policy.md', 'AWG-GOV-005',
            'Human Subjects and Real-Person Representation Policy',
            'Define protections for simulations derived from interviews, personal records, identifiable individuals, or sensitive population data.',
            depends_on=['AWG-GOV-002', 'AWG-GOV-004'],
            requirements=['A synthetic agent must not be presented as a faithful digital replica of a real person without a documented lawful and ethical basis.',
                          'Real-person grounding records consent, permitted uses, retention, access, and withdrawal handling.',
                          'Generated traits are distinguished from observed or supplied facts.',
                          'High-risk research involving vulnerable groups requires independent ethics review appropriate to the deployment context.']),
    DocSpec('docs/01-governance-and-safety/claims-communication-and-responsible-use-policy.md', 'AWG-GOV-006',
            'Claims, Communication, and Responsible Use Policy',
            'Control how simulation results, uncertainty, forecasts, synthetic populations, and causal findings are described to users and stakeholders.',
            depends_on=['AWG-GOV-001', 'AWG-SCN-002'],
            requirements=['Outputs are labelled as simulated, scenario-dependent, and uncertain.',
                          'A single run is not reported as a predicted future.',
                          'Validation scope and known limitations accompany consequential conclusions.',
                          'Synthetic populations and model-generated explanations are not represented as observed human testimony.']),
    DocSpec('docs/01-governance-and-safety/compliance-audit-and-evidence-retention.md', 'AWG-GOV-007',
            'Compliance, Audit, and Evidence Retention',
            'Define audit events, evidence packages, access reviews, approval records, reproducibility bundles, and compliance reporting.',
            depends_on=['AWG-GOV-003', 'AWG-GOV-004', 'AWG-PLAT-002'],
            requirements=['Privileged operator actions, data imports, model changes, plugin changes, and scenario interventions are auditable.',
                          'Audit records identify actor, authority, reason, time, affected objects, and result.',
                          'Evidence packages include versions, checksums, run records, licences, data provenance, validation reports, and approvals.']),

    DocSpec('docs/02-domain-model/temporal-model-and-simulation-clock.md', 'AWG-DOM-008',
            'Temporal Model and Simulation Clock',
            'Define simulation time, wall-clock time, event time, valid time, processing time, schedules, durations, recurrence, causality, and time-zone handling.',
            depends_on=['AWG-GOV-001', 'AWG-DOM-001'],
            requirements=['Simulation time is authoritative for world causality and is distinct from wall-clock processing time.',
                          'Every state transition records its effective simulation time and event sequence.',
                          'Travel, work, sleep, communication delay, queueing, and action duration consume simulation time.',
                          'Time-zone and daylight-saving rules are explicit for real-world scenarios.',
                          'The scheduler supports deterministic ordering rules for simultaneous events.']),
    DocSpec('docs/02-domain-model/perception-sensing-and-observation-model.md', 'AWG-DOM-009',
            'Perception, Sensing, and Observation Model',
            'Define how physical, digital, institutional, and communication channels create bounded observations for agents.',
            depends_on=['AWG-DOM-002', 'AWG-DOM-003', 'AWG-DOM-004', 'AWG-DOM-008'],
            requirements=['Agents never receive global state directly.',
                          'Observations identify source channel, location or network path, time, fidelity, uncertainty, and visibility rules.',
                          'Physical sensing depends on position, obstacles, range, attention, and environment.',
                          'Digital exposure depends on platform mechanics, subscriptions, ranking, permissions, and connectivity.',
                          'Observation failure and ambiguity are explicit states rather than silent absence.']),
    DocSpec('docs/02-domain-model/object-affordance-reservation-and-smart-object-model.md', 'AWG-DOM-010',
            'Object Affordance, Reservation, and Smart Object Model',
            'Define objects and places as stateful providers of typed interactions, capacity, ownership, reservations, slots, durations, and observable consequences.',
            depends_on=['AWG-DOM-001', 'AWG-DOM-002', 'AWG-DOM-003', 'AWG-DOM-006'],
            requirements=['Every interactive object declares affordances, preconditions, effects, duration, capacity, permissions, resources, interruption rules, and failure states.',
                          'Exclusive slots use reservation or claim semantics to prevent impossible concurrent use.',
                          'Affordances are data-defined and versioned independently from dialogue wording.',
                          'The LLM may select or describe an affordance but cannot bypass its executor.']),
    DocSpec('docs/02-domain-model/human-state-needs-health-and-life-model.md', 'AWG-DOM-011',
            'Human State, Needs, Health, and Life Model',
            'Define bounded humanistic state for needs, fatigue, health, emotion, roles, obligations, habits, preferences, skills, and life events.',
            depends_on=['AWG-DOM-003', 'AWG-DOM-008'],
            requirements=['Humanistic state uses explicit models and parameters rather than unconstrained personality narration.',
                          'Needs influence utility and planning but do not deterministically force identical behaviour.',
                          'Health and emotional representations declare simplifications, uncertainty, and prohibited clinical interpretation.',
                          'Life histories preserve provenance and distinguish observed, sampled, generated, and inferred attributes.']),
    DocSpec('docs/02-domain-model/population-synthesis-cohorts-and-instantiation.md', 'AWG-DOM-012',
            'Population Synthesis, Cohorts, and Individual Instantiation',
            'Define creation of aggregate populations, calibrated cohorts, scheduled individuals, cognitive agents, and promotion or demotion between fidelity levels.',
            depends_on=['AWG-DOM-001', 'AWG-DOM-003', 'AWG-PLAT-005'],
            requirements=['Population synthesis records source distributions, constraints, sampling method, seed, uncertainty, and validation targets.',
                          'Demographic categories must not become personality stereotypes.',
                          'Promotion from aggregate to individual creates synthetic details marked as unobserved and constrained by prior aggregate state.',
                          'Demotion retains exceptional state, obligations, causal references, and future commitments.']),
    DocSpec('docs/02-domain-model/communication-and-virtual-social-platform-model.md', 'AWG-DOM-013',
            'Communication and Virtual Social Platform Model',
            'Define face-to-face, phone, message, group, email, broadcast, news, forum, and social-platform channels plus feed, ranking, privacy, moderation, and interaction actions.',
            depends_on=['AWG-DOM-004', 'AWG-DOM-005', 'AWG-DOM-008', 'AWG-DOM-009'],
            requirements=['Every transmission has a source, channel, message or claim, audience rule, timing, delivery state, and recipient exposure event.',
                          'Likes, reposts, comments, follows, blocks, views, belief, and endorsement remain separate states.',
                          'Platform ranking and recommendation systems are swappable adapters with recorded configuration.',
                          'Information-space-only actors such as news organizations, bots, and external analysts are explicitly typed.']),

    DocSpec('docs/03-platform-architecture/simulation-kernel-scheduler-and-action-execution.md', 'AWG-PLAT-007',
            'Simulation Kernel, Scheduler, and Action Execution',
            'Define the deterministic world loop, event calendar, activation rules, command validation, action channels, interruption, completion, and failure semantics.',
            depends_on=['AWG-GOV-001', 'AWG-DOM-003', 'AWG-DOM-008', 'AWG-PLAT-002'],
            requirements=['The kernel is the sole authority for accepted state transitions.',
                          'Routine behaviour is event-driven and scheduled rather than polled through an LLM each tick.',
                          'Actions use typed states such as proposed, accepted, scheduled, running, interrupted, completed, failed, and cancelled.',
                          'Simultaneous events follow stable ordering and conflict-resolution rules.',
                          'Long-running actions survive snapshots and replay.']),
    DocSpec('docs/03-platform-architecture/api-service-and-boundary-contracts.md', 'AWG-PLAT-008',
            'API, Service, and Boundary Contracts',
            'Define public, internal, streaming, administrative, plugin, and data-import interfaces without leaking storage implementation into domain contracts.',
            depends_on=['AWG-PLAT-001', 'AWG-PLAT-002', 'AWG-PLAT-003'],
            requirements=['APIs use versioned schemas and idempotency where state-changing retries are possible.',
                          'Read models are projections and cannot be used to bypass command validation.',
                          'Administrative interfaces require explicit authorization and produce audit events.',
                          'Streaming consumers support cursors, backpressure, filtering, and replay from checkpoints.']),
    DocSpec('docs/03-platform-architecture/configuration-secrets-and-feature-flags.md', 'AWG-PLAT-009',
            'Configuration, Secrets, and Feature Flags',
            'Define configuration layering, secrets isolation, scenario parameters, plugin settings, model routing, feature flags, and reproducible run capture.',
            depends_on=['AWG-GOV-002', 'AWG-PLAT-003', 'AWG-SCN-001'],
            requirements=['Secrets never appear in scenario packages, prompts, events, logs, exports, or generated documentation.',
                          'Run-effective configuration is immutable and included by reference or digest in the run record.',
                          'Feature flags declare compatibility, default state, owner, expiry policy, and effect on determinism.',
                          'Environment-specific configuration cannot silently alter scientific parameters.']),
    DocSpec('docs/03-platform-architecture/identity-access-tenancy-and-authorization.md', 'AWG-PLAT-010',
            'Identity, Access, Tenancy, and Authorization',
            'Define users, service identities, agents, simulation actors, operators, tenants, roles, permissions, and delegation boundaries.',
            depends_on=['AWG-GOV-002', 'AWG-GOV-007', 'AWG-PLAT-008'],
            requirements=['Human users, service accounts, simulated agents, and information-space accounts use distinct identity types.',
                          'Simulation-agent authority never grants platform-administration authority.',
                          'Scenario creation, intervention, export, plugin installation, and sensitive data access are separately authorized.',
                          'Tenant and project boundaries are enforced in storage, caches, events, exports, and model context.']),
    DocSpec('docs/03-platform-architecture/world-partitioning-region-ownership-and-handoff.md', 'AWG-PLAT-011',
            'World Partitioning, Region Ownership, and Handoff',
            'Define spatial partitions, authoritative region ownership, border events, journeys across partitions, rebalance, recovery, and consistency guarantees.',
            depends_on=['AWG-DOM-002', 'AWG-PLAT-002', 'AWG-PLAT-005', 'AWG-PLAT-007'],
            requirements=['At any simulation instant, one authority owns mutation rights for an entity or partition.',
                          'Cross-partition movement uses explicit prepare, transfer, commit, and recovery semantics.',
                          'Partition boundaries do not create teleportation, duplicate entities, lost commitments, or information leaks.',
                          'Rebalancing and failover are visible in software telemetry but do not alter world causality.']),

    DocSpec('docs/04-scenarios-and-validation/experiment-reproducibility-and-run-record.md', 'AWG-SCN-006',
            'Experiment Reproducibility and Run Record',
            'Define the immutable record needed to reconstruct a run, including inputs, versions, seeds, plugins, models, datasets, interventions, snapshots, and outputs.',
            depends_on=['AWG-SCN-001', 'AWG-PLAT-002', 'AWG-OPS-005'],
            requirements=['Every run has a unique ID, scenario digest, configuration digest, data-source versions, plugin versions, model records, random streams, and environment details.',
                          'Recorded model responses can be replayed without external inference.',
                          'A reproducibility package includes checksums and declares any unavailable external dependency.',
                          'Run records are append-preserving and cannot be retroactively edited.']),
    DocSpec('docs/04-scenarios-and-validation/metrics-measurements-and-outcome-catalog.md', 'AWG-SCN-007',
            'Metrics, Measurements, and Outcome Catalog',
            'Define measurement semantics, units, windows, populations, denominators, uncertainty, provenance, and branch-comparison compatibility.',
            depends_on=['AWG-SCN-001', 'AWG-SCN-002'],
            requirements=['Metrics distinguish raw observations, derived measures, model outputs, and analyst interpretations.',
                          'Every metric defines unit, population, time window, filters, aggregation, missing-data handling, and uncertainty.',
                          'Metrics are versioned; changed definitions do not overwrite historical results.',
                          'A measure used for validation declares the observed benchmark and acceptable tolerance.']),
    DocSpec('docs/04-scenarios-and-validation/scenario-cards-model-cards-and-limitations.md', 'AWG-SCN-008',
            'Scenario Cards, Model Cards, and Limitations',
            'Define concise disclosure artifacts for scenarios, agent policies, AI models, datasets, validation scope, risks, and prohibited interpretations.',
            depends_on=['AWG-GOV-006', 'AWG-SCN-001', 'AWG-SCN-002', 'AWG-SCN-006'],
            requirements=['Every released scenario has a scenario card describing purpose, population, geography, interventions, assumptions, validation, limitations, and intended use.',
                          'Every AI or learned component has a model record describing provider, version, role, input/output bounds, fallback, and evaluation.',
                          'Limitations are carried into exports and stakeholder reports.']),
    DocSpec('docs/04-scenarios-and-validation/data-calibration-and-parameter-estimation-protocol.md', 'AWG-SCN-009',
            'Data Calibration and Parameter Estimation Protocol',
            'Define calibration datasets, train/validation separation, parameter fitting, objective functions, identifiability, overfitting controls, and recalibration.',
            depends_on=['AWG-SCN-002', 'AWG-SCN-003', 'AWG-GOV-004'],
            requirements=['Calibration and validation datasets are separated where feasible.',
                          'Parameter provenance includes data version, method, code version, uncertainty, and reviewer.',
                          'Unidentifiable parameters are reported rather than assigned false precision.',
                          'Recalibration creates a new model or scenario version and does not rewrite prior run records.']),

    DocSpec('docs/05-ui-ux/building-interior-and-local-world-ux.md', 'AWG-UX-009',
            'Building, Interior, and Local World UX',
            'Define entry from map to building, floors, rooms, entrances, corridors, lifts, stairs, objects, occupants, activities, and local routes.',
            depends_on=['AWG-DOM-002', 'AWG-DOM-010', 'AWG-UX-001', 'AWG-UX-002'],
            requirements=['The UI preserves continuity from geographic location to entrance, floor, room, object, and agent.',
                          'Exact, estimated, room-level, building-level, and aggregate positions are visually distinguished.',
                          'Large occupancy is summarized by building, floor, zone, or room before individual rendering.',
                          'Radial expansion is used only as a selection aid and never implies physical movement.']),
    DocSpec('docs/05-ui-ux/information-space-and-social-platform-ux.md', 'AWG-UX-010',
            'Information Space and Social Platform UX',
            'Define participant-style social interfaces and analyst views for claims, exposure, posts, messages, feeds, diffusion, provenance, trust, and moderation.',
            depends_on=['AWG-DOM-004', 'AWG-DOM-013', 'AWG-UX-001'],
            requirements=['Observed platform actions and inferred motives are shown separately.',
                          'Users can trace a claim from world event through witnesses, messages, posts, exposures, reactions, and belief changes.',
                          'Feed ranking and recommendation settings are inspectable in analyst mode.',
                          'Fact-checking, corrections, retractions, blocking, and moderation remain event-based and historically visible.']),
    DocSpec('docs/05-ui-ux/scenario-studio-ux.md', 'AWG-UX-011',
            'Scenario Studio UX',
            'Define world/scenario creation, data selection, population setup, interventions, seeds, validation, branching, run controls, assumptions, and export.',
            depends_on=['AWG-SCN-001', 'AWG-SCN-007', 'AWG-UX-001'],
            requirements=['Scenario authoring uses typed forms and schema-backed editors rather than one unrestricted prompt.',
                          'The interface shows data provenance, assumptions, unresolved validation errors, and run-affecting configuration.',
                          'Interventions state target, time, authority, scope, duration, and rollback semantics.',
                          'A scenario cannot start when constitutional invariants or required inputs fail validation.']),
    DocSpec('docs/05-ui-ux/firehose-causal-explorer-ux.md', 'AWG-UX-012',
            'Firehose and Causal Explorer UX',
            'Define scalable event browsing, filters, event details, parent and cause links, raw payloads, human summaries, and why-chain navigation.',
            depends_on=['AWG-PLAT-002', 'AWG-UX-001', 'AWG-UX-005'],
            requirements=['The firehose defaults to structured grouping and filtering rather than an unreadable terminal stream.',
                          'Users can navigate from outcome to command, validator, action, observation, belief, source, and originating world event.',
                          'Raw records and readable interpretations are both available and clearly distinguished.',
                          'Sensitive payload fields are redacted according to permissions without destroying event identity.']),
    DocSpec('docs/05-ui-ux/design-tokens-components-and-domain-visual-language.md', 'AWG-UX-013',
            'Design Tokens, Components, and Domain Visual Language',
            'Define design tokens, component states, domain symbols, uncertainty encodings, density modes, motion, themes, and reusable visual primitives.',
            depends_on=['AWG-UX-001', 'AWG-UX-006'],
            requirements=['Tokens cover colour semantics, typography, spacing, radius, elevation, motion, chart scales, map symbols, focus, and density.',
                          'World truth, agent belief, projection, warning, uncertainty, selection, and simulation status have distinct semantics.',
                          'Components support keyboard, screen reader, reduced motion, high contrast, and dense analyst workflows.',
                          'Plugins consume design-system contracts rather than introducing incompatible visual conventions.']),
    DocSpec('docs/05-ui-ux/workspaces-navigation-selection-and-context.md', 'AWG-UX-014',
            'Workspaces, Navigation, Selection, and Context',
            'Define global context, workspace switching, selection persistence, breadcrumbs, coordinated views, saved investigations, and deep links.',
            depends_on=['AWG-UX-001', 'AWG-UX-002', 'AWG-UX-004', 'AWG-UX-005'],
            requirements=['World, scenario, branch, simulation time, perspective mode, and selected entities remain visible in the global context strip.',
                          'Selections persist across compatible zoom and workspace changes.',
                          'Every map-only workflow has a list or table alternative.',
                          'Deep links restore enough context to reproduce an investigation view.']),

    DocSpec('docs/06-delivery-and-operations/developer-environment-and-contributor-workflow.md', 'AWG-OPS-006',
            'Developer Environment and Contributor Workflow',
            'Define local, Docker, offline, branch, pull-request, review, formatting, validation, and release workflows.',
            depends_on=['AWG-OPS-002', 'AWG-OPS-005'],
            requirements=['A clean environment can validate and build the documentation pack with one documented command.',
                          'The workflow works on Windows through Docker Desktop and on standard Linux environments.',
                          'Changes reference Linear issues, document IDs, requirements, tests, risks, and ADRs where applicable.',
                          'Generated outputs are rebuilt rather than manually edited.']),
    DocSpec('docs/06-delivery-and-operations/data-migration-and-backward-compatibility.md', 'AWG-OPS-007',
            'Data Migration and Backward Compatibility',
            'Define migrations for schemas, events, snapshots, scenarios, plugins, projections, datasets, and model records.',
            depends_on=['AWG-PLAT-002', 'AWG-PLAT-003', 'AWG-PLAT-004', 'AWG-OPS-005'],
            requirements=['Breaking schema changes provide migration or explicit unsupported-version handling.',
                          'Historical events remain readable and are not rewritten merely to match a new schema.',
                          'Projection rebuilds are distinguished from authoritative data migrations.',
                          'Migration execution is idempotent or safely resumable and produces audit evidence.']),
    DocSpec('docs/06-delivery-and-operations/backup-restore-and-disaster-recovery.md', 'AWG-OPS-008',
            'Backup, Restore, and Disaster Recovery',
            'Define backup scopes, recovery point and time objectives, snapshot consistency, restore testing, offline media, and corruption recovery.',
            depends_on=['AWG-GOV-004', 'AWG-PLAT-004', 'AWG-OPS-004'],
            requirements=['Backups cover authoritative state, event history, scenario packages, registers, configuration digests, and required external-data manifests.',
                          'Restore procedures are tested and record achieved recovery objectives.',
                          'Encrypted or sensitive backups follow access and retention controls.',
                          'A restore never silently merges incompatible branches or world identities.']),
    DocSpec('docs/06-delivery-and-operations/documentation-quality-gates.md', 'AWG-OPS-009',
            'Documentation Quality Gates',
            'Define structural, semantic, traceability, link, schema, example, licensing, provenance, and release validation for the pack.',
            depends_on=['AWG-GOV-003', 'AWG-OPS-002', 'AWG-OPS-005'],
            linear_issue='ELE-148',
            requirements=['The manifest declares every required document and artifact.',
                          'Normative documents contain required sections and stable metadata.',
                          'Every accepted requirement links to implementation and acceptance-test targets.',
                          'Examples validate against schemas and internal links resolve.',
                          'Releases contain checksums, a file manifest, a validation report, and no unresolved authored placeholders.']),
    DocSpec('docs/06-delivery-and-operations/linear-project-and-execution-mapping.md', 'AWG-OPS-010',
            'Linear Project and Execution Mapping',
            'Define how the canonical disk or Git repository maps to the existing AWG Linear project, milestones, issues, branches, reviews, and delivery status.',
            depends_on=['AWG-GOV-003', 'AWG-OPS-006'],
            requirements=['Linear is an execution tracker rather than the canonical specification store.',
                          'Every reviewable normative document has a Linear issue or documented grouping.',
                          'Issue descriptions reference the canonical document ID and path.',
                          'Completion in Linear does not override failed repository validation.']),
    DocSpec('docs/06-delivery-and-operations/software-supply-chain-and-dependency-assurance.md', 'AWG-OPS-011',
            'Software Supply Chain and Dependency Assurance',
            'Define dependency intake, SBOMs, signatures, vulnerability review, licence review, pinning, reproducible builds, and plugin provenance.',
            depends_on=['AWG-GOV-002', 'AWG-PLAT-003', 'AWG-OPS-005'],
            requirements=['Every shipped dependency and plugin is represented in an SBOM or equivalent inventory.',
                          'Source, version, checksum, licence, maintainer, security status, and update policy are recorded.',
                          'Untrusted plugins do not execute with unrestricted filesystem, network, secret, or database access.',
                          'Offline releases include all required artefacts or explicitly declare external prerequisites.']),

    DocSpec('docs/10-appendices/standards-conventions-and-identifiers.md', 'AWG-APP-001',
            'Standards, Conventions, and Identifiers',
            'Define document IDs, requirement IDs, test IDs, event names, schema versions, timestamps, units, coordinates, naming, and normative language.',
            depends_on=['AWG-GOV-001', 'AWG-DOM-001'],
            requirements=['Normative statements use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY consistently.',
                          'Identifiers are stable, opaque where appropriate, and never reused for different concepts.',
                          'Times use ISO 8601 representations and units are explicit.',
                          'Coordinates identify reference system and axis order.']),
    DocSpec('docs/10-appendices/open-decisions-and-research-backlog.md', 'AWG-APP-002',
            'Open Decisions and Research Backlog',
            'Record unresolved choices and research questions without leaving hidden gaps inside normative specifications.',
            normative=False, depends_on=['AWG-GOV-003']),
    DocSpec('docs/10-appendices/pack-completeness-criteria.md', 'AWG-APP-003',
            'Pack Completeness Criteria',
            'Define what it means for the documentation and executable-contract pack to be structurally complete, reviewable, releasable, and implementation-ready.',
            depends_on=['AWG-OPS-009'],
            requirements=['Every manifest entry exists and every authored file is classified.',
                          'Conversation-derived requirements are mapped to normative requirements and documents.',
                          'Core schemas and valid/invalid examples exist for commands, events, scenarios, agents, plugins, world entities, claims, and beliefs.',
                          'Validation scripts, tests, release tooling, checksums, and area archives execute successfully.']),
]

for spec in new_specs:
    add_doc(spec)

print(f'Created {len(DOCS)} documents including additional specifications.')

# Area navigation and root documentation.
AREA_INFO = {
    '00-vision-and-research': ('Vision and Research', 'Product intent, boundaries, evidence, prior art, and design principles.'),
    '01-governance-and-safety': ('Governance and Safety', 'Constitution, security, privacy, responsible use, retention, and change control.'),
    '02-domain-model': ('Domain Model', 'World entities, agents, space, time, information, groups, resources, and humanistic systems.'),
    '03-platform-architecture': ('Platform Architecture', 'Kernel, events, plugins, storage, scaling, APIs, configuration, and deployment.'),
    '04-scenarios-and-validation': ('Scenarios and Validation', 'Experiments, run records, calibration, metrics, uncertainty, and counterfactuals.'),
    '05-ui-ux': ('UI/UX', 'World Explorer, semantic zoom, inspectors, scenario authoring, causal analysis, and design system.'),
    '06-delivery-and-operations': ('Delivery and Operations', 'MVP plan, testing, performance, reliability, releases, migrations, and supply chain.'),
    '10-appendices': ('Appendices', 'Standards, identifiers, open decisions, and completeness criteria.'),
}

for area, (label, description) in AREA_INFO.items():
    area_docs = [d for d in DOCS if d.path.startswith(f'docs/{area}/')]
    lines = [f'# {label}', '', description, '', '## Documents', '']
    for d in sorted(area_docs, key=lambda x: x.document_id):
        rel = Path(d.path).name
        marker = 'Normative' if d.normative else 'Informative'
        lines.append(f'- [{d.document_id} — {d.title}]({rel}) — {marker}; {d.summary}')
    lines += ['', '## Reading rule', '', 'Read the Simulation Constitution and controlled vocabulary before treating any document in this area as implementation authority.']
    write(f'docs/{area}/README.md', '\n'.join(lines))

write('docs/README.md', clean('''
# Agentic World Graph Documentation

This directory contains the authored specification set. The canonical entry points are the repository root `README.md`, `AGENTS.md`, `pack-manifest.yaml`, and the Simulation Constitution.

## Reading order

1. `../README.md`
2. `../AGENTS.md`
3. `01-governance-and-safety/simulation-constitution-and-invariants.md`
4. `../generated/glossary-and-controlled-vocabulary.md`
5. The relevant area `README.md`
6. The target normative specification
7. Related ADRs, schemas, requirements, risks, tests, and examples

Generated reports under `../generated/` are projections of YAML registers and must not be edited directly.
'''))

root_readme = clean(f'''
# Agentic World Graph

**Version:** {VERSION}  
**Status:** complete architecture and documentation baseline; normative documents remain subject to formal review  
**Generated:** {TODAY}

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
python scripts/validate_all.py
pytest -q
```

Or with Docker:

```bash
docker compose run --rm docs validate
docker compose run --rm docs release
```

## Completeness model

The pack is considered structurally complete only when the manifest, authored files, YAML registers, generated indexes, schemas, examples, tests, checksums, and release archives agree. A passed build does not mean that every draft normative decision has received human approval; document status is tracked separately from structural completeness.

## Source-of-truth rule

The authored files and canonical YAML registers in this repository are the source of truth. Linear tracks work, ownership, review, and delivery; exported ZIPs and generated reports are immutable projections of a release.
''')
write('README.md', root_readme)

agents = clean('''
# Instructions for AI Agents and Automated Contributors

## Mandatory reading order

Before changing any file, read:

1. `README.md`
2. this file
3. `docs/01-governance-and-safety/simulation-constitution-and-invariants.md`
4. `generated/glossary-and-controlled-vocabulary.md`
5. `generated/document-map.md`
6. the target normative specification
7. related requirements, schemas, tests, risks, evidence, and ADRs

## Authority order

1. Simulation Constitution
2. Accepted ADRs
3. Accepted normative specifications
4. Versioned machine-readable contracts
5. Draft normative specifications
6. Informative research and examples
7. Generated indexes and projections
8. Archived conversation-derived material

## Non-negotiable behaviour

- Never allow an LLM, UI, projection, or plugin to mutate authoritative world state directly.
- Never invent physical movement, arrival, ownership, access, knowledge, or causal success.
- Never give an agent global simulator knowledge; observations require a physical or informational path.
- Never treat a like, repost, comment, view, or follow as proof of belief or endorsement.
- Never use PMTiles or display clusters as authoritative geography.
- Never merge world truth, agent belief, UI projection, and software telemetry into one semantic plane.
- Never replace seeded, typed randomness with unexplained activity intended only to make the world look alive.
- Never silently alter model, prompt, plugin, dataset, scenario, or schema versions during a run.
- Never present fluent dialogue or a visually convincing map as scientific validation.
- Never edit generated files directly.

## Change procedure

1. Identify the Linear issue or create a local work record.
2. Identify affected document IDs, requirement IDs, test IDs, schemas, risks, assumptions, data sources, and ADRs.
3. Change canonical authored files or YAML registers.
4. Update executable contracts and examples when semantics change.
5. Run `python scripts/validate_all.py` and `pytest -q`.
6. Rebuild generated reports and release artefacts.
7. Record breaking changes and migrations.

## Terminology

Use canonical terms from `registers/glossary.yaml`. Do not treat `agent`, `LLM`, `user`, `actor`, `cohort`, `entity`, and `account` as interchangeable. Do not introduce a new core noun without a glossary entry and ontology review.

## Normative language

Use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY for requirements. Every new normative rule requires a stable requirement ID and an acceptance-test mapping.

## File placement

- Narrative specifications: `docs/`
- JSON Schemas: `contracts/`
- Canonical structured records: `registers/`
- Generated Markdown/JSON: `generated/`
- Valid and invalid fixtures: `examples/fixtures/`
- Architecture decisions: `decisions/`
- Validation code: `scripts/` and `tests/`
- Historical source material: `archive/`

## Completion rule

Do not claim that the pack or a document is complete merely because files exist. Completion requires the manifest, required sections, traceability, schemas, examples, tests, links, provenance, licensing records, checksums, and validation report to agree.
''')
write('AGENTS.md', agents)

write('CONTRIBUTING.md', clean('''
# Contributing

All changes follow a specification-first workflow.

1. Read `AGENTS.md` and the Simulation Constitution.
2. Work from a Linear issue or documented local work item.
3. Use stable document, requirement, test, schema, and ADR identifiers.
4. Update authored specifications before generated reports.
5. Add or update machine-readable contracts and fixtures when behaviour changes.
6. Run the full validator and test suite.
7. Describe compatibility, security, offline, performance, data, licensing, and migration effects in the pull request.

Direct edits to `generated/` and `dist/` are rejected by validation.
'''))

write('SECURITY.md', clean('''
# Security Policy

Report security issues through the private security channel selected by the repository owner after import. Do not disclose exploitable details in public issues.

The threat model includes model-output injection, malicious social content, untrusted plugins, data poisoning, secret leakage, cross-tenant access, unsafe administrative interventions, dependency compromise, event-log tampering, replay corruption, and sensitive geospatial disclosure.

Security fixes must preserve evidence and causal history. A security response may restrict access or disable a capability, but it must not silently rewrite simulation events.
'''))

write('GOVERNANCE.md', clean('''
# Governance

The Simulation Constitution is the highest project authority. Breaking changes to constitutional rules, the canonical ontology, command/event envelopes, plugin contracts, or reproducibility requirements require an Architecture Decision Record and explicit review.

The canonical repository owns specifications and structured registers. Linear owns planning and execution status. Generated packs, documentation sites, and PDFs are release projections.
'''))

write('CHANGELOG.md', clean(f'''
# Changelog

## {VERSION} — {TODAY}

- Rebuilt the conversation-derived v0.1.0 material as a manifest-controlled repository.
- Preserved the full research, UI/UX, randomness, and semantic-zoom material.
- Added missing governance, domain, kernel, API, reproducibility, UX, operations, and completeness specifications.
- Added canonical YAML registers, conversation-requirement coverage, JSON Schemas, fixtures, validators, tests, Docker workflow, CI templates, checksums, and area release archives.

## 0.1.0 — 2026-08-20

- Initial 68-file Markdown documentation baseline and Linear project mapping.
'''))

write('LICENSE', clean('''
Copyright (c) 2026. All rights reserved.

This documentation and source pack is provided for evaluation and internal development. No public open-source licence is granted by this file. A repository owner may replace this notice only after a documented licensing decision and third-party dependency review.
'''))

write('NOTICE.md', clean('''
# Third-Party Notice

This pack discusses and may later integrate third-party software, standards, papers, datasets, and services. Discussion or architectural reference does not imply that code, data, model weights, or documentation has been redistributed.

Before adoption, consult `registers/open-source-components.yaml`, `registers/data-sources.yaml`, the relevant licence text, and legal review. OpenStreetMap-derived artefacts require appropriate attribution and database-licence handling.
'''))

write('.gitignore', clean('''
__pycache__/
.pytest_cache/
.venv/
site/
dist/*
!dist/.gitkeep
*.pyc
.DS_Store
'''))
write('dist/.gitkeep', '')
write('.editorconfig', clean('''
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.py]
indent_style = space
indent_size = 4
'''))

# Canonical glossary.
glossary = [
    ('Adapter', 'A replaceable implementation of a stable capability contract.', ['connector'], ['plugin implementation']),
    ('Agent', 'A persistent simulated actor with identity, state, constraints, history, perception, goals, and executable actions.', ['NPC', 'simulated person'], ['LLM', 'user account', 'cohort']),
    ('Analytical cluster', 'A visual grouping created by a query or filter rather than physical co-location.', [], ['geographic cluster', 'co-location cluster']),
    ('Belief', 'An agent-specific disposition toward a claim, including confidence, uncertainty, provenance, and contradiction state.', [], ['world truth']),
    ('Branch', 'A scenario-run lineage that inherits state at a branch point and then diverges through declared changes and consequences.', [], ['copy']),
    ('Building', 'A spatial entity with geometry, entrances, occupancy areas, and optional floors, rooms, routes, and affordances.', [], ['place name']),
    ('Claim', 'A proposition carried through observation or communication with source and lineage.', [], ['fact']),
    ('Co-location cluster', 'A visual grouping of agents occupying the same place, room, vehicle, entrance, or near-identical coordinate.', [], ['geographic cluster']),
    ('Command', 'A typed request for a state-changing operation that is validated before execution.', [], ['event', 'intent']),
    ('Counterfactual', 'A branch comparison that changes declared conditions after a common baseline; it is not proof of real-world causality by itself.', [], ['prediction']),
    ('Event', 'An immutable record that something occurred or was rejected at a defined simulation time and sequence.', [], ['command']),
    ('Evidence', 'An observation, record, message, measurement, or source used to support or challenge a claim.', [], ['belief']),
    ('Firehose', 'The structured, ordered stream of domain events emitted by worlds, agents, groups, infrastructure, and information systems.', ['event stream'], ['software log']),
    ('Gazetteer', 'A system that resolves named places and addresses to geographic entities and geometry references.', [], ['routing engine']),
    ('Geographic cluster', 'A visual aggregation of agents distributed within a screen-space or map area.', [], ['co-location cluster']),
    ('Information space', 'The network of claims, messages, posts, media, channels, audiences, platforms, and exposures connected to the physical world.', [], ['global knowledge']),
    ('Intent', 'A proposed goal or desired action before typed command creation and validation.', [], ['command', 'event']),
    ('Journey', 'A time-consuming movement process from origin to destination using one or more routes and transport legs.', [], ['teleport']),
    ('LLM', 'A language model used through bounded adapters for defined reasoning or language tasks.', ['language model'], ['agent', 'simulation kernel']),
    ('Observation', 'A bounded record made available to an agent through a valid physical, digital, institutional, or communication path.', [], ['world state']),
    ('Place', 'A stable spatial identity linked to one or more geometries, names, relationships, access rules, and provenance.', [], ['coordinate']),
    ('Plugin', 'A packaged extension that declares capabilities, permissions, versions, dependencies, and compatibility.', [], ['core contract']),
    ('Projection', 'A derived read model used for maps, dashboards, search, analytics, feeds, or other views.', [], ['authoritative state']),
    ('Provenance', 'The lineage explaining origin, transformations, sources, actors, times, and derivations of data, claims, events, or artefacts.', [], ['citation only']),
    ('Random stream', 'A named, owned sequence of stochastic values with a seed or recorded position.', [], ['unexplained noise']),
    ('Replay', 'Reconstruction of a run from recorded inputs, versions, random streams, events, snapshots, and model outputs.', [], ['rerun with new model calls']),
    ('Scenario', 'A versioned package of world state, population, assumptions, configuration, events, interventions, measurements, and stop conditions.', [], ['prompt']),
    ('Semantic zoom', 'A visualization strategy that changes what information is shown as scale changes, rather than only resizing the same marks.', [], ['marker scaling']),
    ('Simulation level of detail', 'The fidelity at which a population, cohort, individual, or local embodied agent is simulated.', ['simulation LOD'], ['visualization LOD']),
    ('Simulation time', 'The authoritative temporal coordinate for world causality.', [], ['wall-clock time']),
    ('Smart object', 'An object or place exposing typed affordances, slots, preconditions, capacity, reservations, and effects.', [], ['decorative prop']),
    ('Snapshot', 'A versioned state checkpoint used with event history for recovery or replay.', [], ['event history replacement']),
    ('Synthetic geography', 'Generated but coherent spatial data using explicit topology, places, geometry, access, routing, and provenance.', [], ['invented place names']),
    ('Telemetry', 'Software-operational measurements such as latency, CPU, memory, queue depth, and errors.', [], ['domain event']),
    ('Trust', 'An agent-specific, domain- and context-dependent evaluation of a source based on relationships, history, and evidence.', [], ['single universal score']),
    ('Visualization level of detail', 'The representation used at the current view scale, such as heatmap, cluster, marker, or detailed avatar.', ['visualization LOD'], ['simulation LOD']),
    ('Wall-clock time', 'Real processing or user-interface time outside the simulated world chronology.', [], ['simulation time']),
    ('World', 'A persistent spatial-temporal state containing entities, systems, rules, histories, and branches.', [], ['map']),
    ('World truth', 'The authoritative simulated state and events, distinct from any agent belief or UI projection.', ['authoritative state'], ['belief']),
]

glossary_records = []
for i, (term, definition, allowed, prohibited) in enumerate(glossary, 1):
    glossary_records.append({
        'id': f'AWG-TERM-{i:03d}', 'term': term, 'definition': definition,
        'allowed_synonyms': allowed, 'not_interchangeable_with': prohibited,
        'status': 'canonical'
    })
write('registers/glossary.yaml', yaml.safe_dump({'version': VERSION, 'terms': glossary_records}, sort_keys=False, allow_unicode=True))

# Conversation requirements establish coverage of every substantive request from this design session.
conversation_items = [
    ('AWG-CONV-001', 'Build complete worlds and scenarios, not isolated chat agents.', 'AWG-REQ-VIS-001', ['AWG-VIS-001', 'AWG-SCN-001']),
    ('AWG-CONV-002', 'Ground real worlds in OpenStreetMap geography and topology.', 'AWG-REQ-GEO-001', ['AWG-DOM-002']),
    ('AWG-CONV-003', 'Support planet and regional tile views while keeping tiles separate from authoritative world state.', 'AWG-REQ-GEO-002', ['AWG-DOM-002', 'AWG-UX-003']),
    ('AWG-CONV-004', 'Use Nominatim-compatible gazetteer semantics for places, streets, and addresses.', 'AWG-REQ-GEO-003', ['AWG-DOM-002']),
    ('AWG-CONV-005', 'Use Protomaps and PMTiles for offline map presentation.', 'AWG-REQ-GEO-004', ['AWG-DOM-002', 'AWG-PLAT-006']),
    ('AWG-CONV-006', 'Support Ollama as a local AI provider.', 'AWG-REQ-PLG-001', ['AWG-PLAT-003', 'AWG-PLAT-006']),
    ('AWG-CONV-007', 'Support OpenRouter as a remote AI provider.', 'AWG-REQ-PLG-002', ['AWG-PLAT-003']),
    ('AWG-CONV-008', 'Use modular plugin and adapter architecture so components can be swapped without breaking core functionality.', 'AWG-REQ-PLG-003', ['AWG-PLAT-003']),
    ('AWG-CONV-009', 'Treat the system as a serious simulation platform rather than a toy agent demo.', 'AWG-REQ-GOV-001', ['AWG-GOV-001', 'AWG-VIS-002']),
    ('AWG-CONV-010', 'Expose a structured firehose for each agent and world.', 'AWG-REQ-EVT-001', ['AWG-PLAT-002']),
    ('AWG-CONV-011', 'Allow scenarios and live changes so agents and groups react and communicate.', 'AWG-REQ-SCN-001', ['AWG-SCN-001', 'AWG-DOM-003', 'AWG-DOM-013']),
    ('AWG-CONV-012', 'Build humanistic systems from established NPC, ABM, cognitive, social, and behavioural patterns rather than unconstrained invention.', 'AWG-REQ-AGT-001', ['AWG-DOM-003', 'AWG-DOM-011', 'AWG-VIS-006']),
    ('AWG-CONV-013', 'Agents must understand the space they occupy.', 'AWG-REQ-GEO-005', ['AWG-DOM-002', 'AWG-DOM-009']),
    ('AWG-CONV-014', 'Synthetic worlds must use coherent OSM-like places, geometry, access, and traversal.', 'AWG-REQ-GEO-006', ['AWG-DOM-002']),
    ('AWG-CONV-015', 'Movement must consume plausible time and obey route, mode, and speed constraints.', 'AWG-REQ-GEO-007', ['AWG-DOM-002', 'AWG-DOM-008']),
    ('AWG-CONV-016', 'Agents cannot randomly spawn at destinations or teleport.', 'AWG-REQ-GEO-008', ['AWG-GOV-001', 'AWG-DOM-002']),
    ('AWG-CONV-017', 'Knowledge learned from another agent must retain source provenance.', 'AWG-REQ-EPI-001', ['AWG-DOM-004']),
    ('AWG-CONV-018', 'Information sources may be reliable, mistaken, deceptive, malicious, or coordinated.', 'AWG-REQ-EPI-002', ['AWG-DOM-004']),
    ('AWG-CONV-019', 'Relationship history and domain context affect trust.', 'AWG-REQ-EPI-003', ['AWG-DOM-004']),
    ('AWG-CONV-020', 'Model witness, second-hand report, post, repost, comment, message, and fact-checking chains.', 'AWG-REQ-EPI-004', ['AWG-DOM-004', 'AWG-DOM-013']),
    ('AWG-CONV-021', 'A contacted witness may reply, clarify, contradict, ignore, block, or remain uncertain.', 'AWG-REQ-EPI-005', ['AWG-DOM-004', 'AWG-DOM-013']),
    ('AWG-CONV-022', 'Provide a virtual social-media site where agents can post, react, comment, repost, and message.', 'AWG-REQ-SOC-001', ['AWG-DOM-013', 'AWG-UX-010']),
    ('AWG-CONV-023', 'Support information-space actors that may not be fully embodied in the physical world.', 'AWG-REQ-SOC-002', ['AWG-DOM-013']),
    ('AWG-CONV-024', 'Capture social and information actions in the firehose.', 'AWG-REQ-EVT-002', ['AWG-PLAT-002', 'AWG-DOM-004']),
    ('AWG-CONV-025', 'Research papers, GitHub projects, systems, and proven game AI before designing replacements.', 'AWG-REQ-RES-001', ['AWG-VIS-004', 'AWG-VIS-005']),
    ('AWG-CONV-026', 'Record useful reusable mechanisms and unsuitable mechanisms.', 'AWG-REQ-RES-002', ['AWG-VIS-004', 'AWG-VIS-006']),
    ('AWG-CONV-027', 'Maintain a never-do list for fake, invalid, or misleading simulation shortcuts.', 'AWG-REQ-GOV-002', ['AWG-GOV-001', 'AWG-VIS-002']),
    ('AWG-CONV-028', 'Prefer established game NPC architecture over prompt-only reinvention.', 'AWG-REQ-AGT-002', ['AWG-DOM-003', 'AWG-VIS-006']),
    ('AWG-CONV-029', 'Balance agent markers with aggregate world views.', 'AWG-REQ-UX-001', ['AWG-UX-007', 'AWG-UX-002']),
    ('AWG-CONV-030', 'Allow thousands of raw dots as an optional debug view without making it the only representation.', 'AWG-REQ-UX-002', ['AWG-UX-007']),
    ('AWG-CONV-031', 'Provide detailed building and interior world views.', 'AWG-REQ-UX-003', ['AWG-UX-009']),
    ('AWG-CONV-032', 'Use controlled randomness for variation, not arbitrary activity.', 'AWG-REQ-RND-001', ['AWG-DOM-007']),
    ('AWG-CONV-033', 'Keep simulation level of detail independent from visualization level of detail.', 'AWG-REQ-SCL-001', ['AWG-PLAT-005', 'AWG-UX-002']),
    ('AWG-CONV-034', 'Use semantic zoom where cluster totals progressively split into smaller clusters and individuals.', 'AWG-REQ-UX-004', ['AWG-UX-002']),
    ('AWG-CONV-035', 'Clicking a geographic cluster should normally zoom to member bounds.', 'AWG-REQ-UX-005', ['AWG-UX-002']),
    ('AWG-CONV-036', 'Use a radial circle of clickable agents for small true co-location overlaps.', 'AWG-REQ-UX-006', ['AWG-UX-002']),
    ('AWG-CONV-037', 'Use building, floor, room, or occupant browsers for large co-located populations.', 'AWG-REQ-UX-007', ['AWG-UX-002', 'AWG-UX-009']),
    ('AWG-CONV-038', 'Distinguish geographic, co-location, and analytical clusters.', 'AWG-REQ-UX-008', ['AWG-UX-002']),
    ('AWG-CONV-039', 'Base UI/UX on research and proven visual analytics patterns.', 'AWG-REQ-UX-009', ['AWG-UX-008', 'AWG-UX-001']),
    ('AWG-CONV-040', 'Provide a design system and frontend architecture.', 'AWG-REQ-UX-010', ['AWG-UX-001', 'AWG-UX-013']),
    ('AWG-CONV-041', 'Create a structured master Markdown documentation pack.', 'AWG-REQ-DOC-001', ['AWG-OPS-009', 'AWG-APP-003']),
    ('AWG-CONV-042', 'Put structure and AI-agent instructions first so future agents know how to work.', 'AWG-REQ-DOC-002', ['AWG-OPS-009']),
    ('AWG-CONV-043', 'Map the work to the AWG Linear project while retaining a separate canonical source.', 'AWG-REQ-OPS-001', ['AWG-OPS-010']),
    ('AWG-CONV-044', 'Generate the full pack on disk with CLI validation.', 'AWG-REQ-OPS-002', ['AWG-OPS-006', 'AWG-OPS-009']),
    ('AWG-CONV-045', 'Provide a complete archive and downloadable logical parts.', 'AWG-REQ-OPS-003', ['AWG-OPS-005', 'AWG-APP-003']),
    ('AWG-CONV-046', 'Preserve all prior conversation-derived specifications and research.', 'AWG-REQ-DOC-003', ['AWG-VIS-004', 'AWG-UX-008', 'AWG-APP-003']),
    ('AWG-CONV-047', 'Validate that no declared document, requirement, schema, example, register, or release file is missing.', 'AWG-REQ-DOC-004', ['AWG-OPS-009', 'AWG-APP-003']),
    ('AWG-CONV-048', 'Record risks, assumptions, data provenance, model versions, and open-source licensing.', 'AWG-REQ-GOV-003', ['AWG-GOV-003', 'AWG-GOV-007', 'AWG-OPS-011']),
]
write('registers/conversation-requirements.yaml', yaml.safe_dump({'version': VERSION, 'requirements': [
    {'id': cid, 'request': req, 'normative_requirement': rid, 'covered_by': docs, 'status': 'covered'}
    for cid, req, rid, docs in conversation_items
]}, sort_keys=False, allow_unicode=True))

# Normative requirements and acceptance test catalogue.
requirements = []
tests_catalog = []
for idx, (cid, statement, rid, covered_by) in enumerate(conversation_items, 1):
    test_id = f'AWG-TEST-COV-{idx:03d}'
    requirements.append({
        'id': rid,
        'title': statement[:100],
        'statement': statement,
        'source_conversation_requirement': cid,
        'source_documents': covered_by,
        'implemented_by': covered_by,
        'verified_by': [test_id],
        'status': 'draft',
    })
    tests_catalog.append({
        'id': test_id,
        'type': 'acceptance',
        'description': f'Verify coverage and implementation evidence for: {statement}',
        'requirements': [rid],
        'automation': 'catalogue; implementation test required before feature acceptance',
        'status': 'defined',
    })

extra_requirements = [
    ('AWG-REQ-TIME-001', 'Simulation time is separate from wall-clock time and is authoritative for causality.', ['AWG-DOM-008'], 'AWG-TEST-TIME-001'),
    ('AWG-REQ-PER-001', 'Agents receive only observations available through valid sensing or communication paths.', ['AWG-DOM-009'], 'AWG-TEST-PER-001'),
    ('AWG-REQ-OBJ-001', 'Object interactions enforce affordances, reservations, capacity, and concurrent-action constraints.', ['AWG-DOM-010'], 'AWG-TEST-OBJ-001'),
    ('AWG-REQ-KER-001', 'The deterministic kernel is the sole authority for accepted state transitions.', ['AWG-PLAT-007'], 'AWG-TEST-KER-001'),
    ('AWG-REQ-REP-001', 'Recorded model outputs support replay without external model calls.', ['AWG-PLAT-002', 'AWG-SCN-006'], 'AWG-TEST-REP-001'),
    ('AWG-REQ-SEC-001', 'Untrusted plugins and model output cannot access secrets or bypass typed interfaces.', ['AWG-GOV-002', 'AWG-PLAT-003', 'AWG-OPS-011'], 'AWG-TEST-SEC-001'),
    ('AWG-REQ-DATA-001', 'Every external dataset records source, licence, coverage, version, transformations, uncertainty, and permitted use.', ['AWG-GOV-007', 'AWG-SCN-009'], 'AWG-TEST-DATA-001'),
    ('AWG-REQ-CMP-001', 'Counterfactual branches remain identical before their declared divergence point.', ['AWG-SCN-004'], 'AWG-TEST-CMP-001'),
    ('AWG-REQ-A11Y-001', 'Every map workflow has a keyboard-operable and non-map alternative.', ['AWG-UX-006', 'AWG-UX-014'], 'AWG-TEST-A11Y-001'),
    ('AWG-REQ-MIG-001', 'Breaking schema changes preserve historical readability and provide migration or explicit rejection.', ['AWG-OPS-007'], 'AWG-TEST-MIG-001'),
    ('AWG-REQ-REL-001', 'Every release includes a file manifest, checksums, validation report, and integrity-tested archives.', ['AWG-OPS-005', 'AWG-OPS-009'], 'AWG-TEST-REL-001'),
]
for rid, statement, docs, tid in extra_requirements:
    requirements.append({'id': rid, 'title': statement[:100], 'statement': statement, 'source_documents': docs,
                         'implemented_by': docs, 'verified_by': [tid], 'status': 'draft'})
    tests_catalog.append({'id': tid, 'type': 'acceptance', 'description': statement, 'requirements': [rid],
                          'automation': 'specified in implementation test plan', 'status': 'defined'})

write('registers/requirements.yaml', yaml.safe_dump({'version': VERSION, 'requirements': requirements}, sort_keys=False, allow_unicode=True))
write('registers/tests.yaml', yaml.safe_dump({'version': VERSION, 'tests': tests_catalog}, sort_keys=False, allow_unicode=True))

# Risk and assumption registers.
risks = [
    ('AWG-RISK-001', 'LLM output mutates authoritative state', 'critical', 'Prevent direct writes; typed command validation and capability isolation.', ['AWG-GOV-001', 'AWG-PLAT-007']),
    ('AWG-RISK-002', 'Spatially impossible movement or teleportation', 'critical', 'Authoritative routes, journey states, elapsed time, and invariant tests.', ['AWG-DOM-002']),
    ('AWG-RISK-003', 'Agents become omniscient through context assembly', 'high', 'Observation service, epistemic state, information paths, and access controls.', ['AWG-DOM-009', 'AWG-DOM-004']),
    ('AWG-RISK-004', 'Per-agent per-tick model calls make scale and cost infeasible', 'high', 'Event-driven activation, classical policies, batching, LOD, budgets, and caching.', ['AWG-DOM-003', 'AWG-PLAT-005']),
    ('AWG-RISK-005', 'Believable dialogue is mistaken for validated human behaviour', 'critical', 'Validation framework, responsible claims policy, human baselines, and uncertainty.', ['AWG-GOV-006', 'AWG-SCN-002']),
    ('AWG-RISK-006', 'Synthetic population stereotypes cause biased outcomes', 'high', 'Provenance, calibration, constrained synthesis, sensitivity tests, and ethics review.', ['AWG-DOM-012', 'AWG-GOV-005']),
    ('AWG-RISK-007', 'Information actions are incorrectly interpreted as belief', 'high', 'Separate exposure, reaction, motive inference, belief, and endorsement.', ['AWG-DOM-004', 'AWG-DOM-013']),
    ('AWG-RISK-008', 'Plugin compromise or dependency supply-chain attack', 'critical', 'Permissions, isolation, SBOM, pinning, verification, and contract tests.', ['AWG-PLAT-003', 'AWG-OPS-011']),
    ('AWG-RISK-009', 'External data or OSM gaps create false precision', 'high', 'Coverage metadata, uncertainty, fallback, visible limitations, and local validation.', ['AWG-DOM-002', 'AWG-SCN-009']),
    ('AWG-RISK-010', 'Indoor geometry and entrances are absent or wrong', 'medium', 'Confidence levels, explicit unresolved access, local authoring, and validation.', ['AWG-DOM-002', 'AWG-UX-009']),
    ('AWG-RISK-011', 'Event volume overwhelms storage and analysis', 'high', 'Partitioning, compression, retention classes, projections, and capacity tests.', ['AWG-PLAT-002', 'AWG-PLAT-004', 'AWG-OPS-003']),
    ('AWG-RISK-012', 'Model or prompt drift invalidates comparisons', 'high', 'Immutable run records, version registry, recorded outputs, and sensitivity analysis.', ['AWG-SCN-006', 'AWG-SCN-003']),
    ('AWG-RISK-013', 'Visual clusters imply false co-location or movement', 'medium', 'Distinct cluster types, precise labels, zoom-to-bounds, and anchored radial expansion.', ['AWG-UX-002']),
    ('AWG-RISK-014', 'Counterfactual results are overclaimed as causal truth', 'critical', 'Baseline alignment, uncertainty, validation scope, and responsible-use wording.', ['AWG-SCN-004', 'AWG-GOV-006']),
    ('AWG-RISK-015', 'Offline deployment still phones home through hidden dependencies', 'high', 'Network-deny tests, local assets, provider capability declarations, and telemetry controls.', ['AWG-PLAT-006', 'AWG-OPS-002']),
    ('AWG-RISK-016', 'Replay diverges due to nondeterministic ordering or missing model records', 'high', 'Stable sequencing, random streams, snapshot validation, and recorded inference.', ['AWG-PLAT-002', 'AWG-DOM-008']),
    ('AWG-RISK-017', 'Licensing obligations block commercial distribution', 'high', 'Provisional register, legal review, architecture-pattern-only alternatives, and SBOM.', ['AWG-OPS-011']),
    ('AWG-RISK-018', 'Sensitive real-person or geospatial data is exposed', 'critical', 'Classification, least privilege, de-identification, retention, redaction, and audit.', ['AWG-GOV-002', 'AWG-GOV-004', 'AWG-GOV-005']),
    ('AWG-RISK-019', 'A single graph database becomes a performance and coupling bottleneck', 'medium', 'Semantic graph model over fit-for-purpose stores and projections.', ['AWG-PLAT-004']),
    ('AWG-RISK-020', 'Documentation, schemas, examples, and Linear drift apart', 'high', 'Manifest validation, generated indexes, traceability, CI gates, and canonical source rule.', ['AWG-OPS-009', 'AWG-OPS-010']),
]
write('registers/risks.yaml', yaml.safe_dump({'version': VERSION, 'risks': [
    {'id': rid, 'description': desc, 'severity': sev, 'mitigation': mit, 'affected_documents': docs,
     'owner': 'AWG project', 'status': 'open', 'residual_risk': 'requires implementation evidence'}
    for rid, desc, sev, mit, docs in risks
]}, sort_keys=False, allow_unicode=True))

assumptions = [
    ('AWG-ASM-001', 'A bounded region can be validated before planetary expansion.', ['AWG-OPS-001']),
    ('AWG-ASM-002', 'OpenStreetMap-derived data provides a useful base but requires local coverage assessment.', ['AWG-DOM-002']),
    ('AWG-ASM-003', 'Offline deployments can obtain local PBF extracts, tiles, gazetteer, routing data, and model artefacts lawfully.', ['AWG-PLAT-006']),
    ('AWG-ASM-004', 'Users will distinguish scenario exploration from prediction when the UI and reports communicate uncertainty correctly.', ['AWG-GOV-006']),
    ('AWG-ASM-005', 'Classical agent systems can handle most routine behaviour without model inference.', ['AWG-DOM-003']),
    ('AWG-ASM-006', 'World state can be partitioned while maintaining one mutation authority per entity or region.', ['AWG-PLAT-011']),
    ('AWG-ASM-007', 'Indoor detail will often be incomplete and must support explicit confidence and authoring.', ['AWG-DOM-002']),
    ('AWG-ASM-008', 'A provider-neutral structured-output boundary is feasible for Ollama, OpenRouter, and future providers.', ['AWG-PLAT-003']),
    ('AWG-ASM-009', 'Event sourcing plus snapshots is suitable for required replay and audit needs.', ['AWG-PLAT-002']),
    ('AWG-ASM-010', 'The repository will later be imported into a version-control system with protected review workflow.', ['AWG-OPS-006']),
]
write('registers/assumptions.yaml', yaml.safe_dump({'version': VERSION, 'assumptions': [
    {'id': aid, 'statement': statement, 'affected_documents': docs, 'owner': 'AWG project',
     'status': 'active', 'review_trigger': 'architecture review or contradictory evidence'}
    for aid, statement, docs in assumptions
]}, sort_keys=False, allow_unicode=True))

# Data provenance register uses candidate status where a scenario must select an exact source.
data_sources = [
    {'id': 'AWG-DATA-001', 'name': 'OpenStreetMap regional PBF extract', 'role': 'authoritative base geography input', 'provider': 'OpenStreetMap contributors or approved extract provider', 'licence': 'ODbL-1.0; verify attribution and produced-work obligations', 'status': 'required_per_world', 'provenance_fields': ['download URL', 'retrieval time', 'extract region', 'replication sequence or timestamp', 'checksum', 'transformation version'], 'known_limits': ['coverage and tagging vary', 'indoor and entrance data may be incomplete']},
    {'id': 'AWG-DATA-002', 'name': 'PostGIS spatial world database', 'role': 'derived authoritative geometry and relationships', 'provider': 'local transformation pipeline', 'licence': 'inherits source-data obligations', 'status': 'derived', 'provenance_fields': ['source PBF IDs', 'osm2pgsql profile version', 'schema version', 'build log', 'checksum'], 'known_limits': ['derived classifications depend on transformation rules']},
    {'id': 'AWG-DATA-003', 'name': 'Nominatim gazetteer index', 'role': 'place and address resolution', 'provider': 'local build from selected OSM source', 'licence': 'inherits source-data obligations', 'status': 'derived', 'provenance_fields': ['OSM source', 'Nominatim version', 'import style', 'build time'], 'known_limits': ['reverse geocoding selects nearest suitable indexed object']},
    {'id': 'AWG-DATA-004', 'name': 'PMTiles vector-tile archive', 'role': 'offline presentation projection', 'provider': 'local tile build or licensed provider', 'licence': 'source and style specific', 'status': 'derived', 'provenance_fields': ['source datasets', 'tile schema', 'style version', 'zoom range', 'checksum'], 'known_limits': ['generalized for display; not authoritative topology']},
    {'id': 'AWG-DATA-005', 'name': 'Routing graph or tiles', 'role': 'walking, cycling, driving, and multimodal routing', 'provider': 'local Valhalla or selected adapter build', 'licence': 'source-data and engine specific', 'status': 'derived', 'provenance_fields': ['OSM source', 'engine version', 'costing profile', 'build time', 'checksum'], 'known_limits': ['route quality follows source access tags and profile assumptions']},
    {'id': 'AWG-DATA-006', 'name': 'GTFS transit feed', 'role': 'optional public-transport schedules and stops', 'provider': 'scenario-selected transport authority', 'licence': 'provider specific', 'status': 'optional', 'provenance_fields': ['feed URL', 'publisher', 'validity period', 'retrieval time', 'checksum'], 'known_limits': ['planned schedules may differ from operations']},
    {'id': 'AWG-DATA-007', 'name': 'Population and census distributions', 'role': 'optional population synthesis and calibration', 'provider': 'scenario-selected official or licensed source', 'licence': 'source specific', 'status': 'optional_sensitive', 'provenance_fields': ['publisher', 'table IDs', 'time period', 'geographic level', 'transformations'], 'known_limits': ['aggregation, suppression, sampling error, outdated values']},
    {'id': 'AWG-DATA-008', 'name': 'Time-use and mobility observations', 'role': 'optional activity and travel calibration', 'provider': 'scenario-selected research or official source', 'licence': 'source specific', 'status': 'optional_sensitive', 'provenance_fields': ['study', 'population', 'sampling', 'period', 'variables', 'licence'], 'known_limits': ['selection bias and context mismatch']},
    {'id': 'AWG-DATA-009', 'name': 'Building interior geometry', 'role': 'optional floor, room, entrance, and local navigation detail', 'provider': 'scenario author, BIM, indoor mapping, or synthetic generator', 'licence': 'source specific', 'status': 'optional_restricted', 'provenance_fields': ['source', 'coordinate reference', 'version', 'author', 'confidence'], 'known_limits': ['security sensitivity and frequent incompleteness']},
    {'id': 'AWG-DATA-010', 'name': 'Weather and environmental inputs', 'role': 'optional scenario conditions', 'provider': 'local dataset, synthetic generator, or approved adapter', 'licence': 'source specific', 'status': 'optional', 'provenance_fields': ['provider', 'station or model', 'time coverage', 'units', 'retrieval time'], 'known_limits': ['forecast and measurement uncertainty']},
]
write('registers/data-sources.yaml', yaml.safe_dump({'version': VERSION, 'data_sources': data_sources}, sort_keys=False, allow_unicode=True))

components = [
    ('PostgreSQL', 'database', 'PostgreSQL Licence', 'candidate'),
    ('PostGIS', 'spatial database extension', 'GPL-2.0-or-later reported; verify exact release', 'candidate'),
    ('osm2pgsql', 'OSM ingestion', 'GPL-2.0-or-later reported; verify exact release', 'candidate'),
    ('Nominatim', 'gazetteer', 'GPL-2.0-or-later reported; verify exact release', 'candidate'),
    ('Protomaps PMTiles', 'offline tile archive', 'verify repository and package licence before adoption', 'candidate'),
    ('MapLibre GL JS', 'map rendering', 'BSD-style reported; verify exact release', 'candidate'),
    ('Valhalla', 'routing', 'MIT reported; verify exact release', 'candidate'),
    ('SUMO', 'microscopic traffic simulation', 'EPL-2.0 reported; verify exact release', 'candidate'),
    ('Recast Navigation and Detour', 'navmesh and local pathfinding', 'zlib reported; verify exact release', 'candidate'),
    ('MATSim', 'activity and mobility simulation patterns', 'verify current distribution licence and module terms', 'pattern_or_candidate'),
    ('Ollama', 'local model runtime adapter', 'MIT reported; verify exact release and model licences separately', 'candidate'),
    ('OpenRouter', 'remote model routing service', 'service terms and model-specific terms; not treated as an open-source dependency', 'service_candidate'),
    ('Concordia', 'generative social simulation patterns', 'Apache-2.0 reported; verify dependencies', 'pattern_or_candidate'),
    ('AgentSociety', 'distributed experiment and agent simulation patterns', 'Apache-2.0 reported with repository-specific exceptions; verify folders', 'pattern_or_candidate'),
    ('OASIS', 'social-platform simulation patterns', 'Apache-2.0 reported; verify datasets and dependencies', 'pattern_or_candidate'),
    ('AgentTorch', 'large-population and archetype patterns', 'licence requires verification before code reuse', 'pattern_only_until_verified'),
    ('CityBehavEx', 'urban behaviour validation patterns', 'AGPL-3.0 reported; legal review required before code reuse', 'pattern_only'),
    ('DuckDB', 'analytical query engine', 'MIT reported; verify exact release', 'candidate'),
    ('Ray', 'distributed task execution', 'Apache-2.0 reported; verify exact release', 'candidate'),
    ('OpenTelemetry', 'software telemetry', 'Apache-2.0 reported; verify exact release', 'candidate'),
    ('PettingZoo', 'multi-agent environment interface patterns', 'MIT reported; verify exact release', 'pattern_or_candidate'),
]
write('registers/open-source-components.yaml', yaml.safe_dump({'version': VERSION, 'components': [
    {'id': f'AWG-COMP-{i:03d}', 'name': name, 'role': role, 'declared_or_reported_licence': licence,
     'adoption_status': status, 'code_reuse_approved': False, 'legal_review_required': True,
     'security_review_required': True, 'notes': 'Architecture discussion does not grant redistribution rights.'}
    for i, (name, role, licence, status) in enumerate(components, 1)
]}, sort_keys=False, allow_unicode=True))

models_prompts = [
    {'id': 'AWG-AI-001', 'provider': 'Ollama', 'deployment': 'local/offline', 'roles': ['dialogue realization', 'bounded option ranking', 'memory summarization', 'claim extraction'], 'model_version': 'assigned per run', 'prompt_policy_version': 'assigned per run', 'fallback': 'deterministic policy or no-op according to capability contract', 'status': 'adapter_required'},
    {'id': 'AWG-AI-002', 'provider': 'OpenRouter', 'deployment': 'remote/hybrid', 'roles': ['optional specialist reasoning and dialogue'], 'model_version': 'assigned per run', 'prompt_policy_version': 'assigned per run', 'fallback': 'local provider or deterministic policy according to scenario configuration', 'status': 'adapter_optional'},
    {'id': 'AWG-AI-003', 'provider': 'Provider-neutral structured-output contract', 'deployment': 'core boundary', 'roles': ['intent proposal', 'option ranking', 'dialogue realization', 'claim extraction', 'summarization'], 'model_version': 'not applicable', 'prompt_policy_version': 'versioned schema and policy', 'fallback': 'reject invalid output and preserve state', 'status': 'required'},
]
write('registers/models-and-prompts.yaml', yaml.safe_dump({'version': VERSION, 'records': models_prompts}, sort_keys=False, allow_unicode=True))

# Evidence register.
evidence_entries = [
    ('AWG-EV-001', 'Generative Agents: Interactive Simulacra of Human Behavior', 'paper', 'https://arxiv.org/abs/2304.03442', 'Memory, reflection, planning, and believable social interaction; not physical or predictive validation.'),
    ('AWG-EV-002', 'Generative Agent Simulations of 1,000 People', 'paper', 'https://arxiv.org/abs/2411.10109', 'Interview grounding and comparison against human retest; limited scope for prediction.'),
    ('AWG-EV-003', 'SOTOPIA', 'paper', 'https://arxiv.org/abs/2310.11667', 'Benchmarking difficult social interactions and human-model gaps.'),
    ('AWG-EV-004', '360CityArena', 'paper', 'https://arxiv.org/abs/2608.08814', 'Evidence that language models should not own authoritative urban navigation.'),
    ('AWG-EV-005', 'Concordia', 'repository and paper', 'https://github.com/google-deepmind/concordia', 'Component composition and grounded game-master pattern; deterministic resolver still required.'),
    ('AWG-EV-006', 'AgentSociety', 'repository and papers', 'https://github.com/tsinghua-fib-lab/AgentSociety', 'Experiment orchestration, replay, distributed tasks, and urban modules.'),
    ('AWG-EV-007', 'OASIS', 'repository and paper', 'https://github.com/camel-ai/oasis', 'Typed social actions, feeds, recommendations, and scale/cost lessons.'),
    ('AWG-EV-008', 'AgentTorch and Large Population Models', 'repository and paper', 'https://github.com/agenttorch/agenttorch', 'Archetypes, batching, calibration, and lower-fidelity population policies.'),
    ('AWG-EV-009', 'CityBehavEx', 'repository and paper', 'https://github.com/gefgu/citybehavex', 'LLM-assisted rather than LLM-only urban behaviour with empirical validation emphasis.'),
    ('AWG-EV-010', 'MATSim', 'simulation platform and book', 'https://matsim.org/', 'Plans, activities, legs, scoring, replanning, and event-driven mobility.'),
    ('AWG-EV-011', 'Three States and a Plan: The AI of F.E.A.R.', 'game AI presentation', 'https://www.gdcvault.com/play/1013459/Three-States-and-a-Plan', 'GOAP preconditions, effects, costs, and separate action execution.'),
    ('AWG-EV-012', 'Unreal Engine AI systems', 'official documentation', 'https://dev.epicgames.com/documentation/en-us/unreal-engine/artificial-intelligence-in-unreal-engine', 'Perception, blackboards, behaviour trees, StateTree, EQS, smart objects, MassEntity, and debugging.'),
    ('AWG-EV-013', 'Concurrent Interactions in The Sims 4', 'game AI presentation', 'https://www.gdcvault.com/play/1020190/Concurrent-Interactions-in-The-Sims', 'Data-defined interactions, compatibility, action channels, and concurrency.'),
    ('AWG-EV-014', 'Valve publications and Left 4 Dead AI', 'game AI publications', 'https://www.valvesoftware.com/en/publications', 'Scenario direction, contextual dialogue, and replayable systems.'),
    ('AWG-EV-015', 'A Context-Aware Character Dialog System in The Last of Us', 'game AI presentation', 'https://www.gdcvault.com/play/1020951/A-Context-Aware-Character-Dialog', 'Dialogue eligibility grounded in individual and shared knowledge state.'),
    ('AWG-EV-016', 'OpenStreetMap', 'data project', 'https://www.openstreetmap.org/', 'Base geography and topology with variable coverage and ODbL obligations.'),
    ('AWG-EV-017', 'osm2pgsql', 'official documentation', 'https://osm2pgsql.org/doc/manual.html', 'Controlled OSM ingestion and transformation.'),
    ('AWG-EV-018', 'PostGIS', 'official project', 'https://postgis.net/', 'Authoritative spatial types, queries, and indexes.'),
    ('AWG-EV-019', 'Nominatim', 'official documentation', 'https://nominatim.org/', 'Gazetteer semantics and reverse-geocoding limitations.'),
    ('AWG-EV-020', 'Protomaps and PMTiles', 'official documentation', 'https://docs.protomaps.com/', 'Offline tile packaging and presentation, not authoritative topology.'),
    ('AWG-EV-021', 'Valhalla', 'official documentation', 'https://valhalla.github.io/valhalla/', 'Hierarchical routing, costing, map matching, and multimodal travel.'),
    ('AWG-EV-022', 'SUMO', 'official documentation', 'https://sumo.dlr.de/docs/', 'Microscopic traffic and transport simulation.'),
    ('AWG-EV-023', 'Recast Navigation', 'official repository', 'https://github.com/recastnavigation/recastnavigation', 'Navmesh generation, pathfinding, and crowd support.'),
    ('AWG-EV-024', 'W3C PROV-O', 'standard', 'https://www.w3.org/TR/prov-o/', 'Vocabulary for agents, entities, activities, derivation, and attribution.'),
    ('AWG-EV-025', 'ActivityStreams 2.0', 'standard', 'https://www.w3.org/TR/activitystreams-core/', 'Actor-activity-object structures for social actions.'),
    ('AWG-EV-026', 'ODD protocol', 'model documentation protocol', 'https://www.usgs.gov/publications/odd-protocol-describing-agent-based-and-other-simulation-models-a-second-update', 'Reproducible description of agent-based models.'),
]
write('registers/evidence.yaml', yaml.safe_dump({'version': VERSION, 'evidence': [
    {'id': eid, 'title': title, 'source_type': typ, 'url': url, 'relevance': rel,
     'retrieved': TODAY, 'quality': 'primary_or_official_where_available', 'limitations': 'See research specification for detailed interpretation.'}
    for eid, title, typ, url, rel in evidence_entries
]}, sort_keys=False, allow_unicode=True))

# Linear mapping retained as execution metadata.
linear_mapping = {
    'project': {'name': 'AWG — Agentic World Graph', 'url': 'https://linear.app/elenta/project/awg-agentic-world-graph-4dda61e419dd', 'team_prefix': 'ELE'},
    'milestones': [
        'AWG 1 — Foundation & Governance', 'AWG 2 — Domain Model', 'AWG 3 — Platform Architecture',
        'AWG 4 — Scenarios & Validation', 'AWG 5 — UI/UX & World Explorer',
        'AWG 6 — Delivery & Operations', 'AWG 7 — Executable Contracts'
    ],
    'issues': {
        'ELE-136': 'AWG-GOV-001', 'ELE-137': 'AWG-DOM-001', 'ELE-138': 'AWG-DOM-002',
        'ELE-139': 'AWG-DOM-003', 'ELE-140': 'AWG-DOM-004', 'ELE-141': 'AWG-PLAT-002',
        'ELE-142': 'AWG-PLAT-003', 'ELE-143': 'AWG-PLAT-005', 'ELE-144': 'AWG-SCN-001',
        'ELE-145': 'AWG-SCN-002', 'ELE-146': 'AWG-UX-001', 'ELE-147': 'AWG-OPS-001',
        'ELE-148': 'AWG-OPS-009'
    },
    'source_of_truth': 'This repository; Linear tracks execution and review only.'
}
write('registers/linear-mapping.yaml', yaml.safe_dump(linear_mapping, sort_keys=False, allow_unicode=True))

print('Created root documentation and canonical registers.')

# Machine-readable contracts.
def write_json(path: str, obj: Any) -> None:
    write(path, json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

SCHEMA = 'https://json-schema.org/draft/2020-12/schema'
BASE = 'https://awg.local/contracts'

common_schema = {
    '$schema': SCHEMA,
    '$id': f'{BASE}/common/common.schema.json',
    'title': 'AWG Common Definitions',
    '$defs': {
        'identifier': {'type': 'string', 'minLength': 3, 'maxLength': 160, 'pattern': r'^[A-Za-z][A-Za-z0-9._:-]+$'},
        'version': {'type': 'string', 'pattern': r'^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$'},
        'simulationTime': {'type': 'string', 'format': 'date-time'},
        'locationRef': {
            'type': 'object',
            'properties': {
                'place_id': {'$ref': '#/$defs/identifier'},
                'geometry_id': {'$ref': '#/$defs/identifier'},
                'building_id': {'$ref': '#/$defs/identifier'},
                'floor_id': {'$ref': '#/$defs/identifier'},
                'room_id': {'$ref': '#/$defs/identifier'},
                'coordinates': {
                    'type': 'object',
                    'properties': {'longitude': {'type': 'number', 'minimum': -180, 'maximum': 180},
                                   'latitude': {'type': 'number', 'minimum': -90, 'maximum': 90}},
                    'required': ['longitude', 'latitude'], 'additionalProperties': False
                },
                'precision': {'enum': ['exact', 'estimated', 'room', 'floor', 'building', 'place', 'aggregate']}
            },
            'minProperties': 1,
            'additionalProperties': False
        },
        'provenanceRef': {
            'type': 'object',
            'properties': {
                'source_id': {'$ref': '#/$defs/identifier'},
                'source_type': {'enum': ['observed', 'imported', 'derived', 'sampled', 'generated', 'inferred', 'scenario_assumption']},
                'version': {'type': 'string'},
                'checksum': {'type': 'string'},
                'recorded_at': {'type': 'string', 'format': 'date-time'}
            },
            'required': ['source_id', 'source_type'],
            'additionalProperties': False
        },
        'modelProvenance': {
            'type': 'object',
            'properties': {
                'provider': {'type': 'string'}, 'model': {'type': 'string'}, 'model_version': {'type': 'string'},
                'prompt_policy_version': {'type': 'string'}, 'adapter_version': {'type': 'string'},
                'temperature': {'type': 'number'}, 'seed': {'type': ['integer', 'null']},
                'input_digest': {'type': 'string'}, 'output_digest': {'type': 'string'},
                'recorded_output_ref': {'type': 'string'}
            },
            'required': ['provider', 'model', 'prompt_policy_version', 'adapter_version'],
            'additionalProperties': False
        }
    }
}
write_json('contracts/common/common.schema.json', common_schema)

base_command = {
    '$schema': SCHEMA, '$id': f'{BASE}/commands/base-command.schema.json', 'title': 'Base Command',
    'type': 'object',
    'properties': {
        'schema_version': {'$ref': f'{BASE}/common/common.schema.json#/$defs/version'},
        'command_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'command_type': {'type': 'string'},
        'world_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'scenario_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'branch_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'actor_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'issued_by': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'requested_simulation_time': {'$ref': f'{BASE}/common/common.schema.json#/$defs/simulationTime'},
        'correlation_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'reason': {'type': 'string', 'maxLength': 2000}
    },
    'required': ['schema_version', 'command_id', 'command_type', 'world_id', 'scenario_id', 'branch_id', 'issued_by', 'requested_simulation_time']
}
write_json('contracts/commands/base-command.schema.json', base_command)

travel_cmd = {
    '$schema': SCHEMA, '$id': f'{BASE}/commands/travel-to-place.command.schema.json', 'title': 'Travel To Place Command',
    'allOf': [
        {'$ref': f'{BASE}/commands/base-command.schema.json'},
        {'type': 'object',
         'properties': {
             'command_type': {'const': 'TravelToPlace'},
             'actor_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'origin': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
             'destination': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
             'transport_mode': {'enum': ['walk', 'wheelchair', 'bicycle', 'car', 'taxi', 'bus', 'tram', 'rail', 'ferry', 'air', 'custom']},
             'depart_not_before': {'$ref': f'{BASE}/common/common.schema.json#/$defs/simulationTime'},
             'route_constraints': {'type': 'object', 'additionalProperties': True}
         },
         'required': ['command_type', 'actor_id', 'origin', 'destination', 'transport_mode']}
    ],
    'unevaluatedProperties': False
}
write_json('contracts/commands/travel-to-place.command.schema.json', travel_cmd)

send_message = {
    '$schema': SCHEMA, '$id': f'{BASE}/commands/send-message.command.schema.json', 'title': 'Send Message Command',
    'allOf': [
        {'$ref': f'{BASE}/commands/base-command.schema.json'},
        {'type': 'object',
         'properties': {
             'command_type': {'const': 'SendMessage'},
             'actor_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'channel_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'recipient_ids': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'}},
             'content': {'type': 'string', 'minLength': 1, 'maxLength': 10000},
             'claim_refs': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'}},
             'visibility': {'enum': ['private', 'group', 'organization', 'public']}
         },
         'required': ['command_type', 'actor_id', 'channel_id', 'recipient_ids', 'content', 'visibility']}
    ],
    'unevaluatedProperties': False
}
write_json('contracts/commands/send-message.command.schema.json', send_message)

create_post = {
    '$schema': SCHEMA, '$id': f'{BASE}/commands/create-social-post.command.schema.json', 'title': 'Create Social Post Command',
    'allOf': [
        {'$ref': f'{BASE}/commands/base-command.schema.json'},
        {'type': 'object',
         'properties': {
             'command_type': {'const': 'CreateSocialPost'},
             'actor_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'platform_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'account_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
             'content': {'type': 'string', 'minLength': 1, 'maxLength': 20000},
             'claim_refs': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'}},
             'audience': {'type': 'object', 'properties': {'visibility': {'enum': ['private', 'followers', 'group', 'public']}, 'group_ids': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['visibility'], 'additionalProperties': False}
         },
         'required': ['command_type', 'actor_id', 'platform_id', 'account_id', 'content', 'audience']}
    ],
    'unevaluatedProperties': False
}
write_json('contracts/commands/create-social-post.command.schema.json', create_post)

base_event = {
    '$schema': SCHEMA, '$id': f'{BASE}/events/domain-event.schema.json', 'title': 'Domain Event',
    'type': 'object',
    'properties': {
        'schema_version': {'$ref': f'{BASE}/common/common.schema.json#/$defs/version'},
        'event_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'event_type': {'type': 'string'},
        'world_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'scenario_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'branch_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'simulation_time': {'$ref': f'{BASE}/common/common.schema.json#/$defs/simulationTime'},
        'sequence': {'type': 'integer', 'minimum': 0},
        'recorded_at': {'type': 'string', 'format': 'date-time'},
        'actor_id': {'type': ['string', 'null']},
        'target_ids': {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True},
        'command_id': {'type': ['string', 'null']},
        'parent_event_ids': {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True},
        'caused_by_event_ids': {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True},
        'location': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
        'payload': {'type': 'object'},
        'plugin': {'type': 'object', 'properties': {'plugin_id': {'type': 'string'}, 'version': {'type': 'string'}}, 'required': ['plugin_id', 'version'], 'additionalProperties': False},
        'model_provenance': {'$ref': f'{BASE}/common/common.schema.json#/$defs/modelProvenance'}
    },
    'required': ['schema_version', 'event_id', 'event_type', 'world_id', 'scenario_id', 'branch_id', 'simulation_time', 'sequence', 'recorded_at', 'payload'],
    'additionalProperties': False
}
write_json('contracts/events/domain-event.schema.json', base_event)

journey_started = {
    '$schema': SCHEMA, '$id': f'{BASE}/events/journey-started.event.schema.json', 'title': 'Journey Started Event',
    'allOf': [
        {'$ref': f'{BASE}/events/domain-event.schema.json'},
        {'type': 'object', 'properties': {
            'event_type': {'const': 'JourneyStarted'},
            'payload': {'type': 'object', 'properties': {
                'journey_id': {'type': 'string'},
                'origin': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
                'destination': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
                'transport_mode': {'type': 'string'},
                'route_id': {'type': 'string'},
                'expected_arrival': {'type': 'string', 'format': 'date-time'}
            }, 'required': ['journey_id', 'origin', 'destination', 'transport_mode', 'route_id', 'expected_arrival'], 'additionalProperties': False}
        }, 'required': ['event_type', 'payload']}
    ]
}
write_json('contracts/events/journey-started.event.schema.json', journey_started)

agent_observed = {
    '$schema': SCHEMA, '$id': f'{BASE}/events/agent-observed.event.schema.json', 'title': 'Agent Observed Event',
    'allOf': [
        {'$ref': f'{BASE}/events/domain-event.schema.json'},
        {'type': 'object', 'properties': {
            'event_type': {'const': 'AgentObserved'},
            'payload': {'type': 'object', 'properties': {
                'observer_id': {'type': 'string'}, 'observed_event_id': {'type': 'string'},
                'observation_id': {'type': 'string'}, 'channel': {'enum': ['vision', 'hearing', 'device', 'message', 'media', 'record', 'institutional']},
                'fidelity': {'type': 'number', 'minimum': 0, 'maximum': 1},
                'uncertainty': {'type': 'number', 'minimum': 0, 'maximum': 1},
                'content': {'type': 'object'}
            }, 'required': ['observer_id', 'observed_event_id', 'observation_id', 'channel', 'fidelity', 'uncertainty', 'content'], 'additionalProperties': False}
        }, 'required': ['event_type', 'payload']}
    ]
}
write_json('contracts/events/agent-observed.event.schema.json', agent_observed)

claim_shared_event = {
    '$schema': SCHEMA, '$id': f'{BASE}/events/claim-shared.event.schema.json', 'title': 'Claim Shared Event',
    'allOf': [
        {'$ref': f'{BASE}/events/domain-event.schema.json'},
        {'type': 'object', 'properties': {
            'event_type': {'const': 'ClaimShared'},
            'payload': {'type': 'object', 'properties': {
                'claim_id': {'type': 'string'}, 'source_agent_id': {'type': 'string'},
                'recipient_ids': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}},
                'channel_id': {'type': 'string'}, 'message_id': {'type': 'string'},
                'parent_transmission_event_id': {'type': ['string', 'null']}
            }, 'required': ['claim_id', 'source_agent_id', 'recipient_ids', 'channel_id', 'message_id'], 'additionalProperties': False}
        }, 'required': ['event_type', 'payload']}
    ]
}
write_json('contracts/events/claim-shared.event.schema.json', claim_shared_event)

belief_updated_event = {
    '$schema': SCHEMA, '$id': f'{BASE}/events/belief-updated.event.schema.json', 'title': 'Belief Updated Event',
    'allOf': [
        {'$ref': f'{BASE}/events/domain-event.schema.json'},
        {'type': 'object', 'properties': {
            'event_type': {'const': 'BeliefUpdated'},
            'payload': {'type': 'object', 'properties': {
                'belief_id': {'type': 'string'}, 'agent_id': {'type': 'string'}, 'claim_id': {'type': 'string'},
                'previous_disposition': {'type': ['string', 'null']},
                'new_disposition': {'enum': ['unknown', 'considering', 'believed', 'disbelieved', 'uncertain', 'suspended']},
                'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1},
                'evidence_refs': {'type': 'array', 'items': {'type': 'string'}},
                'reason_code': {'type': 'string'}
            }, 'required': ['belief_id', 'agent_id', 'claim_id', 'new_disposition', 'confidence', 'evidence_refs', 'reason_code'], 'additionalProperties': False}
        }, 'required': ['event_type', 'payload']}
    ]
}
write_json('contracts/events/belief-updated.event.schema.json', belief_updated_event)

agent_profile = {
    '$schema': SCHEMA, '$id': f'{BASE}/agents/agent-profile.schema.json', 'title': 'Agent Profile',
    'type': 'object',
    'properties': {
        'schema_version': {'$ref': f'{BASE}/common/common.schema.json#/$defs/version'},
        'agent_id': {'$ref': f'{BASE}/common/common.schema.json#/$defs/identifier'},
        'identity': {'type': 'object', 'properties': {'display_name': {'type': 'string'}, 'synthetic': {'type': 'boolean'}, 'provenance': {'type': 'array', 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/provenanceRef'}}}, 'required': ['display_name', 'synthetic', 'provenance'], 'additionalProperties': True},
        'home': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
        'roles': {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True},
        'capabilities': {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True},
        'simulation_fidelity': {'enum': ['S1_cohort', 'S2_scheduled', 'S3_cognitive', 'S4_embodied']},
        'policy': {'type': 'object', 'properties': {'routine_policy': {'type': 'string'}, 'planner': {'type': 'string'}, 'llm_policy': {'type': ['string', 'null']}}, 'required': ['routine_policy', 'planner'], 'additionalProperties': False},
        'initial_state': {'type': 'object'}
    },
    'required': ['schema_version', 'agent_id', 'identity', 'roles', 'capabilities', 'simulation_fidelity', 'policy', 'initial_state'],
    'additionalProperties': False
}
write_json('contracts/agents/agent-profile.schema.json', agent_profile)

place_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/world-entities/place.schema.json', 'title': 'Place',
    'type': 'object',
    'properties': {
        'schema_version': {'$ref': f'{BASE}/common/common.schema.json#/$defs/version'},
        'place_id': {'type': 'string'}, 'place_type': {'type': 'string'},
        'names': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'properties': {'value': {'type': 'string'}, 'language': {'type': ['string', 'null']}, 'primary': {'type': 'boolean'}}, 'required': ['value', 'primary'], 'additionalProperties': False}},
        'geometry_refs': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}},
        'parent_place_ids': {'type': 'array', 'items': {'type': 'string'}},
        'access_rules': {'type': 'array', 'items': {'type': 'object'}},
        'provenance': {'type': 'array', 'minItems': 1, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/provenanceRef'}}
    },
    'required': ['schema_version', 'place_id', 'place_type', 'names', 'geometry_refs', 'provenance'],
    'additionalProperties': False
}
write_json('contracts/world-entities/place.schema.json', place_schema)

building_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/world-entities/building.schema.json', 'title': 'Building',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'building_id': {'type': 'string'}, 'place_id': {'type': 'string'},
        'footprint_geometry_id': {'type': 'string'},
        'entrances': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'properties': {'entrance_id': {'type': 'string'}, 'location': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'}, 'accessibility': {'type': 'array', 'items': {'type': 'string'}}, 'access_rules': {'type': 'array', 'items': {'type': 'object'}}}, 'required': ['entrance_id', 'location'], 'additionalProperties': False}},
        'floors': {'type': 'array', 'items': {'type': 'object', 'properties': {'floor_id': {'type': 'string'}, 'level': {'type': 'number'}, 'room_ids': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['floor_id', 'level', 'room_ids'], 'additionalProperties': False}},
        'occupancy_zones': {'type': 'array', 'items': {'type': 'object', 'properties': {'zone_id': {'type': 'string'}, 'capacity': {'type': ['integer', 'null'], 'minimum': 0}}, 'required': ['zone_id', 'capacity'], 'additionalProperties': False}},
        'position_precision': {'enum': ['exact', 'estimated', 'building_only']},
        'provenance': {'type': 'array', 'minItems': 1, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/provenanceRef'}}
    },
    'required': ['schema_version', 'building_id', 'place_id', 'footprint_geometry_id', 'entrances', 'floors', 'occupancy_zones', 'position_precision', 'provenance'],
    'additionalProperties': False
}
write_json('contracts/world-entities/building.schema.json', building_schema)

claim_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/claims-and-provenance/claim.schema.json', 'title': 'Claim',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'claim_id': {'type': 'string'},
        'proposition': {'type': 'string', 'minLength': 1},
        'subject_refs': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}},
        'asserted_by': {'type': 'string'}, 'original_source': {'type': 'string'},
        'source_chain': {'type': 'array', 'items': {'type': 'string'}},
        'evidence_refs': {'type': 'array', 'items': {'type': 'string'}},
        'acquired_at': {'type': 'string', 'format': 'date-time'},
        'location_context': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
        'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1},
        'disputed': {'type': 'boolean'}, 'parent_claim_id': {'type': ['string', 'null']},
        'provenance': {'type': 'array', 'minItems': 1, 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/provenanceRef'}}
    },
    'required': ['schema_version', 'claim_id', 'proposition', 'subject_refs', 'asserted_by', 'original_source', 'source_chain', 'evidence_refs', 'acquired_at', 'confidence', 'disputed', 'provenance'],
    'additionalProperties': False
}
write_json('contracts/claims-and-provenance/claim.schema.json', claim_schema)

belief_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/claims-and-provenance/belief.schema.json', 'title': 'Belief',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'belief_id': {'type': 'string'}, 'agent_id': {'type': 'string'}, 'claim_id': {'type': 'string'},
        'disposition': {'enum': ['unknown', 'considering', 'believed', 'disbelieved', 'uncertain', 'suspended']},
        'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1},
        'source_trust': {'type': 'array', 'items': {'type': 'object', 'properties': {'source_id': {'type': 'string'}, 'domain': {'type': 'string'}, 'score': {'type': 'number', 'minimum': 0, 'maximum': 1}}, 'required': ['source_id', 'domain', 'score'], 'additionalProperties': False}},
        'evidence_refs': {'type': 'array', 'items': {'type': 'string'}},
        'contradiction_claim_ids': {'type': 'array', 'items': {'type': 'string'}},
        'updated_at': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['schema_version', 'belief_id', 'agent_id', 'claim_id', 'disposition', 'confidence', 'source_trust', 'evidence_refs', 'contradiction_claim_ids', 'updated_at'],
    'additionalProperties': False
}
write_json('contracts/claims-and-provenance/belief.schema.json', belief_schema)

social_action_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/social-platform/social-action.schema.json', 'title': 'Social Platform Action',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'action_id': {'type': 'string'}, 'actor_id': {'type': 'string'},
        'platform_id': {'type': 'string'}, 'account_id': {'type': 'string'},
        'action_type': {'enum': ['view', 'create_post', 'reply', 'comment', 'like', 'dislike', 'repost', 'quote_post', 'follow', 'unfollow', 'mute', 'block', 'report', 'direct_message', 'join_group', 'leave_group', 'fact_check_request']},
        'object_ref': {'type': ['string', 'null']}, 'target_refs': {'type': 'array', 'items': {'type': 'string'}},
        'content': {'type': ['string', 'null']}, 'claim_refs': {'type': 'array', 'items': {'type': 'string'}},
        'visibility': {'enum': ['private', 'group', 'followers', 'public']},
        'simulation_time': {'type': 'string', 'format': 'date-time'},
        'inferred_motive': {'type': ['string', 'null']}, 'motive_confidence': {'type': ['number', 'null'], 'minimum': 0, 'maximum': 1}
    },
    'required': ['schema_version', 'action_id', 'actor_id', 'platform_id', 'account_id', 'action_type', 'target_refs', 'claim_refs', 'visibility', 'simulation_time'],
    'additionalProperties': False
}
write_json('contracts/social-platform/social-action.schema.json', social_action_schema)

plugin_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/plugins/plugin-manifest.schema.json', 'title': 'Plugin Manifest',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'plugin_id': {'type': 'string'}, 'name': {'type': 'string'}, 'version': {'type': 'string'},
        'api_version': {'type': 'string'}, 'capabilities': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}, 'uniqueItems': True},
        'entrypoint': {'type': 'string'},
        'permissions': {'type': 'object', 'properties': {'network': {'enum': ['none', 'restricted', 'full']}, 'filesystem': {'enum': ['none', 'read', 'read_write']}, 'secrets': {'type': 'array', 'items': {'type': 'string'}}, 'world_commands': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['network', 'filesystem', 'secrets', 'world_commands'], 'additionalProperties': False},
        'offline_support': {'enum': ['required', 'supported', 'not_supported']},
        'determinism': {'enum': ['deterministic', 'seeded', 'record_and_replay', 'nondeterministic_external']},
        'configuration_schema': {'type': ['string', 'null']},
        'health_check': {'type': 'object'},
        'compatibility': {'type': 'object', 'properties': {'core_min': {'type': 'string'}, 'core_max_exclusive': {'type': ['string', 'null']}}, 'required': ['core_min'], 'additionalProperties': False},
        'licence_record_id': {'type': 'string'}
    },
    'required': ['schema_version', 'plugin_id', 'name', 'version', 'api_version', 'capabilities', 'entrypoint', 'permissions', 'offline_support', 'determinism', 'health_check', 'compatibility', 'licence_record_id'],
    'additionalProperties': False
}
write_json('contracts/plugins/plugin-manifest.schema.json', plugin_schema)

scenario_schema = {
    '$schema': SCHEMA, '$id': f'{BASE}/scenarios/scenario-package.schema.json', 'title': 'Scenario Package',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'scenario_id': {'type': 'string'}, 'name': {'type': 'string'}, 'version': {'type': 'string'},
        'purpose': {'type': 'string'}, 'base_world': {'type': 'object'},
        'start_time': {'type': 'string', 'format': 'date-time'}, 'time_zone': {'type': 'string'},
        'geographic_extent': {'type': 'object'}, 'data_source_ids': {'type': 'array', 'items': {'type': 'string'}},
        'population': {'type': 'object'}, 'organizations': {'type': 'array', 'items': {'type': 'object'}},
        'plugins': {'type': 'array', 'items': {'type': 'object', 'properties': {'plugin_id': {'type': 'string'}, 'version': {'type': 'string'}, 'configuration_digest': {'type': 'string'}}, 'required': ['plugin_id', 'version', 'configuration_digest'], 'additionalProperties': False}},
        'models': {'type': 'array', 'items': {'type': 'object'}},
        'random_streams': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'properties': {'stream_id': {'type': 'string'}, 'owner': {'type': 'string'}, 'seed': {'type': 'integer'}}, 'required': ['stream_id', 'owner', 'seed'], 'additionalProperties': False}},
        'initial_conditions': {'type': 'array', 'items': {'type': 'object'}},
        'scheduled_events': {'type': 'array', 'items': {'type': 'object'}},
        'interventions': {'type': 'array', 'items': {'type': 'object', 'properties': {'intervention_id': {'type': 'string'}, 'time': {'type': 'string', 'format': 'date-time'}, 'type': {'type': 'string'}, 'target_refs': {'type': 'array', 'items': {'type': 'string'}}, 'parameters': {'type': 'object'}}, 'required': ['intervention_id', 'time', 'type', 'target_refs', 'parameters'], 'additionalProperties': False}},
        'measurements': {'type': 'array', 'items': {'type': 'string'}},
        'stop_conditions': {'type': 'array', 'minItems': 1, 'items': {'type': 'object'}},
        'assumption_ids': {'type': 'array', 'items': {'type': 'string'}}, 'risk_ids': {'type': 'array', 'items': {'type': 'string'}},
        'validation_profile': {'type': 'string'}, 'created_by': {'type': 'string'}, 'created_at': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['schema_version', 'scenario_id', 'name', 'version', 'purpose', 'base_world', 'start_time', 'time_zone', 'geographic_extent', 'data_source_ids', 'population', 'organizations', 'plugins', 'models', 'random_streams', 'initial_conditions', 'scheduled_events', 'interventions', 'measurements', 'stop_conditions', 'assumption_ids', 'risk_ids', 'validation_profile', 'created_by', 'created_at'],
    'additionalProperties': False
}
write_json('contracts/scenarios/scenario-package.schema.json', scenario_schema)

firehose_subscription = {
    '$schema': SCHEMA, '$id': f'{BASE}/firehose/subscription.schema.json', 'title': 'Firehose Subscription',
    'type': 'object',
    'properties': {
        'schema_version': {'type': 'string'}, 'subscription_id': {'type': 'string'},
        'world_ids': {'type': 'array', 'items': {'type': 'string'}}, 'branch_ids': {'type': 'array', 'items': {'type': 'string'}},
        'event_type_patterns': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}},
        'actor_ids': {'type': 'array', 'items': {'type': 'string'}}, 'place_ids': {'type': 'array', 'items': {'type': 'string'}},
        'cursor': {'type': ['string', 'null']},
        'delivery': {'enum': ['stream', 'batch', 'file']},
        'batch_size': {'type': 'integer', 'minimum': 1, 'maximum': 10000},
        'backpressure': {'enum': ['pause', 'spill_to_disk', 'disconnect_with_cursor']},
        'redaction_profile': {'type': 'string'}
    },
    'required': ['schema_version', 'subscription_id', 'event_type_patterns', 'delivery', 'batch_size', 'backpressure', 'redaction_profile'],
    'additionalProperties': False
}
write_json('contracts/firehose/subscription.schema.json', firehose_subscription)

schema_catalog = []
for p in sorted((ROOT / 'contracts').rglob('*.schema.json')):
    data = json.loads(p.read_text(encoding='utf-8'))
    schema_catalog.append({'path': p.relative_to(ROOT).as_posix(), 'id': data.get('$id'), 'title': data.get('title'), 'version': VERSION})
write('contracts/schema-catalog.yaml', yaml.safe_dump({'version': VERSION, 'schemas': schema_catalog}, sort_keys=False, allow_unicode=True))

write('contracts/README.md', clean('''
# Machine-Readable Contracts

These JSON Schemas are the executable boundary corresponding to the normative Markdown specifications. They are versioned, validated, and exercised by valid and invalid fixtures.

A schema validates structural admissibility. World-specific feasibility such as route reachability, ownership, capacity, elapsed time, knowledge access, or causal consistency remains the responsibility of deterministic validators and invariant tests.

Breaking schema changes require migration guidance and an ADR.
'''))

# Fixtures and walkthroughs.
fixtures: list[dict[str, Any]] = []
def fixture(path: str, schema_id: str, expected_valid: bool, data: Any, note: str) -> None:
    write_json(path, data)
    fixtures.append({'path': path, 'schema_id': schema_id, 'expected_valid': expected_valid, 'note': note})

base_cmd_fields = {
    'schema_version': '0.2.0', 'command_id': 'cmd:travel:001', 'command_type': 'TravelToPlace',
    'world_id': 'world:london-demo', 'scenario_id': 'scenario:bridge-closure', 'branch_id': 'branch:baseline',
    'actor_id': 'agent:a-10482', 'issued_by': 'agent:a-10482',
    'requested_simulation_time': '2042-05-04T08:10:00Z', 'correlation_id': 'corr:journey:001', 'reason': 'Travel to work'
}
fixture('examples/fixtures/commands/travel-to-place.valid.json', travel_cmd['$id'], True, {
    **base_cmd_fields,
    'origin': {'place_id': 'place:home-10482', 'building_id': 'building:home-10482', 'precision': 'building'},
    'destination': {'place_id': 'place:work-220', 'building_id': 'building:work-220', 'precision': 'building'},
    'transport_mode': 'bus', 'depart_not_before': '2042-05-04T08:10:00Z', 'route_constraints': {'accessible': True}
}, 'Valid typed travel intent; the kernel must still validate route, capacity, access, and elapsed time.')
fixture('examples/fixtures/commands/travel-to-place.invalid.json', travel_cmd['$id'], False, {
    **{k: v for k, v in base_cmd_fields.items() if k != 'actor_id'},
    'origin': {'place_id': 'place:home-10482'}, 'transport_mode': 'teleport'
}, 'Invalid because actor, destination, and permitted transport mode are absent or wrong.')

fixture('examples/fixtures/events/journey-started.valid.json', journey_started['$id'], True, {
    'schema_version': '0.2.0', 'event_id': 'event:journey-started:001', 'event_type': 'JourneyStarted',
    'world_id': 'world:london-demo', 'scenario_id': 'scenario:bridge-closure', 'branch_id': 'branch:baseline',
    'simulation_time': '2042-05-04T08:10:01Z', 'sequence': 1204, 'recorded_at': '2026-08-20T20:00:00Z',
    'actor_id': 'agent:a-10482', 'target_ids': ['place:work-220'], 'command_id': 'cmd:travel:001',
    'parent_event_ids': [], 'caused_by_event_ids': [],
    'location': {'place_id': 'place:home-10482', 'precision': 'building'},
    'payload': {'journey_id': 'journey:001', 'origin': {'place_id': 'place:home-10482'}, 'destination': {'place_id': 'place:work-220'}, 'transport_mode': 'bus', 'route_id': 'route:bus:55', 'expected_arrival': '2042-05-04T08:46:00Z'},
    'plugin': {'plugin_id': 'mobility:reference', 'version': '0.2.0'}
}, 'Valid journey start event.')

fixture('examples/fixtures/agents/agent-profile.valid.json', agent_profile['$id'], True, {
    'schema_version': '0.2.0', 'agent_id': 'agent:a-10482',
    'identity': {'display_name': 'A-10482', 'synthetic': True, 'provenance': [{'source_id': 'scenario:bridge-closure', 'source_type': 'generated', 'version': '0.2.0', 'recorded_at': '2042-05-04T00:00:00Z'}]},
    'home': {'place_id': 'place:home-10482', 'precision': 'building'}, 'roles': ['resident', 'employee'],
    'capabilities': ['walk', 'use_bus', 'speak', 'message', 'post'], 'simulation_fidelity': 'S3_cognitive',
    'policy': {'routine_policy': 'schedule-utility-v1', 'planner': 'goap-v1', 'llm_policy': 'bounded-dialogue-v1'},
    'initial_state': {'fatigue': 0.2, 'money': 42.0, 'current_place_id': 'place:home-10482'}
}, 'Valid synthetic cognitive agent profile with provenance.')

fixture('examples/fixtures/world/place.valid.json', place_schema['$id'], True, {
    'schema_version': '0.2.0', 'place_id': 'place:cafe-orion', 'place_type': 'cafe',
    'names': [{'value': 'Café Orion', 'language': 'en', 'primary': True}], 'geometry_refs': ['geom:cafe-orion'],
    'parent_place_ids': ['place:district-01'], 'access_rules': [{'rule': 'public_during_open_hours'}],
    'provenance': [{'source_id': 'osm:node:12345', 'source_type': 'imported', 'version': '2026-08-01', 'recorded_at': '2026-08-20T00:00:00Z'}]
}, 'Valid place identity distinct from geometry.')

fixture('examples/fixtures/world/building.valid.json', building_schema['$id'], True, {
    'schema_version': '0.2.0', 'building_id': 'building:cafe-orion', 'place_id': 'place:cafe-orion', 'footprint_geometry_id': 'geom:cafe-orion',
    'entrances': [{'entrance_id': 'entrance:cafe-orion:main', 'location': {'place_id': 'place:cafe-orion', 'geometry_id': 'geom:entrance-main', 'precision': 'exact'}, 'accessibility': ['step_free'], 'access_rules': []}],
    'floors': [{'floor_id': 'floor:cafe-orion:ground', 'level': 0, 'room_ids': ['room:cafe-orion:main']}],
    'occupancy_zones': [{'zone_id': 'room:cafe-orion:main', 'capacity': 42}], 'position_precision': 'exact',
    'provenance': [{'source_id': 'scenario:authoring:001', 'source_type': 'derived', 'version': '0.2.0', 'recorded_at': '2026-08-20T00:00:00Z'}]
}, 'Valid building with entrance, floor, room, capacity, and provenance.')

fixture('examples/fixtures/claims/claim.valid.json', claim_schema['$id'], True, {
    'schema_version': '0.2.0', 'claim_id': 'claim:transformer:001', 'proposition': 'A loud bang and smoke were observed near the substation.',
    'subject_refs': ['event:transformer-failure:001'], 'asserted_by': 'agent:a-0001', 'original_source': 'agent:a-0001',
    'source_chain': ['agent:a-0001'], 'evidence_refs': ['observation:0001'], 'acquired_at': '2042-05-04T14:30:04Z',
    'location_context': {'place_id': 'place:substation-01', 'precision': 'place'}, 'confidence': 0.78, 'disputed': False, 'parent_claim_id': None,
    'provenance': [{'source_id': 'observation:0001', 'source_type': 'observed', 'recorded_at': '2042-05-04T14:30:04Z'}]
}, 'Valid first-hand claim with lineage.')

fixture('examples/fixtures/claims/belief.valid.json', belief_schema['$id'], True, {
    'schema_version': '0.2.0', 'belief_id': 'belief:a-0099:claim-001', 'agent_id': 'agent:a-0099', 'claim_id': 'claim:transformer:001',
    'disposition': 'uncertain', 'confidence': 0.62,
    'source_trust': [{'source_id': 'agent:a-0001', 'domain': 'local_incident_observation', 'score': 0.75}],
    'evidence_refs': ['message:0042'], 'contradiction_claim_ids': [], 'updated_at': '2042-05-04T14:32:10Z'
}, 'Valid agent-specific belief distinct from world truth.')

fixture('examples/fixtures/social/social-action.valid.json', social_action_schema['$id'], True, {
    'schema_version': '0.2.0', 'action_id': 'social-action:repost:001', 'actor_id': 'agent:d-0004',
    'platform_id': 'platform:town-square', 'account_id': 'account:d-0004', 'action_type': 'repost',
    'object_ref': 'post:c-0003:001', 'target_refs': ['account:c-0003'], 'content': None,
    'claim_refs': ['claim:transformer:002'], 'visibility': 'public', 'simulation_time': '2042-05-04T14:32:18Z',
    'inferred_motive': None, 'motive_confidence': None
}, 'Valid repost action that does not assert belief or motive.')

fixture('examples/fixtures/plugins/ollama-adapter.valid.json', plugin_schema['$id'], True, {
    'schema_version': '0.2.0', 'plugin_id': 'ai-provider:ollama', 'name': 'Ollama AI Provider Adapter', 'version': '0.2.0',
    'api_version': '1.0.0', 'capabilities': ['structured_generation', 'dialogue_realization', 'summarization'], 'entrypoint': 'awg_plugins.ollama:Plugin',
    'permissions': {'network': 'restricted', 'filesystem': 'none', 'secrets': [], 'world_commands': []},
    'offline_support': 'required', 'determinism': 'record_and_replay', 'configuration_schema': 'contracts/plugins/ollama-config.schema.json',
    'health_check': {'type': 'model_list'}, 'compatibility': {'core_min': '0.2.0', 'core_max_exclusive': None}, 'licence_record_id': 'AWG-COMP-011'
}, 'Valid provider adapter with no direct world-command permissions.')

fixture('examples/fixtures/scenarios/bridge-closure.valid.json', scenario_schema['$id'], True, {
    'schema_version': '0.2.0', 'scenario_id': 'scenario:bridge-closure', 'name': 'Bridge closure and information diffusion', 'version': '0.2.0',
    'purpose': 'Test mobility replanning and information diffusion after a declared bridge closure.',
    'base_world': {'world_id': 'world:london-demo', 'world_version': '0.2.0'}, 'start_time': '2042-05-04T08:00:00Z', 'time_zone': 'Europe/London',
    'geographic_extent': {'place_id': 'place:district-01'}, 'data_source_ids': ['AWG-DATA-001', 'AWG-DATA-003', 'AWG-DATA-004', 'AWG-DATA-005'],
    'population': {'cohorts': 3, 'scheduled_agents': 5000, 'cognitive_agents': 25, 'embodied_agents_max': 200},
    'organizations': [{'organization_id': 'org:transport-authority'}],
    'plugins': [{'plugin_id': 'mobility:reference', 'version': '0.2.0', 'configuration_digest': 'sha256:demo'}, {'plugin_id': 'ai-provider:ollama', 'version': '0.2.0', 'configuration_digest': 'sha256:demo2'}],
    'models': [{'record_id': 'AWG-AI-001', 'model': 'scenario-assigned-local-model'}],
    'random_streams': [{'stream_id': 'random:mobility', 'owner': 'mobility', 'seed': 1001}, {'stream_id': 'random:information', 'owner': 'information', 'seed': 2001}],
    'initial_conditions': [{'type': 'bridge_state', 'bridge_id': 'bridge:001', 'open': True}],
    'scheduled_events': [],
    'interventions': [{'intervention_id': 'intervention:bridge-close', 'time': '2042-05-04T08:20:00Z', 'type': 'CloseInfrastructure', 'target_refs': ['bridge:001'], 'parameters': {'reason': 'structural_damage'}}],
    'measurements': ['metric:journey-delay', 'metric:claim-reach', 'metric:belief-change'], 'stop_conditions': [{'type': 'simulation_time', 'at': '2042-05-04T12:00:00Z'}],
    'assumption_ids': ['AWG-ASM-001', 'AWG-ASM-002'], 'risk_ids': ['AWG-RISK-002', 'AWG-RISK-003', 'AWG-RISK-014'],
    'validation_profile': 'validation:district-mobility-information-v1', 'created_by': 'user:scenario-author', 'created_at': '2026-08-20T20:00:00Z'
}, 'Valid bounded scenario with declared intervention and seeded random streams.')

fixture('examples/fixtures/firehose/subscription.valid.json', firehose_subscription['$id'], True, {
    'schema_version': '0.2.0', 'subscription_id': 'subscription:analyst:001', 'world_ids': ['world:london-demo'],
    'branch_ids': ['branch:baseline'], 'event_type_patterns': ['movement.*', 'claim.*', 'social.*'],
    'actor_ids': [], 'place_ids': ['place:district-01'], 'cursor': None, 'delivery': 'stream', 'batch_size': 250,
    'backpressure': 'spill_to_disk', 'redaction_profile': 'analyst-standard'
}, 'Valid filtered firehose subscription.')

write('examples/fixtures/index.yaml', yaml.safe_dump({'version': VERSION, 'fixtures': fixtures}, sort_keys=False, allow_unicode=True))

# Preserve and expand human-readable examples.
for p in sorted((SOURCE_ROOT / '08-examples').glob('*.md')):
    if p.name == 'README.md':
        continue
    target = ROOT / 'examples' / 'walkthroughs' / p.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, target)
write('examples/README.md', clean('''
# Examples and Fixtures

- `fixtures/` contains schema-valid and intentionally invalid machine-readable examples.
- `walkthroughs/` contains human-readable journeys, information cascades, building occupancy, social platforms, interventions, and replay examples.

Examples illustrate contracts; they do not override normative specifications.
'''))

# Templates.
templates = {
    'templates/architecture-decision-record-template.md': '''# ADR-NNNN: Decision title\n\n## Status\n\nProposed\n\n## Context and problem\n\n## Constraints\n\n## Options considered\n\n## Decision\n\n## Rationale\n\n## Positive consequences\n\n## Negative consequences\n\n## Risks and mitigations\n\n## Compatibility and migration\n\n## Requirements, tests, and documents affected\n\n## Reversal strategy\n''',
    'templates/scenario-template.md': '''# Scenario Template\n\n## Purpose and intended use\n## Base world and geographic extent\n## Start time and time zone\n## Data sources and provenance\n## Population and organizations\n## Plugins, models, and configuration digests\n## Random streams and seeds\n## Initial conditions\n## Scheduled events\n## Interventions\n## Measurements\n## Stop conditions\n## Assumptions and risks\n## Validation profile\n## Scenario card and limitations\n''',
    'templates/plugin-specification-template.md': '''# Plugin Specification Template\n\n## Capability and non-goals\n## Stable interface\n## Configuration schema\n## Permissions\n## Offline support\n## Determinism and replay\n## Errors, timeouts, retries, and fallback\n## Health checks\n## Security boundary\n## Compatibility and versioning\n## Contract tests\n## Licence and supply-chain record\n''',
    'templates/validation-report-template.md': '''# Validation Report Template\n\n## Scope\n## Model and software versions\n## Data and provenance\n## Verification results\n## Calibration results\n## Out-of-sample validation\n## Human comparison\n## Sensitivity and uncertainty\n## Failures and limitations\n## Use-specific conclusion\n## Evidence package and checksums\n''',
    'templates/data-source-entry-template.yaml': '''id: AWG-DATA-NNN\nname: \nrole: \nprovider: \nlicence: \nstatus: candidate\nprovenance_fields: []\nknown_limits: []\n''',
    'templates/risk-entry-template.yaml': '''id: AWG-RISK-NNN\ndescription: \nseverity: medium\nmitigation: \naffected_documents: []\nowner: \nstatus: open\nresidual_risk: \n''',
    'templates/research-evidence-entry-template.yaml': '''id: AWG-EV-NNN\ntitle: \nsource_type: \nurl: \nrelevance: \nretrieved: \nquality: \nlimitations: \n''',
    'templates/model-card-template.md': '''# Model Card Template\n\n## Provider and model identity\n## Version and quantization\n## Intended bounded roles\n## Prohibited roles\n## Input and output schemas\n## Prompt-policy version\n## Evaluation and failure modes\n## Bias and limitations\n## Offline and data-handling properties\n## Fallback and replay\n''',
    'templates/scenario-card-template.md': '''# Scenario Card Template\n\n## Purpose\n## Intended users and decisions\n## Geography and time\n## Population and data sources\n## Interventions\n## Validation and calibration\n## Uncertainty and sensitivity\n## Known limitations\n## Prohibited interpretations\n## Reproduction instructions\n''',
}
for path, content in templates.items():
    write(path, clean(content))

# Architecture decisions.
write('decisions/README.md', clean('''
# Architecture Decision Records

ADRs capture decisions that alter constitutional interpretation, canonical entities, event envelopes, storage authority, plugin contracts, compatibility, or major technology direction. Accepted ADRs are immutable; superseding decisions create new ADRs.
'''))
write('decisions/template.md', templates['templates/architecture-decision-record-template.md'])
write('decisions/ADR-0001-canonical-source-and-linear-separation.md', clean('''
# ADR-0001: Canonical repository and Linear separation

## Status

Accepted for the v0.2.0 baseline.

## Context

The project needs complete specifications and executable contracts without manually duplicating 74 documents into Linear.

## Decision

The disk or future Git repository is the canonical source of specifications, registers, schemas, examples, tests, and releases. Linear tracks milestones, ownership, review, dependencies, and delivery status.

## Consequences

Linear issues must link to canonical paths and document IDs. A Linear status cannot override failed repository validation. Generated ZIPs are immutable release projections.
'''))
write('decisions/ADR-0002-deterministic-kernel-authority.md', clean('''
# ADR-0002: Deterministic kernel authority

## Status

Accepted for the v0.2.0 baseline.

## Decision

AI models may propose bounded intentions, rankings, interpretations, summaries, and language. Only validated deterministic systems may create authoritative state transitions and domain events.

## Consequences

Model output is untrusted input. Direct model database writes and narrator-declared success are prohibited. Recorded model outputs may be replayed without inference.
'''))
write('decisions/ADR-0003-semantic-world-graph-over-multiple-stores.md', clean('''
# ADR-0003: Semantic world graph over fit-for-purpose stores

## Status

Accepted for the v0.2.0 baseline.

## Decision

The world graph is a semantic domain model and API, not a mandate to store every workload in one graph database.

## Consequences

Spatial truth may use PostGIS, events append-only storage, transactions relational tables, analytics columnar storage, relationships graph projections, and retrieval indexes. Authority and provenance remain explicit across stores.
'''))

# Archive all source material so no prior discussion artefact is lost.
archive_map = {
    '/mnt/data/agentic-world-graph-research.md': 'archive/conversation-derived/agentic-world-graph-research.md',
    '/mnt/data/agentic-world-graph-research-ui-ux.md': 'archive/conversation-derived/agentic-world-graph-research-ui-ux.md',
    '/mnt/data/agent-map-clustering-and-semantic-zoom.md': 'archive/conversation-derived/agent-map-clustering-and-semantic-zoom.md',
    '/mnt/data/agentic-world-graph-documentation-sense-check.md': 'archive/conversation-derived/agentic-world-graph-documentation-sense-check.md',
    '/mnt/data/agentic-world-graph-master-pack-v0.1.0.zip': 'archive/releases/agentic-world-graph-master-pack-v0.1.0.zip',
}
for s, d in archive_map.items():
    p = Path(s)
    if p.exists():
        target = ROOT / d
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
(ROOT / 'archive/build-scripts').mkdir(parents=True, exist_ok=True)
shutil.copy2(Path(__file__), ROOT / 'archive/build-scripts/initial-v0.2.0-generator.py')
write('archive/build-scripts/README.md', clean('''
# Historical Build Script

`initial-v0.2.0-generator.py` records how this baseline was assembled in the `/mnt/data` working environment. It contains environment-specific paths and destructive target-directory recreation logic. It is preserved for provenance only and MUST NOT be used as the normal contributor workflow. The repository's authored files, registers, validation scripts, and release tooling are the canonical ongoing source.
'''))

write('archive/README.md', clean('''
# Archive

This area preserves conversation-derived source documents and the v0.1.0 release for traceability. Archived files are informative historical inputs, not current normative authority.
'''))

print(f'Created {len(schema_catalog)} schemas and {len(fixtures)} indexed fixtures.')

# Additional core schemas close the remaining domain and run-record gaps.
additional_schemas = {
    'contracts/world-entities/world.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/world-entities/world.schema.json', 'title': 'World', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'world_id': {'type': 'string'}, 'name': {'type': 'string'}, 'world_version': {'type': 'string'},
                       'world_type': {'enum': ['real', 'historical', 'hypothetical', 'synthetic', 'hybrid']},
                       'coordinate_reference_system': {'type': 'string'}, 'root_place_ids': {'type': 'array', 'items': {'type': 'string'}},
                       'simulation_ruleset': {'type': 'string'}, 'data_source_ids': {'type': 'array', 'items': {'type': 'string'}},
                       'created_at': {'type': 'string', 'format': 'date-time'}},
        'required': ['schema_version', 'world_id', 'name', 'world_version', 'world_type', 'coordinate_reference_system', 'root_place_ids', 'simulation_ruleset', 'data_source_ids', 'created_at'],
        'additionalProperties': False
    },
    'contracts/world-entities/organization.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/world-entities/organization.schema.json', 'title': 'Organization', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'organization_id': {'type': 'string'}, 'organization_type': {'type': 'string'}, 'name': {'type': 'string'},
                       'member_ids': {'type': 'array', 'items': {'type': 'string'}}, 'leader_ids': {'type': 'array', 'items': {'type': 'string'}},
                       'asset_ids': {'type': 'array', 'items': {'type': 'string'}}, 'place_ids': {'type': 'array', 'items': {'type': 'string'}},
                       'policies': {'type': 'array', 'items': {'type': 'object'}}, 'goals': {'type': 'array', 'items': {'type': 'object'}},
                       'provenance': {'type': 'array', 'items': {'$ref': f'{BASE}/common/common.schema.json#/$defs/provenanceRef'}}},
        'required': ['schema_version', 'organization_id', 'organization_type', 'name', 'member_ids', 'leader_ids', 'asset_ids', 'place_ids', 'policies', 'goals', 'provenance'],
        'additionalProperties': False
    },
    'contracts/world-entities/smart-object.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/world-entities/smart-object.schema.json', 'title': 'Smart Object', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'object_id': {'type': 'string'}, 'object_type': {'type': 'string'},
                       'location': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'}, 'owner_id': {'type': ['string', 'null']},
                       'affordances': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'properties': {
                           'affordance_id': {'type': 'string'}, 'preconditions': {'type': 'array', 'items': {'type': 'object'}},
                           'effects': {'type': 'array', 'items': {'type': 'object'}}, 'duration_seconds': {'type': 'number', 'minimum': 0},
                           'capacity': {'type': 'integer', 'minimum': 1}, 'exclusive_slots': {'type': 'array', 'items': {'type': 'string'}},
                           'interruptible': {'type': 'boolean'}},
                           'required': ['affordance_id', 'preconditions', 'effects', 'duration_seconds', 'capacity', 'exclusive_slots', 'interruptible'], 'additionalProperties': False}},
                       'state': {'type': 'object'}},
        'required': ['schema_version', 'object_id', 'object_type', 'location', 'affordances', 'state'], 'additionalProperties': False
    },
    'contracts/world-entities/journey.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/world-entities/journey.schema.json', 'title': 'Journey', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'journey_id': {'type': 'string'}, 'actor_id': {'type': 'string'},
                       'state': {'enum': ['planned', 'scheduled', 'departed', 'in_progress', 'interrupted', 'rerouting', 'arrived', 'failed', 'cancelled']},
                       'origin': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'}, 'destination': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
                       'legs': {'type': 'array', 'minItems': 1, 'items': {'type': 'object'}}, 'departed_at': {'type': ['string', 'null'], 'format': 'date-time'},
                       'arrived_at': {'type': ['string', 'null'], 'format': 'date-time'}, 'current_location': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'},
                       'route_revision': {'type': 'integer', 'minimum': 0}},
        'required': ['schema_version', 'journey_id', 'actor_id', 'state', 'origin', 'destination', 'legs', 'route_revision'], 'additionalProperties': False
    },
    'contracts/agents/observation.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/agents/observation.schema.json', 'title': 'Observation', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'observation_id': {'type': 'string'}, 'observer_id': {'type': 'string'},
                       'source_event_id': {'type': ['string', 'null']}, 'channel': {'type': 'string'}, 'observed_at': {'type': 'string', 'format': 'date-time'},
                       'location': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'}, 'fidelity': {'type': 'number', 'minimum': 0, 'maximum': 1},
                       'uncertainty': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'content': {'type': 'object'},
                       'access_path': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}},
        'required': ['schema_version', 'observation_id', 'observer_id', 'channel', 'observed_at', 'fidelity', 'uncertainty', 'content', 'access_path'], 'additionalProperties': False
    },
    'contracts/agents/schedule.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/agents/schedule.schema.json', 'title': 'Agent Schedule', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'schedule_id': {'type': 'string'}, 'agent_id': {'type': 'string'},
                       'time_zone': {'type': 'string'}, 'activities': {'type': 'array', 'items': {'type': 'object', 'properties': {
                           'activity_id': {'type': 'string'}, 'activity_type': {'type': 'string'}, 'place_id': {'type': 'string'},
                           'earliest_start': {'type': 'string', 'format': 'date-time'}, 'latest_end': {'type': 'string', 'format': 'date-time'},
                           'duration_seconds': {'type': 'number', 'minimum': 0}, 'priority': {'type': 'number'}},
                           'required': ['activity_id', 'activity_type', 'place_id', 'earliest_start', 'latest_end', 'duration_seconds', 'priority'], 'additionalProperties': False}}},
        'required': ['schema_version', 'schedule_id', 'agent_id', 'time_zone', 'activities'], 'additionalProperties': False
    },
    'contracts/scenarios/intervention.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/scenarios/intervention.schema.json', 'title': 'Scenario Intervention', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'intervention_id': {'type': 'string'}, 'scenario_id': {'type': 'string'}, 'branch_id': {'type': 'string'},
                       'authority_id': {'type': 'string'}, 'effective_time': {'type': 'string', 'format': 'date-time'}, 'intervention_type': {'type': 'string'},
                       'target_refs': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}, 'parameters': {'type': 'object'},
                       'duration_seconds': {'type': ['number', 'null'], 'minimum': 0}, 'rollback': {'type': ['object', 'null']}, 'reason': {'type': 'string'}},
        'required': ['schema_version', 'intervention_id', 'scenario_id', 'branch_id', 'authority_id', 'effective_time', 'intervention_type', 'target_refs', 'parameters', 'reason'], 'additionalProperties': False
    },
    'contracts/scenarios/run-record.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/scenarios/run-record.schema.json', 'title': 'Run Record', 'type': 'object',
        'properties': {'schema_version': {'type': 'string'}, 'run_id': {'type': 'string'}, 'scenario_id': {'type': 'string'}, 'scenario_digest': {'type': 'string'},
                       'branch_id': {'type': 'string'}, 'core_version': {'type': 'string'}, 'configuration_digest': {'type': 'string'},
                       'data_source_versions': {'type': 'array', 'items': {'type': 'object'}}, 'plugin_versions': {'type': 'array', 'items': {'type': 'object'}},
                       'model_records': {'type': 'array', 'items': {'type': 'object'}}, 'random_streams': {'type': 'array', 'items': {'type': 'object'}},
                       'started_at': {'type': 'string', 'format': 'date-time'}, 'completed_at': {'type': ['string', 'null'], 'format': 'date-time'},
                       'final_event_sequence': {'type': ['integer', 'null'], 'minimum': 0}, 'snapshot_refs': {'type': 'array', 'items': {'type': 'string'}},
                       'event_archive_ref': {'type': ['string', 'null']}, 'environment': {'type': 'object'}},
        'required': ['schema_version', 'run_id', 'scenario_id', 'scenario_digest', 'branch_id', 'core_version', 'configuration_digest', 'data_source_versions', 'plugin_versions', 'model_records', 'random_streams', 'started_at', 'snapshot_refs', 'environment'], 'additionalProperties': False
    },
    'contracts/plugins/ollama-config.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/plugins/ollama-config.schema.json', 'title': 'Ollama Adapter Configuration', 'type': 'object',
        'properties': {'base_url': {'type': 'string'}, 'model': {'type': 'string'}, 'timeout_seconds': {'type': 'number', 'minimum': 0.1},
                       'structured_output': {'type': 'boolean'}, 'network_policy': {'enum': ['loopback_only', 'local_network']}},
        'required': ['base_url', 'model', 'timeout_seconds', 'structured_output', 'network_policy'], 'additionalProperties': False
    },
    'contracts/plugins/openrouter-config.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/plugins/openrouter-config.schema.json', 'title': 'OpenRouter Adapter Configuration', 'type': 'object',
        'properties': {'base_url': {'type': 'string'}, 'model': {'type': 'string'}, 'secret_ref': {'type': 'string'}, 'timeout_seconds': {'type': 'number', 'minimum': 0.1},
                       'data_policy': {'enum': ['scenario_approved_remote', 'prohibited_for_sensitive_data']}, 'fallback_provider_id': {'type': ['string', 'null']}},
        'required': ['base_url', 'model', 'secret_ref', 'timeout_seconds', 'data_policy'], 'additionalProperties': False
    },
    'contracts/events/command-rejected.event.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/events/command-rejected.event.schema.json', 'title': 'Command Rejected Event',
        'allOf': [{'$ref': f'{BASE}/events/domain-event.schema.json'}, {'type': 'object', 'properties': {
            'event_type': {'const': 'CommandRejected'}, 'payload': {'type': 'object', 'properties': {'command_id': {'type': 'string'}, 'reason_code': {'type': 'string'}, 'violated_requirement_ids': {'type': 'array', 'items': {'type': 'string'}}, 'details': {'type': 'object'}}, 'required': ['command_id', 'reason_code', 'violated_requirement_ids', 'details'], 'additionalProperties': False}}, 'required': ['event_type', 'payload']}]
    },
    'contracts/events/journey-completed.event.schema.json': {
        '$schema': SCHEMA, '$id': f'{BASE}/events/journey-completed.event.schema.json', 'title': 'Journey Completed Event',
        'allOf': [{'$ref': f'{BASE}/events/domain-event.schema.json'}, {'type': 'object', 'properties': {
            'event_type': {'const': 'JourneyCompleted'}, 'payload': {'type': 'object', 'properties': {'journey_id': {'type': 'string'}, 'destination': {'$ref': f'{BASE}/common/common.schema.json#/$defs/locationRef'}, 'elapsed_seconds': {'type': 'number', 'minimum': 0}, 'route_revisions': {'type': 'integer', 'minimum': 0}}, 'required': ['journey_id', 'destination', 'elapsed_seconds', 'route_revisions'], 'additionalProperties': False}}, 'required': ['event_type', 'payload']}]
    },
}
for path, schema in additional_schemas.items():
    write_json(path, schema)

# Add representative fixtures for additional schemas.
fixture('examples/fixtures/world/world.valid.json', additional_schemas['contracts/world-entities/world.schema.json']['$id'], True, {
    'schema_version': '0.2.0', 'world_id': 'world:london-demo', 'name': 'London District Demonstrator', 'world_version': '0.2.0',
    'world_type': 'hypothetical', 'coordinate_reference_system': 'EPSG:4326', 'root_place_ids': ['place:district-01'],
    'simulation_ruleset': 'ruleset:awg-reference-0.2.0', 'data_source_ids': ['AWG-DATA-001', 'AWG-DATA-003', 'AWG-DATA-004', 'AWG-DATA-005'],
    'created_at': '2026-08-20T20:00:00Z'
}, 'Valid bounded world descriptor.')
fixture('examples/fixtures/scenarios/run-record.valid.json', additional_schemas['contracts/scenarios/run-record.schema.json']['$id'], True, {
    'schema_version': '0.2.0', 'run_id': 'run:bridge-closure:baseline:001', 'scenario_id': 'scenario:bridge-closure',
    'scenario_digest': 'sha256:scenario-demo', 'branch_id': 'branch:baseline', 'core_version': '0.2.0', 'configuration_digest': 'sha256:config-demo',
    'data_source_versions': [{'id': 'AWG-DATA-001', 'version': '2026-08-01'}], 'plugin_versions': [{'plugin_id': 'mobility:reference', 'version': '0.2.0'}],
    'model_records': [{'record_id': 'AWG-AI-001', 'model': 'scenario-assigned-local-model'}], 'random_streams': [{'stream_id': 'random:mobility', 'seed': 1001}],
    'started_at': '2026-08-20T20:00:00Z', 'completed_at': None, 'final_event_sequence': None, 'snapshot_refs': [], 'event_archive_ref': None,
    'environment': {'python': '3.13', 'platform': 'container'}
}, 'Valid immutable run record.')

# Intentionally invalid representatives prove rejection behaviour in every executable contract family.
invalid_representatives = [
    ('examples/fixtures/events/domain-event.invalid.json', base_event['$id'], 'Invalid event: required envelope fields are absent.'),
    ('examples/fixtures/agents/agent-profile.invalid.json', agent_profile['$id'], 'Invalid agent profile: identity, provenance, and state are absent.'),
    ('examples/fixtures/world/place.invalid.json', place_schema['$id'], 'Invalid place: identity, type, and geometry references are absent.'),
    ('examples/fixtures/claims/claim.invalid.json', claim_schema['$id'], 'Invalid claim: proposition and provenance lineage are absent.'),
    ('examples/fixtures/social/social-action.invalid.json', social_action_schema['$id'], 'Invalid social action: actor, platform, action type, and time are absent.'),
    ('examples/fixtures/plugins/plugin-manifest.invalid.json', plugin_schema['$id'], 'Invalid plugin manifest: capability, permissions, compatibility, and identity are absent.'),
    ('examples/fixtures/scenarios/scenario-package.invalid.json', scenario_schema['$id'], 'Invalid scenario package: world, time, seeds, interventions, and measurements are absent.'),
    ('examples/fixtures/firehose/subscription.invalid.json', firehose_subscription['$id'], 'Invalid firehose subscription: identity, filters, delivery, and backpressure are absent.'),
]
for invalid_path, schema_id, note in invalid_representatives:
    fixture(invalid_path, schema_id, False, {}, note)

# Refresh fixture and schema indexes after additional contracts.
write('examples/fixtures/index.yaml', yaml.safe_dump({'version': VERSION, 'fixtures': fixtures}, sort_keys=False, allow_unicode=True))
schema_catalog = []
for p in sorted((ROOT / 'contracts').rglob('*.schema.json')):
    data = json.loads(p.read_text(encoding='utf-8'))
    schema_catalog.append({'path': p.relative_to(ROOT).as_posix(), 'id': data.get('$id'), 'title': data.get('title'), 'version': VERSION})
write('contracts/schema-catalog.yaml', yaml.safe_dump({'version': VERSION, 'schemas': schema_catalog}, sort_keys=False, allow_unicode=True))

# Ensure every normative document participates in traceability.
req_data = yaml.safe_load((ROOT / 'registers/requirements.yaml').read_text(encoding='utf-8'))
test_data = yaml.safe_load((ROOT / 'registers/tests.yaml').read_text(encoding='utf-8'))
covered_docs = {doc_id for req in req_data['requirements'] for doc_id in req.get('source_documents', [])}
seq = 1
for d in DOCS:
    if not d.normative or d.document_id in covered_docs:
        continue
    rid = f'AWG-REQ-COV-{seq:03d}'
    tid = f'AWG-TEST-DOC-{seq:03d}'
    seq += 1
    req_data['requirements'].append({'id': rid, 'title': f'Conform to {d.title}', 'statement': f'The implementation and review process must conform to {d.document_id}: {d.title}.', 'source_documents': [d.document_id], 'implemented_by': [d.document_id], 'verified_by': [tid], 'status': 'draft'})
    test_data['tests'].append({'id': tid, 'type': 'document_acceptance', 'description': f'Verify required sections, traceability, examples, and acceptance criteria for {d.document_id}.', 'requirements': [rid], 'automation': 'pack validation plus domain review', 'status': 'defined'})
write('registers/requirements.yaml', yaml.safe_dump(req_data, sort_keys=False, allow_unicode=True))
write('registers/tests.yaml', yaml.safe_dump(test_data, sort_keys=False, allow_unicode=True))

print(f'Expanded contract catalogue to {len(schema_catalog)} schemas and {len(fixtures)} fixtures.')

# Document registry and pack manifest.
document_records = []
for d in sorted(DOCS, key=lambda x: x.document_id):
    document_records.append({
        'document_id': d.document_id,
        'path': d.path,
        'title': d.title,
        'summary': d.summary,
        'normative': d.normative,
        'status': d.status,
        'version': VERSION,
        'owners': d.owners,
        'audience': d.audience,
        'depends_on': d.depends_on,
        'linear_issue': d.linear_issue,
        'required_sections': d.required_sections,
    })
write('registers/documents.yaml', yaml.safe_dump({'version': VERSION, 'documents': document_records}, sort_keys=False, allow_unicode=True))

manifest = {
    'pack': {
        'id': 'AWG', 'name': 'Agentic World Graph', 'version': VERSION, 'status': 'baseline',
        'generated': TODAY, 'canonical_root': '.',
        'source_of_truth': 'Authored files and canonical YAML registers in this repository.'
    },
    'documents_registry': 'registers/documents.yaml',
    'requirements_registry': 'registers/requirements.yaml',
    'tests_registry': 'registers/tests.yaml',
    'conversation_requirements_registry': 'registers/conversation-requirements.yaml',
    'required_root_files': [
        'README.md', 'AGENTS.md', 'CONTRIBUTING.md', 'SECURITY.md', 'GOVERNANCE.md',
        'CHANGELOG.md', 'LICENSE', 'NOTICE.md', 'pack-manifest.yaml', 'pyproject.toml',
        'Dockerfile', 'docker-compose.yml', 'Makefile', 'mkdocs.yml'
    ],
    'required_registers': [
        'registers/documents.yaml', 'registers/requirements.yaml', 'registers/tests.yaml',
        'registers/conversation-requirements.yaml', 'registers/glossary.yaml', 'registers/risks.yaml',
        'registers/assumptions.yaml', 'registers/data-sources.yaml', 'registers/open-source-components.yaml',
        'registers/models-and-prompts.yaml', 'registers/evidence.yaml', 'registers/linear-mapping.yaml'
    ],
    'required_contract_groups': [
        'contracts/common', 'contracts/commands', 'contracts/events', 'contracts/agents',
        'contracts/world-entities', 'contracts/claims-and-provenance', 'contracts/social-platform',
        'contracts/plugins', 'contracts/scenarios', 'contracts/firehose'
    ],
    'required_generated_reports': [
        'generated/document-map.md', 'generated/document-status-matrix.md',
        'generated/requirements-traceability-matrix.md', 'generated/conversation-requirements-coverage.md',
        'generated/glossary-and-controlled-vocabulary.md', 'generated/risk-and-assumption-register.md',
        'generated/data-source-and-provenance-register.md', 'generated/open-source-reuse-and-licensing-register.md',
        'generated/model-and-prompt-version-register.md', 'generated/evidence-register.md',
        'generated/completeness-report.md', 'generated/validation-report.md',
        'generated/pack-manifest.json'
    ],
    'required_scripts': [
        'scripts/build_generated.py', 'scripts/validate_pack.py', 'scripts/validate_traceability.py',
        'scripts/validate_contracts.py', 'scripts/validate_links.py', 'scripts/validate_all.py',
        'scripts/build_release.py', 'scripts/entrypoint.py'
    ],
    'required_tests': ['tests/test_pack.py', 'tests/test_contracts.py', 'tests/test_traceability.py'],
    'documents': [{'document_id': d.document_id, 'path': d.path, 'required_sections': d.required_sections} for d in DOCS],
    'archive_policy': 'Archive is retained for traceability and excluded from normative completeness checks.',
    'release_outputs': [
        'agentic-world-graph-v0.2.0.zip',
        'agentic-world-graph-v0.2.0-part-1-foundation-domain.zip',
        'agentic-world-graph-v0.2.0-part-2-platform-scenarios.zip',
        'agentic-world-graph-v0.2.0-part-3-ui-delivery.zip',
        'agentic-world-graph-v0.2.0-part-4-contracts-tools-archive.zip'
    ]
}
write('pack-manifest.yaml', yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))

# MkDocs navigation is generated from the document registry but the package is optional for offline validation.
nav = []
for area, (label, _) in AREA_INFO.items():
    entries = []
    for d in sorted([x for x in DOCS if x.path.startswith(f'docs/{area}/')], key=lambda x: x.document_id):
        entries.append({f'{d.document_id} — {d.title}': d.path.removeprefix('docs/')})
    nav.append({label: entries})
mkdocs = {
    'site_name': 'Agentic World Graph', 'site_description': 'Grounded agentic world simulation architecture and contracts',
    'docs_dir': 'docs', 'site_dir': 'site', 'theme': {'name': 'material'},
    'nav': [{'Home': 'README.md'}] + nav,
    'markdown_extensions': ['tables', 'fenced_code', 'toc'],
}
write('mkdocs.yml', yaml.safe_dump(mkdocs, sort_keys=False, allow_unicode=True))

write('pyproject.toml', clean('''
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "agentic-world-graph-docpack"
version = "0.2.0"
description = "Validation and release tooling for the Agentic World Graph documentation and contract pack"
requires-python = ">=3.11"
dependencies = [
  "PyYAML>=6.0",
  "jsonschema>=4.20",
  "referencing>=0.35"
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "mkdocs>=1.6",
  "mkdocs-material>=9.5"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
'''))
write('requirements-dev.txt', clean('''
PyYAML>=6.0
jsonschema>=4.20
referencing>=0.35
pytest>=8.0
mkdocs>=1.6
mkdocs-material>=9.5
'''))

write('Dockerfile', clean('''
FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
ENTRYPOINT ["python", "scripts/entrypoint.py"]
CMD ["validate"]
'''))
write('docker-compose.yml', clean('''
services:
  docs:
    build: .
    working_dir: /workspace
    volumes:
      - .:/workspace
    network_mode: none
    command: validate
'''))
write('Makefile', clean('''
.PHONY: generate validate test release clean

generate:
	python scripts/build_generated.py

validate:
	python scripts/validate_all.py

test:
	pytest -q

release:
	python scripts/build_release.py

clean:
	rm -rf site .pytest_cache scripts/__pycache__ tests/__pycache__
	find dist -type f ! -name .gitkeep -delete
'''))

print('Created pack manifest and build configuration.')

# Validation and generation tooling.
write('scripts/_common.py', clean(r'''
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load((ROOT / path).read_text(encoding='utf-8'))


def load_json(path: str | Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write_text(path: str | Path, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + '\n', encoding='utf-8')


def parse_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}, text
    parts = text.split('---\n', 2)
    if len(parts) != 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    def esc(value: Any) -> str:
        return str(value if value is not None else '').replace('|', '\\|').replace('\n', ' ')
    lines = ['| ' + ' | '.join(map(esc, headers)) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |']
    lines.extend('| ' + ' | '.join(esc(v) for v in row) + ' |' for row in rows)
    return '\n'.join(lines)


def headings(body: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r'^##\s+(.+?)\s*$', body, flags=re.MULTILINE)}


def all_files(exclude_dist: bool = True) -> list[Path]:
    result = []
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if exclude_dist and rel.parts and rel.parts[0] == 'dist':
            continue
        if '__pycache__' in rel.parts or '.pytest_cache' in rel.parts or '.git' in rel.parts:
            continue
        result.append(p)
    return sorted(result)
'''))

write('scripts/build_generated.py', clean(r'''
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from _common import ROOT, load_yaml, markdown_table, write_text


def main() -> None:
    manifest = load_yaml('pack-manifest.yaml')
    docs = load_yaml('registers/documents.yaml')['documents']
    requirements = load_yaml('registers/requirements.yaml')['requirements']
    tests = load_yaml('registers/tests.yaml')['tests']
    conversations = load_yaml('registers/conversation-requirements.yaml')['requirements']
    glossary = load_yaml('registers/glossary.yaml')['terms']
    risks = load_yaml('registers/risks.yaml')['risks']
    assumptions = load_yaml('registers/assumptions.yaml')['assumptions']
    data_sources = load_yaml('registers/data-sources.yaml')['data_sources']
    components = load_yaml('registers/open-source-components.yaml')['components']
    models = load_yaml('registers/models-and-prompts.yaml')['records']
    evidence = load_yaml('registers/evidence.yaml')['evidence']
    linear = load_yaml('registers/linear-mapping.yaml')

    by_area: dict[str, list[dict]] = defaultdict(list)
    for d in docs:
        area = Path(d['path']).parts[1]
        by_area[area].append(d)
    lines = ['# Document Map', '', 'Generated from `registers/documents.yaml`.', '']
    for area in sorted(by_area):
        lines += [f'## {area}', '']
        for d in sorted(by_area[area], key=lambda x: x['document_id']):
            rel_from_generated = '../' + d['path']
            kind = 'Normative' if d['normative'] else 'Informative'
            lines.append(f"- [{d['document_id']} — {d['title']}]({rel_from_generated}) — {kind}, {d['status']}")
        lines.append('')
    write_text('generated/document-map.md', '\n'.join(lines))

    status_rows = [[d['document_id'], d['title'], 'Normative' if d['normative'] else 'Informative', d['status'], d['version'], d.get('linear_issue') or '', d['path']] for d in docs]
    write_text('generated/document-status-matrix.md', '# Document Status Matrix\n\n' + markdown_table(['ID', 'Title', 'Authority', 'Status', 'Version', 'Linear', 'Path'], status_rows))

    req_rows = []
    for r in requirements:
        req_rows.append([r['id'], r['statement'], ', '.join(r.get('source_documents', [])), ', '.join(r.get('implemented_by', [])), ', '.join(r.get('verified_by', [])), r['status']])
    write_text('generated/requirements-traceability-matrix.md', '# Requirements Traceability Matrix\n\n' + markdown_table(['Requirement', 'Statement', 'Source documents', 'Implemented by', 'Verified by', 'Status'], req_rows))

    conv_rows = [[c['id'], c['request'], c['normative_requirement'], ', '.join(c['covered_by']), c['status']] for c in conversations]
    write_text('generated/conversation-requirements-coverage.md', '# Conversation Requirements Coverage\n\nEvery substantive requirement from the design session is mapped to a normative requirement and document set.\n\n' + markdown_table(['Conversation ID', 'Request', 'Requirement', 'Covered by', 'Status'], conv_rows))

    glossary_lines = ['# Glossary and Controlled Vocabulary', '', 'Generated from `registers/glossary.yaml`.', '']
    for t in sorted(glossary, key=lambda x: x['term'].lower()):
        glossary_lines += [f"## {t['term']}", '', t['definition'], '']
        if t.get('allowed_synonyms'):
            glossary_lines += ['**Allowed synonyms:** ' + ', '.join(t['allowed_synonyms']), '']
        if t.get('not_interchangeable_with'):
            glossary_lines += ['**Do not use interchangeably with:** ' + ', '.join(t['not_interchangeable_with']), '']
    write_text('generated/glossary-and-controlled-vocabulary.md', '\n'.join(glossary_lines))

    risk_rows = [[r['id'], r['description'], r['severity'], r['mitigation'], ', '.join(r['affected_documents']), r['status']] for r in risks]
    asm_rows = [[a['id'], a['statement'], ', '.join(a['affected_documents']), a['status'], a['review_trigger']] for a in assumptions]
    write_text('generated/risk-and-assumption-register.md', '# Risk and Assumption Register\n\n## Risks\n\n' + markdown_table(['ID', 'Description', 'Severity', 'Mitigation', 'Documents', 'Status'], risk_rows) + '\n\n## Assumptions\n\n' + markdown_table(['ID', 'Statement', 'Documents', 'Status', 'Review trigger'], asm_rows))

    data_rows = [[d['id'], d['name'], d['role'], d['provider'], d['licence'], d['status'], '; '.join(d['known_limits'])] for d in data_sources]
    write_text('generated/data-source-and-provenance-register.md', '# Data Source and Provenance Register\n\n' + markdown_table(['ID', 'Name', 'Role', 'Provider', 'Licence', 'Status', 'Known limits'], data_rows))

    comp_rows = [[c['id'], c['name'], c['role'], c['declared_or_reported_licence'], c['adoption_status'], c['code_reuse_approved'], c['legal_review_required']] for c in components]
    write_text('generated/open-source-reuse-and-licensing-register.md', '# Open-Source Reuse and Licensing Register\n\nReported licences are provisional until verified for the selected version and dependency tree.\n\n' + markdown_table(['ID', 'Component', 'Role', 'Reported licence', 'Status', 'Code approved', 'Legal review'], comp_rows))

    model_rows = [[m['id'], m['provider'], m['deployment'], ', '.join(m['roles']), m['model_version'], m['prompt_policy_version'], m['fallback'], m['status']] for m in models]
    write_text('generated/model-and-prompt-version-register.md', '# Model and Prompt Version Register\n\n' + markdown_table(['ID', 'Provider', 'Deployment', 'Roles', 'Model version', 'Prompt policy', 'Fallback', 'Status'], model_rows))

    evidence_rows = [[e['id'], e['title'], e['source_type'], e['url'], e['relevance'], e['retrieved']] for e in evidence]
    write_text('generated/evidence-register.md', '# Evidence Register\n\n' + markdown_table(['ID', 'Title', 'Type', 'Source', 'Relevance', 'Retrieved'], evidence_rows))

    linear_lines = ['# Linear Project Mapping', '', f"**Project:** [{linear['project']['name']}]({linear['project']['url']})", '', linear['source_of_truth'], '', '## Milestones', '']
    linear_lines += [f'- {m}' for m in linear['milestones']]
    linear_lines += ['', '## Issue-to-document mapping', '']
    linear_lines += [f'- `{issue}` → `{doc}`' for issue, doc in sorted(linear['issues'].items())]
    write_text('generated/linear-project-mapping.md', '\n'.join(linear_lines))

    schema_count = len(list((ROOT / 'contracts').rglob('*.schema.json')))
    fixture_count = len(load_yaml('examples/fixtures/index.yaml')['fixtures'])
    normative = sum(1 for d in docs if d['normative'])
    completeness = f"""# Pack Completeness Report

This report is generated before the final validation report.

| Measure | Count |
|---|---:|
| Registered documents | {len(docs)} |
| Normative documents | {normative} |
| Informative documents | {len(docs) - normative} |
| Conversation requirements | {len(conversations)} |
| Normative requirements | {len(requirements)} |
| Acceptance-test records | {len(tests)} |
| JSON Schemas | {schema_count} |
| Indexed valid/invalid fixtures | {fixture_count} |
| Risks | {len(risks)} |
| Assumptions | {len(assumptions)} |
| Data-source records | {len(data_sources)} |
| Component/licensing records | {len(components)} |
| Evidence records | {len(evidence)} |

Structural completeness is confirmed only after `scripts/validate_all.py` passes. Draft document status means formal human approval remains outstanding; it does not mean the element is missing.
"""
    write_text('generated/completeness-report.md', completeness)
    write_text('generated/pack-manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
    write_text('generated/README.md', '# Generated Reports\n\nThese files are generated from canonical YAML registers and must not be edited directly.')
    report = ROOT / 'generated/validation-report.md'
    if not report.exists():
        write_text('generated/validation-report.md', '# Validation Report\n\nValidation has not yet run for the current working tree.')


if __name__ == '__main__':
    main()
'''))

write('scripts/validate_pack.py', clean(r'''
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from _common import ROOT, headings, load_yaml, parse_front_matter

ALLOWED_STATUS = {'outline', 'draft', 'in_review', 'accepted', 'deprecated', 'superseded', 'baseline'}
PLACEHOLDER_PATTERN = re.compile(r'\b(?:TBD|TODO|FIXME|PLACEHOLDER)\b', re.IGNORECASE)


def validate() -> list[str]:
    errors: list[str] = []
    manifest = load_yaml('pack-manifest.yaml')
    registry = load_yaml('registers/documents.yaml')['documents']
    doc_ids = {d['document_id'] for d in registry}

    for rel in manifest['required_root_files'] + manifest['required_registers'] + manifest['required_generated_reports'] + manifest['required_scripts'] + manifest['required_tests']:
        if not (ROOT / rel).is_file():
            errors.append(f'Missing required file: {rel}')

    for group in manifest['required_contract_groups']:
        p = ROOT / group
        if not p.is_dir() or not list(p.glob('*.schema.json')):
            errors.append(f'Missing or empty contract group: {group}')

    seen: set[str] = set()
    registered_paths = set()
    deps: dict[str, list[str]] = {}
    normative: set[str] = set()
    for record in registry:
        did = record['document_id']
        path = ROOT / record['path']
        registered_paths.add(record['path'])
        if did in seen:
            errors.append(f'Duplicate document ID: {did}')
        seen.add(did)
        deps[did] = record.get('depends_on', [])
        if record.get('normative'):
            normative.add(did)
        if not path.is_file():
            errors.append(f'Missing document {did}: {record["path"]}')
            continue
        meta, body = parse_front_matter(path)
        for field in ['title', 'document_id', 'status', 'version', 'last_updated', 'normative', 'owners', 'audience', 'depends_on']:
            if field not in meta:
                errors.append(f'{did} missing front-matter field: {field}')
        if meta.get('document_id') != did:
            errors.append(f'{did} front matter ID mismatch: {meta.get("document_id")}')
        if meta.get('title') != record['title']:
            errors.append(f'{did} title mismatch between registry and file')
        if meta.get('version') != record['version']:
            errors.append(f'{did} version mismatch between registry and file')
        if meta.get('status') not in ALLOWED_STATUS:
            errors.append(f'{did} has invalid status: {meta.get("status")}')
        missing_sections = set(record.get('required_sections', [])) - headings(body)
        if missing_sections:
            errors.append(f'{did} missing sections: {sorted(missing_sections)}')
        if PLACEHOLDER_PATTERN.search(body):
            errors.append(f'{did} contains unresolved placeholder marker')
        if record.get('normative') and '## Acceptance criteria' not in body:
            errors.append(f'{did} normative document lacks acceptance criteria')

    for did, targets in deps.items():
        for target in targets:
            if target not in doc_ids:
                errors.append(f'{did} depends on unknown document {target}')

    # Detect dependency cycles so reading order and authority cannot become ambiguous.
    state: dict[str, int] = {}
    stack: list[str] = []
    reported_cycles: set[tuple[str, ...]] = set()

    def visit_dependency(did: str) -> None:
        current = state.get(did, 0)
        if current == 2:
            return
        if current == 1:
            if did in stack:
                cycle = tuple(stack[stack.index(did):] + [did])
                if cycle not in reported_cycles:
                    reported_cycles.add(cycle)
                    errors.append('Document dependency cycle: ' + ' -> '.join(cycle))
            return
        state[did] = 1
        stack.append(did)
        for target in deps.get(did, []):
            if target in deps:
                visit_dependency(target)
        stack.pop()
        state[did] = 2

    for did in sorted(deps):
        visit_dependency(did)

    def reaches_constitution(did: str, trail: set[str] | None = None) -> bool:
        if did == 'AWG-GOV-001':
            return True
        trail = set() if trail is None else set(trail)
        if did in trail:
            return False
        trail.add(did)
        return any(reaches_constitution(dep, trail) for dep in deps.get(did, []))

    for did in sorted(normative - {'AWG-GOV-001'}):
        if not reaches_constitution(did):
            errors.append(f'{did} has no dependency path to AWG-GOV-001')

    authored = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / 'docs').rglob('*.md')
        if p.name != 'README.md'
    }
    unregistered = authored - registered_paths
    stale = registered_paths - authored
    if unregistered:
        errors.append(f'Unregistered authored documents: {sorted(unregistered)}')
    if stale:
        errors.append(f'Registry paths not found among authored documents: {sorted(stale)}')

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        raise SystemExit(1)
    print('Pack structure and document metadata validation passed.')


if __name__ == '__main__':
    main()
'''))

write('scripts/validate_traceability.py', clean(r'''
from __future__ import annotations

from _common import load_yaml


def unique(records: list[dict], field: str, label: str, errors: list[str]) -> set[str]:
    values: set[str] = set()
    for record in records:
        value = record[field]
        if value in values:
            errors.append(f'Duplicate {label}: {value}')
        values.add(value)
    return values


def validate() -> list[str]:
    errors: list[str] = []
    docs = load_yaml('registers/documents.yaml')['documents']
    reqs = load_yaml('registers/requirements.yaml')['requirements']
    tests = load_yaml('registers/tests.yaml')['tests']
    conv = load_yaml('registers/conversation-requirements.yaml')['requirements']
    risks = load_yaml('registers/risks.yaml')['risks']
    assumptions = load_yaml('registers/assumptions.yaml')['assumptions']
    components = load_yaml('registers/open-source-components.yaml')['components']
    data_sources = load_yaml('registers/data-sources.yaml')['data_sources']
    evidence = load_yaml('registers/evidence.yaml')['evidence']
    glossary = load_yaml('registers/glossary.yaml')['terms']

    doc_ids = unique(docs, 'document_id', 'document ID', errors)
    req_ids = unique(reqs, 'id', 'requirement ID', errors)
    test_ids = unique(tests, 'id', 'test ID', errors)
    unique(conv, 'id', 'conversation requirement ID', errors)
    unique(risks, 'id', 'risk ID', errors)
    unique(assumptions, 'id', 'assumption ID', errors)
    unique(components, 'id', 'component ID', errors)
    unique(data_sources, 'id', 'data-source ID', errors)
    unique(evidence, 'id', 'evidence ID', errors)
    unique(glossary, 'id', 'glossary ID', errors)

    terms = [t['term'].casefold() for t in glossary]
    if len(terms) != len(set(terms)):
        errors.append('Duplicate canonical glossary term')

    for c in conv:
        if c.get('status') != 'covered':
            errors.append(f'Conversation requirement not covered: {c["id"]}')
        if c['normative_requirement'] not in req_ids:
            errors.append(f'{c["id"]} maps to unknown requirement {c["normative_requirement"]}')
        for did in c.get('covered_by', []):
            if did not in doc_ids:
                errors.append(f'{c["id"]} maps to unknown document {did}')

    doc_requirement_coverage: set[str] = set()
    for r in reqs:
        for did in r.get('source_documents', []):
            doc_requirement_coverage.add(did)
            if did not in doc_ids:
                errors.append(f'{r["id"]} references unknown source document {did}')
        for did in r.get('implemented_by', []):
            if did not in doc_ids:
                errors.append(f'{r["id"]} references unknown implementation document {did}')
        if not r.get('verified_by'):
            errors.append(f'{r["id"]} has no verification target')
        for tid in r.get('verified_by', []):
            if tid not in test_ids:
                errors.append(f'{r["id"]} references unknown test {tid}')

    for t in tests:
        for rid in t.get('requirements', []):
            if rid not in req_ids:
                errors.append(f'{t["id"]} references unknown requirement {rid}')

    for d in docs:
        if d.get('normative') and d['document_id'] not in doc_requirement_coverage:
            errors.append(f'Normative document has no requirement coverage: {d["document_id"]}')

    for r in risks:
        for did in r.get('affected_documents', []):
            if did not in doc_ids:
                errors.append(f'{r["id"]} references unknown document {did}')
    for a in assumptions:
        for did in a.get('affected_documents', []):
            if did not in doc_ids:
                errors.append(f'{a["id"]} references unknown document {did}')

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        raise SystemExit(1)
    print('Requirements, tests, conversation coverage, risks, assumptions, and registries are traceable.')


if __name__ == '__main__':
    main()
'''))

write('scripts/validate_contracts.py', clean(r'''
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urldefrag, unquote

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from _common import ROOT, load_yaml


def iter_refs(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == '$ref' and isinstance(item, str):
                yield item
            else:
                yield from iter_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_refs(item)


def resolve_pointer(document, fragment: str):
    if not fragment:
        return document
    if not fragment.startswith('/'):
        raise ValueError(f'unsupported non-JSON-pointer fragment #{fragment}')
    current = document
    for token in fragment.lstrip('/').split('/'):
        token = unquote(token).replace('~1', '/').replace('~0', '~')
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise KeyError(token)
    return current


def validate() -> list[str]:
    errors: list[str] = []
    schemas: dict[str, dict] = {}
    paths_by_id: dict[str, str] = {}
    resources = []
    actual_schema_paths: set[str] = set()

    for path in sorted((ROOT / 'contracts').rglob('*.schema.json')):
        rel = path.relative_to(ROOT).as_posix()
        actual_schema_paths.add(rel)
        try:
            schema = json.loads(path.read_text(encoding='utf-8'))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f'Invalid schema {rel}: {exc}')
            continue
        sid = schema.get('$id')
        if not sid:
            errors.append(f'Schema lacks $id: {rel}')
            continue
        if sid in schemas:
            errors.append(f'Duplicate schema $id: {sid}')
        schemas[sid] = schema
        paths_by_id[sid] = rel
        resources.append((sid, Resource.from_contents(schema)))

    # All references must point to a known schema and a valid JSON Pointer when a fragment is present.
    for sid, schema in schemas.items():
        for ref in iter_refs(schema):
            base, fragment = urldefrag(ref)
            target_id = base or sid
            target = schemas.get(target_id)
            if target is None:
                errors.append(f'Unknown $ref in {paths_by_id[sid]}: {ref}')
                continue
            try:
                resolve_pointer(target, fragment)
            except Exception as exc:
                errors.append(f'Invalid $ref fragment in {paths_by_id[sid]}: {ref} ({exc})')

    # The schema catalog must exactly match the on-disk executable contracts.
    catalog = load_yaml('contracts/schema-catalog.yaml').get('schemas', [])
    catalog_paths = {item['path'] for item in catalog}
    if catalog_paths != actual_schema_paths:
        missing = sorted(actual_schema_paths - catalog_paths)
        stale = sorted(catalog_paths - actual_schema_paths)
        if missing:
            errors.append(f'Schemas missing from catalog: {missing}')
        if stale:
            errors.append(f'Stale schema catalog paths: {stale}')
    for item in catalog:
        if item.get('id') not in schemas:
            errors.append(f'Catalog references unknown schema ID: {item.get("id")}')
        elif paths_by_id[item['id']] != item['path']:
            errors.append(f'Catalog path/ID mismatch: {item["path"]} -> {item["id"]}')

    registry = Registry().with_resources(resources)
    fixture_items = load_yaml('examples/fixtures/index.yaml')['fixtures']
    actual_fixture_paths = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / 'examples/fixtures').rglob('*.json')
    }
    indexed_fixture_paths = {item['path'] for item in fixture_items}
    if actual_fixture_paths != indexed_fixture_paths:
        missing = sorted(actual_fixture_paths - indexed_fixture_paths)
        stale = sorted(indexed_fixture_paths - actual_fixture_paths)
        if missing:
            errors.append(f'Fixture files missing from index: {missing}')
        if stale:
            errors.append(f'Stale fixture index entries: {stale}')

    coverage: dict[str, set[bool]] = {}
    seen_fixture_paths: set[str] = set()
    for item in fixture_items:
        if item['path'] in seen_fixture_paths:
            errors.append(f'Duplicate fixture index path: {item["path"]}')
        seen_fixture_paths.add(item['path'])
        path = ROOT / item['path']
        if not path.is_file():
            errors.append(f'Missing fixture: {item["path"]}')
            continue
        schema = schemas.get(item['schema_id'])
        if schema is None:
            errors.append(f'Fixture references unknown schema: {item["schema_id"]}')
            continue
        group = Path(paths_by_id[item['schema_id']]).parts[1]
        coverage.setdefault(group, set()).add(bool(item['expected_valid']))
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'Invalid JSON fixture {item["path"]}: {exc}')
            continue
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        fixture_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if item['expected_valid'] and fixture_errors:
            errors.append(f'Expected valid fixture failed {item["path"]}: {fixture_errors[0].message}')
        if not item['expected_valid'] and not fixture_errors:
            errors.append(f'Expected invalid fixture unexpectedly passed: {item["path"]}')

    executable_groups = {Path(p).parts[1] for p in actual_schema_paths if Path(p).parts[1] != 'common'}
    for group in sorted(executable_groups):
        states = coverage.get(group, set())
        if True not in states:
            errors.append(f'Contract group lacks a valid indexed fixture: {group}')
        if False not in states:
            errors.append(f'Contract group lacks an invalid indexed fixture: {group}')

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        raise SystemExit(1)
    print('All JSON Schemas compile, all references/catalog entries resolve, and indexed valid/invalid fixtures behave as expected.')


if __name__ == '__main__':
    main()
'''))

write('scripts/validate_links.py', clean(r'''
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from _common import ROOT

LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')


def validate() -> list[str]:
    errors: list[str] = []
    for path in sorted(list((ROOT / 'docs').rglob('*.md')) + list((ROOT / 'generated').rglob('*.md')) + [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'CONTRIBUTING.md']):
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        for target in LINK.findall(text):
            target = target.strip().split()[0]
            if target.startswith(('http://', 'https://', 'mailto:', '#', 'sandbox:')):
                continue
            clean_target = unquote(target.split('#', 1)[0])
            if not clean_target:
                continue
            resolved = (path.parent / clean_target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f'Link escapes repository in {path.relative_to(ROOT)}: {target}')
                continue
            if not resolved.exists():
                errors.append(f'Broken internal link in {path.relative_to(ROOT)}: {target}')
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        raise SystemExit(1)
    print('Internal Markdown links resolve.')


if __name__ == '__main__':
    main()
'''))

write('scripts/validate_all.py', clean(r'''
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, write_text

CHECKS = [
    ('Pack structure and front matter', 'validate_pack.py'),
    ('Traceability and registries', 'validate_traceability.py'),
    ('JSON Schemas and fixtures', 'validate_contracts.py'),
    ('Internal links', 'validate_links.py'),
]


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_generated.py')], cwd=ROOT, check=True)
    results = []
    failed = False
    for label, script in CHECKS:
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, text=True, capture_output=True)
        ok = proc.returncode == 0
        failed = failed or not ok
        results.append((label, ok, (proc.stdout + proc.stderr).strip()))
        print((proc.stdout + proc.stderr).strip())
    lines = ['# Validation Report', '', f"**Run at:** {datetime.now(timezone.utc).isoformat()}", '', f"**Overall result:** {'FAIL' if failed else 'PASS'}", '', '## Checks', '']
    for label, ok, output in results:
        lines += [f"### {label}: {'PASS' if ok else 'FAIL'}", '', '```text', output or '(no output)', '```', '']
    lines += ['## Interpretation', '', 'A PASS confirms structural completeness, traceability, schema/fixture validity, and internal-link integrity for the current working tree. It does not substitute for human approval of draft normative decisions or empirical validation of a future implementation.']
    write_text('generated/validation-report.md', '\n'.join(lines))
    if failed:
        raise SystemExit(1)
    print('All AWG pack validation checks passed.')


if __name__ == '__main__':
    main()
'''))

write('scripts/build_release.py', clean(r'''
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from _common import ROOT, all_files, load_yaml, sha256_file, write_text

VERSION = load_yaml('pack-manifest.yaml')['pack']['version']
DIST = ROOT / 'dist'


def zip_paths(output: Path, paths: list[Path]) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(set(paths)):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            zf.write(path, Path('agentic-world-graph') / rel)


def expand(prefixes: list[str], include_root: bool = True) -> list[Path]:
    paths: list[Path] = []
    if include_root:
        paths += [p for p in ROOT.iterdir() if p.is_file() and p.name not in {'dist'}]
    for prefix in prefixes:
        p = ROOT / prefix
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            paths += [x for x in p.rglob('*') if x.is_file() and not ({'dist', '__pycache__', '.pytest_cache', '.git'} & set(x.relative_to(ROOT).parts))]
    return paths


def audit_zip(path: Path, expected_names: set[str] | None = None) -> list[str]:
    messages: list[str] = []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError(f'Duplicate archive entries in {path.name}')
        for name in names:
            posix = PurePosixPath(name)
            if posix.is_absolute() or '..' in posix.parts or not posix.parts or posix.parts[0] != 'agentic-world-graph':
                raise RuntimeError(f'Unsafe archive path in {path.name}: {name}')
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f'Archive integrity failure in {path.name}: {bad}')
        if expected_names is not None and set(names) != expected_names:
            missing = sorted(expected_names - set(names))[:10]
            extra = sorted(set(names) - expected_names)[:10]
            raise RuntimeError(f'Archive content mismatch in {path.name}; missing={missing}, extra={extra}')
        messages.append(f'{path.name}: {len(names)} entries, integrity and path safety PASS')
    return messages


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / 'scripts/validate_all.py')], cwd=ROOT, check=True)
    subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=ROOT, check=True)
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob('*'):
        if old.name != '.gitkeep':
            old.unlink() if old.is_file() else shutil.rmtree(old)

    # The manifest covers every source file except itself and release artefacts, avoiding an impossible self-hash.
    source_files = [p for p in all_files(exclude_dist=True) if p.relative_to(ROOT).as_posix() != 'generated/file-manifest.json']
    inventory = [
        {'path': p.relative_to(ROOT).as_posix(), 'size': p.stat().st_size, 'sha256': sha256_file(p)}
        for p in source_files
    ]
    manifest = {
        'pack': 'Agentic World Graph',
        'version': VERSION,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'scope': 'All source files except generated/file-manifest.json and dist release artefacts.',
        'excluded_paths': ['generated/file-manifest.json', 'dist/**'],
        'file_count': len(inventory),
        'files': inventory,
    }
    write_text('generated/file-manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
    source_files = all_files(exclude_dist=True)

    full = DIST / f'agentic-world-graph-v{VERSION}.zip'
    zip_paths(full, source_files)

    shared = ['README.md', 'AGENTS.md', 'pack-manifest.yaml', 'docs/README.md', 'generated', 'registers', 'LICENSE', 'NOTICE.md']
    parts = [
        (f'agentic-world-graph-v{VERSION}-part-1-foundation-domain.zip', shared + ['docs/00-vision-and-research', 'docs/01-governance-and-safety', 'docs/02-domain-model']),
        (f'agentic-world-graph-v{VERSION}-part-2-platform-scenarios.zip', shared + ['docs/03-platform-architecture', 'docs/04-scenarios-and-validation', 'contracts']),
        (f'agentic-world-graph-v{VERSION}-part-3-ui-delivery.zip', shared + ['docs/05-ui-ux', 'docs/06-delivery-and-operations', 'decisions', '.github']),
        (f'agentic-world-graph-v{VERSION}-part-4-contracts-tools-archive.zip', shared + ['docs/10-appendices', 'contracts', 'examples', 'scripts', 'tests', 'templates', 'archive', 'pyproject.toml', 'requirements-dev.txt', 'Dockerfile', 'docker-compose.yml', 'Makefile', 'mkdocs.yml']),
    ]
    archives = [full]
    for name, prefixes in parts:
        output = DIST / name
        zip_paths(output, expand(prefixes, include_root=True))
        archives.append(output)

    audit_lines: list[str] = []
    expected_full_names = {f'agentic-world-graph/{p.relative_to(ROOT).as_posix()}' for p in source_files}
    audit_lines.extend(audit_zip(full, expected_full_names))
    part_union: set[str] = set()
    for archive in archives[1:]:
        audit_lines.extend(audit_zip(archive))
        with zipfile.ZipFile(archive) as zf:
            part_union.update(zf.namelist())
    if part_union != expected_full_names:
        missing = sorted(expected_full_names - part_union)[:20]
        extra = sorted(part_union - expected_full_names)[:20]
        raise RuntimeError(f'Logical part union does not reconstruct the full source set; missing={missing}, extra={extra}')
    audit_lines.append('Logical part union reconstructs the complete full-archive source set: PASS')

    # Extract and verify every hash covered by the self-excluding source manifest.
    with tempfile.TemporaryDirectory(prefix='awg-release-audit-') as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(full) as zf:
            zf.extractall(tmp_path)
        extracted_root = tmp_path / 'agentic-world-graph'
        extracted_manifest = json.loads((extracted_root / 'generated/file-manifest.json').read_text(encoding='utf-8'))
        for item in extracted_manifest['files']:
            candidate = extracted_root / item['path']
            if not candidate.is_file():
                raise RuntimeError(f'Manifest file missing after extraction: {item["path"]}')
            if candidate.stat().st_size != item['size']:
                raise RuntimeError(f'Manifest size mismatch after extraction: {item["path"]}')
            if sha256_file(candidate) != item['sha256']:
                raise RuntimeError(f'Manifest hash mismatch after extraction: {item["path"]}')
        audit_lines.append(f'Full archive manifest: {extracted_manifest["file_count"]} source files verified by SHA-256')

        # Re-run the repository checks from the extracted release to prove it is self-contained.
        validation = subprocess.run(
            [sys.executable, 'scripts/validate_all.py'], cwd=extracted_root,
            text=True, capture_output=True, check=True,
        )
        tests = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q'], cwd=extracted_root,
            text=True, capture_output=True, check=True,
        )
        audit_lines.append('Extracted full archive validation: PASS')
        audit_lines.append('Extracted full archive pytest suite: PASS')
        validation_output = (validation.stdout + validation.stderr).strip()
        tests_output = (tests.stdout + tests.stderr).strip()

    checksum_lines = [f'{sha256_file(a)}  {a.name}' for a in archives]
    write_text('dist/SHA256SUMS.txt', '\n'.join(checksum_lines))
    release_rows = ['# Release Inventory', '', f'Version: {VERSION}', '', 'The full ZIP contains the complete repository. Logical part ZIPs are independently downloadable subsets and do not require binary recombination.', '']
    for a in archives:
        release_rows.append(f'- `{a.name}` — {a.stat().st_size} bytes — SHA-256 `{sha256_file(a)}`')
    write_text('dist/RELEASE-INVENTORY.md', '\n'.join(release_rows))

    audit_report = [
        '# Release Validation Report', '',
        f'**Version:** {VERSION}',
        f'**Created at:** {datetime.now(timezone.utc).isoformat()}',
        '**Overall result:** PASS', '',
        '## Archive and manifest checks', '',
    ]
    audit_report += [f'- {line}' for line in audit_lines]
    audit_report += ['', '## Validation output from extracted full archive', '', '```text', validation_output, '```', '', '## Test output from extracted full archive', '', '```text', tests_output, '```', '', '## Interpretation', '', 'PASS confirms repository structure, traceability, schema references/catalogue, valid and invalid fixtures, internal links, file-manifest hashes, archive integrity/path safety, extracted-package validation, and the packaged Python test suite. It does not imply that draft architecture decisions are human-approved or that a future simulator implementation is empirically validated.']
    write_text('dist/RELEASE-VALIDATION.md', '\n'.join(audit_report))

    print(f'Built, extracted, hash-verified, and integrity-tested {len(archives)} release archives in {DIST}.')


if __name__ == '__main__':
    main()
'''))

write('scripts/entrypoint.py', clean(r'''
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = {
    'generate': 'build_generated.py',
    'validate': 'validate_all.py',
    'release': 'build_release.py',
}


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else 'validate'
    script = COMMANDS.get(command)
    if not script:
        raise SystemExit(f'Unknown command {command!r}. Use one of: {", ".join(COMMANDS)}')
    raise SystemExit(subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT).returncode)


if __name__ == '__main__':
    main()
'''))

# Tests execute the same canonical validators.
write('tests/test_pack.py', clean(r'''
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from build_generated import main as build_generated
from validate_links import validate as validate_links
from validate_pack import validate as validate_pack


def test_pack_and_links() -> None:
    build_generated()
    assert validate_pack() == []
    assert validate_links() == []
'''))
write('tests/test_contracts.py', clean(r'''
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from validate_contracts import validate


def test_contracts_and_fixtures() -> None:
    assert validate() == []
'''))
write('tests/test_traceability.py', clean(r'''
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from validate_traceability import validate


def test_traceability() -> None:
    assert validate() == []
'''))

# GitHub workflow templates for later repository import.
write('.github/workflows/documentation-quality.yml', clean('''
name: documentation-quality
on:
  pull_request:
  push:
    branches: [main]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: python scripts/validate_all.py
      - run: pytest -q
'''))
write('.github/workflows/release-pack.yml', clean('''
name: release-pack
on:
  workflow_dispatch:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: python scripts/build_release.py
      - uses: actions/upload-artifact@v4
        with:
          name: agentic-world-graph-release
          path: dist/*
'''))
write('.github/pull_request_template.md', clean('''
## Linear

- Issue:

## Documents and contracts changed

- Document IDs:
- Requirement IDs:
- Test IDs:
- Schema IDs:
- ADRs:

## Impact

- Compatibility:
- Security and privacy:
- Offline operation:
- Performance and scale:
- Data, licensing, and provenance:
- Migration:

## Validation

- [ ] `python scripts/validate_all.py`
- [ ] `pytest -q`
- [ ] Valid and invalid fixtures updated where required
- [ ] Risks, assumptions, evidence, and Linear mapping updated
'''))
write('.github/ISSUE_TEMPLATE/specification-change.md', clean('''
---
name: Specification change
description: Propose a normative AWG specification or contract change
---

## Problem
## Document and requirement IDs
## Proposed change
## Options considered
## Compatibility and migration
## Security, privacy, offline, and performance impact
## Tests and evidence
'''))
write('.github/CODEOWNERS.template', clean('''
# Copy to .github/CODEOWNERS after the GitHub organization and review teams exist.
# Replace example handles with real repository owners.
* @repository-maintainers
/docs/01-governance-and-safety/ @architecture-reviewers @security-reviewers
/contracts/ @architecture-reviewers
'''))

print('Created validation, generation, test, release, Docker, and CI tooling.')
