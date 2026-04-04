# Welcome to the Sonic wiki

Updated: 2026-03-09

This wiki is the student-facing orientation layer for `sonic-screwdriver`.

Use it when you want the shortest path to understanding:

- what Sonic is
- what it owns
- how it relates to `uDOS-host`, `uDOS-wizard`, and `uHOME`
- where to start learning

When you want implementation detail, move from the wiki into the Sonic course
and then into `docs/`.

## Start Here

- first steps: [Getting Started](Getting-Started.md)
- Sonic course map: [Education Pathways](Education-Pathways.md)
- repo boundaries: [Repo Map](Repo-Map.md)
- common questions: [FAQ](FAQ.md)

## Project Snapshot

- repo front door: [../README.md](../README.md)
- Sonic course: [../courses/README.md](../courses/README.md)
- docs index: [../docs/README.md](../docs/README.md)
- archived structure assessment: [../docs/v1/sonic-structure-assessment-2026-03-08.md](../docs/v1/sonic-structure-assessment-2026-03-08.md)

## Core Idea

Sonic is the deployment and hardware bootstrap pathway for the repo family.

It plans and applies deployments to real hardware, but it does not own the full
runtime of every system it can install.

Current family split:

- `uDOS-core` / `uDOS-shell` = shared semantic and shell surfaces
- `uDOS-host` = always-on command-centre runtime
- `uDOS-wizard` = provider, assist, MCP, and remote publishing adapters
- `sonic-screwdriver` = deployment and hardware bootstrap
- `uHOME-server` = downstream `uHOME` service stream
