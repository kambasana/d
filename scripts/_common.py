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
