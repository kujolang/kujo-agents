# WebOps Permission Model

Permission is a run input and an upper bound, not a trust label.

## OBSERVE

May crawl, query, search, inspect, read repositories and prior reports, collect evidence, calculate findings, and write its own run artifacts. It may not mutate a site or source repository.

## PROPOSE

Includes OBSERVE and may draft changes, repair briefs, patches, issue/PR content, and metadata, schema, link, or content proposals. It may not apply production changes.

## ACT

Includes PROPOSE and only the explicitly authorized role-bounded actions named by the run: for example edit scoped source, commit, open a PR, repair links, update metadata/schema, publish approved assets, or submit approved URLs. ACT is never unlimited authority.

Every run records selected mode, target, allowed actions, approval boundary, and receipt. The agent's maximum mode can only narrow authority. Provider submissions and distribution publishing require ACT even when credentials exist.
