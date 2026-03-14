
# Sonic Screwdriver Architecture

Sonic is a hardware deployment toolchain.

It converts reviewed deployment profiles into executable device provisioning.

Architecture layers:

Operator Surface
    CLI
    Web UI
    MCP endpoint

Service Layer
    planner
    manifest generator
    verification
    device catalog

Execution Layer
    USB provisioning
    disk layout
    payload staging
    installer execution

Device Layer
    bare metal machine
    USB installer
    diskless target
