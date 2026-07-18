# KUJO Ecosystem Inventory

This inventory summarizes the inspected KUJO ecosystem for the agent chain. It is concise by design; use the referenced repo docs before making tool-behavior claims.

## Existing Agents

- `archivist/`: universal source-bound project researcher and dossier builder.
- `kujo-archivist/`: KUJO-specific source-bound ecosystem researcher and dossier builder.

Existing agents use package directories with `AGENT.md`, `SKILL.md`, and optional `references/`.

## Existing Skills

The local `kujo-skills/skills/` folder contains workflow skills for Agents SDK, AI SDK, CaseFile, ChangeBucket, Concord, Dispatch, Eval, Fence, Howl, Kennel, Lens, MCP, Muzzle, PackWrite, PatchBrief, RAG, RunLedger, Scent, Scout, ShipCheck, Spec, SSG, Watchdog, release gates, readiness auditing, maintainer review, security hardening, tool building, runtime parity, CLI contracts, docs drift, and related KUJO repo work.

## Existing Workflows

- `kujo-workflows/`: runnable workflow kits such as agency runner, verified fix loop, AI SDK + Muzzle benchmark, CaseFile evidence packet, Dispatch approval router, MCP agent gateway review, RAG enterprise knowledge gate, Howl content factory, doc generation contract runner, loop engineering, Tribunal decision gate, Relay lifecycle handoff, and Workcell execution gate.
- Individual tool repos include repo-specific workflow scripts, release gates, contract tests, examples, and AGENTS guidance.

## Existing Tools

Confirmed tool repos include Kujo runtime, Kujo Doctor, Agents SDK, AI SDK, Spec, Eval, Scout, Dispatch, MCP, RAG, Watchdog, Scent, Fence, PatchBrief, ShipCheck, Concord, RunLedger, Muzzle, Howl, ChangeBucket, PackWrite, CaseFile, Lens, Kennel, CMS, CRUD API, SSG, AI Chat, Intake, Cinch, Site Kit, Relay, Workcell, Tribunal, StegoCipher Kujo, CMS Experience, and benchmark/showcase repos.

## Recently Verified Agent-Facing Capabilities

These repositories changed during the 2026-07-18 audit window and expose usable but bounded agent-facing capabilities:

- `relay`: Kujo-native bounded agent mission composition, pause/resume/cancel, lifecycle handoff receipts, provider/tool bridges, run evidence export, and repair replay. Treat as a local alpha orchestration layer for Integration Engineer, General Commander, Chief of Staff, Triage Agent, Receipt Collector, and Release Verifier. Do not treat it as remote exactly-once delivery, enterprise tenancy, or universal provider proof.
- `workcell`: local Docker/Podman-backed disposable execution workspaces with declared commands, exported artifacts, receipts, verification, and cleanup. Treat as a bounded execution gate for Tooling Developer, Routine Worker, Test Runner, QA Lead, Security Reviewer, Release Verifier, and Risk Officer when host Docker/Podman trust is acceptable. Do not treat it as a hardened microVM or hosted sandbox.
- `tribunal`: local-first adversarial decision review engine with hearing, fatal-flaw, ruling, and decision-packet artifacts. Treat as advisory governance evidence for Risk Officer, Product Strategist, Systems Architect, General Commander, and Release Verifier. Human authority remains required for consequential business, release, security, legal, or production decisions.
- `site-kit`: private internal design-system and component bundle with token, component, CSS, snapshot, lint, and validation commands. Treat as a frontend/documentation capability for Frontend Developer, Visual QA Agent, Documentation Writer, Product Strategist, and Release Verifier. Browser/accessibility proof remains separate for consuming layouts.
- `stego-cipher-kujo`: educational steganography/obfuscation CLI with Kujo smoke tests. Treat as a narrow demo or security-review subject only. Do not route secrets or cryptographic security requirements to it.
- `cms-experience`: Studio/public-site application layer for the sibling CMS backend with explicit auth and production-readiness gaps. Treat as a frontend/backend/integration showcase tied to `cms`; do not claim CMS human auth, preview-token, or public production readiness.

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

Repo docs support routine local use for Spec, Eval, Scout, Dispatch offline fixture workflows, CaseFile, RunLedger, Scent, Muzzle trusted local workflows, PackWrite local/team pack generation, Fence architecture checks, ShipCheck release scanning, Lens local browser QA, Kennel launch-safe package workflows, Watchdog local telemetry/proxy workflows, Relay local alpha lifecycle handoffs, Workcell local Docker/Podman execution gates, Tribunal advisory decision gates, and SiteKit local design-system builds. Each still requires environment-specific validation before broad enterprise claims.

## Experimental Or Underdocumented

- Concord is useful but explicitly early dogfood and not enterprise-ready.
- PatchBrief is dogfood beta.
- Lens is beta/stabilizing.
- ShipCheck is production-forward alpha.
- MCP is launch-honest as a local foundation but production deployment needs target validation.
- Public Kennel registry behavior, public discovery, moderation, malware scanning, and trust scoring are deferred.
- SITREP appears as a useful role name but not as a confirmed standalone KUJO tool.

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
