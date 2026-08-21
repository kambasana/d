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
