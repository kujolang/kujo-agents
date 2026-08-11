# WebOps Capability Integration Map

Capabilities describe evidence access, not vendors. Provider-specific credentials grant only their declared families.

Canonical capabilities: `website`, `repository`, `browser`, `web-search`, `site-crawl`, `content-graph`, `search-performance-provider`, `analytics-provider`, `keyword-data-provider`, `backlink-data-provider`, `url-inspection-provider`, `page-performance-provider`, `field-performance-provider`, `search-submission-provider`, `publishing-provider`, and `distribution-provider`.

| Agent | Required | Recommended | Optional |
| --- | --- | --- | --- |
| Trend Scout | website, web-search | content-graph | keyword-data-provider |
| Keyword Opportunity Analyst | website | search-performance-provider, content-graph | keyword-data-provider, web-search |
| Competitor Intelligence Analyst | web-search | site-crawl | backlink-data-provider, keyword-data-provider |
| Content Gap Analyst | website, content-graph | web-search | search-performance-provider, keyword-data-provider |
| Backlink & Mention Analyst | web-search | None | backlink-data-provider |
| SEO Auditor | website | site-crawl, search-performance-provider, content-graph | analytics-provider, backlink-data-provider, page-performance-provider, field-performance-provider |
| Search Performance Analyst | search-performance-provider | None | content-graph, analytics-provider |
| Indexation Analyst | website, site-crawl | url-inspection-provider | search-performance-provider |
| Technical SEO Auditor | website, site-crawl | content-graph | browser, url-inspection-provider |
| AI Search Visibility Analyst | website, web-search | None | search-performance-provider |
| Content Decay Analyst | website | search-performance-provider, content-graph | analytics-provider, keyword-data-provider |
| Internal Link Specialist | website, content-graph | repository | search-performance-provider |
| Content Accuracy Reviewer | website, web-search | None | repository, content-graph |
| Cannibalization Analyst | website, content-graph | search-performance-provider | keyword-data-provider |
| Content Portfolio Manager | website, content-graph | search-performance-provider, analytics-provider | keyword-data-provider |
| Content Pruning Analyst | website, content-graph | search-performance-provider, analytics-provider | backlink-data-provider |
| Site QA Operator | website, browser | site-crawl | repository |
| Performance Analyst | website | page-performance-provider | field-performance-provider, browser |
| Accessibility Auditor | website, browser | None | repository |
| Schema Auditor | website, site-crawl | browser | web-search, repository |
| Link Health Auditor | website, site-crawl | None | browser, repository |
| Metadata Auditor | website, site-crawl | browser | repository |
| Search Submission Operator | search-submission-provider | website | None |
| Analytics Analyst | analytics-provider | None | content-graph, search-performance-provider |
| Information Architecture Auditor | website, content-graph | site-crawl | browser, repository |
| Distribution Operator | website | distribution-provider | publishing-provider |
| Search & Web Standards Watch | web-search | None | website |
| WebOps Reporter | website | None | site-crawl, content-graph, search-performance-provider, analytics-provider |

SearchBridge preflight reports each family independently. Missing credentials skip only dependent modules and never convert unavailable data into zero.
