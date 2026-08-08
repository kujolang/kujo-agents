# Weekly Kujo Agents Audit - 2026-08-08

## Scope

- Repository audited: `/Users/robertdevore/2026/Kujolang/kujo-repos/kujo-agents`
- Sibling repository root: `/Users/robertdevore/2026/Kujolang/kujo-repos`
- Priority window: repositories with latest local commits from 2026-08-01 through 2026-08-08, plus previously untracked sibling repositories with agent-facing surfaces.
- Requested skill: `$kujo-agent-auditor`; no installed or local skill package with that name was found again. This audit used local agent conventions, prior weekly audit notes, sibling README/AGENTS/SKILL evidence, git commit dates, and repository-backed workflow/skill records.

## Repositories Reviewed

| Repository | Latest local commit date | Agent-facing capability | Classification |
|---|---:|---|---|
| `kujo` | 2026-08-08 | v1.0.0 launch evidence, release artifact handling, DocGen concurrency, stable contract guards | Directly verified; existing core/tooling/release/security/docs ownership preserved |
| `kujo-docs` | 2026-08-08 | Official `docs.kujolang.ai` SSG/SiteKit-backed public docs site with deploy, favicon, IA, content, and validation guidance | Directly verified; added to docs/frontend/visual/product/release routing |
| `kujo-skills` | 2026-08-08 | Refreshed Kujo v1 release skill guidance plus Howl and Kennel workflow routing | Directly verified; existing skill-reference relationships preserved |
| `kujo-workflows` | 2026-08-08 | Weekly workflow audit refresh; contract-gated workflow boundaries remain current | Directly verified |
| `howl` | 2026-08-08 | Deterministic branded social-card rendering in addition to Markdown/HTML/SVG galleries and captions | Directly verified; existing Documentation Writer ownership preserved with product/visual review support when assigned |
| `kennel` | 2026-08-08 | v1.0.0 release prep, CLI compatibility shims, module-name collision fix, trust/source/package workflows | Directly verified; existing Dependency Scanner and Tooling Developer ownership preserved |
| `ssg` | 2026-08-08 | v1.0.0 release prep, nested-output repair, Kujo docs IA support | Directly verified; existing docs/frontend/visual/release ownership preserved |
| `agents-sdk`, `eval`, `lens`, `mcp`, `muzzle`, `packwrite`, `patchbrief`, `rag`, `runledger`, `scent`, `scout`, `shipcheck`, `watchdog` | 2026-08-08 | v1.0.0 release prep; Watchdog pricing catalog refresh | Directly verified from git/README/skill evidence; no ownership changes |
| `totalrecall` | 2026-08-08 | Local-first ingestion from Fathom/chat/Slack/GitHub into Strata, markdown, HTML, or local indexes | Deferred; no dedicated chain skill/workflow and live-provider credential boundaries remain |
| `ward` | 2026-07-25 | Local Dependabot alert collection/planning/report/dashboard/fix prep with read-only defaults | Deferred; no dedicated chain skill/workflow and GitHub token/process boundary remains |
| `leash` | 2026-07-25 | Local/mobile AI-agent supervision with policy, adapters, JWT auth, audit trail, and approvals | Deferred; no dedicated chain skill/workflow and device/runtime validation remains |
| `diff-viewer-inline-review-fresh` | 2026-08-02 | Inline-review fixture with finite-score validation | Unsupported as active Kujo agent capability |

## Agent File Completeness

- Added missing canonical `AGENT.md` files for root `archivist/` and `kujo-archivist/` packages using their existing `SKILL.md` and reference rules as source of truth.
- Chain agents still retain paired `AGENT.md` and `SKILL.md` files.
- Zelus agent packages still retain `AGENT.md`, `SKILL.md`, and `definition.json`.
- No new agents were created.

## Changes Made

- Updated `chain-of-command/00-ecosystem-inventory.md` for 2026-08-08 sibling repository evidence, including Kujo Docs, Howl, Kennel, TotalRecall, Ward, Leash, and the inline diff-review fixture.
- Updated `chain-of-command/00-tool-agent-map.md` with Kujo Docs active routing, Howl social-card boundaries, deferred TotalRecall/Ward/Leash relationships, and current evidence sources.
- Updated `chain-of-command/README.md` and affected agent contracts for Kujo Docs as a concrete docs/frontend/visual/product surface.
- Added deferred opportunity records for Context Ingestion Steward, Dependabot Security Coordinator, and Mobile Agent Supervisor.
- Added root `archivist/AGENT.md` and `kujo-archivist/AGENT.md`.

## Preserved Boundaries

- Kujo Docs content does not promote every documented repository to production-ready.
- Howl social cards remain deterministic source-backed artifacts; Howl does not post, schedule, call LLMs, or invent claims.
- TotalRecall, Ward, Leash, Intake, and Cinch remain deferred until stable chain skills/workflows and approval/credential/runtime boundaries exist.
- Diff Viewer repositories remain fixtures, not tool capabilities.
- Existing separation between strategy, planning, execution, verification, knowledge, and worker agents remains intact.

## Validation

Completed validation:

- Agent package completeness check passed for root, chain, and Zelus agent packages after adding the two root `AGENT.md` files.
- Chain skill references were checked against local installed skills and sibling `kujo-skills` entries.
- Sibling README/git-log/skill/workflow evidence was inspected for changed or newly assessed repositories.
- Required agent inventory command completed: `find . -maxdepth 3 \( -name AGENT.md -o -name SKILL.md -o -name README.md \) | sort`.
- Zelus doctor passed with 10 agents, 83 skills, and 14 workflows.
- Zelus reference campaign passed and wrote `/tmp/zelus-reference-20260808/casefile.json`.
- Zelus contract tests passed: 15 passed, 0 failed.
- Zelus CLI contract tests passed.
- Zelus registry and adapter tests passed.
- `git diff --check` passed.

Partial boundary:

- Live sibling repository gates were not run for docs-only agent-contract updates. Relationship classifications are limited to README paths, local skill/index evidence, git-log evidence, and existing workflow-contract documentation.
- `$kujo-agent-auditor` remains unavailable as an installed or local skill.

## Potential New Agents

- Recorded deferred `Context Ingestion Steward` for TotalRecall.
- Recorded deferred `Dependabot Security Coordinator` for Ward.
- Recorded deferred `Mobile Agent Supervisor` for Leash.
- Rejected creating new agents during this audit; existing roles can review or consume artifacts from these repositories when explicitly assigned.

## Confirmed Current

- Active tool ownership remains least-privilege and capability-scoped.
- Implementation agents still cannot approve their own release, security, or governance outcomes.
- Common recovery, suspension, stop-condition, and token-efficiency protocol remains centralized in `chain-of-command/README.md`.
- Root Archivist packages now match the repository convention for canonical agent instructions plus skills.

## Watch Items For Next Audit

- Verify whether `$kujo-agent-auditor` becomes an installed skill or repository-backed workflow.
- Check whether TotalRecall, Ward, Leash, Intake, or Cinch gain narrow `kujo-skills` entries or `kujo-workflows` contracts.
- Check whether Kujo Docs adds new agent-facing docs generation, deployment, or visual proof obligations.
- Check whether Howl social-card use creates repeated product/docs review work requiring stronger routing.
- Check whether Diff Viewer fixture repositories remain temporary review fixtures or become a maintained review harness.
