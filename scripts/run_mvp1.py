from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_mvp1 import SimulationKernel, load_reference_bundle  # noqa: E402


def main() -> None:
    started = time.perf_counter()
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    kernel.run_24_hours()
    errors = kernel.state_integrity_errors()
    snapshot = kernel.snapshot()
    replayed = SimulationKernel.replay(bundle, kernel.firehose)
    replay_matches = replayed.state_checksum() == snapshot.state_checksum
    result = {
        "scenario_id": kernel.scenario_id,
        "population": bundle.population,
        "simulated_hours": bundle.manifest["duration_hours"],
        "events": len(kernel.firehose),
        "state_integrity_errors": errors,
        "state_checksum": snapshot.state_checksum,
        "replay_matches": replay_matches,
        "wall_clock_seconds": round(time.perf_counter() - started, 6),
        "external_network_dependencies": bundle.manifest["external_network_dependencies"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors or not replay_matches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
