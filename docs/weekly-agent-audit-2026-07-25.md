# Weekly Kujo Agents Audit - 2026-07-25

## Scope

- Repository audited: `/Users/robertdevore/2026/Kujolang/kujo-repos/kujo-agents`
- Sibling repository root: `/Users/robertdevore/2026/Kujolang/kujo-repos`
- Priority window: repositories with latest local commits from 2026-07-18 through 2026-07-25.
- Requested skill: `$kujo-agent-auditor`; no installed or local skill package with that name was found. This audit used the prior weekly audit record, local agent conventions, sibling README/AGENTS/SKILL evidence, git commit dates, and repository-backed workflow records.

## Repositories Reviewed

Recent sibling repositories with agent-facing evidence:

| Repository | Latest local commit date | Agent-facing capability | Classification |
|---|---:|---|---|
| `kujo-skills` | 2026-07-25 | Skills index now includes `kujo-benchmarks-capsule-workflows` and refreshed weekly audit targets | Directly verified from `SKILLS_INDEX.md` |
| `kujo-workflows` | 2026-07-25 | Workflow catalog dependency audit contract and refreshed weekly workflow evidence | Directly verified from README |
| `kujo` | 2026-07-24 | Runtime/stdlib release-contract stabilization and local binary installer work | Preserved existing Tooling/Core/Release ownership |
| `ai-sdk` | 2026-07-24 | Artifact guard workflow pin; no new agent-facing ownership | Preserved existing Integration/Backend ownership |
| `watchdog` | 2026-07-24 | Session token visibility, backup/archive views, dashboard and trace interaction fixes, telemetry preservation | Directly verified from git log and README; existing Integration/Receipt ownership preserved |
| `ai-chat` | 2026-07-24 | Streaming durability, tool continuation timeout, local runtime tool errors, usage accounting, public tunnel probes, UI state fixes | Directly verified from git log and README; existing app/integration ownership preserved |
| `spec` | 2026-07-24 | Parity verifier tolerance for runtime banners | Preserved existing planning/spec ownership |
| `eval` | 2026-07-24 | Command policy gate repair | Preserved verification ownership |
| `fence` | 2026-07-24 | CLI argument parsing inlined | Preserved architecture/security/release ownership |
| `patchbrief` | 2026-07-24 | CLI parsing helpers inlined | Preserved code-review/triage/docs ownership |
| `rag` | 2026-07-24 | Release evaluation gate stabilization | Preserved research/backend ownership |
| `shipcheck` | 2026-07-24 | CLI helpers inlined | Preserved release/risk ownership |
| `changebucket` | 2026-07-24 | CLI parsing repair | Preserved code-review/risk ownership |
| `workcell` | 2026-07-20 | Patch generation, environment policy, artifact policy, and local Docker artifact ignore repairs | Preserved bounded execution-gate ownership |
| `tribunal` | 2026-07-20 | Input-boundary hardening | Preserved advisory decision-gate ownership |
| `benchmarks-capsule-v3` | none recorded | Kujo-native deterministic offline project handoff CLI with `make`, `inspect`, `validate`, stable output, manifests, checksums, and shallow redaction | Directly verified from README; added to existing roles |
| `benchmarks-system` | none recorded | Provider-neutral benchmark execution/review prompt kits for AI Chat pane-profile runs and PDF-quality review artifacts | Partially verified from README; deferred as prompt-kit relationship |
| `kujo-hyperframes` | 2026-07-15 | Source-grounded static campaign and video composition surface with claim-map constraints | Directly verified from README; added to existing frontend/docs/product/visual roles |

## Agent File Completeness

- All root and chain agents still have `AGENT.md` and `SKILL.md`.
- Every Zelus agent still has `AGENT.md`, `SKILL.md`, and `definition.json`.
- No missing canonical agent files were found.
- No new agents were created.

## Changes Made

