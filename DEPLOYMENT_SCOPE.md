
# Deployment Scope

Sonic Screwdriver is intentionally scoped to deployment and hardware bootstrap.

This repository performs potentially destructive operations such as disk
partitioning and device provisioning.

Because of this, its scope must remain tightly defined.

## Allowed Responsibilities

- deployment planning
- manifest generation
- USB installer provisioning
- image and disk staging
- device catalog management
- deployment verification

## Responsibilities That Belong Elsewhere

Runtime semantics → uDOS-core

Networking, AI providers, API orchestration → uDOS-wizard

Long-running home server runtime → uHOME-server

## Safety Principles

- destructive operations require explicit execution
- dry-run must always be available
- manifests must be reviewable before execution
- device targets must be explicitly confirmed

Maintaining these boundaries keeps Sonic safe, predictable,
and suitable for both operators and learners.
