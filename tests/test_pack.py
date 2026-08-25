from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from build_generated import main as build_generated
from validate_links import validate as validate_links
from validate_pack import validate as validate_pack


def test_pack_and_links() -> None:
    build_generated()
    assert validate_pack() == []
    assert validate_links() == []
