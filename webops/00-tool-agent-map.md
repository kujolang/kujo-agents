# WebOps Tool–Agent Map

Primary tools own the role's central evidence contract. Secondary tools enrich or verify within their documented boundaries.

| Agent | Primary tools | Secondary tools |
| --- | --- | --- |
| Trend Scout | SearchBridge | ContentGraph, RAG |
| Keyword Opportunity Analyst | SearchBridge, ContentGraph | SiteProbe |
| Competitor Intelligence Analyst | SiteProbe, SearchBridge | ContentGraph, RAG |
| Content Gap Analyst | ContentGraph | SearchBridge, RAG |
| Backlink & Mention Analyst | SearchBridge | SiteProbe |
| SEO Auditor | SiteProbe, SearchBridge, ContentGraph | Lens |
| Search Performance Analyst | SearchBridge | ContentGraph |
| Indexation Analyst | SiteProbe, SearchBridge | ContentGraph |
| Technical SEO Auditor | SiteProbe | ContentGraph, Lens, SearchBridge |
| AI Search Visibility Analyst | SearchBridge | RunLedger |
| Content Decay Analyst | SearchBridge, ContentGraph | SiteProbe, RAG |
| Internal Link Specialist | ContentGraph | SiteProbe, SearchBridge, Eval |
| Content Accuracy Reviewer | RAG | ContentGraph, SiteProbe |
| Cannibalization Analyst | ContentGraph, SearchBridge | SiteProbe |
| Content Portfolio Manager | ContentGraph, SearchBridge | SiteProbe |
| Content Pruning Analyst | ContentGraph, SearchBridge | SiteProbe |
| Site QA Operator | Lens, SiteProbe | CaseFile, Eval |
| Performance Analyst | SearchBridge | Lens |
| Accessibility Auditor | Lens | Eval, CaseFile |
| Schema Auditor | SiteProbe | Lens, Eval |
| Link Health Auditor | SiteProbe | Lens, CaseFile |
| Metadata Auditor | SiteProbe | Lens |
| Search Submission Operator | SearchBridge | RunLedger, Dispatch |
| Analytics Analyst | SearchBridge | ContentGraph |
| Information Architecture Auditor | ContentGraph, SiteProbe | Lens |
| Distribution Operator | Howl | CMS, SSG, RunLedger |
| Search & Web Standards Watch | RAG | RunLedger |
| WebOps Reporter | RunLedger | CaseFile |

SiteProbe never replaces Lens or Scout. ContentGraph never replaces RAG. SearchBridge fetches normalized evidence and does not perform analyst interpretation.
