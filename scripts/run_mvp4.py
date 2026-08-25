from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_mvp4 import InformationKernel  # noqa: E402


def main() -> None:
    started = time.monotonic()
    kernel = InformationKernel()
    kernel.run_reference()
    elapsed = time.monotonic() - started
    replayed = InformationKernel.replay(kernel.events)
    report = {
        "actors": len(kernel.actors),
        "events": len(kernel.events),
        "elapsed_seconds": round(elapsed, 6),
        "replay_matches": replayed.state_checksum() == kernel.state_checksum(),
        "outsider_knows_claim": kernel.knows(kernel.outsider, kernel.claim_id),
        "like_implies_belief": kernel.believes(kernel.liker, kernel.claim_id),
        "original_post_preserved": kernel.posts["post:c-0003:001"]["content"]
        == kernel.original_post["content"],
        "live_network": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if (
        report["actors"] < 100
        or report["events"] < 1000
        or elapsed >= 5
        or not report["replay_matches"]
        or report["outsider_knows_claim"]
        or report["like_implies_belief"]
        or not report["original_post_preserved"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
