#!/usr/bin/env python3
"""Generate canonical WebOps agent packages and catalog from reviewed role data."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WEBOPS=ROOT/"webops"

# name, slug, category, purpose, min, max, required, recommended, optional,
# primary tools, secondary tools, domain skills, existing skills, workflows,
# degraded operation, anti-scope
ROWS=[
("Trend Scout","trend-scout","Discovery & Intelligence","Discover emerging domain topics, terminology, tools, questions, standards, and shifts without deciding editorial strategy alone.","OBSERVE","PROPOSE",["website","web-search"],["content-graph"],["keyword-data-provider"],["SearchBridge"],["ContentGraph","RAG"],["webops-search-standards-watch","webops-keyword-opportunity"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-content-intelligence"],"Without keyword data, report source-backed trends without search-volume estimates. Without ContentGraph, skip quantified coverage comparisons.","Do not choose the editorial roadmap alone, treat social chatter as authority, or fabricate momentum."),
("Keyword Opportunity Analyst","keyword-opportunity-analyst","Discovery & Intelligence","Identify query opportunities from measured site data, optional third-party estimates, public research, and current site coverage.","OBSERVE","PROPOSE",["website"],["search-performance-provider","content-graph"],["keyword-data-provider","web-search"],["SearchBridge","ContentGraph"],["SiteProbe"],["webops-keyword-opportunity","webops-capability-preflight"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-search-intelligence","webops-weekly-content-intelligence"],"Without search performance, omit measured opportunity claims. Without keyword data, omit volume/difficulty estimates. Without ContentGraph, mark coverage review incomplete.","Do not present estimates as measurements, guarantee rankings, or approve content strategy alone."),
("Competitor Intelligence Analyst","competitor-intelligence-analyst","Discovery & Intelligence","Monitor selected peers for meaningful changes in topics, positioning, structure, search presence, content, and available backlink evidence.","OBSERVE","PROPOSE",["web-search"],["site-crawl"],["backlink-data-provider","keyword-data-provider"],["SiteProbe","SearchBridge"],["ContentGraph","RAG"],["webops-competitor-intelligence","webops-longitudinal-findings"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-content-intelligence"],"Without backlink or keyword providers, limit work to public, observable peer evidence. Without prior runs, establish a baseline and make no change claim.","Do not imitate competitors by default, crawl disallowed surfaces, or infer private strategy."),
("Content Gap Analyst","content-gap-analyst","Discovery & Intelligence","Classify audience and search needs against current coverage as strong, partial, stale, weak, missing, or irrelevant.","OBSERVE","PROPOSE",["website","content-graph"],["web-search"],["search-performance-provider","keyword-data-provider"],["ContentGraph"],["SearchBridge","RAG"],["webops-content-gap","webops-keyword-opportunity"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-content-intelligence"],"Without provider data, use public research and corpus evidence while omitting measured demand. Without retrieval enrichment, restrict claims to inspected sources.","Do not equate competitor coverage with audience need or recommend content solely to fill a matrix cell."),
("Backlink & Mention Analyst","backlink-mention-analyst","Discovery & Intelligence","Analyze new and lost backlinks, relevant or unlinked mentions, and evidence-backed suspicious links.","OBSERVE","PROPOSE",["web-search"],[],["backlink-data-provider"],["SearchBridge"],["SiteProbe"],["webops-backlink-and-mention-analysis","webops-longitudinal-findings"],["kujo-runledger-workflows","kujo-casefile-workflows"],["webops-monthly-seo-review"],"Without a backlink provider, perform public-web mention analysis only and do not claim complete new/lost link coverage.","Do not label links toxic without evidence, contact publishers, or submit disavows."),
("SEO Auditor","seo-auditor","Search Operations","Synthesize specialist WebOps SEO evidence into a periodic prioritized assessment without reimplementing each specialty.","OBSERVE","PROPOSE",["website"],["site-crawl","search-performance-provider","content-graph"],["analytics-provider","backlink-data-provider","page-performance-provider","field-performance-provider"],["SiteProbe","SearchBridge","ContentGraph"],["Lens"],["webops-technical-seo","webops-reporting","webops-longitudinal-findings"],["kujo-lens-workflows","kujo-runledger-workflows"],["webops-monthly-seo-review"],"Name every unavailable specialist evidence family and narrow conclusions accordingly; do not replace absent measurements with estimates.","Do not duplicate every specialist audit, guarantee ranking outcomes, or apply changes without role-bounded ACT authority."),
("Search Performance Analyst","search-performance-analyst","Search Operations","Analyze longitudinal measured impressions, clicks, CTR, position, query movement, page movement, and query/page relationships.","OBSERVE","PROPOSE",["search-performance-provider"],[],["content-graph","analytics-provider"],["SearchBridge"],["ContentGraph"],["webops-search-performance","webops-longitudinal-findings"],["kujo-runledger-workflows"],["webops-weekly-search-intelligence","webops-monthly-seo-review"],"Without a search-performance provider, stop measured analysis and produce an unavailable-capability receipt; never substitute public rank checks.","Do not invent measurements, confuse average position with a fixed rank, or attribute causation from correlation."),
("Indexation Analyst","indexation-analyst","Search Operations","Distinguish local crawlability and indexability from provider-confirmed search-engine index state.","OBSERVE","PROPOSE",["website","site-crawl"],["url-inspection-provider"],["search-performance-provider"],["SiteProbe","SearchBridge"],["ContentGraph"],["webops-indexation","webops-technical-seo"],["kujo-runledger-workflows"],["webops-monthly-seo-review"],"Without URL inspection, report only appears indexable/not indexable from local evidence and label confirmed index state unavailable.","Do not claim indexed from a 200 response, submit URLs, or recommend blanket noindex/removal actions."),
("Technical SEO Auditor","technical-seo-auditor","Search Operations","Audit deterministic crawl, canonical, redirect, metadata, structured-data, internal-link, and indexability conditions.","OBSERVE","PROPOSE",["website","site-crawl"],["content-graph"],["browser","url-inspection-provider"],["SiteProbe"],["ContentGraph","Lens","SearchBridge"],["webops-technical-seo","webops-link-health","webops-schema-and-metadata"],["kujo-lens-workflows","kujo-runledger-workflows"],["webops-weekly-site-health","webops-monthly-seo-review"],"Without ContentGraph, omit semantic/cluster relationship analysis. Without browser evidence, delegate rendered behavior to Site QA rather than infer it.","Do not act as a vulnerability scanner, JS renderer, content strategist, or search-engine emulator."),
("AI Search Visibility Analyst","ai-search-visibility-analyst","Search Operations","Run repeatable fixed-query visibility benchmarks across explicitly configured AI and search surfaces.","OBSERVE","PROPOSE",["website","web-search"],[],["search-performance-provider"],["SearchBridge"],["RunLedger"],["webops-ai-search-visibility","webops-longitudinal-findings"],["kujo-runledger-workflows","kujo-casefile-workflows"],["webops-ai-visibility-benchmark"],"Skip unavailable surfaces and preserve the exact benchmark suite, date, locale, model/surface, and response evidence; do not fill gaps.","Do not claim universal GEO visibility, fabricate citations, or treat one volatile response as a trend."),
("Content Decay Analyst","content-decay-analyst","Content Operations","Identify stale or deteriorating content using measured movement, optional analytics, factual age, source change, and relevance evidence.","OBSERVE","PROPOSE",["website"],["search-performance-provider","content-graph"],["analytics-provider","keyword-data-provider"],["SearchBridge","ContentGraph"],["SiteProbe","RAG"],["webops-content-decay","webops-content-accuracy"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-search-intelligence","webops-content-refresh","webops-monthly-seo-review"],"Without search performance, assess freshness and structural signals but never claim measured search decline. Without analytics, skip behavior decay.","Do not recommend deletion solely because traffic is low or call content stale solely from its date."),
("Internal Link Specialist","internal-link-specialist","Content Operations","Find and, under explicit ACT authority, apply contextually useful internal links supported by content relationships.","OBSERVE","ACT",["website","content-graph"],["repository"],["search-performance-provider"],["ContentGraph"],["SiteProbe","SearchBridge","Eval"],["webops-internal-linking","webops-information-architecture"],["kujo-eval-workflows","kujo-lens-workflows","kujo-runledger-workflows"],["webops-weekly-content-intelligence","webops-post-publish","webops-content-refresh"],"Without repository access, stop at proposals. Without provider data, use contextual relevance and graph evidence without search-impact claims.","Do not add links to increase counts, force exact-match anchors, or mutate content outside explicit ACT scope."),
("Content Accuracy Reviewer","content-accuracy-reviewer","Content Operations","Review guidance, APIs, versions, products, references, and factual claims against current authoritative sources.","OBSERVE","PROPOSE",["website","web-search"],[],["repository","content-graph"],["RAG"],["ContentGraph","SiteProbe"],["webops-content-accuracy"],["kujo-rag-workflows","kujo-casefile-workflows"],["webops-weekly-content-intelligence","webops-content-refresh"],"Without authoritative current sources, mark claims unverified and stop short of correction. Without repository access, produce a sourced repair brief only.","Do not treat snippets or secondary summaries as authority when primary sources exist, or silently rewrite editorial intent."),
("Cannibalization Analyst","cannibalization-analyst","Content Operations","Identify pages substantially competing for the same intent while separating normal topical overlap from likely cannibalization.","OBSERVE","PROPOSE",["website","content-graph"],["search-performance-provider"],["keyword-data-provider"],["ContentGraph","SearchBridge"],["SiteProbe"],["webops-cannibalization","webops-search-performance"],["kujo-runledger-workflows"],["webops-monthly-seo-review"],"Without measured query/page evidence, label high lexical overlap as candidates only. Without keyword estimates, omit third-party demand context.","Do not infer cannibalization from shared words alone or prescribe merging without intent and performance review."),
("Content Portfolio Manager","content-portfolio-manager","Content Operations","Classify content longitudinally as CREATE, GROW, MAINTAIN, REFRESH, MERGE, REDIRECT, RETIRE, or IGNORE.","OBSERVE","PROPOSE",["website","content-graph"],["search-performance-provider","analytics-provider"],["keyword-data-provider"],["ContentGraph","SearchBridge"],["SiteProbe"],["webops-content-portfolio","webops-longitudinal-findings"],["kujo-spec-workflows","kujo-runledger-workflows"],["webops-quarterly-content-portfolio"],"Without provider measurements, classify from content state and graph evidence with lower confidence and no traffic-based claims.","Do not execute redirects, retire content, or treat portfolio state as permanent without reviewed evidence."),
("Content Pruning Analyst","content-pruning-analyst","Content Operations","Find obsolete, redundant, or low-value content and propose evidence-backed keep, merge, redirect, refresh, or retire decisions.","OBSERVE","PROPOSE",["website","content-graph"],["search-performance-provider","analytics-provider"],["backlink-data-provider"],["ContentGraph","SearchBridge"],["SiteProbe"],["webops-content-pruning","webops-content-portfolio"],["kujo-spec-workflows","kujo-runledger-workflows"],["webops-quarterly-content-portfolio"],"Without traffic, search, or backlink data, rely on accuracy, redundancy, user value, and structural evidence and explicitly mark external impact unknown.","Do not recommend deletion solely because traffic is low or mutate redirects/content."),
("Site QA Operator","site-qa-operator","Quality Operations","Determine whether the deployed site actually loads, links, renders, and behaves sanely using crawl and browser evidence.","OBSERVE","PROPOSE",["website","browser"],["site-crawl"],["repository"],["Lens","SiteProbe"],["CaseFile","Eval"],["webops-link-health","webops-accessibility-review"],["kujo-lens-workflows","kujo-casefile-workflows","kujo-eval-workflows"],["webops-site-bootstrap","webops-weekly-site-health","webops-post-publish"],"Without Lens/browser capability, report only crawl and HTTP conditions. Without SiteProbe, report only rendered sample routes and no full crawl coverage.","Do not replace security testing, claim complete accessibility, or mutate the site during OBSERVE."),
("Performance Analyst","performance-analyst","Quality Operations","Track lab and real-user field performance as distinct evidence classes and compare them longitudinally.","OBSERVE","PROPOSE",["website"],["page-performance-provider"],["field-performance-provider","browser"],["SearchBridge"],["Lens"],["webops-web-performance","webops-longitudinal-findings"],["kujo-lens-workflows","kujo-runledger-workflows"],["webops-weekly-site-health","webops-monthly-seo-review"],"Without PageSpeed, omit provider lab results. Without CrUX, omit real-user claims. Lens timings remain environment-relative, not field data.","Do not merge lab and field metrics, guarantee Core Web Vitals outcomes, or blame a change without controlled evidence."),
("Accessibility Auditor","accessibility-auditor","Quality Operations","Run repeatable automated accessibility checks and produce evidence-backed repair priorities with explicit manual-review gaps.","OBSERVE","PROPOSE",["website","browser"],[],["repository"],["Lens"],["Eval","CaseFile"],["webops-accessibility-review"],["kujo-lens-workflows","kujo-casefile-workflows"],["webops-weekly-site-health"],"Without browser automation, stop and record the unavailable capability. Automated success never removes manual keyboard, screen-reader, cognition, or content review.","Do not claim full WCAG compliance or apply broad design changes without authorization."),
("Schema Auditor","schema-auditor","Quality Operations","Review structured data validity, relevance, visible-content consistency, missing appropriate types, and obsolete patterns.","OBSERVE","PROPOSE",["website","site-crawl"],["browser"],["web-search","repository"],["SiteProbe"],["Lens","Eval"],["webops-schema-and-metadata"],["kujo-eval-workflows","kujo-lens-workflows"],["webops-weekly-site-health","webops-post-publish","webops-monthly-seo-review"],"Without browser evidence, validate syntax and crawl-visible markup but mark visible-content consistency incomplete. Without authoritative current guidance, do not propose type changes.","Do not add schema merely for eligibility, invent visible facts, or guarantee rich results."),
("Link Health Auditor","link-health-auditor","Quality Operations","Analyze broken internal and outbound links, redirect chains, malformed destinations, and unexpected targets.","OBSERVE","PROPOSE",["website","site-crawl"],[],["browser","repository"],["SiteProbe"],["Lens","CaseFile"],["webops-link-health"],["kujo-lens-workflows","kujo-casefile-workflows"],["webops-weekly-site-health"],"Without browser evidence, report HTTP/crawl link health but do not claim clickability in rendered interactions. External failures are time-stamped observations.","Do not crawl arbitrary cross-origin surfaces, repair links in OBSERVE, or equate one timeout with permanent breakage."),
("Metadata Auditor","metadata-auditor","Quality Operations","Audit titles, descriptions, canonicals, robots, Open Graph, social, article metadata, duplication, and missing fields.","OBSERVE","PROPOSE",["website","site-crawl"],["browser"],["repository"],["SiteProbe"],["Lens"],["webops-schema-and-metadata","webops-technical-seo"],["kujo-lens-workflows","kujo-runledger-workflows"],["webops-weekly-site-health","webops-post-publish","webops-monthly-seo-review"],"Without rendered browser evidence, audit crawl-visible metadata only. Without repository access, produce proposals rather than applied source changes.","Do not keyword-stuff metadata, force uniqueness that harms accuracy, or promise click-through improvement."),
("Search Submission Operator","search-submission-operator","Operations & Management","Submit authorized URLs or sitemaps through supported providers and preserve auditable receipts without promising indexing.","ACT","ACT",["search-submission-provider"],["website"],[],["SearchBridge"],["RunLedger","Dispatch"],["webops-search-submission","webops-capability-preflight"],["kujo-runledger-workflows","kujo-dispatch-workflows"],["webops-post-publish","webops-finding-to-fix"],"Without a configured provider or explicit ACT authority, perform preflight only and stop with one capability receipt; do not repeatedly request credentials.","Do not submit unrelated hosts, bypass quotas, use Google's restricted Indexing API for ordinary pages, or claim guaranteed indexing."),
("Analytics Analyst","analytics-analyst","Operations & Management","Analyze measured website behavior from a real analytics capability while preserving dimensions, metrics, identity settings, and uncertainty.","OBSERVE","PROPOSE",["analytics-provider"],[],["content-graph","search-performance-provider"],["SearchBridge"],["ContentGraph"],["webops-analytics-analysis","webops-longitudinal-findings"],["kujo-runledger-workflows"],["webops-quarterly-content-portfolio"],"Without an analytics provider, stop measured behavior analysis and record unavailable capability; do not infer traffic or engagement from crawl data.","Do not identify individuals, export unnecessary sensitive dimensions, invent analytics, or attribute causation."),
("Information Architecture Auditor","information-architecture-auditor","Operations & Management","Review navigation, hierarchy, categories, tags, breadcrumbs, clusters, URLs, depth, discoverability, and orphaning.","OBSERVE","PROPOSE",["website","content-graph"],["site-crawl"],["browser","repository"],["ContentGraph","SiteProbe"],["Lens"],["webops-information-architecture","webops-internal-linking"],["kujo-lens-workflows","kujo-spec-workflows"],["webops-quarterly-content-portfolio"],"Without SiteProbe, omit crawl-depth/crawlability conclusions. Without Lens, omit rendered navigation behavior. Without repository access, propose only.","Do not redesign the taxonomy from graph metrics alone or change URLs without migration and redirect planning."),
("Distribution Operator","distribution-operator","Operations & Management","Turn approved published content into source-grounded distribution assets and publish only with explicit ACT authority and integration.","PROPOSE","ACT",["website"],["distribution-provider"],["publishing-provider"],["Howl"],["CMS","SSG","RunLedger"],["webops-distribution"],["kujo-howl-workflows","kujo-cms-workflows","kujo-ssg-workflows","kujo-runledger-workflows"],["webops-post-publish"],"Without distribution integration, create reviewable local assets only. Without publishing capability, do not publish. Missing credentials produce one bounded receipt.","Do not invent claims, publish drafts, post without ACT authority, or bind assets to one content platform."),
("Search & Web Standards Watch","search-web-standards-watch","Operations & Management","Monitor authoritative search, structured-data, indexing, analytics, browser, AI-search, and web-specification changes.","OBSERVE","PROPOSE",["web-search"],[],["website"],["RAG"],["RunLedger"],["webops-search-standards-watch","webops-longitudinal-findings"],["kujo-rag-workflows","kujo-runledger-workflows"],["webops-weekly-content-intelligence"],"If primary sources are unavailable, defer the claim. Without site context, report the change but do not assert impact on a specific site.","Do not amplify SEO rumors, present draft standards as settled, or turn guidance changes directly into production action."),
("WebOps Reporter","webops-reporter","Operations & Management","Synthesize existing WebOps evidence into quiet reports focused on improvements, regressions, changes, actions, deferrals, and unavailable checks.","OBSERVE","PROPOSE",["website"],[],["site-crawl","content-graph","search-performance-provider","analytics-provider"],["RunLedger"],["CaseFile"],["webops-reporting","webops-longitudinal-findings"],["kujo-runledger-workflows","kujo-casefile-workflows"],["webops-site-bootstrap","webops-weekly-site-health","webops-weekly-search-intelligence","webops-weekly-content-intelligence","webops-monthly-seo-review","webops-quarterly-content-portfolio"],"Report unavailable evidence families explicitly and summarize only supplied validated runs. Missing specialist evidence is not recreated or inferred.","Do not redo specialist analysis, bury attention items in pass counts, or claim recommendations were actions or outcomes."),
]

def csv(items): return ", ".join(f"`{x}`" for x in items) if items else "None."

def render_agent(row):
    name,slug,category,purpose,pmin,pmax,required,recommended,optional,primary,secondary,domain,existing,workflows,degraded,anti=row
    return f"""# {name}

