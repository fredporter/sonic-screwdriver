# Services: Testing Patterns

This document summarizes current test coverage for service interfaces and gives
repeatable patterns for extending coverage.

## Current Tests

Runtime service:

- `tests/test_runtime_service.py`
- covers unsupported OS rejection and repo-relative path resolution in
  `SonicService.build_plan(...)`

HTTP API:

- `tests/test_http_api.py`
- covers `POST /api/sonic/plan` error mapping (`ValueError` -> HTTP 400)

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
pytest tests/test_runtime_service.py tests/test_http_api.py tests/test_sonic_cli.py
```

Optional wider pass:

```bash
pytest tests/test_linux_smoke_script.py tests/test_packaging_setup.py
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

1. Manifest validator deep tests (`validate_manifest_data`) for surfaces,
   boot targets, and payload reference checks.
2. Device catalog merge tests verifying user-overlay precedence by ID.
3. Pagination/filter tests for `list_devices(...)` edge cases.
4. MCP tool contract tests for `sonic_plan`, `sonic_devices`, and
   `sonic_manifest_verify`.
5. End-to-end integration test combining plan generation and manifest verify.

## Stability Guidance

When service contracts change:

- update architecture docs and tests in the same PR
- keep response envelopes stable (`ok`, `errors`, `warnings`, summary keys)
- treat path and schema changes as contract changes requiring test updates
