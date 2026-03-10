# Production Install Workflow

Use this workflow for a clean installation test from a package build context.

## 1. Create a Clean Virtual Environment

```bash
python3 -m venv /tmp/sonic-prod-venv
source /tmp/sonic-prod-venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

## 2. Install Package

From repository root:

```bash
python -m pip install .
```

From index (when published):

```bash
python -m pip install udos-sonic
```

## 3. Verify CLI Entry Points

```bash
sonic --help
sonic-api --help
sonic-mcp --help
```

## 4. Verify Public Imports

```bash
python -c "import udos_sonic; from udos_sonic import SonicService; from udos_sonic.services import default_manifest; print('ok')"
```

## 5. Optional Smoke

```bash
python -m pytest tests/test_packaging_setup.py tests/test_import_paths.py
```

## Notes

- Production install should avoid editable mode.
- Validate on Linux, macOS, and Windows/WSL where possible.