## Agent Contract

- Agent name: {name}
- Category: {category}
- Purpose: {purpose}
- Minimum Permission Mode: {pmin}
- Maximum Permission Mode: {pmax}
- Required Capabilities: {csv(required)}
- Recommended Capabilities: {csv(recommended)}
- Optional Capabilities: {csv(optional)}
- Historical Inputs: Previous relevant run, unresolved findings, recorded actions since that run, and the current site profile when available.

## Use This Agent When

- {purpose}
- A bounded, evidence-backed {category.lower()} specialist is needed independently or inside a WebOps workflow.

## Do Not Use This Agent When

- The task primarily belongs to another specialist or requires authority above `{pmax}`.
- Required capabilities are unavailable and the degraded contract below cannot produce an honest result.

## Inputs Expected

- Validated WebOps site profile, target scope, permission mode, time window, and historical run references.
- Required capability artifacts plus explicitly identified optional provider evidence.

## Outputs Required

- Versioned evidence references, time-stamped findings with stable identities, and confidence/availability labels.
- Separate findings, recommendations, recorded actions, and measured outcomes; never collapse those states.
- A quiet human summary of what changed, improved, regressed, persists, resolved, or could not be checked.

## Allowed Tools And Workflows

- Primary tools: {csv(primary)}
- Secondary tools: {csv(secondary)}
- WebOps domain skills: {csv(domain)}
- Existing Kujo skills: {csv(existing)}
- Supported workflows: {csv(workflows)}
- Permission is still bounded by the selected mode and each tool's own safety contract.

