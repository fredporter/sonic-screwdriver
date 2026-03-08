from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UHOME_LAUNCHER = REPO_ROOT / "distribution" / "launchers" / "uhome" / "uhome-console.sh"
WINDOWS_HOME = REPO_ROOT / "distribution" / "launchers" / "windows" / "WindowsHome.cmd"
WINDOWS_LIBRARY = REPO_ROOT / "distribution" / "launchers" / "windows" / "WindowsLibrary.cmd"
WINDOWS_SETTINGS = REPO_ROOT / "distribution" / "launchers" / "windows" / "WindowsSettings.cmd"


def _run_uhome_launcher(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["SONIC_LAUNCHER_TEST_MODE"] = "1"
    return subprocess.run(
        ["/bin/sh", str(UHOME_LAUNCHER), *args],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def test_uhome_home_launcher_command() -> None:
    result = _run_uhome_launcher("--module", "home")
    assert result.returncode == 0
    assert result.stdout.strip() == "steam -bigpicture steam://open/library"


def test_uhome_library_launcher_command() -> None:
    result = _run_uhome_launcher("--module", "library")
    assert result.returncode == 0
    assert result.stdout.strip() == "steam -bigpicture steam://open/games"


def test_uhome_settings_launcher_command() -> None:
    result = _run_uhome_launcher("--module", "settings")
    assert result.returncode == 0
    assert result.stdout.strip() == "/usr/bin/env sh -lc printf 'uHOME settings placeholder\\n'"


def test_uhome_unknown_module_fails() -> None:
    result = _run_uhome_launcher("--module", "unknown")
    assert result.returncode != 0
    assert "Unknown uHOME module" in result.stderr


def test_windows_home_launcher_points_to_playnite() -> None:
    contents = WINDOWS_HOME.read_text(encoding="utf-8")
    assert "Playnite.FullscreenApp.exe" in contents


def test_windows_library_launcher_points_to_steam_big_picture() -> None:
    contents = WINDOWS_LIBRARY.read_text(encoding="utf-8")
    assert "steam://open/bigpicture" in contents


def test_windows_settings_launcher_opens_settings() -> None:
    contents = WINDOWS_SETTINGS.read_text(encoding="utf-8")
    assert "ms-settings:" in contents
