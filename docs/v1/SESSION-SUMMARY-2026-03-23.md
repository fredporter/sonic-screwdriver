# Session Summary - 2026-03-23

Status: active handoff

## What Changed

- expanded service contract coverage for manifest validation, MCP responses,
  HTTP API route wiring, device overlay pagination, and end-to-end
  `build_plan -> get_manifest_status`
- enabled non-destructive dry-run planning on macOS and other non-Linux hosts
  while keeping destructive disk operations Linux-only
- enabled `scripts/sonic-stick.sh --dry-run` to run without `sudo`, without a
  real block device, and without Linux-only disk tools
- enabled `scripts/partition-layout.sh --dry-run` to skip block-device and
  size-probe requirements when no real Linux device is present
- enabled `scripts/apply-payloads-v2.sh --dry-run` to skip Linux-only mount
  requirements
- installed `apps/sonic-ui` dependencies and verified production build output

## Verified Commands

Run from repo root:

```bash
./.venv/bin/python -m pytest -q
bash scripts/run-sonic-checks.sh
bash scripts/first-run-preflight.sh
npm --prefix apps/sonic-ui run build
./.venv/bin/sonic plan --dry-run --out /tmp/sonic-mac-dry-run.json
bash scripts/sonic-stick.sh --manifest /tmp/sonic-stick-mac/manifest.json --dry-run
```

Verified results on 2026-03-23:

- `pytest`: 52 passed
- `run-sonic-checks.sh`: pass
- `first-run-preflight.sh`: pass on macOS
- `apps/sonic-ui` build: pass
- live `sonic-api` route checks: pass
- live `sonic-mcp` initialize/tools/call checks: pass
- real sibling-repo Ventoy/Ubuntu helper flow: pass through direct Python calls

## Mac vs Linux Boundary

Mac-safe now:

- CLI dry-run plan generation
- HTTP API
- MCP facade
- device catalog and bootstrap
- GUI build
- Ventoy/Ubuntu file integration helpers
- `sonic-stick.sh --dry-run`

Still Linux-only by design:

- real partition table writes
- filesystem formatting
- payload mounting and writes to block devices
- `sgdisk`, `lsblk`, `partprobe`, `mkfs.*`, `mount`, `dd`

## Remaining Linux Checks

These still need a real Linux runner:

```bash
bash scripts/smoke/linux-runtime-smoke.sh
bash scripts/smoke/ubuntu-ventoy-integration-smoke.sh
./.venv/bin/sonic plan --usb-device /dev/sdX --out memory/sonic/sonic-manifest.json
bash scripts/sonic-stick.sh --manifest memory/sonic/sonic-manifest.json
```

Expected focus:

- confirm dry-run still passes on Linux with `/dev/sdz`
- confirm real block-device path detection for USB and NVMe naming
- confirm required packages are present: `sgdisk`, `lsblk`, `partprobe`,
  `mkfs.fat`, `mkfs.ext4`, `mkfs.ntfs`, exFAT tooling

## Suggested VS Code Pass

1. Review the new dry-run boundary in
   `services/runtime_service.py`, `sonic_cli.py`,
   `apps/sonic-cli/cli.py`, `scripts/sonic-stick.sh`,
   `scripts/partition-layout.sh`, and `scripts/apply-payloads-v2.sh`.
2. Decide whether `README.md` should explicitly say:
   dry-run validation works on macOS, real apply stays Linux-only.
3. Add one follow-up test batch for API `health/gui/db` routes and MCP
   `sonic_plan` / DB actions.
4. Run the true Linux smoke scripts on the next Ubuntu/Alpine box and capture
   outputs into a follow-up note.