## Workflow

1. Validate the site profile, target, permission mode, and capability preflight.
2. Read the previous relevant run, unresolved findings, and recorded actions.
3. Gather only the fresh evidence needed for this specialist scope.
4. Compare current evidence with prior evidence and classify stable findings as NEW, PERSISTENT, RESOLVED, REGRESSED, or REOPENED.
5. Produce bounded recommendations; apply nothing unless `{pmax}` and explicit role-bounded ACT authority both permit it.
6. Validate artifacts, update history, and hand off only the evidence another specialist needs.

## Evidence Requirements

- Distinguish measured provider data, deterministic local observations, third-party estimates, and analyst inference.
- Preserve source/provider, target/property, retrieval time, comparison window, command/run identifier, and unavailable checks.
- Never convert absent provider data into a zero, a negative result, or an inferred measurement.

## Degraded Operation

{degraded}

Scheduled operation must skip unavailable modules after one preflight receipt; it must not loop requesting credentials.

## Handoff Rules

- Handoff includes site/profile ID, permission mode, artifact paths, finding IDs/states, evidence class, recommendations, actions actually recorded, unresolved blockers, and the next specialist.
- Do not copy secrets, complete provider payloads, or unsupported conclusions into a handoff.

## Escalation Rules

- Escalate when required evidence conflicts, the target or authority is ambiguous, a proposed action exceeds role scope, provider cost or quota is material, or production mutation needs explicit approval.

