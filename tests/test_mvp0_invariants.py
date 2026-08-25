from __future__ import annotations

import ast
import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from validate_contracts import validate as validate_contracts  # noqa: E402

INV_RE = re.compile(r'^### (INV-\d{3}) - ', re.M)
FORBIDDEN_TOP_LEVEL = ('openai', 'ollama', 'anthropic', 'litellm', 'langchain')


def _load_yaml(rel: str) -> dict:
    return yaml.safe_load((ROOT / rel).read_text(encoding='utf-8'))


def test_constitution_invariants_have_requirement_and_test_ids() -> None:
    constitution = (ROOT / 'docs/01-governance-and-safety/simulation-constitution-and-invariants.md').read_text(
        encoding='utf-8'
    )
    inv_ids = INV_RE.findall(constitution)
    assert len(inv_ids) >= 20, 'Constitution MUST declare INV-001 through INV-020'
    reqs = {r['id']: r for r in _load_yaml('registers/requirements.yaml')['requirements']}
    tests = {t['id']: t for t in _load_yaml('registers/tests.yaml')['tests']}
    for inv in inv_ids:
        num = inv.split('-')[1]
        req_id = f'AWG-REQ-INV-{num}'
        test_id = f'AWG-TEST-INV-{num}'
        assert req_id in reqs, f'{inv} MUST have requirement {req_id}'
        assert test_id in tests, f'{inv} MUST have acceptance test {test_id}'
        assert test_id in reqs[req_id]['verified_by']
        assert req_id in tests[test_id]['requirements']
        assert tests[test_id]['type'] == 'invariant'


def test_travel_command_rejects_teleport_without_ai_provider() -> None:
    for name in FORBIDDEN_TOP_LEVEL:
        assert name not in sys.modules, f'AI provider module {name} MUST NOT be loaded to validate commands'
    schema = json.loads((ROOT / 'contracts/commands/travel-to-place.command.schema.json').read_text(encoding='utf-8'))
    modes = schema['allOf'][1]['properties']['transport_mode']['enum']
    assert 'teleport' not in modes
    payload = json.loads((ROOT / 'examples/fixtures/commands/travel-to-place.invalid.json').read_text(encoding='utf-8'))
    assert payload.get('transport_mode') == 'teleport'
    assert validate_contracts() == []


def test_pack_python_does_not_import_ai_providers() -> None:
    for directory in (ROOT / 'scripts', ROOT / 'tests'):
        for path in directory.rglob('*.py'):
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert alias.name.split('.')[0] not in FORBIDDEN_TOP_LEVEL, f'{path} imports {alias.name}'
                elif isinstance(node, ast.ImportFrom) and node.module:
                    assert node.module.split('.')[0] not in FORBIDDEN_TOP_LEVEL, f'{path} imports {node.module}'


def test_ai_provider_sdks_are_not_pack_dependencies() -> None:
    for name in FORBIDDEN_TOP_LEVEL:
        assert importlib.util.find_spec(name) is None, f'{name} MUST NOT be a pack dependency'
