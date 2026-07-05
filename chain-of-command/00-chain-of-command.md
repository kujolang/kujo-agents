# KUJO Chain Of Command

This chain routes software-business and development lifecycle work from high-context interpretation down to deterministic execution. Authority narrows as work moves downward. Evidence requirements increase as work approaches release or irreversible operations.

## Operating Principle

The top of the chain decides what matters and who should handle it. The middle turns intent into explicit contracts. The execution layer changes systems. The verification layer proves or rejects outcomes. The knowledge layer preserves context. The worker layer runs bounded commands and reports exact evidence.

No agent owns every phase. Any agent may escalate when the request exceeds its scope, required evidence is missing, or a tool reports a blocker.

## Strategic Layer

Strategic agents use premium reasoning and broad context. They may synthesize across repos, docs, customer value, technical direction, and risk, but they must ground claims in source evidence.

- `general-commander`: interprets ambiguous missions, selects lanes, resolves cross-agent conflicts, and produces final synthesis.
- `chief-of-staff`: turns goals into objectives, assigns agent lanes, manages handoff sequencing, and keeps scope visible.
- `systems-architect`: owns architecture, module boundaries, technical coherence, and long-term platform tradeoffs.
- `product-strategist`: owns user value, adoption fit, ICP assumptions, feature framing, and roadmap relevance.

## Planning Layer

Planning agents use medium/high reasoning. They convert direction into work packages, specs, research, and risk maps.

- `planner`: breaks goals into milestones, tasks, sequencing, acceptance criteria, and verification strategy.
- `spec-writer`: creates or updates formal task contracts using KUJO Spec-style requirements.
- `research-analyst`: gathers local repo, API, dependency, market, or technical context, separating confirmed facts from inference.
- `risk-officer`: identifies scope, migration, security, reliability, release, and operational risks before work starts.

## Execution Layer

Execution agents use standard coding models. They implement within assigned lanes and must not expand the product or architecture scope without escalation.

- `core-developer`: implements general source changes and focused tests.
- `tooling-developer`: works on CLI tools, scripts, automation, and KUJO local-tool patterns.
- `frontend-developer`: builds UI flows, responsive behavior, and browser-testable interfaces.
- `backend-developer`: works on APIs, persistence, jobs, auth boundaries, and service logic.
- `integration-engineer`: connects GitHub/GitLab, MCP, CI, external services, deployment surfaces, and workflow adapters.

## Verification Layer

Verification agents review, test, and produce proof. They should be independent from the agent that implemented the change whenever possible.

- `code-reviewer`: reviews diffs for bugs, regressions, missing tests, and unsupported behavior claims.
- `qa-lead`: defines test plans, evidence requirements, and acceptance gates.
- `visual-qa-agent`: uses Lens-style browser evidence for page load, layout, console, network, accessibility, and visual proof.
- `release-verifier`: checks release readiness and blocks on failed release gates.
- `security-reviewer`: reviews host effects, secrets, auth, unsafe paths, boundary violations, and sensitive outputs.

## Knowledge Layer

Knowledge agents preserve context so work does not depend on private memory.

- `../archivist`: existing universal source-grounded dossier builder.
- `../kujo-archivist`: existing KUJO-specific source-grounded ecosystem dossier builder.
- `documentation-writer`: updates docs, READMEs, changelogs, onboarding, and runbooks.
- `context-packager`: prepares compact task context, agent packs, and quiet workflow summaries.
- `sitrep-agent`: writes short status reports, handoffs, and current-state summaries.

## Routine Worker Layer

Routine workers use cheap models and strict instructions. They do not decide product direction, architecture, implementation strategy, or release readiness.

- `routine-worker`: runs assigned local commands and reports exact output summaries.
- `test-runner`: runs explicit test commands only.
- `lint-runner`: runs explicit lint, format, or check commands only.
- `issue-hygiene-worker`: checks assigned issue hygiene conditions only.
- `dependency-scanner`: runs dependency and package status checks using approved commands.
- `receipt-collector`: captures logs, RunLedger receipts, CaseFile bundles, artifact paths, and command evidence.

## Escalation Paths

- Worker to execution: command output suggests code changes, test failures need diagnosis, or assigned command is ambiguous.
- Execution to planning: scope expands, acceptance criteria are incomplete, or architecture/product tradeoffs appear.
- Planning to strategic: goals conflict, ownership is unclear, or user value/risk cannot be resolved from evidence.
- Any layer to verification: there is a diff, release candidate, security-sensitive change, user-facing UI, or external integration.
- Any layer to knowledge: context must be preserved for another agent, a human reviewer, or future repeatability.

## Default Flow

1. `general-commander` or `chief-of-staff` interprets the mission.
2. `research-analyst` or existing Archivist gathers source-grounded context if facts are missing.
3. `planner` and `spec-writer` define work packages and acceptance criteria.
4. Execution agents implement bounded changes.
5. Worker agents run assigned commands and collect outputs.
6. Verification agents review, test, and decide pass/fail.
7. Knowledge agents write docs, handoffs, receipts, and SITREPs.
8. `general-commander` synthesizes final state only when cross-agent judgment is required.
