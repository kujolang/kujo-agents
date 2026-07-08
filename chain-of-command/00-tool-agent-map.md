# KUJO Tool To Agent Map

This map uses repo-backed behavior from local READMEs, AGENTS files, and KUJO skill definitions inspected in this workspace. Where a relationship is useful but not explicitly documented by a tool repo, it is marked `inferred`.

## Tool Maturity Snapshot

| Tool | Repo-backed behavior | Maturity signal from docs | Primary agents |
|---|---|---|---|
| Kujo runtime | Language/runtime with `run`, `test-run`, `doctor`, `docgen`, security controls, CLI contracts | Core runtime; use repo-specific validation | Tooling Developer, Core Developer, Release Verifier |
| Kujo Doctor | Generic development-environment and repository readiness checks; no writes, no network | First-party workflow extension | Routine Worker, Release Verifier |
| Agents SDK | Local-first agent primitives: runner, tools, security, memory, retrieval, handoffs, tracing, artifacts, budgets | Stable primitives; live production controls environment-dependent | Systems Architect, Integration Engineer |
| AI SDK | Provider-gated OpenAI-compatible chat/embedding primitives and redaction/reliability tests | Strong enterprise-hardening baseline, not blanket certification | Integration Engineer, Backend Developer |
| Spec | Task contracts, acceptance criteria, eval requirements, review expectations, approval points | Built for production use with environment validation | Planner, Spec Writer, Chief of Staff |
| Eval | Deterministic local/CI checks for commands, files, JSON, HTTP, snapshots, workflow outputs | Verified local/CI scope; no isolated sandbox | QA Lead, Test Runner, Release Verifier |
| Scout | Codebase intelligence packs: file tree, dependencies, routes, security smells, AGENTS.md, llms.txt | v1.0.0; does not replace human review | Research Analyst, Security Reviewer |
| Dispatch | Workflow orchestration, templates, persisted state, traces, reports, approvals, handoffs | Verified offline fixture path; live SDK optional | General Commander, Chief of Staff, Integration Engineer, Triage Agent |
| MCP | Local MCP server foundation, repo-specific scaffolds, bounded file operations, guardrails | Launch-honest local foundation; production needs validation | Integration Engineer |
| RAG | Local RAG pipeline with ingest/query/API, auth options, namespace isolation, release gates | Production-oriented starter kit, not managed service | Research Analyst, Backend Developer |
| Watchdog | Local AI telemetry/proxy layer with SQLite, dashboard, JSON APIs, redaction/auth/rate limits | Strong local-first reference; production behind controls | Integration Engineer, Receipt Collector |
| Scent | Task-specific context packs with provenance and redaction metadata | v1.0.0; pattern redaction must be reviewed | Context Packager, Research Analyst |
| Fence | Deterministic architecture-boundary enforcement with JSON/SARIF/Markdown outputs | Local-first guardrail suitable for CI gating | Systems Architect, Security Reviewer, Release Verifier |
| PatchBrief | Working-tree diff briefs for implementation review handoffs | Dogfood beta, useful locally | Code Reviewer, Triage Agent, Documentation Writer |
| ShipCheck | Release-readiness scan and gate with blockers/warnings | Production-forward alpha; human release decision remains | Release Verifier, Risk Officer |
| Concord | Cross-artifact drift checks across CLI/docs/examples/spec/eval/manifests | Early dogfood, not enterprise-ready | Code Reviewer, Documentation Writer, Risk Officer |
| RunLedger | Local JSON ledger for AI-agent build-run receipts | Practical local receipt system, not workflow manager | Receipt Collector, SITREP Agent, Triage Agent |
| Muzzle | Quiet workflow runner with logs, reports, JSON summaries, loop state | Trusted local workflow compression, not sandbox | Context Packager, Routine Worker, Lint Runner |
| Howl | Deterministic showcase artifact generation from examples and manifests | Production-ready for narrow offline scope | Documentation Writer |
| ChangeBucket | Git change footprint and blast-radius metrics | Read-only local footprint tool | Code Reviewer, Risk Officer |
| PackWrite | MEGA_PROMPT to validated `/agent` execution pack | Production-usable local/team pack compiler | Context Packager, Planner |
| CaseFile | Local failure/log/manual incident evidence bundles with redaction and handoff docs | Strong local-first v1 CLI; plaintext artifacts | Risk Officer, QA Lead, Triage Agent, Receipt Collector |
| Lens | Deterministic local browser QA with screenshots, reports, repair briefs, flows | Beta/stabilizing, local-first | Visual QA Agent, Frontend Developer |
| Kennel | Kujo package/dependency manager with manifests, lockfiles, trust/source policies | Production-oriented for launch-safe local/static scope | Dependency Scanner, Tooling Developer |

