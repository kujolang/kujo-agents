# KUJO Agent Chain

This folder defines a reusable KUJO-specific agent chain of command. The chain is operational, not theatrical: it shows who interprets goals, who turns them into work, who implements, who verifies, who preserves knowledge, and which agents are cheap deterministic workers.

Use this system when a team wants to run software-business or development lifecycle work through specialized agents while keeping authority, evidence, and handoffs explicit.

## How To Choose An Agent

Start as high as the ambiguity requires:

- Use strategic agents when the goal, product framing, architecture direction, or risk posture is unclear.
- Use planning agents when the goal is known but needs milestones, specs, research, or acceptance criteria.
- Use execution agents when the task has a bounded implementation lane.
- Use verification agents when there is a diff, build, release candidate, visual surface, or security-sensitive change to inspect.
- Use knowledge agents when context, docs, handoff, or status artifacts are the main output.
- Use routine workers only for explicit, bounded commands and evidence collection.

## Model Tiers

Use premium reasoning for `General Commander`, `Chief of Staff`, `Systems Architect`, `Product Strategist`, `Risk Officer`, `Security Reviewer`, and major release calls.

Use standard coding models for implementation, integration, QA planning, documentation, and most review work.

Use cheap worker models for deterministic command runners, lint/test execution, issue hygiene checks, dependency scans, and receipt collection.

## Handoffs

Every handoff must include:

- Goal and scope.
- Current evidence.
- Files, repos, or artifacts already inspected.
- Decisions made and decisions still open.
- Commands run and their results.
- Next agent or human owner.
- Stop condition or escalation trigger.

The existing `../archivist/` and `../kujo-archivist/` packages remain the source-grounded research agents. Use them before strategic or planning work when context is thin.

## Tool Support

KUJO workflows support the chain by turning work into artifacts:

- `Spec` defines task contracts and acceptance criteria.
- `Dispatch` routes repeatable workflows and produces traces.
- `Scout`, `Scent`, `PackWrite`, and `Muzzle` prepare and compress context.
- `Eval`, `Lens`, `Fence`, `ShipCheck`, `Concord`, and `ChangeBucket` verify outcomes from different angles.
- `CaseFile`, `RunLedger`, and PatchBrief-style reports preserve evidence.
- `Watchdog` captures local AI/proxy telemetry where configured.
- `Kennel`, `MCP`, `RAG`, and related tools support package, integration, and retrieval work.

See `00-tool-agent-map.md` for supported-versus-inferred behavior.

## Running A Campaign

Use [00-docs/templates/general-campaign-wrapper.md](00-docs/templates/general-campaign-wrapper.md) as the reusable intake packet for the `General Commander`.

Paste an existing project mega prompt into the wrapper's `Project Payload` section, fill the metadata and constraints, and send the full packet to the General. The wrapper tells the General to route work through the chain, require evidence, preserve handoffs, and produce a final review packet plus agent-chain improvement notes.

For repeatable testing, use:

- [00-docs/benchmarks/general-chain-benchmark-mega-prompt.md](00-docs/benchmarks/general-chain-benchmark-mega-prompt.md)
- [00-docs/benchmarks/general-chain-scorecard.md](00-docs/benchmarks/general-chain-scorecard.md)

The benchmark is intentionally small but cross-functional. It should reveal whether the chain can handle product framing, planning, implementation, verification, documentation, evidence collection, and retrospective improvement.

## Agent Table

