# Sonic Runtime State

`memory/sonic/` is the local-only runtime root for standalone Sonic.

Use it for:

- `artifacts/` for large downloaded files, staged payload libraries, generated bundles, and release outputs
- `seed/` and `user/` for local device database state
- `logs/` for script and build logs
- generated manifests such as `sonic-manifest.json`

Do not store tracked source files, docs, or canonical config here.
