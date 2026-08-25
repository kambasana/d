from __future__ import annotations

import json
import socket
import threading
import urllib.error
import urllib.request
from http import HTTPStatus

from datetime import timedelta

import pytest

from awg_mvp1.kernel import _format_time, _parse_time
from awg_world_explorer import load_review_bundle, ui_review_bundle
from awg_world_explorer.projections import world_projection
from awg_world_explorer.server import WorldExplorerHandler, _BundleHolder
from http.server import ThreadingHTTPServer


def _start_server(bundle):
    holder = _BundleHolder()
    holder.bundle = bundle
    server = ThreadingHTTPServer(("127.0.0.1", 0), WorldExplorerHandler)
    server.bundle_holder = holder
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


def _get(url: str) -> tuple[int, dict]:
    with urllib.request.urlopen(url) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _request(method: str, url: str) -> int:
    request = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code


@pytest.fixture(scope="module")
def review_bundle():
    return load_review_bundle()


@pytest.fixture(scope="module")
def server_url(review_bundle):
    server, base = _start_server(review_bundle)
    yield base
    server.shutdown()


def test_review_bundle_preserves_invariants(review_bundle) -> None:
    context = review_bundle.context()
    assert context["read_only"] is True
    assert context["mutation_allowed"] is False
    assert set(context["invariants_preserved"]) >= {
        "INV-001",
        "INV-006",
        "INV-007",
        "INV-011",
        "INV-016",
    }
    assert context["external_network_dependencies"] == []
    assert context["pmtiles_authority"] == "presentation_only"


def test_world_projection_is_read_only(review_bundle) -> None:
    mid_time = _format_time(
        _parse_time(review_bundle.start_time) + timedelta(hours=10)
    )
    checksum = review_bundle.spatial_kernel_at(mid_time).state_checksum()
    payload = world_projection(
        review_bundle,
        simulation_time=mid_time,
        zoom=14,
        building_id="building:office",
    )
    assert payload["read_only"] is True
    assert payload["cluster_position_authority"] == "projection_only"
    assert payload["building_occupancy"]["occupant_count"] == 50
    assert review_bundle.spatial_kernel_at(mid_time).state_checksum() == checksum


def test_information_summary_separates_truth_and_belief(review_bundle) -> None:
    participant = review_bundle.information_summary(agent_id=review_bundle._mvp4_kernel.outsider)
    analyst = review_bundle.information_summary(mode="analyst")
    assert participant["projection"]["world_truth"] is None
    assert participant["world_truth_exposed"] is False
    assert analyst["projection"]["world_truth"] is not None
    assert participant["likes_are_not_belief"] is True


def test_scale_summary_reports_separate_counts(review_bundle) -> None:
    summary = review_bundle.scale_summary()
    assert summary["population_separate_from_active_cognition"] is True
    assert summary["totals"]["population_records"] == 1000
    assert summary["branch_comparison"]["tokens_conserved"] is True


def test_health_endpoint(server_url) -> None:
    status, payload = _get(f"{server_url}/health")
    assert status == HTTPStatus.OK
    assert payload["status"] == "ok"
    assert payload["read_only"] is True


def test_context_and_status_endpoints(server_url, review_bundle) -> None:
    _, context = _get(f"{server_url}/api/v1/context")
    _, status_payload = _get(f"{server_url}/api/v1/status")
    assert context["bundle_id"] == review_bundle.bundle_id
    assert status_payload["healthy"] is True
    assert status_payload["event_counts"]["spatial"] == 1400


def test_world_firehose_timeline_information_scale_endpoints(server_url, review_bundle) -> None:
    _, world = _get(
        f"{server_url}/api/v1/world?simulation_time={review_bundle.end_time}&zoom=14&building_id=building:office"
    )
    _, firehose = _get(f"{server_url}/api/v1/firehose?limit=5")
    _, timeline = _get(f"{server_url}/api/v1/timeline")
    _, information = _get(f"{server_url}/api/v1/information?mode=participant")
    _, scale = _get(f"{server_url}/api/v1/scale")

    assert world["agents"]
    assert world["clusters"]
    assert firehose["returned"] == 5
    assert timeline["event_totals"]["spatial"] == 1400
    assert information["mode"] == "participant"
    assert scale["totals"]["population_records"] == 1000


def test_review_bundle_endpoint_matches_ui_contract(server_url, review_bundle) -> None:
    status, payload = _get(f"{server_url}/api/review-bundle")
    local = ui_review_bundle(review_bundle)
    assert status == HTTPStatus.OK
    assert payload["bundle_id"] == review_bundle.bundle_id
    assert payload["read_only"] is True
    assert payload["mutation_allowed"] is False
    assert payload["map_projection"]["authority"] == "projection_only"
    assert payload["agents"]
    assert payload["clusters"]
    assert payload["firehose"]
    assert payload["timeline"]["ticks"]
    assert payload["world"]["agent_count"] == len(payload["agents"])
    assert payload["scale_summary"]["population_total"] == 1000
    assert local["bundle_id"] == payload["bundle_id"]


def test_mutating_methods_return_405(server_url) -> None:
    for method in ("POST", "PUT", "PATCH", "DELETE"):
        assert _request(method, f"{server_url}/api/v1/context") == HTTPStatus.METHOD_NOT_ALLOWED
        assert _request(method, f"{server_url}/api/review-bundle") == HTTPStatus.METHOD_NOT_ALLOWED


def test_offline_bundle_build_rejects_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def network_denied(*args: object, **kwargs: object) -> None:
        raise AssertionError("World Explorer attempted external networking")

    monkeypatch.setattr(socket, "create_connection", network_denied)
    bundle = load_review_bundle()
    assert bundle.context()["external_network_dependencies"] == []
