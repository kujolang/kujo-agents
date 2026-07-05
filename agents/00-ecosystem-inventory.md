# KUJO Ecosystem Inventory

This inventory summarizes the inspected KUJO ecosystem for the agent chain. It is concise by design; use the referenced repo docs before making tool-behavior claims.

## Existing Agents

- `archivist/`: universal source-bound project researcher and dossier builder.
- `kujo-archivist/`: KUJO-specific source-bound ecosystem researcher and dossier builder.

Existing agents use package directories with `AGENT.md`, `SKILL.md`, and optional `references/`.

## Existing Skills

The local `kujo-skills/skills/` folder contains workflow skills for Agents SDK, AI SDK, CaseFile, ChangeBucket, Concord, Dispatch, Eval, Fence, Howl, Kennel, Lens, MCP, Muzzle, PackWrite, PatchBrief, RAG, RunLedger, Scent, Scout, ShipCheck, Spec, SSG, Watchdog, release gates, readiness auditing, maintainer review, security hardening, tool building, runtime parity, CLI contracts, docs drift, and related KUJO repo work.

## Existing Workflows

- `kujo-workflows/`: runnable workflow kits such as agency runner, verified fix loop, AI SDK + Muzzle benchmark, CaseFile evidence packet, Dispatch approval router, MCP agent gateway review, RAG enterprise knowledge gate, Howl content factory, doc generation contract runner, and loop engineering.
- Individual tool repos include repo-specific workflow scripts, release gates, contract tests, examples, and AGENTS guidance.

## Existing Tools

Confirmed tool repos include Kujo runtime, Kujo Doctor, Agents SDK, AI SDK, Spec, Eval, Scout, Dispatch, MCP, RAG, Watchdog, Scent, Fence, PatchBrief, ShipCheck, Concord, RunLedger, Muzzle, Howl, ChangeBucket, PackWrite, CaseFile, Lens, Kennel, CMS, CRUD API, SSG, AI Chat, Intake, Cinch, Site Kit, and benchmark/showcase repos.

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

Repo docs support routine local use for Spec, Eval, Scout, Dispatch offline fixture workflows, CaseFile, RunLedger, Scent, Muzzle trusted local workflows, PackWrite local/team pack generation, Fence architecture checks, ShipCheck release scanning, Lens local browser QA, Kennel launch-safe package workflows, and Watchdog local telemetry/proxy workflows. Each still requires environment-specific validation before broad enterprise claims.

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
agents/<agent-name>/AGENT.md
agents/<agent-name>/SKILL.md
```

The existing root Archivist packages are preserved and referenced rather than moved.
