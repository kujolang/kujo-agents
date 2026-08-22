# KUJO Ecosystem Inventory

This inventory summarizes the inspected KUJO ecosystem for the agent chain. It is concise by design; use the referenced repo docs before making tool-behavior claims.

## Existing Agents

The public agent roster lives entirely under `chain-of-command/`. Each role uses
a package directory containing `AGENT.md` and `SKILL.md`; supporting maps and
templates remain in the same chain package.

## Existing Skills

The local `kujo-skills/skills/` folder contains workflow skills for Agents SDK, AI SDK, CaseFile, ChangeBucket, Concord, Dispatch, Eval, Fence, Howl, Kennel, Lens, MCP, Muzzle, PackWrite, PatchBrief, RAG, RunLedger, Scent, Scout, ShipCheck, Spec, SSG, Watchdog, Redact, Capsule benchmark work, release gates, readiness auditing, maintainer review, security hardening, tool building, runtime parity, CLI contracts, docs drift, and related KUJO repo work.

## Existing Workflows

- `kujo-workflows/`: runnable workflow kits such as agency runner, verified fix loop, AI SDK + Muzzle benchmark, CaseFile evidence packet, Dispatch approval router, MCP agent gateway review, RAG enterprise knowledge gate, Howl content factory, doc generation contract runner, loop engineering, Tribunal decision gate, Relay lifecycle handoff, and Workcell execution gate.
- Individual tool repos include repo-specific workflow scripts, release gates, contract tests, examples, and AGENTS guidance.

## Existing Tools

Confirmed tool repos include Kujo runtime, Kujo Doctor, Agents SDK, AI SDK, Spec, Eval, Scout, Dispatch, MCP, RAG, Watchdog, Scent, Redact, Fence, PatchBrief, ShipCheck, Concord, RunLedger, Muzzle, Howl, ChangeBucket, PackWrite, CaseFile, Lens, Kennel, CMS, CRUD API, SSG, AI Chat, Intake, Cinch, Site Kit, Relay, Workcell, Tribunal, Source, StegoCipher Kujo, CMS Experience, Capsule benchmark tooling, Benchmark System prompt kits, Kujo Hyperframes, TotalRecall, Ward, Leash, Kujo Docs, SiteProbe, SearchBridge, ContentGraph, StoryDesk, Dossier, GalleyPack, BluePencil, AssetWorks, VersionSeal, PressWire, ReaderSignal, Commerce, TruthLens, the `agents.kujolang.ai` static agent library, and other benchmark/showcase repos.

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
- `kujo-hyperframes`: static public campaign and video composition repository backed by a source-grounded handoff dossier and claim map. Treat as a frontend/documentation/product surface for Frontend Developer, Visual QA Agent, Documentation Writer, and Product Strategist when assigned. Do not let campaign copy bypass source-grounded claim constraints.
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

The 2026-08-08 audit window added or refreshed these agent-facing relationships:

