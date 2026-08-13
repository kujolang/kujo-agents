# Kujo WebOps

Kujo WebOps is a composable team of specialized AI website operators that continuously research, measure, audit, maintain, optimize, and improve websites.

It is a peer agent set, not an SEO prompt pack, autonomous webmaster, commander hierarchy, or replacement for the Kujo Chain of Command. The agent is the primitive and the workflow is the composition.

## Start here

1. Select a specialist from [`00-agent-map.md`](00-agent-map.md).
2. Preflight the normalized capabilities in [`00-capability-integration-map.md`](00-capability-integration-map.md).
3. Select `OBSERVE`, `PROPOSE`, or explicitly bounded `ACT` using [`00-permission-model.md`](00-permission-model.md).
4. Read prior state and preserve finding history using [`00-history-and-reporting.md`](00-history-and-reporting.md).
5. Run directly or compose through [`00-workflow-map.md`](00-workflow-map.md).

## Structure

Each of the 28 directories contains a complete `AGENT.md` contract and a short role-routing `SKILL.md`. `webops-catalog.json` is generated from the same reviewed role data and drives deterministic cross-repository validation. Existing Chain of Command contracts remain independent.

## Website intelligence layer

- SiteProbe: crawlable website state, links, metadata, indexability, and crawl history.
- SearchBridge: capability-scoped external search, analytics, performance, backlink, keyword, and submission evidence.
- ContentGraph: deterministic content relationships, clusters, overlaps, orphans, and link opportunities.

Existing Kujo tools remain authoritative for Spec, Eval, Dispatch, Scout, Scent, RAG, Lens, RunLedger, CaseFile, Workcell, Relay, Redact, Muzzle, PackWrite, PatchBrief, ChangeBucket, ShipCheck, Fence, Watchdog, SSG, CMS, Howl, MCP, Agents SDK, and AI SDK responsibilities.

## Human reporting surface

The sibling [`kujo-workflows` WebOps Dashboard](https://github.com/kujolang/kujo-workflows/tree/main/webops-dashboard)
imports the ten workflow run-packet contracts and this repository's 28-role
catalog into a local SQLite database. Its SiteKit interface and Dither Kit
charts make runs, findings, degraded capabilities, approval gates, workflow
coverage, and agent responsibilities visible without making the operator read
artifact files directly. Machine-readable run evidence remains authoritative,
and the dashboard never grants `ACT`.

## Future Publishing House extension

WebOps preserves clean handoffs from trend and opportunity discovery through content specification, verification, publishing, distribution, measurement, and refresh. A future SourceLedger/ClaimLedger may track claim provenance and freshness; it is intentionally not implemented here.