## Agent Ownership

| Agent | Primary tools | Secondary tools |
|---|---|---|
| General Commander | Dispatch, RunLedger, Spec | ShipCheck, Concord |
| Chief of Staff | Spec, Dispatch, Scent | Muzzle, PackWrite |
| Systems Architect | Scout, Fence, Concord | Spec, Agents SDK |
| Product Strategist | Archivist, Spec | Eval, RunLedger |
| Planner | Spec, Dispatch, Eval | PackWrite |
| Spec Writer | Spec | CaseFile, Eval |
| Research Analyst | Archivist, KUJO Archivist, Scout, RAG | Scent |
| Risk Officer | ShipCheck, Fence, Concord, ChangeBucket | CaseFile |
| Core Developer | Spec, Eval | PatchBrief, CaseFile |
| Tooling Developer | Kujo runtime, Kujo Tool Building, Muzzle | Kennel, Eval |
| Frontend Developer | Lens, Eval | CaseFile |
| Backend Developer | Eval, Scout | RAG, Watchdog |
| Integration Engineer | MCP, Dispatch, Watchdog | AI SDK, Agents SDK |
| Code Reviewer | PatchBrief, ChangeBucket, Concord | Fence |
| Triage Agent | CaseFile, RunLedger, Dispatch | PatchBrief, ChangeBucket, Eval |
| QA Lead | Eval, CaseFile | RunLedger |
| Visual QA Agent | Lens | Eval |
| Release Verifier | ShipCheck, Eval, Fence, RunLedger | Concord |
| Security Reviewer | Scout, Fence, Scent, Eval | CaseFile |
| Documentation Writer | Concord, PatchBrief, Howl | Spec |
| Context Packager | Scent, PackWrite, Muzzle | Scout |
| SITREP Agent | RunLedger, CaseFile | PatchBrief |
| Routine Worker | Muzzle, Kujo Doctor | CaseFile |
| Test Runner | Eval, repo test scripts | Muzzle |
| Lint Runner | Repo lint/check scripts | Muzzle |
| Issue Hygiene Worker | GitHub/GitLab issue tools when available | Concord inferred for doc/task drift |
| Dependency Scanner | Kennel, Scout | ShipCheck |
| Receipt Collector | RunLedger, CaseFile | Watchdog |

## Inferred Relationships

- `SITREP` is treated as a short status-report role, not a confirmed standalone KUJO tool. Local search found workflow references and evidence tools, but no dedicated SITREP repo.
- `Issue Hygiene Worker` depends on the issue tracker available in the host environment. KUJO docs inspected here do not define a dedicated issue-hygiene tool.
- `Security` is distributed across tool behavior such as Scout security smells, Fence boundaries, Eval policy controls, Scent redaction, Watchdog auth/redaction, and Kujo runtime capability controls. A standalone `Security` tool repo was not found in the inspected roots.

## Evidence Sources

- `../../kujo/README.md`, `../../kujo/AGENTS.md`, `../../kujo/tools/kujo-doctor/README.md`
- `../../agents-sdk/README.md`, `../../ai-sdk/README.md`
- `../../spec/README.md`, `../../eval/README.md`, `../../dispatch/README.md`
- `../../scout/README.md`, `../../scent/README.md`, `../../packwrite/README.md`, `../../muzzle/README.md`
- `../../fence/README.md`, `../../shipcheck/README.md`, `../../concord/README.md`, `../../changebucket/README.md`
- `../../patchbrief/README.md`, `../../casefile/README.md`, `../../runledger/README.md`, `../../lens/README.md`
- `../../mcp/README.md`, `../../rag/README.md`, `../../watchdog/README.md`, `../../kennel/README.md`, `../../howl/README.md`
- `../../kujo-skills/skills/*/SKILL.md`
