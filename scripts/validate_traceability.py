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
