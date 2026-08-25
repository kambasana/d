from __future__ import annotations

import json
import mimetypes
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .bundle import ReviewBundle, load_review_bundle
from .projections import ui_review_bundle, world_projection

ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = ROOT / "apps" / "world-explorer" / "dist"
PMTILES_PATH = ROOT / "examples" / "mvp1-district" / "reference-district.pmtiles"
MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


class _BundleHolder:
    bundle: ReviewBundle | None = None
    ui_bundle: dict[str, Any] | None = None


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("X-AWG-Read-Only", "true")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
    handler.end_headers()
    handler.wfile.write(body)


def _error(handler: BaseHTTPRequestHandler, status: int, message: str) -> None:
    _json_response(handler, status, {"error": message, "read_only": True})


def _parse_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    return int(value)


class WorldExplorerHandler(BaseHTTPRequestHandler):
    server_version = "AWGWorldExplorer/0.2.0"

    @property
    def review_bundle(self) -> ReviewBundle:
        holder = self.server.bundle_holder  # type: ignore[attr-defined]
        if holder.bundle is None:
            holder.bundle = load_review_bundle()
        return holder.bundle

    @property
    def review_payload(self) -> dict[str, Any]:
        holder = self.server.bundle_holder  # type: ignore[attr-defined]
        if holder.ui_bundle is None:
            holder.ui_bundle = ui_review_bundle(self.review_bundle)
        return holder.ui_bundle

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.end_headers()

    def do_HEAD(self) -> None:
        if self.path.startswith("/api/") or self.path == "/health":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("X-AWG-Read-Only", "true")
            self.end_headers()
            return
        if STATIC_ROOT.is_dir():
            target = self._static_target()
            if target and target.is_file():
                self.send_response(HTTPStatus.OK)
                content_type, _ = mimetypes.guess_type(str(target))
                self.send_header("Content-Type", content_type or "application/octet-stream")
                self.end_headers()
                return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path
        query = parse_qs(parsed.query)

        if route == "/health":
            _json_response(
                self,
                HTTPStatus.OK,
                {"status": "ok", "read_only": True, "service": "world-explorer"},
            )
            return

        if route == "/api/review-bundle":
            _json_response(self, HTTPStatus.OK, self.review_payload)
            return

        if route == "/api/v1/context":
            _json_response(self, HTTPStatus.OK, self.review_bundle.context())
            return

        if route == "/api/v1/status":
            _json_response(self, HTTPStatus.OK, self.review_bundle.status())
            return

        if route == "/api/v1/world":
            simulation_time = (query.get("simulation_time") or [self.review_bundle.end_time])[0]
            zoom = _parse_int((query.get("zoom") or ["14"])[0], 14)
            building_id = (query.get("building_id") or [None])[0]
            try:
                payload = world_projection(
                    self.review_bundle,
                    simulation_time=simulation_time,
                    zoom=zoom,
                    building_id=building_id,
                )
            except ValueError as exc:
                _error(self, HTTPStatus.BAD_REQUEST, str(exc))
                return
            _json_response(self, HTTPStatus.OK, payload)
            return

        if route == "/api/v1/firehose":
            from_sequence = _parse_int((query.get("from_sequence") or ["1"])[0], 1)
            limit = _parse_int((query.get("limit") or ["50"])[0], 50)
            world_id = (query.get("world_id") or [None])[0]
            _json_response(
                self,
                HTTPStatus.OK,
                self.review_bundle.firehose_page(
                    from_sequence=from_sequence,
                    limit=limit,
                    world_id=world_id,
                ),
            )
            return

        if route == "/api/v1/timeline":
            _json_response(self, HTTPStatus.OK, self.review_bundle.timeline_summary())
            return

        if route == "/api/v1/information":
            agent_id = (query.get("agent_id") or [None])[0]
            mode = (query.get("mode") or ["participant"])[0]
            if mode not in {"participant", "analyst"}:
                _error(self, HTTPStatus.BAD_REQUEST, "mode must be participant or analyst")
                return
            _json_response(
                self,
                HTTPStatus.OK,
                self.review_bundle.information_summary(agent_id=agent_id, mode=mode),
            )
            return

        if route == "/api/v1/scale":
            _json_response(self, HTTPStatus.OK, self.review_bundle.scale_summary())
            return

        if route == "/assets/reference-district.pmtiles":
            if not PMTILES_PATH.is_file():
                _error(self, HTTPStatus.NOT_FOUND, "pmtiles archive missing")
                return
            content = PMTILES_PATH.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/vnd.pmtiles")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-AWG-Read-Only", "true")
            self.send_header("X-AWG-Authority", "presentation_only")
            self.end_headers()
            self.wfile.write(content)
            return

        if STATIC_ROOT.is_dir():
            target = self._static_target(route)
            if target and target.is_file():
                self._serve_static(target)
                return
            if route in {"/", ""} and (STATIC_ROOT / "index.html").is_file():
                self._serve_static(STATIC_ROOT / "index.html")
                return

        _error(self, HTTPStatus.NOT_FOUND, "route not found")

    def _static_target(self, route: str | None = None) -> Path | None:
        requested = route if route is not None else urlparse(self.path).path
        if requested in {"/", ""}:
            candidate = STATIC_ROOT / "index.html"
            return candidate if candidate.is_file() else None
        relative = requested.lstrip("/")
        candidate = (STATIC_ROOT / relative).resolve()
        if candidate == STATIC_ROOT or STATIC_ROOT not in candidate.parents:
            return None
        return candidate

    def _serve_static(self, target: Path) -> None:
        content = target.read_bytes()
        content_type, _ = mimetypes.guess_type(str(target))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-AWG-Read-Only", "true")
        self.end_headers()
        self.wfile.write(content)

    def _unsupported(self) -> None:
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header("Allow", "GET, HEAD, OPTIONS")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body = json.dumps(
            {"error": "mutating methods are not supported", "read_only": True},
            sort_keys=True,
        ).encode("utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        self._unsupported()

    def do_PUT(self) -> None:
        self._unsupported()

    def do_PATCH(self) -> None:
        self._unsupported()

    def do_DELETE(self) -> None:
        self._unsupported()


def serve(host: str = "127.0.0.1", port: int = 8765, *, bundle: ReviewBundle | None = None) -> None:
    holder = _BundleHolder()
    holder.bundle = bundle
    server = ThreadingHTTPServer((host, port), WorldExplorerHandler)
    server.bundle_holder = holder  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        thread.join()
    except KeyboardInterrupt:
        server.shutdown()
