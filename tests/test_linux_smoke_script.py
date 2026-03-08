from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = REPO_ROOT / "scripts" / "smoke" / "linux-runtime-smoke.sh"


def test_linux_smoke_script_uses_current_runtime_paths() -> None:
    contents = SMOKE_SCRIPT.read_text(encoding="utf-8")

    assert "apps/sonic-cli/cli.py plan" in contents
    assert "apps/sonic-cli/cli.py serve-api" in contents
    assert "scripts/sonic-stick.sh" in contents
    assert "/api/sonic/plan" in contents
    assert "installers/usb/cli.py" not in contents

