# Lesson 01 - Framework And Boundaries

Sonic is the universal Sonic Screwdriver framework for the repo family.

It is responsible for:

- planning deployments
- generating manifests
- staging and applying reviewed hardware changes
- exposing CLI, API, MCP, and UI surfaces for those workflows

It is not responsible for owning every runtime it can install.

Current family split:

- `uDOS` owns shared architecture language and wider family coordination
- `uDOS-sonic` owns deployment and hardware bootstrap
- `uHOME-server` owns canonical `uHOME` runtime contracts

The key educational habit is boundary clarity:

- plan in Python and structured data
- apply destructive steps through explicit Linux-side scripts
- hand off runtime ownership to the correct sibling repo
