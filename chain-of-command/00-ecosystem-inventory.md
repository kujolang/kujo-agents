# KUJO Ecosystem Inventory

This inventory summarizes the inspected KUJO ecosystem for the agent chain. It is concise by design; use the referenced repo docs before making tool-behavior claims.

## Existing Agents

- `archivist/`: universal source-bound project researcher and dossier builder.
- `kujo-archivist/`: KUJO-specific source-bound ecosystem researcher and dossier builder.

Existing agents use package directories with `AGENT.md`, `SKILL.md`, and optional `references/`.

## Existing Skills

The local `kujo-skills/skills/` folder contains workflow skills for Agents SDK, AI SDK, CaseFile, ChangeBucket, Concord, Dispatch, Eval, Fence, Howl, Kennel, Lens, MCP, Muzzle, PackWrite, PatchBrief, RAG, RunLedger, Scent, Scout, ShipCheck, Spec, SSG, Watchdog, Redact, Capsule benchmark work, release gates, readiness auditing, maintainer review, security hardening, tool building, runtime parity, CLI contracts, docs drift, and related KUJO repo work.

## Existing Workflows

- `kujo-workflows/`: runnable workflow kits such as agency runner, verified fix loop, AI SDK + Muzzle benchmark, CaseFile evidence packet, Dispatch approval router, MCP agent gateway review, RAG enterprise knowledge gate, Howl content factory, doc generation contract runner, loop engineering, Tribunal decision gate, Relay lifecycle handoff, and Workcell execution gate.
- Individual tool repos include repo-specific workflow scripts, release gates, contract tests, examples, and AGENTS guidance.

## Existing Tools

Confirmed tool repos include Kujo runtime, Kujo Doctor, Agents SDK, AI SDK, Spec, Eval, Scout, Dispatch, MCP, RAG, Watchdog, Scent, Redact, Fence, PatchBrief, ShipCheck, Concord, RunLedger, Muzzle, Howl, ChangeBucket, PackWrite, CaseFile, Lens, Kennel, CMS, CRUD API, SSG, AI Chat, Intake, Cinch, Site Kit, Relay, Workcell, Tribunal, StegoCipher Kujo, CMS Experience, Capsule benchmark tooling, Benchmark System prompt kits, Kujo Hyperframes, and other benchmark/showcase repos.

## Recently Verified Agent-Facing Capabilities

These repositories changed during the 2026-07-18 audit window and expose usable but bounded agent-facing capabilities:

- `relay`: Kujo-native bounded agent mission composition, pause/resume/cancel, lifecycle handoff receipts, provider/tool bridges, run evidence export, and repair replay. Treat as a local alpha orchestration layer for Integration Engineer, General Commander, Chief of Staff, Triage Agent, Receipt Collector, and Release Verifier. Do not treat it as remote exactly-once delivery, enterprise tenancy, or universal provider proof.
- `workcell`: local Docker/Podman-backed disposable execution workspaces with declared commands, exported artifacts, receipts, verification, and cleanup. Treat as a bounded execution gate for Tooling Developer, Routine Worker, Test Runner, QA Lead, Security Reviewer, Release Verifier, and Risk Officer when host Docker/Podman trust is acceptable. Do not treat it as a hardened microVM or hosted sandbox.
- `tribunal`: local-first adversarial decision review engine with hearing, fatal-flaw, ruling, and decision-packet artifacts. Treat as advisory governance evidence for Risk Officer, Product Strategist, Systems Architect, General Commander, and Release Verifier. Human authority remains required for consequential business, release, security, legal, or production decisions.
- `site-kit`: private internal design-system and component bundle with token, component, CSS, snapshot, lint, and validation commands. Treat as a frontend/documentation capability for Frontend Developer, Visual QA Agent, Documentation Writer, Product Strategist, and Release Verifier. Browser/accessibility proof remains separate for consuming layouts.
- `stego-cipher-kujo`: educational steganography/obfuscation CLI with Kujo smoke tests. Treat as a narrow demo or security-review subject only. Do not route secrets or cryptographic security requirements to it.
- `cms-experience`: Studio/public-site application layer for the sibling CMS backend with explicit auth and production-readiness gaps. Treat as a frontend/backend/integration showcase tied to `cms`; do not claim CMS human auth, preview-token, or public production readiness.

