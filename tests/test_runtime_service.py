from __future__ import annotations

from pathlib import Path

import pytest

from services import runtime_service


def test_build_plan_rejects_unsupported_platform_for_non_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    service = runtime_service.SonicService(repo_root=Path("/tmp/sonic"))
    monkeypatch.setattr(runtime_service, "is_supported", lambda: False)

    with pytest.raises(ValueError, match="Unsupported OS for build operations. Use Linux."):
        service.build_plan(dry_run=False)


def test_build_plan_allows_unsupported_platform_for_dry_run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    service = runtime_service.SonicService(repo_root=tmp_path)
    calls: dict[str, object] = {}

    monkeypatch.setattr(runtime_service, "is_supported", lambda: False)

    def fake_write_plan(**kwargs: object) -> dict[str, object]:
        calls.update(kwargs)
        return {"usb_device": kwargs["usb_device"], "dry_run": kwargs["dry_run"]}

    monkeypatch.setattr(runtime_service, "write_plan", fake_write_plan)

    result = service.build_plan(dry_run=True, out="memory/sonic/manifest.json")

    assert result["ok"] is True
    assert calls["dry_run"] is True


def test_build_plan_resolves_repo_relative_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    service = runtime_service.SonicService(repo_root=tmp_path)
    calls: dict[str, object] = {}

    monkeypatch.setattr(runtime_service, "is_supported", lambda: True)

    def fake_write_plan(**kwargs: object) -> dict[str, object]:
        calls.update(kwargs)
        return {"usb_device": kwargs["usb_device"], "dry_run": kwargs["dry_run"]}

    monkeypatch.setattr(runtime_service, "write_plan", fake_write_plan)

    result = service.build_plan(
        usb_device="/dev/sdz",
        dry_run=True,
        layout_file="config/custom-layout.json",
        out="memory/sonic/custom-manifest.json",
        payloads_dir="memory/sonic/artifacts/custom",
        format_mode="skip",
    )

    assert result["ok"] is True
    assert result["manifest_path"] == str(tmp_path / "memory" / "sonic" / "custom-manifest.json")
    assert calls["repo_root"] == tmp_path
    assert calls["layout_path"] == tmp_path / "config" / "custom-layout.json"
    assert calls["out_path"] == tmp_path / "memory" / "sonic" / "custom-manifest.json"
    assert calls["payload_dir"] == tmp_path / "memory" / "sonic" / "artifacts" / "custom"
    assert calls["format_mode"] == "skip"


def test_list_devices_merges_user_overlay_and_applies_pagination(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    service = runtime_service.SonicService(repo_root=tmp_path)

    seed_rows = [
        {"id": "device-b", "vendor": "Acme", "reflash_potential": "high", "usb_boot": "yes", "uefi_native": "yes"},
        {"id": "device-a", "vendor": "Acme", "reflash_potential": "low", "usb_boot": "no", "uefi_native": "yes"},
    ]
    user_rows = [
        {
            "id": "device-a",
            "vendor": "Overlay Corp",
            "reflash_potential": "medium",
            "usb_boot": "yes",
            "uefi_native": "yes",
        },
        {"id": "device-c", "vendor": "Other", "reflash_potential": "medium", "usb_boot": "yes", "uefi_native": "no"},
    ]

    monkeypatch.setattr(service, "_ensure_seed_catalog", lambda force=False: None)
    monkeypatch.setattr(
        service,
        "_load_device_rows",
        lambda path: seed_rows if path == service.seed_db_path else user_rows if path == service.user_db_path else [],
    )

    result = service.list_devices(vendor="overlay corp", usb_boot="YES", limit=1, offset=0)

    assert result["ok"] is True
    assert result["total"] == 1
    assert result["limit"] == 1
    assert result["offset"] == 0
    assert result["items"] == [user_rows[0]]


def test_build_plan_and_verify_manifest_end_to_end(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo_root = tmp_path
    manifest_path = repo_root / "memory" / "sonic" / "generated-manifest.json"
    payload_dir = repo_root / "memory" / "sonic" / "artifacts" / "payloads"
    iso_dir = repo_root / "memory" / "sonic" / "artifacts" / "images"

    for path in (
        repo_root / "distribution" / "launchers" / "uhome" / "uhome-console.sh",
        repo_root / "distribution" / "launchers" / "windows" / "WindowsHome.cmd",
        repo_root / "distribution" / "launchers" / "windows" / "WindowsLibrary.cmd",
        repo_root / "distribution" / "launchers" / "windows" / "WindowsSettings.cmd",
        payload_dir,
        iso_dir,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix:
            path.write_text("stub\n", encoding="utf-8")

    service = runtime_service.SonicService(repo_root=repo_root)
    monkeypatch.setattr(runtime_service, "is_supported", lambda: True)

    result = service.build_plan(dry_run=True, out=str(manifest_path))

    assert result["ok"] is True
    assert manifest_path.exists()

    status = service.get_manifest_status(str(manifest_path))

    assert status["ok"] is True
    assert status["summary"]["partition_count"] == 8
    assert status["summary"]["surface_count"] == 2
    assert status["summary"]["boot_target_count"] == 2
    assert status["summary"]["missing_payload_references"] > 0
