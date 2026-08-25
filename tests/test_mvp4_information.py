from __future__ import annotations

from awg_mvp4 import InformationKernel


def _kernel() -> InformationKernel:
    kernel = InformationKernel()
    kernel.run_reference()
    return kernel


def test_observation_to_repost_chain_is_reconstructable() -> None:
    kernel = _kernel()
    types = [
        kernel.events[[item["event_id"] for item in kernel.events].index(event_id)]["event_type"]
        for event_id in kernel.lineage(kernel.chain_anchor)
    ]
    assert types[0] == "ObservationCreated"
    assert "ClaimAsserted" in types
    assert "MessageSent" in types
    assert "PostCreated" in types
    assert types[-1] == "PostReposted"


def test_belief_is_separate_from_truth_and_likes() -> None:
    kernel = _kernel()
    assert kernel.world_truth == "electrical transformer failure"
    assert kernel.believes(kernel.liker, kernel.claim_id) is False
    assert kernel.knows(kernel.liker, kernel.claim_id) is True
    assert kernel.participant_projection(kernel.liker)["world_truth"] is None
    assert kernel.analyst_projection()["world_truth"] == kernel.world_truth


def test_unexposed_agent_cannot_know_claim() -> None:
    kernel = _kernel()
    assert kernel.knows(kernel.outsider, kernel.claim_id) is False
    assert kernel.claim_id not in kernel.participant_projection(kernel.outsider)["exposed_claims"]
    assert "post:c-0003:001" not in kernel.feed_for(kernel.outsider)


def test_correction_preserves_original_history() -> None:
    kernel = _kernel()
    original = [event for event in kernel.events if event["event_type"] == "PostCreated"][0]
    correction = [event for event in kernel.events if event["event_type"] == "ClaimCorrected"][0]
    retraction = [event for event in kernel.events if event["event_type"] == "ClaimRetracted"][0]
    assert original["payload"]["content"] == "Explosion reported downtown."
    assert correction["payload"]["original_post_id"] == original["payload"]["post_id"]
    assert kernel.posts[original["payload"]["post_id"]]["content"] == original["payload"]["content"]
    assert retraction["payload"]["original_preserved"] is True


def test_reference_replay_and_budget() -> None:
    kernel = _kernel()
    replayed = InformationKernel.replay(kernel.events)
    assert len(kernel.actors) >= 100
    assert len(kernel.events) >= 1000
    assert replayed.state_checksum() == kernel.state_checksum()
    assert kernel.actors["org:news-desk"]["information_only"] is True
    assert kernel.actors["org:news-desk"]["embodiment"] == "none"