The 2026-07-25 audit window added or refreshed these agent-facing relationships:

- `benchmarks-capsule-v3`: Kujo-native Capsule CLI that writes deterministic, offline project handoff packages (`capsule.json`, `capsule.md`, `manifest.json`) with command detection, checksums, shallow secret exclusions, and validation. Treat as a directly verified context-packaging and benchmark-evidence capability for Context Packager, Research Analyst, QA Lead, and Receipt Collector. Do not treat its filename/keyword redaction as a complete secret scanner.
- `benchmarks-system`: provider-neutral benchmark execution and review prompt kits that currently drive saved AI Chat pane profiles and produce quality, token/cost, time, dream-team, and PDF review outputs. Treat as a documentation/prompt-kit reference for QA Lead, Product Strategist, General Commander, and Documentation Writer, not as a supported standalone CLI until repository-backed executable contracts exist.
- `kujo-hyperframes`: static public campaign and video composition repository backed by the Archivist handoff dossier and claim map. Treat as a frontend/documentation/product surface for Frontend Developer, Visual QA Agent, Documentation Writer, and Product Strategist when assigned. Do not let campaign copy bypass source-grounded claim constraints.
- `watchdog`: recent changes strengthened dashboard, backup/archive views, long-running trace display, session token visibility, and telemetry preservation. Existing Integration Engineer and Receipt Collector ownership remains current; use Watchdog evidence for visible local proxy telemetry only.
- `ai-chat`: recent changes hardened streaming durability, tool continuation timeout handling, local runtime tool errors, public tunnel probe endpoints, usage accounting, sidebar/archive UI state, and token-budget behavior. Existing Integration Engineer, Backend Developer, Frontend Developer, Visual QA Agent, and QA Lead routing remains current.
- `eval`, `fence`, `patchbrief`, `shipcheck`, and `changebucket`: recent CLI parsing and policy-gate fixes strengthen existing verification relationships but do not change agent ownership.

The 2026-08-01 audit window added or refreshed these agent-facing relationships:

- `redact`: deterministic local scan/sanitize/verify/pack pipeline for text and Markdown with `.redact/runs/<timestamp>/` audit artifacts. Treat as directly verified for Security Reviewer, Context Packager, and Receipt Collector when sensitive context must be anonymized before sharing or retention. Do not treat it as complete PII removal, compliance approval, full YAML support, stdin support on current Kujo VM builds, or permission to store originals.
- `ssg`: deterministic Kujo static-site generator with generated-output validation, release gates, DocGen bridge, and reusable docs starter. Treat as directly verified for Documentation Writer, Frontend Developer, Visual QA Agent, and Release Verifier when static docs/sites are in scope. Do not treat it as hosted publishing or a production-certified docs platform.
- `agents-sdk`: MCP 2026 adapter helpers now cover stateless JSON-RPC helpers, per-request `_meta`, Streamable HTTP routing headers, tool-list cache metadata, input-required normalization, unsupported-version errors, and schema/display metadata mapping. Existing Systems Architect and Integration Engineer ownership remains current.
- `ai-chat`: recent changes improved sidebar action/title behavior, provider-independent offline smoke, clean port-conflict handling, stream continuity after browser disconnects, and streamed provider error handling. Existing app/integration/frontend/QA ownership remains current; do not infer broader provider quality or production readiness.
- `kujo-workflows`: weekly workflow audit refreshed the catalog and confirmed Workcell temp-root repair plus contract-gated Tribunal, Relay, and Workcell integrations. Existing General Commander, Chief of Staff, Integration Engineer, QA, Release, Risk, and worker boundaries remain current.
- `kujo-skills`: weekly skill audit refreshed Agents SDK, AI Chat, SiteKit, and SSG skills. Prefer canonical `kujo-site-kit-workflows`; keep `kujo-sitekit-workflows` only as a compatibility alias.
- `kujo-hyperframes`: `kujo-ai-transmission/` added a new source-grounded video composition and rendered media outputs. Existing Frontend Developer, Visual QA Agent, Documentation Writer, and Product Strategist ownership remains current.
- `diff-viewer-demo`, `diff-viewer-demo-fresh`, and `diff-viewer-verified`: small diff-review fixture repositories. Treat as unsupported for active agent capability routing outside testing review UI behavior.
- `intake`: local-first inbound work normalization, policy-gated actions, dashboard, adapter, and audit-log app. Defer chain integration until a dedicated Kujo skill/workflow contract or explicit task assignment exists.
- `cinch`: macOS-first local AI development harness with workspaces, files, git, commands, MCP, proof artifacts, and Trail export. Defer broad chain integration until a dedicated Kujo skill/workflow contract exists.

