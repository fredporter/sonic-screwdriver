# Sonic Docs

## Current
- specs/sonic-screwdriver.md
- integration-spec.md
- specs/uDOS_Xbox_Entertainment_Spec.md
- specs/uDOS-Gameplay-Anchors-v1.3-Spec.md
- specs/v1-3 GAMEPLAY.md
- howto/build-usb.md
- howto/dry-run.md
- howto/standalone-release-and-install.md
- devlog/2026-01-24-sonic-standalone-baseline.md

## Active Direction

- `integration-spec.md` is the active Sonic integration contract
- `specs/sonic-screwdriver.md` now describes the active Sonic
  provisioning contract
- `distribution/` and `memory/sonic/` define the tracked-vs-local storage boundary
- the active `uHOME` runtime and install spec is external to this repository
  and should be referenced as an integration dependency, not an internal doc
- Wizard owns active network-control surfaces such as beacon and Home Assistant
  integration

## Legacy
- `specs/sonic-screwdriver-legacy-baseline.md` captures the first standalone planning split.
- `roadmap-v1-4-*.md` files capture historical exploration that is still kept in
  this repo.
