# Publishing House Shared Contracts

These are semantic contracts for agent packages. Machine-readable schemas and evaluation fixtures will be added only after this review stage. Every record requires a stable ID, version, created time, actor, provenance, and status.

## House Profile

Contains owner and approval roles, mission, principles, risk posture, portfolio constraints, default permission mode, publication destinations, and escalation contacts. It must not embed credentials.

## Brand Profile

Contains position, audience promise, category frame, proof, voice principles, distinctive assets, terminology, prohibited shortcuts, examples, validity dates, and owner approval. A new operator supplies this profile; agents do not assume Robert, Kujo, or any specific brand.

## Audience Profile

Contains audience identity, context, needs, tensions, existing knowledge, desired movement, channels, accessibility needs, evidence sources, assumptions, and review date.

## Editorial Brief

Contains assignment ID, campaign and parent IDs, problem or opportunity, thesis, audience, editorial purpose, format, channel, evidence burden, source signals, desired response, CTA, artifact bundle, assigned roles, deadline, quality requirements, non-goals, kill conditions, permission mode, and approval owner.

## Evidence Record

Contains evidence ID, claim ID, artifact version, source, source location, retrieval date, freshness, evidence class, support or conflict, reviewer result, uncertainty, rights or privacy notes, and unavailable checks.

## Artifact Manifest

Contains entry and assignment IDs, package version, files, kinds, paths, mime types, checksums, source lineage, parent artifacts, claim deltas, required reviews, completed reviews, approval state, destination constraints, and drift result.

## Review Record

Contains review ID, role, artifact version, quality dimensions, passage or asset references, blocking and non-blocking findings, requested changes, decision, uncertainty, and next owner. Reviews append; they do not silently replace prior judgments.

## Approval Record

Contains approval ID, human actor, exact artifact/package version and checksum, scope, destination, decision, timestamp, conditions, expiration or invalidation rules, and later drift. Editing an approved artifact invalidates approval unless the approval explicitly covers that transformation.

## Publication Receipt

Contains receipt ID, approval ID, artifact version, adapter and version, destination, target identity, idempotency key, preflight result, external action, provider reference, URL, timestamp, response reference, rollback or correction state, and unavailable fields.

## Handoff Record

Contains assignment, current owner, next owner, permission mode, goal, scope, exact artifacts, evidence, decisions, unresolved questions, blockers, allowed next actions, stop condition, and expected return artifact. Optional cross-team handoffs additionally name the team and may not confer approval or ACT authority implicitly.

## Status Boundary

Suggested states are `idea`, `commissioned`, `researching`, `drafting`, `developmental-review`, `copy-review`, `standards-review`, `production-review`, `ready-for-review`, `approved`, `scheduled`, `published`, `measuring`, `refresh-needed`, `blocked`, and `rejected`. Status alone never substitutes for the records required by the corresponding gate.
