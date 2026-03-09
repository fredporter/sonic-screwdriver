# Sonic Course 02 - Deployment Patterns

Status: Outline stub for Task 1.5 (`#binder/sonic-education-pathway`)

Course 02 extends Course 01 from single-host safety into repeatable deployment
patterns used in labs, fleets, and staged rollouts.

## Purpose

- teach repeatable operational patterns beyond one-off apply runs
- introduce release-gate checkpoints for safer staged deployment
- provide reusable templates for validation and rollback planning
- prepare learners for extension-level customization in Course 03

## Entry Conditions

Complete Course 01 first:
- [Course 01 - Universal Sonic Screwdriver](../01-sonic-screwdriver/README.md)

Then review:
- [Overview](overview.md)
- [Objectives](objectives.md)
- [Prerequisites](prerequisites.md)

## Lessons

1. [Lesson 01 - Staged Rollouts and Release Gates](lessons/01-staged-rollouts-and-release-gates.md)
2. [Lesson 02 - Multi-Host and Fleet Planning](lessons/02-multi-host-and-fleet-planning.md)
3. [Lesson 03 - Dualboot and Recovery Patterns](lessons/03-dualboot-and-recovery-patterns.md)
4. [Lesson 04 - Post-Deploy Validation and Audit Trails](lessons/04-post-deploy-validation-and-audit-trails.md)

## Project

- [Project Overview](project/README.md)
- [Project Phases](project/PHASES.md)

## Completion Criteria

By the end of this course, the learner should be able to:

- choose an appropriate deployment pattern for a target environment
- define release gates before each destructive stage
- plan rollback and rescue flows for fleet-level changes
- produce a repeatable validation report after deployment

## Next Step

Continue to:
- [Course 03 - Extension and Customization](../03-extension-and-customization/README.md)
