# Sonic Screwdriver Changelog

## v1.5.2 (2026-03-07)

- Move USB installer planning into `installers/usb/`.
- Move standalone `uHOME` bundle installer code into `installers/bundles/uhome/`.
- Remove transitional `core/*` shims and switch live entrypoints to the new package layout.
- De-version the active contract docs so future upgrades do not require another path rename.

## v1.0.1.0 (2026-01-24)

- Introduce core planning layer and manifest output.
- Separate OS-specific bash execution from core planning.
- Add OS limitation checks and dry-run mode.
- Restructure docs into specs/howto/devlog with legacy archive.

## v1.0.0.6

- Legacy Sonic Stick Pack (Ventoy USB toolkit).
