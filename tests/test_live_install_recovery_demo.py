from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = REPO_ROOT / "scripts" / "demo-live-install-recovery.sh"
PRODUCT_DOC = REPO_ROOT / "docs" / "LIVE_INSTALL_RECOVERY_PRODUCT.md"
HANDOFF_DOC = REPO_ROOT / "docs" / "UBUNTU_VENTOY_SONIC_HANDOFF.md"


def test_live_install_recovery_demo_mentions_all_product_lanes() -> None:
    contents = DEMO_SCRIPT.read_text(encoding="utf-8")

    assert "Live lane:" in contents
    assert "Install lane:" in contents
    assert "Recovery lane:" in contents
    assert "scripts/sonic-stick.sh --dry-run" in contents


def test_product_doc_references_handoff_and_evidence() -> None:
    contents = PRODUCT_DOC.read_text(encoding="utf-8")

    assert "Ubuntu, Ventoy, And Sonic Handoff" in contents
    assert "scripts/smoke/ubuntu-ventoy-integration-smoke.sh" in contents
    assert "vault/manifests/reference-rescue-maintenance-dry-run.manifest.json" in contents


def test_handoff_doc_keeps_ownership_split_explicit() -> None:
    contents = HANDOFF_DOC.read_text(encoding="utf-8")

    assert "uDOS-host" in contents
    assert "sonic-ventoy" in contents
    assert "sonic-screwdriver" in contents
    assert "Sonic owns:" in contents
