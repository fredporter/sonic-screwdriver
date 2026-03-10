# Cross-Platform Packaging Validation

This guide describes how to validate the `udos-sonic` package installation across multiple operating systems.

## Purpose

Verify that `pip install udos-sonic` works correctly on:
- **macOS** (local development primary)
- **Linux** (USB target primary)
- **Windows/WSL** (developer secondary)

## Validation Scripts

Two automated scripts are provided:

| Script | Platform | Location |
|--------|----------|----------|
| `validate-packaging.sh` | macOS, Linux, WSL | [scripts/validate-packaging.sh](../../scripts/validate-packaging.sh) |
| `validate-packaging.ps1` | Windows PowerShell | [scripts/validate-packaging.ps1](../../scripts/validate-packaging.ps1) |

## What Gets Tested

Each script validates:

1. **Clean venv creation** - Ensures no contamination from development environment
2. **Package installation** - `pip install` from repository path succeeds
3. **Python import paths** - All public API imports work:
   - `import udos_sonic`
   - `from udos_sonic import SonicService, SonicManifest, ...`
   - `from udos_sonic.services import write_plan, build_plan, ...`
4. **Console entrypoints** - All installed commands work:
   - `sonic` (plan/run/serve-api/serve-mcp subcommands)
   - `sonic-api`
   - `sonic-mcp`
5. **Extension example** - Custom build engine example executes

## Usage

### macOS / Linux / WSL

```bash
# Navigate to repository root
cd /path/to/uDOS-sonic

# Run validation (auto-cleans venv)
./scripts/validate-packaging.sh

# Keep test venv for inspection
./scripts/validate-packaging.sh --keep-venv
```

### Windows PowerShell

```powershell
# Navigate to repository root
cd C:\path\to\uDOS-sonic

# Run validation (auto-cleans venv)
.\scripts\validate-packaging.ps1

# Keep test venv for inspection
.\scripts\validate-packaging.ps1 -KeepVenv
```

## Expected Output

Successful validation shows:

```
===============================================
uDOS-sonic Packaging Validation
===============================================
OS: [platform info]
Python: [version]
Repo: [path]
Test venv: [temp path]
===============================================

Step 1: Create clean virtual environment
✓ Virtual environment created

Step 2: Install package from repository
✓ Package installed

Step 3: Verify Python import paths
  ✓ import udos_sonic
  ✓ from udos_sonic import SonicService
  ✓ from udos_sonic import SonicManifest, default_manifest, validate_manifest_data
  ✓ from udos_sonic.services import write_plan, build_plan
  ✓ from udos_sonic.services import SonicService
  ✓ SonicService() construction succeeds
✓ All import paths verified

Step 4: Verify console script entrypoints
  ✓ sonic --help
  ✓ sonic plan --help
  ✓ sonic run --help
  ✓ sonic-api --help
  ✓ sonic-mcp --help
✓ All console entrypoints verified

Step 5: Test custom build engine example
  ✓ Custom build engine example executes
✓ Extension example verified

===============================================
✅ All validation checks passed!
===============================================

Platform: [details]
Python: [version]
Package version: [version]
```

## Failure Modes

### Import Errors

If imports fail:
- Check `pyproject.toml` has correct `packages` configuration
- Verify `udos_sonic/__init__.py` exports are correct
- Ensure `udos_sonic/services/__init__.py` exists

### Entrypoint Errors

If console scripts fail:
- Check `pyproject.toml` `[project.scripts]` section
- Verify `sonic_cli.py` is self-contained (no repo-path dependencies)
- Test script help before full commands

### Path Resolution Issues

On Windows:
- Use forward slashes or `os.path.join()` in Python code
- Test both PowerShell and WSL environments
- Check for hardcoded Unix paths

## Recording Results

When running cross-platform validation for a release:

1. Run script on each target platform
2. Capture full output (screenshot or log file)
3. Record in binder progress report:

```markdown
### Cross-OS Validation Results

**macOS** (Darwin 21.6.0, Python 3.13.12):
- Status: ✅ Pass
- Output: [link to log or screenshot]

**Linux** (Ubuntu 22.04, Python 3.11):
- Status: ✅ Pass
- Output: [link to log or screenshot]

**Windows/WSL** (WSL2 Ubuntu, Python 3.10):
- Status: ✅ Pass
- Output: [link to log or screenshot]
```

## Troubleshooting

### Script Permission Denied (macOS/Linux)

```bash
chmod +x scripts/validate-packaging.sh
```

### PowerShell Execution Policy (Windows)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Python Not Found

Ensure Python 3.9+ is in PATH:

```bash
# macOS/Linux
which python3

# Windows (PowerShell)
where python
```

## Next Steps

After successful cross-platform validation:

1. Update [BINDER-PROGRESS-v1.6.5-2026-03-10.md](../BINDER-PROGRESS-v1.6.5-2026-03-10.md)
2. Mark completion criteria as fully met
3. Tag package release if appropriate
4. Update [DEVELOPMENT-STATUS-v1.6.md](../DEVELOPMENT-STATUS-v1.6.md)

---

**Related**:
- [Development Install Workflow](development-install.md)
- [Production Install Workflow](production-install.md)
- [Packaging Binder Progress](../BINDER-PROGRESS-v1.6.5-2026-03-10.md)
