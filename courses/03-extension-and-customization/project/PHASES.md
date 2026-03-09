# Project Phases

## Phase 1 - Extension Proposal and Boundaries

Goal: define one extension idea with explicit ownership and non-goals.

Tasks:

1. write an extension proposal and boundary matrix
2. identify core contracts that must remain stable
3. define rollback path if extension integration fails

Outputs:

- `extension-proposal.md`
- `boundary-matrix.md`
- `rollback-strategy.md`

## Phase 2 - Contract and Test Design

Goal: make extension safety testable before implementation.

Tasks:

1. draft contract expectations for impacted services
2. build a minimal integration test matrix
3. map failure classes to owner and response flow

Outputs:

- `service-contracts.md`
- `integration-test-matrix.md`
- `failure-response-map.md`

## Phase 3 - Packaging and Compatibility

Goal: package extension expectations for maintainers and users.

Tasks:

1. write compatibility policy and versioning commitments
2. produce extension release note template
3. document migration guidance for future updates

Outputs:

- `compatibility-policy.md`
- `release-notes-template.md`
- `migration-guide.md`
