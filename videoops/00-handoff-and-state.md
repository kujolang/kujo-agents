# VideoOps Handoff and State

Every stage emits `kujo.handoff/v1` with assignment, current owner, next owner, goal, scope, artifact paths, evidence, decisions, unresolved questions, allowed next actions, and stop condition.

Supported states are `INTAKE_READY`, `PLANNING`, `PLANNING_READY`, `ASSETING`, `ASSETS_READY`, `GENERATING`, `PRODUCTION_READY`, `EDITING`, `DRAFT_READY`, `REVIEWING`, `REVISION_REQUIRED`, `APPROVED`, `FINAL_RENDERING`, `COMPLETE`, and `BLOCKED`.

Only declared transitions are valid. A stage cannot advance while required artifacts fail validation. Critic FAIL returns a fix list to the editor. After three unsuccessful editor/critic cycles, state becomes BLOCKED and the unresolved issues go to a human rather than looping.
