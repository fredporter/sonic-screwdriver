#!/usr/bin/env python3
"""Reference custom build-engine example for Sonic manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class CustomBuildEngine:
    """Builds a staged execution plan from a Sonic manifest payload."""

    def __init__(self, manifest: dict[str, Any], *, dry_run: bool = False) -> None:
        self.manifest = manifest
        self.dry_run = dry_run

    def build(self) -> dict[str, Any]:
        return {
            "profile": self.manifest.get("install_profile", "unknown"),
            "usb_device": self.manifest.get("usb_device", "unknown"),
            "dry_run": self.dry_run,
            "stages": {
                "partition": self._partition_stage(),
                "payload": self._payload_stage(),
                "boot": self._boot_stage(),
            },
        }

    def _partition_stage(self) -> list[str]:
        steps: list[str] = []
        for partition in self.manifest.get("partitions", []):
            name = partition.get("name", "unknown")
            label = partition.get("label", "")
            fs_type = partition.get("fs", "")
            format_mode = "format" if partition.get("format", True) else "skip-format"
            steps.append(f"partition:{name}:{label}:{fs_type}:{format_mode}")
        return steps

    def _payload_stage(self) -> list[str]:
        steps: list[str] = []
        for partition in self.manifest.get("partitions", []):
            name = partition.get("name", "unknown")
            image = partition.get("image")
            payload_dir = partition.get("payload_dir")
            if image:
                steps.append(f"payload-image:{name}:{image}")
            if payload_dir:
                steps.append(f"payload-dir:{name}:{payload_dir}")
        return steps

    def _boot_stage(self) -> list[str]:
        steps: list[str] = []
        for target in self.manifest.get("boot_targets", []):
            target_id = target.get("id", "unknown")
            chain = target.get("chain", "unknown")
            default_flag = "default" if target.get("default", False) else "secondary"
            steps.append(f"boot-target:{target_id}:{chain}:{default_flag}")
        return steps


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a custom Sonic build plan from manifest")
    parser.add_argument("--manifest", required=True, help="Path to a Sonic manifest JSON file")
    parser.add_argument("--out", default=None, help="Optional output path for generated custom plan")
    parser.add_argument("--dry-run", action="store_true", help="Mark generated plan as non-destructive")
    return parser.parse_args(argv)


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR manifest not found: {manifest_path}")
        return 1

    manifest = load_manifest(manifest_path)
    engine = CustomBuildEngine(manifest, dry_run=bool(args.dry_run))
    plan = engine.build()

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
        print(f"Custom build plan written: {out_path}")
    else:
        print(json.dumps(plan, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
