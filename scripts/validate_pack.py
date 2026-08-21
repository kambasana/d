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
