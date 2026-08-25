from __future__ import annotations

from datetime import timedelta

import pytest

from awg_mvp1.kernel import CommandRejected
from awg_mvp2 import NpcKernel


def _bootstrapped() -> NpcKernel:
    kernel = NpcKernel()
    kernel.run_until(kernel.now)
    return kernel


def test_daily_activity_without_llm() -> None:
    kernel = NpcKernel()
    kernel.run_24_hours()
    places = kernel.daily_place_counts()
    assert kernel.bundle.population == 100
    assert min(places.values()) >= 2
    assert any(event.event_type == "ResourceConsumed" for event in kernel.firehose)
    assert any(event.event_type == "ActionStarted" and event.payload.get("action") == "work" for event in kernel.firehose)
    assert kernel.state_integrity_errors() == []
    replayed = NpcKernel.replay(kernel.bundle, kernel.firehose)
    assert replayed.state_checksum() == kernel.state_checksum()


def test_impossible_concurrent_actions_are_blocked() -> None:
    kernel = _bootstrapped()
    agent_id = "agent:district-0000"
    kernel._claim_channels(agent_id, "sleep", "command:test-sleep")
    with pytest.raises(CommandRejected, match="conflicts with occupied channels"):
        kernel.start_travel(agent_id, "place:office")
    kernel._release_channels(agent_id, "sleep", "command:test-sleep")
    kernel._claim_channels(agent_id, "eat", "command:test-eat")
    with pytest.raises(CommandRejected, match="conflicts with occupied channels"):
        kernel._claim_channels(agent_id, "work", "command:test-work")


def test_exclusive_reservation_and_resource_conservation() -> None:
    kernel = _bootstrapped()
    start = kernel.resource_totals()
    assert start["token"] == 20 * 100 + 1000 + 50
    assert start["meal"] == 100

    kernel.transfer_resource("agent:district-0000", "agent:district-0001", "token", 5)
    assert kernel.resource_totals() == start
    assert kernel._inventories["agent:district-0000"]["token"] == 15
    assert kernel._inventories["agent:district-0001"]["token"] == 25

    with pytest.raises(CommandRejected, match="insufficient resources"):
        kernel.transfer_resource("agent:district-0000", "agent:district-0001", "token", 100)
    with pytest.raises(CommandRejected, match="at least 1"):
        kernel.transfer_resource("agent:district-0000", "agent:district-0001", "token", 0)

    kernel.transfer_resource(
        "org:civic-office",
        "agent:district-0000",
        "unique_asset",
        1,
        asset_id="asset:office-key-01",
    )
    assert kernel._owners["asset:office-key-01"] == "agent:district-0000"
    with pytest.raises(CommandRejected, match="does not own"):
        kernel.transfer_resource(
            "org:civic-office",
            "agent:district-0001",
            "unique_asset",
            1,
            asset_id="asset:office-key-01",
        )

    first = "agent:district-0000"
    second = "agent:district-0002"
    kernel.start_travel(first, "place:cafe")
    kernel.start_travel(second, "place:cafe")
    kernel.run_until(kernel.now + timedelta(hours=1))
    kernel.reserve_slot(first, "object:cafe-counter")
    with pytest.raises(CommandRejected, match="already reserved"):
        kernel.reserve_slot(second, "object:cafe-counter")
    assert kernel.resource_totals()["token"] == start["token"]
    assert kernel.state_integrity_errors() == []


def test_perception_does_not_leak_global_state() -> None:
    kernel = _bootstrapped()
    traveler = "agent:district-0000"
    witness = "agent:district-0002"
    outsider = "agent:district-0001"
    kernel.start_travel(traveler, "place:office")
    kernel.run_until(kernel.now + timedelta(hours=1))
    entered = next(
        event
        for event in kernel.firehose
        if event.event_type == "LocationEntered" and event.actor_id == traveler
    )
    exited = next(
        event
        for event in kernel.firehose
        if event.event_type == "LocationExited" and event.actor_id == traveler
    )
    assert kernel.knows(traveler, entered.event_id)
    assert kernel.knows(witness, exited.event_id)
    assert not kernel.knows(witness, entered.event_id)
    assert not kernel.knows(outsider, entered.event_id)
    assert not kernel.knows(outsider, exited.event_id)
    office_inventory_events = [
        event.event_id
        for event in kernel.firehose
        if event.event_type == "ResourceGranted" and event.payload.get("holder_id") == "org:civic-office"
    ]
    assert office_inventory_events
    assert not kernel.knows(outsider, office_inventory_events[0])
