from __future__ import annotations

from pathlib import Path

from services.manifest import validate_manifest_data


def test_validate_manifest_data_reports_missing_payloads_and_unknown_links(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    payload_dir = repo_root / "payloads"
    iso_dir = repo_root / "images"
    source_path = repo_root / "distribution" / "launchers" / "uhome" / "uhome-console.sh"

    payload_dir.mkdir(parents=True)
    iso_dir.mkdir(parents=True)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("#!/usr/bin/env bash\n", encoding="utf-8")

    manifest = {
        "usb_device": "/dev/sdz",
        "boot_mode": "uefi-native",
        "repo_root": str(repo_root),
        "payload_dir": str(payload_dir),
        "iso_dir": str(iso_dir),
        "format_mode": "full",
        "partitions": [
            {"name": "esp", "label": "ESP", "fs": "fat32", "size_gb": 0.5},
            {"name": "root", "label": "ROOT", "fs": "ext4", "size_gb": 8, "payload_dir": "rootfs"},
        ],
        "controller_mappings": [{"id": "pad-1", "driver": "xinput", "profile": "default"}],
        "navigation_modules": [
            {
                "id": "nav-1",
                "name": "Home",
                "shell": "console",
                "entrypoint": "/opt/sonic/home",
                "controller_mapping": "pad-1",
                "source_path": "distribution/launchers/uhome/uhome-console.sh",
            }
        ],
        "surfaces": [
            {
                "id": "surface-1",
                "name": "Main",
                "os": "linux",
                "kind": "service",
                "boot_target": "boot-1",
                "controller_mapping": "pad-1",
                "partition_refs": ["root", "missing"],
                "navigation_modules": ["nav-1", "missing-nav"],
            }
        ],
        "boot_targets": [
            {
                "id": "boot-1",
                "name": "Main Boot",
                "surface_id": "surface-1",
                "os": "linux",
                "bootloader": "grub",
                "chain": "linux-efi",
                "default": True,
                "entry_partition": "missing-partition",
            }
        ],
    }

    result = validate_manifest_data(manifest)

    assert result["ok"] is False
    assert "surface 'surface-1' references unknown partition 'missing'" in result["errors"]
    assert "surface 'surface-1' references unknown navigation module 'missing-nav'" in result["errors"]
    assert "boot target 'boot-1' references unknown entry_partition 'missing-partition'" in result["errors"]
    assert result["summary"]["partition_count"] == 2
    assert result["summary"]["surface_count"] == 1
    assert result["summary"]["boot_target_count"] == 1
    assert result["summary"]["missing_payload_references"] == 1
    assert any("missing payload reference: root:payload_dir:" in warning for warning in result["warnings"])


def test_validate_manifest_data_rejects_duplicate_defaults_and_bad_modes(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    payload_dir = repo_root / "payloads"
    iso_dir = repo_root / "images"

    payload_dir.mkdir(parents=True)
    iso_dir.mkdir(parents=True)

    manifest = {
        "usb_device": "disk1",
        "boot_mode": "bios",
        "repo_root": str(repo_root),
        "payload_dir": str(payload_dir),
        "iso_dir": str(iso_dir),
        "format_mode": "partial",
        "partitions": [
            {"name": "esp", "label": "ESP", "fs": "fat32", "size_gb": 0.5},
            {"name": "cache", "label": "CACHE", "fs": "ext4", "remainder": True},
        ],
        "controller_mappings": [{"id": "pad-1", "driver": "xinput", "profile": "default"}],
        "navigation_modules": [
            {
                "id": "nav-1",
                "name": "Home",
                "shell": "console",
                "entrypoint": "/opt/sonic/home",
                "controller_mapping": "pad-1",
            }
        ],
        "surfaces": [
            {
                "id": "surface-1",
                "name": "Main",
                "os": "linux",
                "kind": "service",
                "boot_target": "boot-1",
                "controller_mapping": "pad-1",
                "partition_refs": ["cache"],
                "navigation_modules": ["nav-1"],
            }
        ],
        "boot_targets": [
            {
                "id": "boot-1",
                "name": "Main Boot",
                "surface_id": "surface-1",
                "os": "linux",
                "bootloader": "grub",
                "chain": "linux-efi",
                "default": True,
                "entry_partition": "esp",
            },
            {
                "id": "boot-2",
                "name": "Backup Boot",
                "surface_id": "surface-1",
                "os": "linux",
                "bootloader": "grub",
                "chain": "linux-efi",
                "default": True,
                "entry_partition": "esp",
            },
        ],
    }

    result = validate_manifest_data(manifest)

    assert result["ok"] is False
    assert "unsupported boot_mode 'bios'" in result["errors"]
    assert "unsupported format_mode 'partial'" in result["errors"]
    assert "only one boot target may be marked default" in result["errors"]
    assert "usb_device 'disk1' is not a Linux block-device path" in result["warnings"]
