# Shared media and review runtime

The executable owner is `kujo-videoops`, not these Markdown roles. See
`docs/videoops-toolchain-contract.json`. Run its CLI from that repository or an
operator-installed environment. Never copy a production's private provider script.

Audio requirements use versioned media requests. Speech, SFX and music are separate
capabilities: successful speech access does not establish music entitlement.
ElevenLabs and local import are implemented adapters; local import is not a second
live provider. Transcription and catalog availability must be discovered separately.
Doctor/providers default to local inspection with no account access or generation.

Creative Director defines speech intent, language, duration and required alignment.
Scout records rights and intended use, then marks bounded missing requirements
GENERATE. Media Generator resolves those items through the shared runtime, retaining
scoped authorization across resume. Requests reference secrets out of band; no
credential values belong in CLI arguments, prompts, artifacts or handoffs. Unknown
outcome requires reconciliation before retry, not another blind billable call.

A successful acquisition is not usage approval. Asset records retain requirement
status, acquisition status, usage_status, and media_result receipt separately. The
result preserves original bytes, derivative hashes, actual metadata, alignment or
explicit absence, observed usage and rights evidence. Never infer zero cost from
missing evidence. Selected voice, glitch treatment and branding are project inputs.

HyperFrames media-use and audio workflows consume approved workspace-local paths
and their result receipts. Editor owns placement, mixing and declared derived edits;
the shared QA tool measures source preservation, phrase-boundary candidates,
clipping, cue overlap and post-master comparisons. A suspicious tail is a review
finding, not authority to trim speech. Preserve originals and rerun affected QA.

Technical PASS and perceptual approval are separate. REVIEW_INCOMPLETE preserves
the exact candidate and routes to a capable reviewer or authorized human, without
rerendering unchanged media or consuming critic-failure/editor-repair cycles. Real
artifact defects still produce bounded fixes and retain the existing cycle limit.
All mandatory gates and the current SHA-256 must pass before promotion; filenames
and previous approvals are insufficient. Keep user revisions, render attempts,
technical repairs, critic failures and review attempts separate.

The canonical new runtime JSON schemas live in `kujo-videoops/contracts`. Regenerate
portable copies with `kujo run scripts/sync_videoops_media_contracts.kujo`; verify
with the same command plus `-- --check`. Copies under `schemas/videoops/runtime`
are byte-identical and have a SHA manifest. The existing legacy schemas and explicit
offline fixtures remain supported; never reinterpret their synthetic approval as
production judgment. Runtime schemas reject unknown versions.

## CLI handoff

From the kujo-videoops runtime directory:

```bash
python3 -m videoops.cli media doctor --workspace /absolute/project
python3 -m videoops.cli media providers --workspace /absolute/project
python3 -m videoops.cli media import --workspace /absolute/project --request /absolute/project/requests/import.json
python3 -m videoops.cli media authorize --workspace /absolute/project --authorization /absolute/project/requests/authority.json --authorize-local
python3 -m videoops.cli media generate --workspace /absolute/project --request /absolute/project/requests/speech.json
python3 -m videoops.cli media status --workspace /absolute/project --request-id speech-001
python3 -m videoops.cli review submit-candidate --workspace /absolute/project --candidate output/draft.mp4
python3 -m videoops.cli review record --workspace /absolute/project --decision /absolute/project/review/human.json --authorize-local
python3 -m videoops.cli review resume --workspace /absolute/project
python3 -m videoops.cli review promote --workspace /absolute/project --destination output/final.mp4 --authorize-local
```

The example IDs/paths require project-specific schema-valid artifacts. Authority
creation and review import are explicit operator actions, never automatic approval.
Results are `media/<request_id>/result.json` and `handoff.json`, registered in
`assets/asset-manifest.json`; pass those artifacts to Editor and HyperFrames.
Use revoke with `--authorization-id`; reconcile with `--request-id` and an explicit
`--disposition confirmed-failed|confirmed-cancelled` only after outcome evidence.
Do not treat this disposition as a provider idempotency guarantee.

`media inspect --authorization-id <id> --authorize-local` is an explicit
authenticated entitlement inspection, not a media-file inspector. Revoke and
reconcile also require `--authorize-local`. Use doctor/providers for local-only
discovery. `review render-attempt --attempt-id <id> --outcome failed|succeeded`
records harness render attempts separately. Source-aware QA is invoked from the
runtime with `python3 scripts/qa_media.py <workspace> --video <relative-media>
--audio-only --audio-config <relative-config>`; the config declares sources, edits
and cue comparisons rather than silently inventing them.

## Operator-approved reservation bounds

Authorization binds a `request_bounds` entry to each exact request fingerprint,
maximum credits/cost and estimate evidence approved by the operator. A request
cannot reduce its own reservation to evade the authorized budget. Compute the
fingerprint with `python3 -m videoops.cli media fingerprint --workspace <absolute-workspace> --request <workspace-request.json>`,
review the request and estimate evidence, then include that exact fingerprint and
bounds in the authorization artifact. Changing the request needs a newly approved
bound; do not reuse a fingerprint for different content, model or output settings.
The runtime enforces those bounds at dispatch across workers and resumes.

Doctor may receive `--request <workspace-request.json>` to evaluate an exact
request against stored scope without network access. Diagnostic test_evidence
records distinguish local, mocked and live observations; configured or executable
is not a claim of live verification. Media results carry an explicit verification
classification (`local`, `mock`, or `live`).
