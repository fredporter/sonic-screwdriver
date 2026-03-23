from __future__ import annotations

import json

from services.mcp_server import PROTOCOL_VERSION, SERVER_INFO, SonicMcpServer


class _FakeService:
    def __init__(self) -> None:
        self.last_devices_args: dict[str, object] | None = None
        self.last_manifest_path: str | None = None

    def get_health(self) -> dict[str, object]:
        return {"ok": True, "service": "health"}

    def get_gui_summary(self) -> dict[str, object]:
        return {"ok": True, "service": "gui"}

    def list_devices(self, **kwargs: object) -> dict[str, object]:
        self.last_devices_args = kwargs
        return {"ok": True, "items": [{"id": "device-1"}], "total": 1}

    def get_schema(self) -> dict[str, object]:
        return {"ok": True, "schema": {"type": "object"}}

    def get_db_status(self) -> dict[str, object]:
        return {"ok": True, "summary": {"device_count": 1}}

    def rebuild_db(self) -> dict[str, object]:
        return {"ok": True, "action": "rebuild"}

    def bootstrap_current_machine(self) -> dict[str, object]:
        return {"ok": True, "action": "bootstrap"}

    def build_plan(self, **kwargs: object) -> dict[str, object]:
        return {"ok": True, "action": "plan", "args": kwargs}

    def get_manifest_status(self, path: str | None = None) -> dict[str, object]:
        self.last_manifest_path = path
        return {"ok": False, "errors": ["bad manifest"]}


def test_initialize_and_tools_list_return_expected_contract() -> None:
    server = SonicMcpServer()
    server.service = _FakeService()

    init_response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    tools_response = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})

    assert init_response["result"]["protocolVersion"] == PROTOCOL_VERSION
    assert init_response["result"]["serverInfo"] == SERVER_INFO
    tool_names = [tool["name"] for tool in tools_response["result"]["tools"]]
    assert "sonic_plan" in tool_names
    assert "sonic_devices" in tool_names
    assert "sonic_manifest_verify" in tool_names


def test_tools_call_returns_structured_content_and_error_flag() -> None:
    server = SonicMcpServer()
    fake_service = _FakeService()
    server.service = fake_service

    devices_response = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "sonic_devices",
                "arguments": {"vendor": "Acme", "limit": 5, "offset": 10},
            },
        }
    )
    manifest_response = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "sonic_manifest_verify",
                "arguments": {"path": "memory/sonic/sonic-manifest.json"},
            },
        }
    )

    assert fake_service.last_devices_args == {
        "vendor": "Acme",
        "reflash_potential": None,
        "usb_boot": None,
        "uefi_native": None,
        "limit": 5,
        "offset": 10,
    }
    assert devices_response["result"]["structuredContent"]["items"] == [{"id": "device-1"}]
    assert devices_response["result"]["content"][0]["text"] == json.dumps(
        devices_response["result"]["structuredContent"], indent=2
    )
    assert devices_response["result"]["isError"] is False

    assert fake_service.last_manifest_path == "memory/sonic/sonic-manifest.json"
    assert manifest_response["result"]["structuredContent"]["errors"] == ["bad manifest"]
    assert manifest_response["result"]["isError"] is True
