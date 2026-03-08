# Lesson 02 - Layout, Manifest, And Dry-Run

Sonic treats deployment structure as explicit and reviewable.

The core surfaces are:

- `config/sonic-layout.json`
- generated manifests under `memory/sonic/`
- `apps/sonic-cli/cli.py` or the installed `sonic` command
- `scripts/sonic-stick.sh`

The standard safe workflow is:

1. generate a manifest
2. inspect the manifest
3. run dry-run
4. only then execute real writes

Example:

```bash
sonic plan \
  --usb-device /dev/sdb \
  --dry-run \
  --layout-file config/sonic-layout.json \
  --out memory/sonic/sonic-manifest.json

bash scripts/sonic-stick.sh \
  --manifest memory/sonic/sonic-manifest.json \
  --dry-run
```

The important concept is not one exact disk layout. The important concept is
that nothing destructive should feel magical or hidden.
