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
| Relay | Bounded agent mission composition, pause/resume/cancel, lifecycle handoff receipts, provider/tool bridges, run evidence export, and repair replay | Hardened local alpha; live-provider and enterprise tenancy remain open | Integration Engineer, Triage Agent, Receipt Collector |
| Workcell | Local Docker/Podman-backed disposable execution workspace with declared commands, exported artifacts, receipts, verification, and cleanup | Release-gated local Docker MVP; host isolation remains operator-owned | Tooling Developer, Test Runner, QA Lead |
| Tribunal | Local adversarial decision review engine with hearings, fatal-flaw checks, rulings, and decision packets | Advisory decision gate; not a replacement for human release/security/legal authority | Risk Officer, Product Strategist, General Commander |
| SiteKit | Internal token-driven design-system and component bundle with build, lint, validation, snapshot, and smoke commands | Private local package; consuming layouts still need browser and accessibility proof | Frontend Developer, Visual QA Agent, Documentation Writer |
| StegoCipher Kujo | Educational quote/PNG steganography and obfuscation CLI with smoke tests and JSON output | Demo/learning utility; explicitly not cryptographic encryption | Security Reviewer, Research Analyst |
| CMS Experience | Studio/public-site application layer for the CMS backend with live contract checks and explicit auth gaps | Showcase/application layer; public production readiness remains gated by documented P1 items | Frontend Developer, Backend Developer, Integration Engineer |
| Capsule | Offline Kujo CLI for deterministic project handoff packages, manifests, checksums, previews, command detection, and validation | Direct local CLI contract in benchmark repo; redaction is shallow filename/keyword protection | Context Packager, Research Analyst, QA Lead |
| Benchmark System | Provider-neutral benchmark execution/review prompt kits for AI Chat pane-profile runs and factual review packets | Prompt/documentation kit; no standalone executable contract verified | QA Lead, Product Strategist, General Commander |
| Kujo Hyperframes | Static/public campaign and video composition repo with source-grounded claim map | Showcase/content surface; claims remain tied to Archivist dossier evidence | Frontend Developer, Visual QA Agent, Documentation Writer |

## Agent Ownership

| Agent | Primary tools | Secondary tools |
|---|---|---|
| General Commander | Dispatch, RunLedger, Spec | ShipCheck, Concord, Relay lifecycle evidence, Tribunal advisory packets |
| Chief of Staff | Spec, Dispatch, Scent | Muzzle, PackWrite |
| Systems Architect | Scout, Fence, Concord | Spec, Agents SDK |
| Product Strategist | Archivist, Spec | Eval, RunLedger |
| Planner | Spec, Dispatch, Eval | PackWrite |
| Spec Writer | Spec | CaseFile, Eval |
| Research Analyst | Archivist, KUJO Archivist, Scout, RAG | Scent, Capsule |
| Risk Officer | ShipCheck, Fence, Concord, ChangeBucket | CaseFile, Tribunal advisory packets, Workcell boundary evidence |
| Core Developer | Spec, Eval | PatchBrief, CaseFile |
| Tooling Developer | Kujo runtime, Kujo Tool Building, Muzzle | Kennel, Eval, Workcell |
| Frontend Developer | Lens, Eval | CaseFile, SiteKit, CMS Experience |
| Backend Developer | Eval, Scout | RAG, Watchdog |
| Integration Engineer | MCP, Dispatch, Watchdog | AI SDK, Agents SDK, Relay, CMS Experience |
| Code Reviewer | PatchBrief, ChangeBucket, Concord | Fence |
| Triage Agent | CaseFile, RunLedger, Dispatch | PatchBrief, ChangeBucket, Eval, Relay run evidence |
| QA Lead | Eval, CaseFile | RunLedger, Workcell receipts, Capsule benchmark evidence |
| Visual QA Agent | Lens | Eval, SiteKit snapshots |
| Release Verifier | ShipCheck, Eval, Fence, RunLedger | Concord, Relay handoff evidence, Workcell execution evidence, Tribunal advisory packets |
| Security Reviewer | Scout, Fence, Scent, Eval | CaseFile, Workcell boundary evidence, StegoCipher review subject |
| Documentation Writer | Concord, PatchBrief, Howl | Spec, SiteKit docs/components evidence |
| Context Packager | Scent, PackWrite, Muzzle, Capsule | Scout |
| SITREP Agent | RunLedger, CaseFile | PatchBrief |
| Routine Worker | Muzzle, Kujo Doctor | CaseFile, Workcell when explicitly assigned |
| Test Runner | Eval, repo test scripts | Muzzle, Workcell when explicitly assigned |
| Lint Runner | Repo lint/check scripts | Muzzle |
| Issue Hygiene Worker | GitHub/GitLab issue tools when available | Concord inferred for doc/task drift |
| Dependency Scanner | Kennel, Scout | ShipCheck |
| Receipt Collector | RunLedger, CaseFile | Watchdog, Relay run evidence, Capsule manifests |

