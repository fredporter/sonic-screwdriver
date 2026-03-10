# Services: Planner

## Purpose

The planner service turns a deployment intent into a concrete manifest JSON that
can be reviewed before apply.

Primary implementation:

- `services/planner.py`

Primary callers:

- CLI plan command: `apps/sonic-cli/cli.py`
- Runtime service facade: `services/runtime_service.py`
- HTTP API: `POST /api/sonic/plan` in `services/http_api.py`
- MCP tool: `sonic_plan` in `services/mcp_server.py`

## Interface

Core writer function:

```python
write_plan(
    repo_root: Path,
    usb_device: str,
    dry_run: bool,
    layout_path: Optional[Path],
    format_mode: Optional[str],
    payload_dir: Optional[Path],
    out_path: Path,
) -> Dict
```

Behavior:

1. Build default or layout-driven manifest via `default_manifest(...)`
2. Persist manifest with `write_manifest(...)`
3. Return manifest as a dict for upstream API responses

CLI args mirror this contract through `parse_args(...)` in `services/planner.py`.

## Lifecycle

`request -> OS check -> manifest build -> manifest write -> response`

Details:

1. Caller provides USB target, layout path, output path, and optional format mode
2. Linux support gate enforced (`is_supported()`)
3. Planner delegates structure generation to manifest service
4. Manifest is written under runtime root (default `memory/sonic/sonic-manifest.json`)
5. Caller receives serialized plan and manifest path

## Inputs and Defaults

- `usb_device`: default `/dev/sdb`
- `layout_file`: default `config/sonic-layout.json`
- `out`: default `memory/sonic/sonic-manifest.json`
- `format_mode`: optional override (`full` or `skip`)
- `payloads_dir`: optional override (defaults to `memory/sonic/artifacts/payloads`)

## Error Model

Planner surfaces `ValueError` from manifest generation/validation and OS guard
logic.

Common error cases:

- unsupported OS for build operations (non-Linux)
- invalid partition config (for example, multiple remainder partitions)
- invalid format mode or malformed layout-derived values

HTTP API maps these to `400`, while CLI prints `ERROR ...` and exits with `1`.

## Output Contract

Runtime and API callers use this structure:

- `ok`: boolean
- `message`: usually `plan written`
- `manifest_path`: path to written manifest
- `plan`: serialized `SonicManifest`

## Boundaries

Planner does not execute destructive disk writes. It only prepares the manifest
and writes the plan artifact.

Execution belongs to:

- apply pipeline scripts (`scripts/sonic-stick.sh`)
- runtime orchestration surfaces outside planner interface
