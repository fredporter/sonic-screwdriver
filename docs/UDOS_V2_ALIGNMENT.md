
# uDOS-sonic in the uDOS v2 Architecture

Sonic Screwdriver is the deployment and hardware bootstrap surface of the
uDOS v2 repo family.

It sits below the runtime layer and above raw operating system provisioning.

The role of Sonic is:

take profile → generate manifest → verify → stage payloads → apply to device

This repository does not own runtime semantics.

Instead it prepares machines capable of running:

- uDOS-core
- uDOS-shell
- uDOS-wizard
- uHOME-server

It also provisions lean deployment targets such as:

- uDOS-alpine devices
- USB installer media
- portable rescue environments

Sonic should remain:

- hardware-aware
- OS bootstrap focused
- manifest driven
- reproducible
- safe for learners and operators
