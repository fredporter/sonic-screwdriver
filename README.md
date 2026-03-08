# Sonic Screwdriver

Sonic Screwdriver is a Linux-only USB build system for multi-boot sticks.
It separates installer planning (Python) from execution (Bash) so destructive operations are explicit,
reviewable, and OS-aware.

The default standalone profile builds a dual-boot disk with:
- a `uHOME` Steam server surface on Linux
- a Windows 10 gaming surface
- controller-first modular navigation on both sides

## Principles

- Installer packages plan, validate, and write manifests or bundle install steps.
- Bash executes disk operations only on Linux.
- Dry-run is supported for inspection before changes.
- v1.3.17+ is Ventoy-free only (legacy Ventoy scripts removed).

## Quick Start (Linux)

1) Generate a manifest:
```bash
python3 installers/usb/cli.py plan --usb-device /dev/sdb --out memory/sonic/sonic-manifest.json
```

2) Run the launcher (reads the manifest):
```bash
bash scripts/sonic-stick.sh --manifest memory/sonic/sonic-manifest.json
```

Dry-run:
```bash
python3 installers/usb/cli.py plan --usb-device /dev/sdb --dry-run --out memory/sonic/sonic-manifest.json
bash scripts/sonic-stick.sh --manifest memory/sonic/sonic-manifest.json --dry-run
```

The generated manifest includes dual-boot surface metadata, boot targets, controller mappings, and modular navigation entrypoints for both OS surfaces.

## OS Support

- Supported: Linux (Ubuntu/Debian/Alpine)
- Unsupported: macOS, Windows (build operations)

## Layout

```
sonic/
├── installers/             # USB and bundle installer domains (Python)
├── core/                   # Shared runtime services and platform limits
├── scripts/                # Execution layer (Bash, Linux-only)
├── config/                 # Native layout + manifest configuration
├── distribution/           # Tracked release/package descriptors
├── memory/sonic/           # Local runtime state, logs, DBs, artifacts
├── library/sonic/          # Local bolt-ons and installed integrations
├── docs/                   # Specs, howto, devlog
└── version.json            # Sonic version metadata
```

## Docs

- docs/specs/sonic-screwdriver.md
- docs/integration-spec.md
- docs/README.md
- docs/howto/build-usb.md
- docs/howto/dry-run.md
- docs/howto/standalone-release-and-install.md
- docs/devlog/2026-01-24-sonic-standalone-baseline.md

Legacy reference:
- docs/specs/sonic-screwdriver-legacy-baseline.md

## Wizard Integration (Current)

Sonic exposes Wizard platform APIs for GUI workflows:
- `/api/platform/sonic/gui/summary`
- `/api/platform/sonic/builds/*` (artifact + release readiness)
- `/api/platform/sonic/boot/*` (boot profile route selection)
- `/api/platform/sonic/windows/launcher*` (mode selector)
- `/api/platform/sonic/windows/gaming/profiles*`
- `/api/platform/sonic/media/*` (Kodi/WantMyMTV workflow)
- `/api/platform/sonic/device/recommendations`

Sonic now also ships a standalone local control plane in this repository:
- `python3 installers/usb/cli.py serve-api` starts the local HTTP API on `127.0.0.1:8991`
- `python3 installers/usb/cli.py serve-mcp` starts a stdio MCP facade over the same service layer
- `ui/` is the Svelte browser GUI and should talk to the HTTP API, not directly to the CLI

Recommended architecture:
- shared Python service layer for plans, manifest validation, health, and device catalog
- HTTP API as the primary browser/runtime control surface
- optional MCP facade for agent/operator tooling
- Svelte browser GUI consuming `/api/sonic/*` endpoints

## Safety Notes

- All destructive operations require sudo and explicit confirmation.
- Always verify target device before running `scripts/sonic-stick.sh`.
- Legacy Ventoy scripts and config assets were removed in v1.3.17.
