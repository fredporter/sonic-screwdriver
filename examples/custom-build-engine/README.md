# Custom Build Engine Example

This example shows how to derive an execution plan from a Sonic manifest without
modifying core runtime code.

## Run

```bash
python3 examples/custom-build-engine/example_engine.py \
  --manifest config/sonic-manifest.json.example \
  --dry-run
```

Optional output file:

```bash
python3 examples/custom-build-engine/example_engine.py \
  --manifest config/sonic-manifest.json.example \
  --out memory/sonic/example-custom-build-plan.json
```

## What It Demonstrates

- a minimal extension-style build engine class
- staged planning (`partition`, `payload`, `boot`)
- deterministic command generation from manifest content
- dry-run mode that preserves safety boundaries

This is a reference pattern for `#binder/sonic-packaging-finalization` Task 5.4.
