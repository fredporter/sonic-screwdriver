# Services: Manifest

## Purpose

The manifest service defines, builds, and validates the Sonic deployment
contract that sits between planning and apply.

Primary implementation:

- `services/manifest.py`

Validation helper integration:

- `services/runtime_service.py` (`get_manifest_status`)
- `services/http_api.py` (`GET /api/sonic/manifest/verify`)
- `services/mcp_server.py` (`sonic_manifest_verify`)

## Data Model

The canonical dataclass is `SonicManifest` with nested specs:

- `PartitionSpec`
- `ControllerMappingSpec`
- `NavigationModuleSpec`
- `SurfaceSpec`
- `BootTargetSpec`

Allowed enumerations in code:

- `ALLOWED_BOOT_MODES = {"uefi-native"}`
- `ALLOWED_FORMAT_MODES = {"full", "skip"}`

## Generation Contract

Entry point:

```python
default_manifest(
    repo_root: Path,
    usb_device: str,
    dry_run: bool,
    layout_path: Optional[Path] = None,
    format_mode: Optional[str] = None,
    payload_dir: Optional[Path] = None,
) -> SonicManifest
```

Generation rules:

1. Resolve runtime paths (`memory/sonic/...`)
2. Load layout fields from `config/sonic-layout.json` when present
3. Fall back to hardcoded defaults when layout is missing/invalid
4. Validate partition geometry (`validate_partitions`)
5. Return structured manifest for serialization

Serialization helpers:

- `write_manifest(path, manifest)`
- `read_manifest(path)`

## Validation Contract

Entry point:

```python
validate_manifest_data(manifest: Dict[str, Any], manifest_path: Optional[Path]) -> Dict[str, Any]
```

Validation coverage:

- required top-level keys (`usb_device`, `boot_mode`, `repo_root`, `payload_dir`, `iso_dir`, `partitions`)
- boot mode and format mode constraints
- partition integrity (name/label uniqueness, size rules, single remainder)
- payload reference existence checks
- controller mapping uniqueness and linkage
- navigation module linkage to mappings and source paths
- surface linkage to known partitions and navigation modules
- boot target linkage to known surfaces, mappings, and entry partitions
- single default boot target constraint

Output shape:

- `ok`: boolean (`False` when errors exist)
- `errors`: blocking issues
- `warnings`: non-blocking issues (for example missing payload paths)
- `summary`: counts and quick health indicators
- `partitions`, `surfaces`, `boot_targets`: normalized summaries

Convenience verifier:

- `verify_manifest_path(path)` reads and validates in one call

## Error and Warning Semantics

- Errors indicate structural or contract violations that should block apply.
- Warnings indicate environmental or path issues that may still require operator
  resolution before apply.

This split is intentionally used by health and GUI summary surfaces to show
readiness and risk without losing detail.

## Boundary

Manifest service owns planning contract validity and readability.

It does not:

- perform disk writes
- execute bootloader installation
- run payload extraction