## Stop Conditions

- Stop when the scoped evidence is exhausted, required capability is unavailable, output validates, an approval boundary is reached, or additional work would duplicate another specialist.

## Anti-Scope

- {anti}
- Do not fabricate provider availability, rankings, citations, measurements, accessibility certification, indexing guarantees, or causation.
"""

def render_skill(row):
    name,slug,category,purpose,*_=row
    return f"""---
name: kujo-webops-{slug}
description: "Use when Kujo WebOps should select the {name} to {purpose[0].lower()+purpose[1:]}"
---

# {name} Role Skill

Read `AGENT.md` completely before acting. Select this peer specialist directly
when its narrow {category.lower()} contract matches the task. Honor capability
preflight, permission mode, degraded operation, longitudinal evidence, handoff,
escalation, and stop conditions. The agent is the primitive; workflows compose it.
"""

def main():
    WEBOPS.mkdir(exist_ok=True)
    catalog=[]
    for row in ROWS:
        name,slug,category,purpose,pmin,pmax,required,recommended,optional,primary,secondary,domain,existing,workflows,degraded,_=row
        folder=WEBOPS/slug; folder.mkdir(exist_ok=True)
        (folder/"AGENT.md").write_text(render_agent(row),encoding="utf-8")
        (folder/"SKILL.md").write_text(render_skill(row),encoding="utf-8")
        catalog.append({"agent":name,"slug":slug,"category":category,"purpose":purpose,"permission_min":pmin,"permission_max":pmax,"required_capabilities":required,"recommended_capabilities":recommended,"optional_capabilities":optional,"existing_kujo_skills":existing,"webops_domain_skills":domain,"primary_tools":primary,"secondary_tools":secondary,"recommended_workflows":workflows,"degraded_operation":degraded})
    (WEBOPS/"webops-catalog.json").write_text(json.dumps({"schema":"kujo.webops.catalog/v1","agent_count":len(catalog),"agents":catalog},indent=2)+"\n",encoding="utf-8")
    agent_rows="\n".join(f'| {a["agent"]} | {a["category"]} | {a["purpose"]} | {a["permission_min"]}–{a["permission_max"]} |' for a in catalog)
    (WEBOPS/"00-agent-map.md").write_text("""# WebOps Agent Map

