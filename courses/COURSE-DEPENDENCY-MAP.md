# Sonic Course Dependency Map

This map helps learners choose the right entry point and sequence.

## Recommended Order

1. [Course 01 - Universal Sonic Screwdriver](01-sonic-screwdriver/README.md)
2. [Course 02 - Deployment Patterns](02-deployment-patterns/README.md)
3. [Course 03 - Extension and Customization](03-extension-and-customization/README.md)

## Dependency Matrix

| Course | Primary Focus | Depends On | Typical Duration |
|---|---|---|---|
| Course 01 | Core Sonic workflow and safety boundaries | None | 90 min |
| Course 02 | Staged rollout and fleet deployment patterns | Course 01 | 120 min |
| Course 03 | Extension design and compatibility policy | Course 01 + Course 02 | 120-180 min |

## Path Selection

- Operators deploying a single target: start and finish with Course 01.
- Operators planning staged or fleet rollout: Course 01 then Course 02.
- Developers building Sonic extensions: complete all three courses.

## Exit Competencies

- After Course 01: safe single-target planning and apply discipline.
- After Course 02: repeatable multi-target rollout and validation flow.
- After Course 03: extension-ready contribution with contract and packaging discipline.
