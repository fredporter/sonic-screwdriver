# Services: Testing Patterns

This document summarizes current test coverage for service interfaces and gives
repeatable patterns for extending coverage.

## Current Tests

Runtime service:

- `tests/test_runtime_service.py`
- covers unsupported OS rejection and repo-relative path resolution in
  `SonicService.build_plan(...)`
- covers merged device catalog precedence, filtering, and pagination
- covers end-to-end `build_plan(...)` -> `get_manifest_status(...)`

Manifest validation:

- `tests/test_manifest_validation.py`
- covers payload-reference warnings, surface/nav/boot-target link validation,
  and default-boot/boot-mode/format-mode contract checks

HTTP API:

- `tests/test_http_api.py`
- covers `POST /api/sonic/plan` error mapping (`ValueError` -> HTTP 400)
- covers `GET /api/sonic/devices`, `GET /api/sonic/schema`, and
  `GET /api/sonic/manifest/verify` argument/response wiring
- covers `POST /api/sonic/bootstrap/current`

MCP facade:

- `tests/test_mcp_server.py`
- covers `initialize`, `tools/list`, and `tools/call` contract envelopes for
  `sonic_devices` and `sonic_manifest_verify`

CLI integration:

- `tests/test_sonic_cli.py`
- covers `plan` command unsupported-platform failure and successful write-plan
  invocation argument wiring

Runtime path guardrail:

- `tests/test_linux_smoke_script.py`
- asserts smoke script uses current API/CLI paths

Packaging entrypoints:

- `tests/test_packaging_setup.py`
- verifies console script exports (`sonic`, `sonic-api`, `sonic-mcp`)

## Recommended Test Commands

```bash
./.venv/bin/python -m pytest \
  tests/test_runtime_service.py \
  tests/test_manifest_validation.py \
  tests/test_http_api.py \
  tests/test_mcp_server.py \
  tests/test_sonic_cli.py
```

Optional wider pass:

```bash
./.venv/bin/python -m pytest
```

## Pattern: Service Method Unit Test

Use monkeypatch to isolate dependencies and assert argument wiring:

- patch environment gates (`is_supported`)
- patch downstream writer (`write_plan`)
- assert resolved absolute paths
- assert response shape (`ok`, `manifest_path`, `plan`)

## Pattern: API Contract Test

Use a bound `SonicApiHandler` with a fake service object:

- provide deterministic fake responses or exceptions
- issue real HTTP requests against a test server
- assert status code and JSON body contract

## Pattern: CLI Wiring Test

Load CLI module dynamically and patch:

- `sys.argv`
- support gate functions
- downstream service calls

Assert both terminal output and call arguments.

## Gaps to Add Next

1. Add HTTP API tests for `GET /api/sonic/health`, `GET /api/sonic/gui/summary`,
   and `GET /api/sonic/db/*` routes.
2. Add MCP tool tests for `sonic_plan` and database actions.
3. Add a launcher/bootstrap smoke test that exercises the browser/API handoff
   without opening an external browser.
4. Add Linux-runner coverage for `sonic init` and the Ubuntu/Ventoy integration
   flow from the service/CLI layer.

## Stability Guidance

When service contracts change:

- update architecture docs and tests in the same PR
- keep response envelopes stable (`ok`, `errors`, `warnings`, summary keys)
- treat path and schema changes as contract changes requiring test updates
