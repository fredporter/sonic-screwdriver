# Project Phases

## Phase 1 - Rollout Design

Goal: define waves, gates, and stop conditions before execution.

Tasks:

1. classify 5-10 targets into rollout groups
2. define canary, pilot, and broad rollout waves
3. document hard stop conditions for each wave

Outputs:

- `rollout-plan.md`
- `release-gates.md`

## Phase 2 - Execution Planning and Recovery

Goal: produce an operator-ready runbook with rollback boundaries.

Tasks:

1. map each wave to preflight and post-wave checks
2. define rollback triggers and ownership for execution calls
3. write communication template for go/no-go handoffs

Outputs:

- `operator-runbook.md`
- `rollback-boundaries.md`
- `handoff-template.md`

## Phase 3 - Validation and Audit

Goal: prove deployment quality and package evidence for handoff.

Tasks:

1. execute post-deploy validation checklist for each wave
2. capture and index evidence artifacts
3. publish final report including unresolved risks

Outputs:

- `validation-checklist.md`
- `deployment-evidence-index.md`
- `final-handoff-report.md`
