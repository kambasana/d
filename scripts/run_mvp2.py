from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_mvp2 import NpcKernel  # noqa: E402


def main() -> None:
    kernel = NpcKernel()
    kernel.run_24_hours()
    errors = kernel.state_integrity_errors()
    replayed = NpcKernel.replay(kernel.bundle, kernel.firehose)
    result = {
        "scenario_id": kernel.scenario_id,
        "population": kernel.bundle.population,
        "events": len(kernel.firehose),
        "min_places_visited": min(kernel.daily_place_counts().values()),
        "state_integrity_errors": errors,
        "resource_totals": kernel.resource_totals(),
        "replay_matches": replayed.state_checksum() == kernel.state_checksum(),
        "llm_required": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors or not result["replay_matches"] or result["min_places_visited"] < 2:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