- `kujo`: v1.0.0 launch evidence, release artifact handling, DocGen concurrency, stable contract version guards, and launch inventory rationale were refreshed. Existing Tooling Developer, Core Developer, Release Verifier, Security Reviewer, and Documentation Writer ownership remains current; use `kujo-testing-release-gates`, `kujo-cli-contracts`, `kujo-docgen-agent-readable`, and related core skills for repository work.
- `kujo-docs`: official `docs.kujolang.ai` static documentation site built through sibling `ssg`, vendored SiteKit assets, production deployment docs, favicon assets, mobile navigation, content IA, and validation guidance. Treat as directly verified for Documentation Writer, Frontend Developer, Visual QA Agent, Product Strategist, and Release Verifier when public documentation site work is explicitly in scope. Do not treat it as a generic docs generator or as proof that every documented sibling repo is production-ready.
- `howl`: branded social-card rendering and the refreshed `kujo-howl-workflows` skill make Howl directly useful for deterministic launch/docs/social showcase artifacts. Existing Documentation Writer ownership remains current; Product Strategist may frame source-backed campaign use, and Visual QA/Frontend can inspect rendered HTML/SVG when assigned. Howl remains offline and must not invent claims, post content, or call LLM/network services.
- `kennel`: v1.0.0 release prep, CLI compatibility shims, module-name collision repair, and refreshed `kujo-kennel-workflows` guidance preserve Kennel as the directly verified dependency/package capability for Dependency Scanner and Tooling Developer. Root compatibility shims must stay aligned with `src/` until downstream root-module imports are retired.
- `ssg`: v1.0.0 release prep, nested-output directory repair, and Kujo documentation IA support strengthen existing Documentation Writer, Frontend Developer, Visual QA Agent, and Release Verifier ownership.
- `agents-sdk`, `eval`, `lens`, `mcp`, `muzzle`, `packwrite`, `patchbrief`, `rag`, `runledger`, `scent`, `scout`, `shipcheck`, and `watchdog`: v1.0.0 release prep refreshed repository maturity without changing existing role ownership. Watchdog also refreshed pricing catalogs for the August audit; treat pricing knowledge as retrieval-date sensitive.
- `kujo-skills`: refreshed Kujo v1 release skill guidance plus Howl and Kennel workflow routing. Existing skill-reference relationships remain current.
- `kujo-workflows`: weekly workflow audit refreshed catalog validation and preserves contract-gated workflow relationships. Existing Dispatch, Workcell, Relay, Tribunal, Howl, RAG, CaseFile, MCP, and DocsGen workflow boundaries remain current.
- `totalrecall`: local-first ingestion and recall pipeline for Fathom, chat exports, Slack threads, and GitHub activity into Strata, markdown, HTML, or local indexes with dry-run/plan/report JSON, state, retry, and deduplication surfaces. Defer chain integration until a dedicated skill/workflow contract exists and live-provider credential boundaries are reviewed; existing Research Analyst, Context Packager, SITREP Agent, and Receipt Collector can inspect its artifacts when explicitly assigned.
- `ward`: local Dependabot security command center with read-only default collection/planning/report/dashboard and explicit `--apply` for fix preparation. Defer active chain routing until a dedicated skill/workflow exists and GitHub token/process-list exposure boundaries are accepted; existing Dependency Scanner, Security Reviewer, Issue Hygiene Worker, Risk Officer, and Release Verifier can review Ward outputs when explicitly assigned.
- `leash`: local-first mobile control plane for supervising AI coding agents through policy, adapters, JWT auth, audit trail, and Android/mobile approval flows. Defer active chain integration until a dedicated skill/workflow and device/runtime validation exist; existing Integration Engineer, Security Reviewer, Risk Officer, Dispatch-oriented agents, and Receipt Collector can review Leash artifacts when explicitly assigned.
- `diff-viewer-inline-review-fresh`: small inline-review fixture repository with finite-score validation. Treat as unsupported for active Kujo agent capability routing outside review UI fixture testing.

The 2026-08-15 audit window added or refreshed these agent-facing relationships:

- `storydesk`, `dossier`, `galleypack`, `bluepencil`, `assetworks`, `versionseal`, `presswire`, and `readersignal`: these eight local-first Publishing House tools now back the standalone Publishing House roster and eleven lifecycle workflow kits. Treat their role bindings as directly verified through `publishing-house/00-tool-workflow-map.md`, `publishing-house/publishing-house-catalog.json`, and sibling README contracts. They do not grant publication approval, rights/consent decisions, hosted identity, distributed coordination, or live adapter access by implication.
- `agents.kujolang.ai`: static public library for Chain of Command, WebOps, and Publishing House agent contracts. Treat as a documentation/frontend/release surface owned by Documentation Writer, Frontend Developer, Visual QA Agent, Release Verifier, and Product Strategist when assigned. Canonical content remains `kujo-agents`; do not hand-maintain divergent generated pages.
- `siteprobe`, `searchbridge`, and `contentgraph`: WebOps toolchain contracts remain current. SiteProbe owns read-only crawl artifacts, SearchBridge owns capability-scoped provider evidence with fail-closed submission authorization, and ContentGraph owns deterministic content relationships. Existing WebOps agents may use them through the WebOps maps; Chain of Command roles should treat them as task-specific website-intelligence tools rather than generic Scout, Lens, RAG, or SEO judgment replacements.
- `commerce`: provider-agnostic static-site commerce layer for Kujo SSG with versioned catalog, cart, and event contracts. Treat as a deferred task-specific capability for Frontend Developer, Backend Developer, Integration Engineer, Security Reviewer, QA Lead, and Release Verifier when a site explicitly needs commerce. Do not fold it into SSG, infer payment/order storage, or grant live checkout/provider authority without an explicit contract and credentials boundary.
- `truthlens`: privacy-first MV3 Chrome extension for local AI-image confidence labeling with deterministic Node/Chrome validation and an explicit probabilistic limitation statement. Treat as a product/security/browser QA target when assigned, not as a general WebOps, editorial fact-checking, or evidence-verification tool.
- `kujo`, `agents-sdk`, `ai-sdk`, `eval`, `fence`, `mcp`, `patchbrief`, `rag`, `runledger`, `scout`, `scent`, `shipcheck`, `ssg`, `watchdog`, `dispatch`, `kennel`, `lens`, `muzzle`, `site-kit`, `tribunal`, `workcell`, and `relay`: recent hardening commits refresh existing ownership and verification relevance without broadening authority or changing role boundaries.

