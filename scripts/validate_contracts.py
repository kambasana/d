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
