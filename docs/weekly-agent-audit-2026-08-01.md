# Weekly Kujo Agents Audit - 2026-08-01

## Scope

- Repository audited: `/Users/robertdevore/2026/Kujolang/kujo-repos/kujo-agents`
- Sibling repository root: `/Users/robertdevore/2026/Kujolang/kujo-repos`
- Priority window: repositories with latest local commits from 2026-07-25 through 2026-08-01.
- Requested skill: `$kujo-agent-auditor`; no installed or local skill package with that name was found. This audit used the prior weekly audit record from git history, local agent conventions, sibling README/AGENTS/SKILL evidence, git commit dates, and repository-backed workflow records.

## Repositories Reviewed

| Repository | Latest local commit date | Agent-facing capability | Classification |
|---|---:|---|---|
| `kujo-skills` | 2026-08-01 | Refreshed Agents SDK, AI Chat, SiteKit, and SSG skills; canonical SiteKit skill is `kujo-site-kit-workflows` with `kujo-sitekit-workflows` retained as compatibility alias | Directly verified from `SKILLS_INDEX.md` and skill files |
| `kujo-workflows` | 2026-08-01 | Refreshed catalog audit and Workcell temp-root gate; Tribunal, Relay, and Workcell remain contract-gated optional workflows | Directly verified from README and git log |
| `kujo-hyperframes` | 2026-08-01 | Added `kujo-ai-transmission/` source-grounded video composition and rendered media outputs | Directly verified; existing frontend/docs/product/visual ownership preserved |
| `ai-chat` | 2026-07-31 | Sidebar action/title fixes, provider-independent offline smoke, clean port-conflict handling, stream continuity after browser disconnects, streamed provider error handling | Directly verified; existing app/integration/frontend/QA ownership preserved |
| `agents-sdk` | 2026-07-28 | MCP 2026 adapter helpers for stateless JSON-RPC, per-request `_meta`, Streamable HTTP headers, tool-list cache metadata, input-required normalization, unsupported-version errors, schema/display metadata | Directly verified; existing Systems Architect and Integration Engineer ownership preserved |
| `redact` | 2026-07-28 | Local deterministic scan/sanitize/verify/pack pipeline for text and Markdown with audit manifests | Directly verified; added to Security Reviewer, Context Packager, and Receipt Collector |
| `ssg` | 2026-07-28 | Static-site generation, generated-output validation, DocGen bridge, reusable docs starter, release gates | Directly verified; added to Documentation Writer, Frontend Developer, Visual QA Agent, and Release Verifier map |
| `intake` | 2026-07-28 | Local-first inbound work normalization, policy-gated actions, dashboard, source adapters, audit logs | Deferred; no dedicated chain skill/workflow verified |
| `cinch` | 2026-07-28 | macOS-first development harness for workspaces, files, git, commands, tools, MCP, proof artifacts, Trail export | Deferred; no dedicated chain skill/workflow verified |
| `diff-viewer-demo`, `diff-viewer-demo-fresh`, `diff-viewer-verified` | 2026-07-31 to 2026-08-01 | Small fixture repositories for diff-review testing | Unsupported as active Kujo agent capability |

## Agent File Completeness

- Root packages and chain agents retain canonical `AGENT.md` and `SKILL.md` files.
- Zelus agent packages retain `AGENT.md`, `SKILL.md`, and `definition.json`.
- The deleted deferred-opportunity record was recreated because recurring audits require a current deferred-opportunity file.
- No new agents were created.

## Changes Made

- Updated `chain-of-command/00-ecosystem-inventory.md` with Redact, SSG, refreshed Agents SDK, AI Chat, Kujo Skills, Kujo Workflows, Hyperframes, Intake, Cinch, and Diff Viewer classifications.
- Updated `chain-of-command/00-tool-agent-map.md` with Redact and SSG supported relationships plus deferred/unsupported Intake, Cinch, and Diff Viewer boundaries.
- Updated `chain-of-command/README.md` and affected agent contracts for SSG, Redact, and canonical `kujo-site-kit-workflows` references.
- Added `docs/deferred-agent-opportunities.md` with current deferred/rejected candidate records for Intake, Cinch, and Diff Viewer fixture stewardship.

## Preserved Boundaries

- Redact is not complete PII removal, compliance signoff, full YAML support, or approval to store originals.
- SSG is not hosted publishing or a production-certified docs platform.
- Intake and Cinch are not granted broad chain ownership until a stable chain-specific skill/workflow contract exists.
- Diff Viewer repositories are fixtures only, not tool capabilities.
- Hyperframes remains source-grounded; video outputs do not bypass claim maps or visual proof requirements.
- AI Chat and Agents SDK updates strengthen existing relationships but do not change strategic ownership.

## Validation

Completed validation:

- Agent package completeness check passed for root, chain, and Zelus agent packages.
- Markdown heading check passed for repository Markdown files.
- Skill references in chain agent contracts were checked against the local installed skill list plus sibling `kujo-skills/SKILLS_INDEX.md`.
- Sibling README/git-log evidence was inspected for Redact, SSG, Intake, Cinch, Diff Viewer fixture repos, AI Chat, Agents SDK, Kujo Skills, Kujo Workflows, and Kujo Hyperframes.
- `git diff --check` passed.
- Zelus interpreter checks passed from `zelus/`: `zelus_contract_tests.kujo`, `zelus_registry_tests.kujo`, and `zelus_cli_tests.kujo`.

Partial boundary:

- Live sibling repository gates were not run for docs-only agent-contract updates. Relationship classifications are limited to directly verified README paths, local skill/index evidence, git-log evidence, and existing workflow-contract documentation.
- Workcell proof was not rerun for this docs-only audit; the current launch checklist still records the last passing Workcell proof.

## Confirmed Current

- Strategic, planning, execution, verification, knowledge, and worker layers remain separated.
- Implementation agents still cannot approve their own release, security, or governance outcomes.
- Worker agents remain bounded to explicit commands and evidence collection.
- Common recovery, suspension, stop-condition, and token-efficiency protocol remains centralized in `chain-of-command/README.md`.

## Watch Items For Next Audit

- Verify whether `$kujo-agent-auditor` becomes an installed skill or repository-backed workflow.
- Check whether Intake or Cinch gain narrow `kujo-skills` entries or `kujo-workflows` contracts.
- Check whether Diff Viewer fixture repositories remain throwaway review fixtures or become a supported review harness.
- Check whether SSG docs starter adoption creates repeated work that needs stronger documentation/visual QA routing.
- Check Redact usage for recurring sensitive-context packaging failures or overclaims.
