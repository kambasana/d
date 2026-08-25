from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from validate_contracts import validate


def test_contracts_and_fixtures() -> None:
    assert validate() == []
