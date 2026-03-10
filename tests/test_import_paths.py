from __future__ import annotations

from pathlib import Path

from udos_sonic import SonicService, default_manifest, validate_manifest_data
from udos_sonic.services import build_plan, write_plan


def test_top_level_public_imports_are_available() -> None:
    assert SonicService is not None
    assert default_manifest is not None
    assert validate_manifest_data is not None


def test_service_namespace_public_imports_are_available() -> None:
    assert build_plan is not None
    assert write_plan is not None


def test_public_service_can_be_constructed(tmp_path: Path) -> None:
    service = SonicService(repo_root=tmp_path)
    assert service.repo_root == tmp_path