- Updated `chain-of-command/00-ecosystem-inventory.md` with Capsule, Benchmark System, Kujo Hyperframes, and recent Watchdog/AI Chat/verification-tool boundary notes.
- Updated `chain-of-command/00-tool-agent-map.md` with Capsule, Benchmark System, and Kujo Hyperframes classifications, ownership, inferred boundaries, and evidence sources.
- Updated `chain-of-command/README.md` to include Capsule, Benchmark System, and Kujo Hyperframes in the chain support model and agent table.
- Updated affected agent contracts:
  - `context-packager`: Capsule packages and `kujo-benchmarks-capsule-workflows`.
  - `research-analyst`: Capsule as deterministic offline handoff evidence.
  - `qa-lead`: Capsule benchmark evidence and Benchmark System prompt-kit boundary.
  - `frontend-developer`: Kujo Hyperframes as an assigned static/campaign surface.
  - `visual-qa-agent`: browser/video proof for Hyperframes surfaces.
  - `documentation-writer`: Hyperframes claim-map copy boundary.
  - `product-strategist`: Benchmark System outputs and Hyperframes claim-map narrative boundary.
  - `receipt-collector`: Capsule manifests as evidence artifacts.
- Updated `docs/deferred-agent-opportunities.md` with rejected/deferred new-agent candidates for Capsule, Benchmark System, and Hyperframes.

## Preserved Boundaries

- Capsule was not treated as a full secret scanner, semantic code-intelligence system, or replacement for Scout/Scent.
- Benchmark System was not treated as a supported standalone CLI because the inspected README describes prompt kits and AI Chat pane-profile workflows.
- Kujo Hyperframes was not granted authority to make unsupported launch, customer, adoption, benchmark, public-registry, sandbox, or AI-vision claims.
- Recent CLI fixes in Eval, Fence, PatchBrief, ShipCheck, and ChangeBucket strengthened existing relationships but did not justify new ownership.
- Watchdog and AI Chat changes preserved current integration, receipt, frontend, backend, QA, and visual QA boundaries.

## Validation

Completed validation:

- Agent package completeness check passed for root, chain, and Zelus agent packages.
- Markdown heading check passed for repository Markdown files.
- Skill references in chain agent contracts were checked against the local installed skill list plus sibling `kujo-skills/SKILLS_INDEX.md`.
- Sibling README evidence was inspected for Capsule, Benchmark System, Kujo Hyperframes, Kujo Workflows, and Kujo Skills.
- `git diff --check` passed.
- Zelus interpreter checks passed from `zelus/`: `zelus_contract_tests.kujo`, `zelus_registry_tests.kujo`, and `zelus_cli_tests.kujo`.

Partial boundary:

- `python3 -m pytest tests` still collected zero tests and exited with pytest code 5 because this checkout has no tracked Python test source files under `tests/`.
- A direct VM run from the repository root failed to resolve `src.common`; the Zelus suites pass when run from the `zelus/` package root with `--interpreter`, matching the package-local import layout.
- Live sibling gates were not run for docs-only agent-contract updates. Relationships are limited to directly verified README paths, local skill/index evidence, git-log evidence, and existing workflow-contract documentation.

## Confirmed Current

- Strategic, planning, execution, verification, knowledge, and worker roles remain separate.
- Implementation agents still cannot approve their own release, security, or governance outcomes.
- Worker agents remain bounded to explicit commands and evidence collection.
- Relay, Workcell, Tribunal, SiteKit, StegoCipher Kujo, and CMS Experience boundaries from the 2026-07-18 audit remain current.

## Watch Items For Next Audit

- Verify whether `$kujo-agent-auditor` becomes an installed skill or repository-backed workflow.
- Check whether `benchmarks-system` gains a stable executable CLI or machine-readable contract.
- Check whether Capsule graduates from benchmark artifact to broader first-party context-packaging tool with installable workflow paths.
- Check whether Hyperframes accumulates recurring campaign surfaces that require a stronger release or claim-validation gate.
- Recheck Watchdog/AI Chat telemetry, token, and streaming changes if agent performance or cost-review failures recur.