## Repeated Operational Patterns

- Read README and AGENTS files first.
- Prefer canonical copyable examples over tests when learning usage.
- Treat tests and fixtures as behavior contracts.
- Exclude generated, dependency, cache, and output folders from broad searches.
- Preserve CLI output and JSON contracts unless intentionally changing them.
- Prefer local deterministic commands and artifact paths over memory.
- Mark enterprise or production claims narrowly and with maturity boundaries.
- Capture evidence through reports, JSON summaries, traces, logs, receipts, or case bundles.

## Mature Enough To Recommend For Routine Use

Repo docs support routine local use for Spec, Eval, Scout, Dispatch offline fixture workflows, CaseFile, RunLedger, Scent, Redact local anonymization, Muzzle trusted local workflows, PackWrite local/team pack generation, Fence architecture checks, ShipCheck release scanning, Lens local browser QA, Kennel launch-safe package workflows, SSG local static-site builds, Watchdog local telemetry/proxy workflows, Relay local alpha lifecycle handoffs, Workcell local Docker/Podman execution gates, Tribunal advisory decision gates, and SiteKit local design-system builds. Each still requires environment-specific validation before broad enterprise claims.

## Experimental Or Underdocumented

- Concord is useful but explicitly early dogfood and not enterprise-ready.
- PatchBrief is dogfood beta.
- Lens is beta/stabilizing.
- ShipCheck is production-forward alpha.
- MCP is launch-honest as a local foundation but production deployment needs target validation.
- Public Kennel registry behavior, public discovery, moderation, malware scanning, and trust scoring are deferred.
- SITREP appears as a useful role name but not as a confirmed standalone KUJO tool.
- Intake and Cinch are deferred as broad chain capabilities until stable chain-specific skills or workflow contracts exist.
- Diff Viewer demo repositories are fixtures, not tool capabilities.

## Missing Docs For Agent Onboarding

- A consolidated "which KUJO tool should my agent use?" guide did not exist before this folder.
- A dedicated SITREP tool or format reference was not found.
- Cross-repo maturity status is spread across individual READMEs.
- Worker-agent guardrails were not centralized before this chain.
- Issue-hygiene workflows appear dependent on external tracker tooling rather than a KUJO-native documented tool.

## Formatting Convention

New agents in this chain use:

```text
chain-of-command/<agent-name>/AGENT.md
chain-of-command/<agent-name>/SKILL.md
```

The existing root Archivist packages are preserved and referenced rather than moved.

Non-agent chain support material lives under `00-docs/` so the remaining folders are visually reserved for agent packages:

```text
chain-of-command/00-docs/templates/
chain-of-command/00-docs/benchmarks/
```