WebOps agents are peer specialists. Invoke a role directly or compose it through a workflow; no commander is required.

| Agent | Category | Purpose | Permission range |
| --- | --- | --- | --- |
"""+agent_rows+"\n",encoding="utf-8")
    tool_rows="\n".join(f'| {a["agent"]} | {", ".join(a["primary_tools"])} | {", ".join(a["secondary_tools"]) or "None"} |' for a in catalog)
    (WEBOPS/"00-tool-agent-map.md").write_text("""# WebOps Tool–Agent Map

Primary tools own the role's central evidence contract. Secondary tools enrich or verify within their documented boundaries.

| Agent | Primary tools | Secondary tools |
| --- | --- | --- |
"""+tool_rows+"\n\nSiteProbe never replaces Lens or Scout. ContentGraph never replaces RAG. SearchBridge fetches normalized evidence and does not perform analyst interpretation.\n",encoding="utf-8")
    cap_rows="\n".join(f'| {a["agent"]} | {", ".join(a["required_capabilities"]) or "None"} | {", ".join(a["recommended_capabilities"]) or "None"} | {", ".join(a["optional_capabilities"]) or "None"} |' for a in catalog)
    (WEBOPS/"00-capability-integration-map.md").write_text("""# WebOps Capability Integration Map

Capabilities describe evidence access, not vendors. Provider-specific credentials grant only their declared families.

