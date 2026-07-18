# Weekly Kujo Agents Audit - 2026-07-18

## Scope

- Repository audited: `/Users/robertdevore/2026/Kujolang/kujo-repos/kujo-agents`
- Sibling repository root: `/Users/robertdevore/2026/Kujolang/kujo-repos`
- Priority window: repositories with latest commits from 2026-07-15 through 2026-07-18.
- Requested skill: `$kujo-agent-auditor`; no installed or local skill package with that name was found. The audit used repository conventions, local agent contracts, sibling README/AGENTS/SKILL evidence, and the closest repo-backed Kujo workflow records instead.

## Repositories Reviewed

Recent sibling repositories with agent-facing evidence:

| Repository | Latest local commit date | Agent-facing capability | Classification |
|---|---:|---|---|
| `ai-chat` | 2026-07-18 | Local multi-provider chat app, browser/tool contracts, persistent instructions, Strata handoff template | Directly verified from README; repo-specific skill exists |
| `kujo-workflows` | 2026-07-18 | Workflow catalog now includes Tribunal decision gate, Relay lifecycle handoff, Workcell execution gate | Directly verified from README |
| `kujo-skills` | 2026-07-18 | Skills include `kujo-relay-workflows`, `kujo-workcell-workflows`, `kujo-tribunal-workflows`, `kujo-sitekit-workflows`, and existing tool skills | Directly verified by local skill inventory |
| `watchdog` | 2026-07-17 | Local AI/proxy telemetry, dashboard APIs, cost/failure traces, agent insight signals | Directly verified from README |
| `relay` | 2026-07-16 | Bounded mission orchestration, run state, pause/resume/cancel, lifecycle receipts, provider/tool bridge evidence | Directly verified from README and `.kujo` files; local alpha boundary preserved |
| `cms-experience` | 2026-07-16 | CMS Studio/public site layer, contract checks, live gate scripts, explicit auth limitations | Directly verified from README |
| `cms` | 2026-07-15 | Server-first CMS backend, delivery/API contracts, release gate evidence, documented public-launch gaps | Directly verified from README |
| `workcell` | 2026-07-15 | Disposable Git worktree/container execution gate, receipts, artifacts, verification, cleanup | Directly verified from README and `.kujo` files; host boundary remains operator-owned |
| `tribunal` | 2026-07-15 | Adversarial decision review, fatal-flaw pass, ruling, decision packet, release/security gate scripts | Directly verified from README and `.kujo` files; advisory only |
| `site-kit` | 2026-07-15 | Internal design-system build, lint, validate, snapshot, smoke, component contracts | Directly verified from README |
| `stego-cipher-kujo` | 2026-07-15 | Educational steganography/obfuscation CLI and smoke suite | Directly verified from README; unsupported for cryptographic secrecy |

## Agent File Completeness

- All root and chain agents have `AGENT.md` and `SKILL.md`: `archivist`, `kujo-archivist`, and every `chain-of-command/*` agent directory.
- Every Zelus agent has `AGENT.md`, `SKILL.md`, and `definition.json`.
- `chain-of-command/00-docs/` correctly remains a support-doc folder, not an agent package.
- No missing canonical agent files were found for existing agents.

## Changes Made

- Updated `chain-of-command/00-ecosystem-inventory.md` with recent repository capabilities and maturity boundaries for Relay, Workcell, Tribunal, SiteKit, StegoCipher Kujo, and CMS Experience.
- Updated `chain-of-command/00-tool-agent-map.md` with capability classifications, agent ownership updates, evidence sources, and explicit unsupported/inferred boundaries.
- Updated `chain-of-command/README.md` with the new optional bounded capabilities and a common recovery/token protocol for all chain agents.
- Updated affected agent contracts:
  - `general-commander`: Relay lifecycle evidence and Tribunal advisory packets.
  - `integration-engineer`: Relay and CMS Experience.
  - `tooling-developer`: Workcell.
  - `frontend-developer`: SiteKit and CMS Experience.
  - `risk-officer`: Tribunal advisory packets and Workcell boundary evidence.
  - `release-verifier`: Relay, Workcell, and Tribunal gate artifacts.
  - `triage-agent`: Relay run evidence.
  - `qa-lead`: Workcell receipts.
  - `security-reviewer`: Workcell boundary evidence and StegoCipher as review subject.
  - `visual-qa-agent`: SiteKit snapshots.
  - `documentation-writer`: SiteKit docs/component evidence.
  - `routine-worker` and `test-runner`: Workcell only when explicitly assigned.
  - `receipt-collector`: Relay lifecycle handoff receipts.
- Added this audit record and the deferred opportunity record for potential future agents.

## Preserved Boundaries

- No new agents were created.
- Relay was not treated as enterprise tenancy, remote exactly-once delivery, or universal provider proof.
- Workcell was not treated as a hardened microVM, hosted sandbox, or replacement for operator-owned Docker/Podman controls.
- Tribunal was not granted decision authority; it remains advisory evidence for humans or authorized strategic/release/security roles.
- SiteKit access stayed tied to frontend, visual QA, documentation, and product surfaces; consuming layouts still need browser/accessibility proof.
- StegoCipher Kujo was recorded only as an educational/demo/security-review subject, not a cryptographic tool.
- CMS Experience remained coupled to CMS backend contracts and documented auth/production gaps.

## Validation

Completed validation:

- Agent package completeness check passed for root, chain, and Zelus agent packages.
- Local skill inventory confirmed newly referenced skill directories for Relay, Workcell, Tribunal, SiteKit, and existing tool skills.
- Sibling repository README/path evidence was checked for all new or recently changed capability relationships listed above.
- Markdown heading check passed for chain/support docs.
- `git diff --check` passed.
- Zelus checks passed: `zelus_contract_tests.kujo`, `zelus_registry_tests.kujo`, and `zelus_cli_tests.kujo`.

Partial boundary:

- `python3 -m pytest tests` collected zero tests and exited with pytest code 5 because this checkout has no tracked Python test files under `tests/`.
- Full live execution of sibling repository gates was not required to support these documentation and agent-contract changes. Relationship support is therefore limited to directly verified repository paths, README contracts, local skill names, and existing workflow-catalog evidence.

## Confirmed Current

- Existing chain layer separation remains current: strategic, planning, execution, verification, knowledge, and worker roles remain distinct.
- Worker agents remain restricted to explicit bounded commands and evidence collection.
- Implementation agents do not gain authority to approve their own release, security, or governance outcomes.
- Root `archivist` and `kujo-archivist` package layout remains intentionally separate from `chain-of-command/`.
- Zelus roster files remain complete and no Zelus authority changes were made.

## Watch Items For Next Audit

- Verify whether `$kujo-agent-auditor` becomes an installed skill or repository-backed workflow.
- Check whether Relay gains live-provider proof, durable concurrent storage, authenticated tenancy, or stronger enterprise-readiness evidence.
- Check whether Workcell adds stronger isolation backends, scheduling/reassignment, or enterprise deployment controls.
- Check whether Tribunal moves from advisory local gates toward signed or multi-host production decision governance.
- Check whether CMS Experience resolves P1 public-production gaps around human auth, tenant/workspace isolation, and secure draft preview.
- Check whether SiteKit gains browser/accessibility proof for representative consuming layouts.