The 2026-08-22 audit window added or refreshed these agent-facing relationships:

- `source`: agent-first Git collaboration platform covering the `Project -> Work -> Session -> Change -> Evidence -> Decision -> Canonical Git State` lifecycle, capability-gated HTTP/Git transport, `source submit`, SQLite/JSON stores, tenant-scoped org/project routes, rate limiting, credential scanning, and 101-test local evidence. Treat as a deferred platform/review target for Systems Architect, Integration Engineer, Tooling Developer, Security Reviewer, Code Reviewer, QA Lead, Risk Officer, Release Verifier, and Receipt Collector when explicitly assigned. Do not grant active chain routing, remote mutation, Git-transport authority, organization policy control, acceptance authority, or credential use until a dedicated skill/workflow contract and governance boundary exist.
- `kujo`: the current stable public runtime is now `v1.0.1`; ecosystem installer and noexec temporary-directory fixes strengthen Tooling Developer, Core Developer, Release Verifier, Security Reviewer, and Documentation Writer guidance. Do not infer that the source tree version string is the published stable release; use release tags, `docs/V1_SCOPE.md`, and release artifact evidence for compatibility claims.
- `workcell`: Git patch secret handling now redacts declared secrets and common base64 encodings from persisted run patches and can reject runs whose generated patch contained declared secrets. Existing Workcell ownership remains current; still treat Docker/Podman and host isolation as operator-owned boundaries.
- `ai-chat`: recent stream handling and tool-path fixes refresh existing Integration Engineer, Backend Developer, Frontend Developer, Visual QA Agent, and QA Lead routing. Existing app boundaries remain current: local showcase app, provider-gated chat workflows, offline fixtures, SQLite state, and no blanket model-quality or production certification claims.
- `kujo-skills`: the catalog now includes 95 focused skills, a release-to-site `kujo-ecosystem-launch` coordinator, refreshed SearchBridge and Workcell evidence, and Publishing House skill hardening notes. Treat these as skill-routing refreshes only; they do not expand agent authority beyond the owning repository and workflow contracts.
- `kujo-workflows`: weekly workflow audit refresh preserves cross-repository validation for agents, skills, website-intelligence tools, workflows, and public-site source content. Existing Dispatch, Workcell, Relay, Tribunal, WebOps, and Publishing House workflow boundaries remain current.
- `watchdog`: pricing catalog refresh is retrieval-date sensitive evidence for telemetry cost estimates only. Do not treat pricing snapshots as stable financial guidance.

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
- Intake, Cinch, TotalRecall, Ward, Leash, Commerce, and Source are deferred as broad chain capabilities until stable chain-specific skills or workflow contracts exist and their approval/credential/runtime boundaries are reviewed.
- TruthLens is a product/browser-extension target, not a chain capability. Use existing frontend, security, QA, and release roles for assigned work instead of adding routing or evidence authority.
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

Non-agent chain support material lives under `00-docs/` so the remaining folders are visually reserved for agent packages:

```text
chain-of-command/00-docs/templates/
chain-of-command/00-docs/benchmarks/
```