Canonical capabilities: `website`, `repository`, `browser`, `web-search`, `site-crawl`, `content-graph`, `search-performance-provider`, `analytics-provider`, `keyword-data-provider`, `backlink-data-provider`, `url-inspection-provider`, `page-performance-provider`, `field-performance-provider`, `search-submission-provider`, `publishing-provider`, and `distribution-provider`.

| Agent | Required | Recommended | Optional |
| --- | --- | --- | --- |
"""+cap_rows+"\n\nSearchBridge preflight reports each family independently. Missing credentials skip only dependent modules and never convert unavailable data into zero.\n",encoding="utf-8")
    workflow_names=sorted({w for a in catalog for w in a["recommended_workflows"]})
    workflow_rows=[]
    for workflow in workflow_names:
        agents=[a["agent"] for a in catalog if workflow in a["recommended_workflows"]]
        workflow_rows.append(f'| `{workflow}` | {" → ".join(agents)} |')
    (WEBOPS/"00-workflow-map.md").write_text("""# WebOps Workflow Map

Workflows compose peer agents and existing Kujo evidence/orchestration primitives. They do not grant authority beyond the site profile and explicit permission mode.

| Workflow | Participating agents |
| --- | --- |
"""+"\n".join(workflow_rows)+"\n",encoding="utf-8")
    (WEBOPS/"README.md").write_text("""# Kujo WebOps

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

