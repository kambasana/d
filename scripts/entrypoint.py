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
