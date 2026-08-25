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
