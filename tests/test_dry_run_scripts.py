from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_manifest(tmp_path: Path) -> Path:
    payload_dir = tmp_path / "payloads"
    payload_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "usb_device": "/dev/sdz",
        "boot_mode": "uefi-native",
        "repo_root": str(REPO_ROOT),
        "payload_dir": str(payload_dir),
        "iso_dir": str(tmp_path / "images"),
        "format_mode": "full",
        "partitions": [
            {"name": "esp", "label": "ESP", "fs": "fat32", "size_gb": 0.5, "role": "efi"},
            {"name": "cache", "label": "CACHE", "fs": "ext4", "remainder": True, "role": "cache"},
        ],
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def test_partition_layout_dry_run_does_not_require_linux_block_device(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)

    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "partition-layout.sh"), "--manifest", str(manifest_path), "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Dry run enabled. No partitioning will occur." in result.stdout
    assert "Planned partitions:" in result.stdout


def test_sonic_stick_dry_run_does_not_require_linux_or_sudo(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)

    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "sonic-stick.sh"), "--manifest", str(manifest_path), "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "WARN Non-Linux dry-run mode enabled." in result.stdout
    assert "Sonic Stick Launcher" in result.stdout
    assert "Dry run enabled. No payloads will be written." in result.stdout
