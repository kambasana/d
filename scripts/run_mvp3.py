from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_mvp3 import CAPABILITIES, OllamaAdapter, RecordedTransport  # noqa: E402


def output_for(capability: str) -> dict:
    proposals = {
        "propose_intent": {
            "proposal_type": "IntentProposed",
            "intent_kind": "wait",
            "parameters": {"duration_seconds": 60},
        },
        "rank_options": {
            "proposal_type": "OptionRanking",
            "ranked_options": [{"option_id": "wait", "score": 1.0}],
        },
        "realize_dialogue": {
            "proposal_type": "DialogueRealization",
            "text": "I will wait here.",
        },
        "summarize_memories": {
            "proposal_type": "MemorySummaryDraft",
            "summary": "The actor waited at the observed place.",
        },
        "extract_claims": {
            "proposal_type": "ClaimDrafts",
            "claims": [{"text": "The actor said they would wait."}],
        },
    }
    return {
        "schema_version": "0.2.0",
        "capability": capability,
        "proposal": proposals[capability],
    }


def main() -> None:
    records = {
        f"recorded-{index:02d}": output_for(CAPABILITIES[index % len(CAPABILITIES)])
        for index in range(20)
    }
    transport = RecordedTransport(records)
    adapter = OllamaAdapter(
        model_version="recorded-model-v1",
        prompt_policy_version="mvp3-policy-v1",
        transport=transport,
    )
    started = time.monotonic()
    results = []
    for index in range(20):
        capability = CAPABILITIES[index % len(CAPABILITIES)]
        method = getattr(adapter, capability)
        results.append(method(f"recorded-{index:02d}", {"observations": []}))
    elapsed = time.monotonic() - started
    report = {
        "accepted": sum(result.accepted for result in results),
        "calls": transport.calls,
        "elapsed_seconds": round(elapsed, 6),
        "live_provider_calls": 0,
        "provider": adapter.provider_id,
        "replay_within_budget": elapsed < 5.0,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["accepted"] != 20 or not report["replay_within_budget"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
