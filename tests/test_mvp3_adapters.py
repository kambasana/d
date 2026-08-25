from __future__ import annotations

from typing import Any, Mapping

from awg_mvp2 import NpcKernel
from awg_mvp3 import CAPABILITIES, OllamaAdapter, OpenRouterAdapter, RecordedTransport


def output_for(capability: str) -> dict[str, Any]:
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


def adapter(adapter_type, records: Mapping[str, Any]):
    return adapter_type(
        model_version="recorded-model-v1",
        prompt_policy_version="mvp3-policy-v1",
        transport=RecordedTransport(records),
    )


def test_provider_swap_preserves_domain_schema() -> None:
    record = {"swap": output_for("propose_intent")}
    ollama = adapter(OllamaAdapter, record).propose_intent("swap", {})
    openrouter = adapter(OpenRouterAdapter, record).propose_intent("swap", {})

    assert ollama.accepted and openrouter.accepted
    assert ollama.proposal == openrouter.proposal
    assert ollama.as_dict().keys() == openrouter.as_dict().keys()
    assert ollama.provenance.provider_id != openrouter.provenance.provider_id


def test_invalid_or_timed_out_output_cannot_mutate_world() -> None:
    kernel = NpcKernel()
    before = kernel.state_checksum()
    before_events = kernel.firehose

    class TimeoutTransport:
        def __call__(self, request, timeout_seconds):
            raise TimeoutError

    failures = [
        OllamaAdapter(
            model_version="recorded-model-v1",
            prompt_policy_version="mvp3-policy-v1",
            transport=TimeoutTransport(),
        ).propose_intent("timeout", {}),
        adapter(OllamaAdapter, {"malformed": "not-json"}).propose_intent("malformed", {}),
        adapter(
            OllamaAdapter,
            {"schema": {**output_for("propose_intent"), "schema_version": "99"}},
        ).propose_intent("schema", {}),
    ]

    assert all(not result.accepted and result.proposal is None for result in failures)
    assert kernel.state_checksum() == before
    assert kernel.firehose == before_events


def test_recorded_outputs_replay_without_provider_calls() -> None:
    records = {
        f"recorded-{index:02d}": output_for(CAPABILITIES[index % len(CAPABILITIES)])
        for index in range(20)
    }
    first_transport = RecordedTransport(records)
    second_transport = RecordedTransport(records)
    first = OllamaAdapter(
        model_version="recorded-model-v1",
        prompt_policy_version="mvp3-policy-v1",
        transport=first_transport,
    )
    replay = OllamaAdapter(
        model_version="recorded-model-v1",
        prompt_policy_version="mvp3-policy-v1",
        transport=second_transport,
    )

    def run(current):
        return [
            getattr(current, CAPABILITIES[index % len(CAPABILITIES)])(
                f"recorded-{index:02d}", {"observations": []}
            ).as_dict()
            for index in range(20)
        ]

    assert run(first) == run(replay)
    assert first_transport.calls == second_transport.calls == 20


def test_model_output_provenance_is_complete() -> None:
    accepted = adapter(
        OpenRouterAdapter, {"accepted": output_for("realize_dialogue")}
    ).realize_dialogue("accepted", {})
    rejected = adapter(OpenRouterAdapter, {"rejected": "{}"}).realize_dialogue("rejected", {})

    expected = {
        "adapter_id",
        "adapter_version",
        "provider_id",
        "model_version",
        "prompt_policy_version",
        "interface_version",
        "output_schema_version",
        "request_id",
        "outcome",
    }
    assert expected == accepted.as_dict()["provenance"].keys()
    assert expected == rejected.as_dict()["provenance"].keys()
    assert accepted.provenance.outcome == "accepted"
    assert rejected.provenance.outcome == "invalid_output"
