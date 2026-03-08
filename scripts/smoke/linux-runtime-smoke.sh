#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/sonic-linux-smoke.XXXXXX")"
PORT="${SONIC_SMOKE_PORT:-8992}"
API_PID=""
API_LOG="${TMP_DIR}/sonic-api.log"
CLI_MANIFEST="${TMP_DIR}/cli-manifest.json"
API_MANIFEST="${TMP_DIR}/api-manifest.json"

cleanup() {
  if [[ -n "${API_PID}" ]] && kill -0 "${API_PID}" 2>/dev/null; then
    kill "${API_PID}" 2>/dev/null || true
    wait "${API_PID}" 2>/dev/null || true
  fi
  rm -rf "${TMP_DIR}"
}

trap cleanup EXIT

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "ERROR This smoke script requires Linux."
  exit 1
fi

cd "${REPO_ROOT}"

echo "[1/5] CLI plan dry-run"
python3 apps/sonic-cli/cli.py plan \
  --usb-device /dev/sdz \
  --dry-run \
  --layout-file config/sonic-layout.json \
  --out "${CLI_MANIFEST}"

echo "[2/5] Apply layer dry-run"
bash scripts/sonic-stick.sh --manifest "${CLI_MANIFEST}" --dry-run

echo "[3/5] Start API"
python3 apps/sonic-cli/cli.py serve-api --host 127.0.0.1 --port "${PORT}" >"${API_LOG}" 2>&1 &
API_PID=$!

for _ in {1..20}; do
  if python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${PORT}/api/sonic/health', timeout=1).read()" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! kill -0 "${API_PID}" 2>/dev/null; then
  echo "ERROR Sonic API failed to start."
  cat "${API_LOG}"
  exit 1
fi

echo "[4/5] API health"
python3 - <<PY
import json
import urllib.request

health = json.loads(
    urllib.request.urlopen("http://127.0.0.1:${PORT}/api/sonic/health", timeout=3).read().decode("utf-8")
)
if not health.get("ok"):
    raise SystemExit(f"api health not ok: {health}")
print("API health ok")
PY

echo "[5/5] API plan dry-run"
python3 - <<PY
import json
import urllib.request

payload = json.dumps(
    {
        "usb_device": "/dev/sdz",
        "dry_run": True,
        "layout_file": "config/sonic-layout.json",
        "out": "${API_MANIFEST}",
    }
).encode("utf-8")
request = urllib.request.Request(
    "http://127.0.0.1:${PORT}/api/sonic/plan",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
response = json.loads(urllib.request.urlopen(request, timeout=5).read().decode("utf-8"))
if not response.get("ok"):
    raise SystemExit(f"api plan failed: {response}")
print(response["manifest_path"])
PY

echo "Linux smoke passed."