| Layer | Agent | Use For | Model Tier | Key Tools |
|---|---|---|---|---|
| Strategic | General Commander | Mission interpretation, delegation, final synthesis | Premium reasoning | Dispatch, RunLedger, Spec, ShipCheck |
| Strategic | Chief of Staff | Objective shaping, assignment lanes, handoff control | Premium reasoning | Spec, Dispatch, Scent, Muzzle |
| Strategic | Systems Architect | Architecture, boundaries, platform decisions | Premium reasoning | Scout, Fence, Concord, Spec |
| Strategic | Product Strategist | User value, roadmap fit, adoption framing | Premium reasoning | Archivist, Spec, Eval |
| Planning | Planner | Milestones, sequencing, acceptance criteria | Standard/high reasoning | Spec, Dispatch, Eval |
| Planning | Spec Writer | Formal task contracts and agent-ready specs | Standard/high reasoning | Spec, CaseFile |
| Planning | Research Analyst | Repo, API, dependency, and technical context | Standard/high reasoning | Archivist, Scout, RAG, Scent |
| Planning | Risk Officer | Scope, migration, release, security, and compliance risk | Premium reasoning | ShipCheck, Fence, Concord, CaseFile |
| Execution | Core Developer | General source changes and tests | Standard coding | Spec, Eval, PatchBrief |
| Execution | Tooling Developer | CLI tools, scripts, automation, local integrations | Standard coding | Kujo Tool Building, Muzzle, Eval |
| Execution | Frontend Developer | UI flows, responsive behavior, browser proof | Standard coding | Lens, Eval |
| Execution | Backend Developer | APIs, persistence, jobs, auth boundaries | Standard coding | Eval, Scout, CaseFile |
| Execution | Integration Engineer | GitHub/GitLab/MCP/CI/service integration | Standard coding | MCP, Dispatch, Watchdog |
| Verification | Code Reviewer | Diff review, regressions, missing tests | Standard/high reasoning | PatchBrief, ChangeBucket, Concord |
| Verification | QA Lead | Test strategy and evidence requirements | Standard/high reasoning | Eval, CaseFile, RunLedger |
| Verification | Visual QA Agent | Browser, layout, accessibility, visual proof | Standard coding | Lens |
| Verification | Release Verifier | Release readiness and blocking gates | Premium/standard | ShipCheck, Eval, Fence, RunLedger |
| Verification | Security Reviewer | Host effects, secrets, auth, boundaries | Premium reasoning | Scout, Fence, Scent, Eval, CaseFile |
| Knowledge | Archivist | Existing source-grounded dossiers | Standard/high reasoning | Archivist, KUJO Archivist |
| Knowledge | Documentation Writer | READMEs, changelogs, onboarding, runbooks | Standard writing/coding | Concord, Spec, PatchBrief |
| Knowledge | Context Packager | Compact execution packs and context bundles | Standard reasoning | Scent, PackWrite, Muzzle |
| Knowledge | SITREP Agent | Short status reports and handoff summaries | Cheap/standard | RunLedger, CaseFile |
| Worker | Routine Worker | Explicit bounded local commands | Cheap worker | Muzzle, CaseFile |
| Worker | Test Runner | Explicit test commands only | Cheap worker | Eval, repo test scripts |
| Worker | Lint Runner | Explicit lint/format/check commands only | Cheap worker | Muzzle, repo scripts |
| Worker | Issue Hygiene Worker | Assigned stale/duplicate/label checks | Cheap worker | GitHub/GitLab tools when available |
| Worker | Dependency Scanner | Dependency/package status checks | Cheap worker | Kennel, Scout |
| Worker | Receipt Collector | Logs, receipts, artifact paths, evidence packets | Cheap worker | RunLedger, CaseFile |

## Adding A New Agent

1. Create `chain-of-command/<agent-name>/AGENT.md` and `chain-of-command/<agent-name>/SKILL.md`.
2. Keep the role narrow enough to audit.
3. Include the common contract fields used by the existing agents.
4. List tools as allowed, recommended, or explicitly out of scope.
5. Add the agent to this README and `00-chain-of-command.md`.
6. Update `00-tool-agent-map.md` if the new role changes tool ownership.

## Keeping Agents Auditable

- Do not create agents that both decide strategy and implement unbounded changes.
- Worker agents must not redesign, investigate broadly, or edit unrelated files.
- Strategic agents may reason broadly, but must cite evidence and assign bounded work.
- Every agent must state stop conditions and escalation rules.
- Tool behavior must be repo-backed or marked as inferred.
