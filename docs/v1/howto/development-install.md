# Development Install Workflow

Use this workflow when actively developing in the repository.

## 1. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

## 2. Install Editable Package

```bash
python -m pip install -e .
```

This installs entrypoints while keeping source edits live.

## 3. Verify Entry Points

```bash
sonic --help
sonic-api --help
sonic-mcp --help
```

## 4. Verify Public Imports

```bash
python -c "from udos_sonic import SonicService; from udos_sonic.services import write_plan; print('ok')"
```

## 5. Run Service-Focused Tests

```bash
python -m pytest tests/test_import_paths.py tests/test_runtime_service.py tests/test_http_api.py tests/test_sonic_cli.py
```

## Notes

- Development install is preferred for local iteration.
- Keep `config/` and `memory/sonic/` boundaries intact when testing.
