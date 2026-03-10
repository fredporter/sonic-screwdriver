# Services: Overview

This page maps how Sonic service modules connect across CLI, HTTP, MCP, and
runtime storage surfaces.

## Integration Diagram

```mermaid
graph TD
    CLI[apps/sonic-cli/cli.py]
    HTTP[services/http_api.py]
    MCP[services/mcp_server.py]

    CLI --> Runtime[SonicService\nservices/runtime_service.py]
    HTTP --> Runtime
    MCP --> Runtime

    Runtime --> Planner[Planner Service\nservices/planner.py]
    Runtime --> Manifest[Manifest Service\nservices/manifest.py]
    Runtime --> Catalog[Catalog Service\nruntime_service catalog methods]

    Planner --> Layout[config/sonic-layout.json]
    Planner --> ManifestFile[memory/sonic/sonic-manifest.json]

    Manifest --> Layout
    Manifest --> RuntimePaths[memory/sonic/artifacts/*]
    Manifest --> Launchers[distribution/launchers/*]

    Catalog --> DatasetSQL[datasets/sonic-devices.sql]
    Catalog --> DatasetSchema[datasets/sonic-devices.schema.json]
    Catalog --> SeedDB[memory/sonic/seed/sonic-devices.seed.db]
    Catalog --> UserDB[memory/sonic/user/sonic-devices.user.db]
    Catalog --> LegacyDB[memory/sonic/sonic-devices.db]
```

## Service Matrix

| Service | Primary Module | Inputs | Outputs | Primary Consumers |
|---|---|---|---|---|
| Planner | `services/planner.py` | repo root, USB target, layout, payload path, format mode | written manifest + dict response | CLI `plan`, HTTP `POST /api/sonic/plan`, MCP `sonic_plan` |
| Manifest | `services/manifest.py` | layout JSON + overrides + manifest payload | `SonicManifest`, validation report | planner, runtime health, HTTP/MCP verify routes |
| Device Catalog | `services/runtime_service.py` (catalog methods) | seed SQL, user overlay DB, filters | merged/paginated catalog + DB status/schema/export | HTTP device/db endpoints, MCP catalog tools, GUI summary |

## Entry Points

CLI:

- `plan`
- `serve-api`
- `serve-mcp`
- `run` (apply pipeline wrapper)

HTTP:

- `/api/sonic/*`
- `/api/platform/sonic/*` aliases

MCP tools:

- health, gui summary, devices, schema, db status/rebuild/bootstrap, plan, manifest verify

## Boundary Notes

- Planner and manifest services own planning contract and validation.
- Catalog service owns hardware metadata lifecycle and query overlay semantics.
- Disk apply execution remains outside these service modules.
