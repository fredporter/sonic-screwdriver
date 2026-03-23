from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_SCRIPT = REPO_ROOT / "scripts" / "linux-runner-validation.sh"


def test_linux_runner_validation_script_covers_required_steps() -> None:
    contents = RUNNER_SCRIPT.read_text(encoding="utf-8")

    assert "scripts/run-sonic-checks.sh" in contents
    assert "scripts/first-run-preflight.sh" in contents
    assert "scripts/smoke/linux-runtime-smoke.sh" in contents
    assert "scripts/smoke/ubuntu-ventoy-integration-smoke.sh" in contents
    assert "SONIC_RUN_REAL_APPLY" in contents
    assert "SONIC_FORCE_REAL_APPLY" in contents
    assert "SONIC_TARGET_USB" in contents