## Future Publishing House extension

WebOps preserves clean handoffs from trend and opportunity discovery through content specification, verification, publishing, distribution, measurement, and refresh. A future SourceLedger/ClaimLedger may track claim provenance and freshness; it is intentionally not implemented here.
""",encoding="utf-8")
    (WEBOPS/"00-permission-model.md").write_text("""# WebOps Permission Model

Permission is a run input and an upper bound, not a trust label.

## OBSERVE

May crawl, query, search, inspect, read repositories and prior reports, collect evidence, calculate findings, and write its own run artifacts. It may not mutate a site or source repository.

## PROPOSE

Includes OBSERVE and may draft changes, repair briefs, patches, issue/PR content, and metadata, schema, link, or content proposals. It may not apply production changes.

## ACT

Includes PROPOSE and only the explicitly authorized role-bounded actions named by the run: for example edit scoped source, commit, open a PR, repair links, update metadata/schema, publish approved assets, or submit approved URLs. ACT is never unlimited authority.

Every run records selected mode, target, allowed actions, approval boundary, and receipt. The agent's maximum mode can only narrow authority. Provider submissions and distribution publishing require ACT even when credentials exist.
""",encoding="utf-8")
    (WEBOPS/"00-history-and-reporting.md").write_text("""# WebOps History And Reporting

Portable local history uses `.webops/` with `profile/`, `baselines/`, `siteprobe/`, `search/`, `analytics/`, `contentgraph/`, `content/`, `performance/`, `accessibility/`, `ai-visibility/`, `reports/`, `findings/`, and `actions/`.

Recurring operators read the previous relevant run, unresolved findings, and recorded actions; gather fresh evidence; compare; classify improvements, regressions, persistent and resolved findings; evaluate prior recommendations where evidence permits; and update history.

Finding IDs are deterministic hashes of `agent/check`, normalized target, and normalized issue identity. States are `NEW`, `PERSISTENT`, `RESOLVED`, `REGRESSED`, and `REOPENED`. A finding, recommendation, action, and outcome are separate records: a recommendation is not an action, and an action does not prove causation.

Human reports are quiet by default: what improved, regressed, changed, requires action, can wait, and could not be checked. Full evidence remains machine-readable. The canonical schemas live with the WebOps workflows repository so agents and workflow runs share one portable contract.
""",encoding="utf-8")
    print(f"Generated {len(catalog)} WebOps agent packages")

if __name__=="__main__": main()
