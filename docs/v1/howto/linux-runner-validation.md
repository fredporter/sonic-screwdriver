# Linux Runner Validation

Use this guide on a real Ubuntu or Alpine machine to validate the true
Sonic deployment lane after macOS dry-run work is complete.

If you want the same sequence as a single script, use:

```bash
bash scripts/linux-runner-validation.sh
```

## Purpose

Prove the parts that macOS cannot prove:

- block-device detection
- partition table creation
- filesystem formatting
- payload validation against a Linux device path
- Linux CLI and API dry-run behavior with `/dev/*`
- Ubuntu/Ventoy integration smoke through the published scripts

## Required Environment

Host OS:

- Ubuntu or Debian-family Linux, or
- Alpine Linux

Sibling repos expected next to `sonic-screwdriver`:

- `sonic-ventoy`
- `uDOS-ubuntu`
- `uHOME-server`
- `uDOS-wizard`

Required tools:

```bash
python3
python3-venv
python3-pip
bash
node
npm
lsblk
sgdisk
partprobe
mkfs.fat
mkfs.ext4
mkfs.ntfs
mkfs.exfat or mkexfatfs
mount
umount
dd
sudo
```

Ubuntu/Debian package hint:

```bash
sudo apt-get update
sudo apt-get install -y \
  python3 python3-venv python3-pip \
  bash nodejs npm \
  gdisk dosfstools e2fsprogs ntfs-3g exfatprogs \
  util-linux mount
```

Alpine package hint:

```bash
sudo apk add \
  python3 py3-pip py3-virtualenv \
  bash nodejs npm \
  gdisk dosfstools e2fsprogs ntfs-3g exfatprogs \
  util-linux
```

## Recommended Order

Run from repo root.

### 1. Baseline Repo Validation

```bash
bash scripts/run-sonic-checks.sh
bash scripts/first-run-preflight.sh
```

Expected result:

- both commands pass
- `pytest` is green
- `first-run-preflight.sh` runs the Linux CLI dry-run path instead of the macOS
  API-only probe

### 2. Linux CLI Dry-Run

```bash
./.venv/bin/sonic plan \
  --usb-device /dev/sdz \
  --dry-run \
  --out /tmp/sonic-linux-dry-run.json
```

Expected result:

- manifest file is written
- no unsupported-platform error

### 3. Linux Bash Dry-Run

```bash
bash scripts/sonic-stick.sh \
  --manifest /tmp/sonic-linux-dry-run.json \
  --dry-run
```

Expected result:

- partition plan prints successfully
- payload dry-run prints successfully
- no `sgdisk`, `mount`, or `sudo` failure should occur in dry-run mode

### 4. Linux Runtime Smoke

```bash
bash scripts/smoke/linux-runtime-smoke.sh
```

Expected result:

- CLI plan dry-run passes
- dry-run `scripts/sonic-stick.sh` passes
- API starts locally
- `GET /api/sonic/health` succeeds
- `POST /api/sonic/plan` succeeds

### 5. Ubuntu/Ventoy Integration Smoke

```bash
bash scripts/smoke/ubuntu-ventoy-integration-smoke.sh
```

Expected result:

- `init`
- `add`
- `update`
- `theme`

all pass, and the script ends with `Ubuntu/Ventoy integration smoke passed`.

## Optional Real Device Apply

Only do this with a disposable USB device you are prepared to erase.

First identify the real device:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN
```

Then run:

```bash
./.venv/bin/sonic plan \
  --usb-device /dev/sdX \
  --out memory/sonic/sonic-manifest.json

bash scripts/sonic-stick.sh \
  --manifest memory/sonic/sonic-manifest.json
```

What this proves:

- real block-device path parsing
- GPT creation via `sgdisk`
- filesystem formatting
- payload copy/image write path

## Failure Triage

If `plan` fails:

- verify Linux host detection
- verify editable install completed
- verify `config/sonic-layout.json` and repo assets are present

If `partition-layout.sh` fails:

- verify target device exists under `/dev`
- verify `lsblk` and `sgdisk` are installed
- verify the target is a block device, not a partition path

If payload application fails:

- verify `payload_dir` exists
- verify required payload directories or images exist
- use `--no-validate-payloads` only when intentionally testing script flow

If Ubuntu/Ventoy smoke fails:

- verify sibling repo paths
- verify profile manifest exists in `../sonic-ventoy/profiles/udos-ubuntu/manifest.json`
- verify template files exist in `../sonic-ventoy/templates/ventoy`

## What macOS Already Proved

Before handing off to Linux, the current repo already proves on macOS:

- standalone API
- MCP facade
- UI build
- device catalog and bootstrap
- dry-run CLI planning
- dry-run `sonic-stick.sh`
- Ventoy/Ubuntu helper flow through direct file operations

That means Linux validation should focus on the real disk and kernel-facing
operations, not general service correctness.
