from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from services.http_api import SonicApiHandler


class _FakeService:
    def __init__(self) -> None:
        self.last_list_devices_args: dict[str, object] | None = None
        self.last_manifest_path: str | None = None

    def get_health(self) -> dict[str, object]:
        return {"ok": False}

    def get_gui_summary(self) -> dict[str, object]:
        return {"ok": True}

    def list_devices(self, **_: object) -> dict[str, object]:
        self.last_list_devices_args = _
        return {"ok": True, "items": []}

    def get_schema(self) -> dict[str, object]:
        return {"ok": True, "schema": {}}

    def get_db_status(self) -> dict[str, object]:
        return {"ok": True}

    def export_db(self) -> dict[str, object]:
        return {"ok": True, "items": []}

    def get_manifest_status(self, _: str | None = None) -> dict[str, object]:
        self.last_manifest_path = _
        return {"ok": False}

    def rebuild_db(self) -> dict[str, object]:
        return {"ok": True}

    def bootstrap_current_machine(self) -> dict[str, object]:
        return {"ok": True}

    def build_plan(self, **_: object) -> dict[str, object]:
        raise ValueError("Unsupported OS for build operations. Use Linux.")


def _start_test_server(service: object) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    class BoundHandler(SonicApiHandler):
        pass

    BoundHandler.service = service
    server = ThreadingHTTPServer(("127.0.0.1", 0), BoundHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, thread, f"http://{host}:{port}"


def test_plan_endpoint_returns_400_for_unsupported_builds() -> None:
    server, thread, base_url = _start_test_server(_FakeService())
    try:
        request = urllib.request.Request(
            f"{base_url}/api/sonic/plan",
            data=json.dumps({"usb_device": "/dev/sdb", "dry_run": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(request)

        assert exc_info.value.code == 400
        payload = json.loads(exc_info.value.read().decode("utf-8"))
        assert payload == {"ok": False, "error": "Unsupported OS for build operations. Use Linux."}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_get_endpoints_return_expected_contracts() -> None:
    service = _FakeService()
    server, thread, base_url = _start_test_server(service)
    try:
        devices = json.loads(
            urllib.request.urlopen(
                f"{base_url}/api/sonic/devices?vendor=Acme&usb_boot=yes&limit=5&offset=10",
                timeout=3,
            ).read().decode("utf-8")
        )
        schema = json.loads(urllib.request.urlopen(f"{base_url}/api/sonic/schema", timeout=3).read().decode("utf-8"))
        manifest = json.loads(
            urllib.request.urlopen(
                f"{base_url}/api/sonic/manifest/verify?path=memory/sonic/custom.json",
                timeout=3,
            ).read().decode("utf-8")
        )

        assert devices == {"ok": True, "items": []}
        assert service.last_list_devices_args == {
            "vendor": "Acme",
            "reflash_potential": None,
            "usb_boot": "yes",
            "uefi_native": None,
            "limit": 5,
            "offset": 10,
        }
        assert schema == {"ok": True, "schema": {}}
        assert manifest == {"ok": False}
        assert service.last_manifest_path == "memory/sonic/custom.json"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_bootstrap_endpoint_returns_service_payload() -> None:
    server, thread, base_url = _start_test_server(_FakeService())
    try:
        request = urllib.request.Request(
            f"{base_url}/api/sonic/bootstrap/current",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        payload = json.loads(urllib.request.urlopen(request, timeout=3).read().decode("utf-8"))

        assert payload == {"ok": True}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
