# Services: Device Catalog

## Purpose

The catalog service provides a merged, queryable hardware dataset for Sonic
planning and UI surfaces.

Primary implementation:

- `services/runtime_service.py`

Primary data assets:

- schema: `datasets/sonic-devices.schema.json`
- seed SQL: `datasets/sonic-devices.sql`
- docs: `datasets/README.md`

Runtime storage split:

- seed DB: `memory/sonic/seed/sonic-devices.seed.db`
- user overlay DB: `memory/sonic/user/sonic-devices.user.db`
- compatibility mirror: `memory/sonic/sonic-devices.db`

## Data Lifecycle

1. `_ensure_seed_catalog()` builds seed DB from SQL when missing or forced
2. `_mirror_seed_catalog()` writes legacy compatibility copy
3. `_ensure_user_catalog()` provisions user DB schema if needed
4. `list_devices()` loads seed + user rows, then overlays by `id`

Overlay behavior:

- user rows replace seed rows when `id` matches
- merged set is sorted by `id`

## Public Interface

Runtime methods:

- `get_db_status()`
- `rebuild_db()`
- `export_db()`
- `get_schema()`
- `bootstrap_current_machine()`
- `list_devices(vendor, reflash_potential, usb_boot, uefi_native, limit, offset)`

HTTP routes (`services/http_api.py`):

- `GET /api/sonic/devices`
- `GET /api/sonic/db/status`
- `POST /api/sonic/db/rebuild`
- `GET /api/sonic/db/export`
- `GET /api/sonic/schema`
- `POST /api/sonic/bootstrap/current`

Wizard-compatible aliases are also exposed under `/api/platform/sonic/*`.

MCP tools (`services/mcp_server.py`):

- `sonic_devices`
- `sonic_db_status`
- `sonic_db_rebuild`
- `sonic_schema`
- `sonic_bootstrap_current`

## Query Semantics

`list_devices(...)` supports exact-match case-insensitive filters on:

- `vendor`
- `reflash_potential`
- `usb_boot`
- `uefi_native`

Pagination:

- `limit` and `offset`
- response includes `total`, `limit`, `offset`

## Schema and Row Notes

Schema version is declared in `datasets/sonic-devices.schema.json` and aligns
with SQL columns in `datasets/sonic-devices.sql`.

Runtime row normalization adds convenience aliases:

- `windows <- windows10_boot`
- `media <- media_mode`
- `boot <- uefi_native`

JSON text columns (`methods`, `sources`) are decoded into arrays when possible.

## Boundary

Catalog service owns metadata access and merge semantics. It does not decide
partition layout or execution steps directly.
