# Sonic UI (Svelte + Tailwind)

This is the standalone Sonic Screwdriver UI shell.
It is intended for mode selection, build plans, and device catalog browsing.
The UI consumes the local Sonic HTTP API exposed by `python3 installers/usb/cli.py serve-api`.

## Dev

```bash
python3 ../installers/usb/cli.py serve-api
npm install
npm run dev
```

## Build

```bash
npm run build
```
