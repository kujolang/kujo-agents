# Canonical VideoOps tools migration

The operator clarified on 2026-09-07 that the standalone `kujo-videoops` repository was retired and new VideoOps work belongs in `kujo-agents`. Repository history confirms the canonical agent team was introduced here in `b8e62745462aa771d010a60675a36abdf4ab9b64` (2026-09-04), followed by the reusable Producer in `062ada111e204934ad4e6adf8c2d06a1366acd48`. No explicit retirement commit was found in either repository; the operator correction establishes retirement authority.

The previous change put executable media/QA/review work in the wrong repository (`94418db`, `5e7512c`, `1dc9b9e`, `4511017`, `6442fbb`, merged as `20b32df7fbe93ddfbad69ab0df9cb3c36519ecf2`). The corresponding agents commit `5db17b3` only routed contracts to that external implementation. This migration corrects that ownership.

`videoops/tools/` now contains the provider service, ElevenLabs TTS/timestamps/SFX/music adapters, local import, scoped authorization and reservations, provenance, source-aware audio QA, exact-candidate review, canonical schemas, CLI, documentation and regression tests. Portable copies are generated locally. Source file hashes and the precise source commit are recorded in `videoops/tools/docs/migration-source.json`. Original MIT license is retained by this MIT repository; source history remains available without rewriting or deleting prior releases.

The old fixture orchestrator, job-control API, duplicate Agent Projects and generated videos were not transplanted into the production tools. Producer orchestration remains with the existing six role packages and the production workflow. Existing v1 artifact identifiers and workspace/receipt formats are preserved. This is ownership correction, not a destructive production-workspace migration.

Use `videoops/tools/bin/videoops` from any working directory, or install the renamed distribution `kujo-agents-videoops` in a dedicated environment. The compatible Python namespace remains `videoops`; do not co-install the retired distribution in that environment. Companion skills and workflow discovery now target `kujo-agents/videoops/tools`.

Historical live verification from the source release is retained as dated evidence, not represented as a fresh provider call: TTS succeeded, SFX was unauthorized, Free-plan music was blocked locally. Migration verification uses offline provider mocks and real local audio/import/review tests; it spends no provider credits. The isolated tools-copy regression demonstrates executable import and CLI discovery without a retired repository dependency.

Three legacy `FixtureWaitingReviewTest` cases depend on the retired job orchestrator and stay with that excluded implementation. All `ReviewService` regressions are retained; candidate binding, incomplete-review resume, failed-attempt counters and promotion are tested directly here. The migration suite counts production-tool coverage rather than claiming the old repository-wide 87-test total.
