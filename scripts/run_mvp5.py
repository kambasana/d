from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_mvp5.scale import ScaleKernel, compare_branches  # noqa: E402


def main() -> None:
    kernel = ScaleKernel()
    before = kernel.totals()["token_sum"]
    kernel.run_profile()
    comparison = compare_branches()
    report = {
        "population_records": kernel.totals()["population_records"],
        "active_cognition": 50,
        "token_sum_before": before,
        "token_sum_after": kernel.totals()["token_sum"],
        "comparison": comparison,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if (
        report["population_records"] != 1000
        or report["token_sum_before"] != report["token_sum_after"]
        or not comparison["effect_is_not_seed_noise"]
        or not comparison["tokens_conserved"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