## Inferred Relationships

- `SITREP` is treated as a short status-report role, not a confirmed standalone KUJO tool. Local search found workflow references and evidence tools, but no dedicated SITREP repo.
- `Issue Hygiene Worker` depends on the issue tracker available in the host environment. KUJO docs inspected here do not define a dedicated issue-hygiene tool.
- `Security` is distributed across tool behavior such as Scout security smells, Fence boundaries, Eval policy controls, Scent redaction, Watchdog auth/redaction, and Kujo runtime capability controls. A standalone `Security` tool repo was not found in the inspected roots.
- `Relay`, `Workcell`, and `Tribunal` have dedicated workflow kits in `kujo-workflows`, but agent access stays capability-scoped: Relay is lifecycle/evidence orchestration, Workcell is bounded local execution, and Tribunal is advisory decision review.
- `StegoCipher Kujo` is a reviewable demo/security subject only. Its README says it is not cryptographic encryption, so no agent should route secrecy, credential storage, or cryptographic security requirements to it.
- `CMS Experience` depends on the sibling `cms` backend contract. Studio uses operator-supplied API tokens and server-side sessions; do not infer human-user auth, MFA, secure preview, or public production readiness.
- `Capsule` overlaps with Scout and Scent but has a different contract: it produces deterministic offline handoff artifacts with checksums and validation, not semantic code intelligence or task-scoped context selection. Use it through Context Packager or Research Analyst instead of creating a standalone agent.
- `Benchmark System` and `Kujo Hyperframes` are useful repo-backed surfaces but are not broad tool integrations. Keep Benchmark System as prompt-kit evidence until an executable contract exists, and keep Hyperframes under existing frontend/docs/product ownership.

## Evidence Sources

- `../../kujo/README.md`, `../../kujo/AGENTS.md`, `../../kujo/tools/kujo-doctor/README.md`
- `../../agents-sdk/README.md`, `../../ai-sdk/README.md`
- `../../spec/README.md`, `../../eval/README.md`, `../../dispatch/README.md`
- `../../scout/README.md`, `../../scent/README.md`, `../../packwrite/README.md`, `../../muzzle/README.md`
- `../../fence/README.md`, `../../shipcheck/README.md`, `../../concord/README.md`, `../../changebucket/README.md`
- `../../patchbrief/README.md`, `../../casefile/README.md`, `../../runledger/README.md`, `../../lens/README.md`
- `../../mcp/README.md`, `../../rag/README.md`, `../../watchdog/README.md`, `../../kennel/README.md`, `../../howl/README.md`
- `../../relay/README.md`, `../../workcell/README.md`, `../../tribunal/README.md`, `../../site-kit/README.md`, `../../stego-cipher-kujo/README.md`, `../../cms-experience/README.md`
- `../../benchmarks-capsule-v3/README.md`, `../../benchmarks-system/README.md`, `../../kujo-hyperframes/README.md`
- `../../kujo-workflows/README.md`
- `../../kujo-skills/skills/*/SKILL.md`
