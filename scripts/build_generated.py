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
