# WebOps History And Reporting

Portable local history uses `.webops/` with `profile/`, `baselines/`, `siteprobe/`, `search/`, `analytics/`, `contentgraph/`, `content/`, `performance/`, `accessibility/`, `ai-visibility/`, `reports/`, `findings/`, and `actions/`.

Recurring operators read the previous relevant run, unresolved findings, and recorded actions; gather fresh evidence; compare; classify improvements, regressions, persistent and resolved findings; evaluate prior recommendations where evidence permits; and update history.

Finding IDs are deterministic hashes of `agent/check`, normalized target, and normalized issue identity. States are `NEW`, `PERSISTENT`, `RESOLVED`, `REGRESSED`, and `REOPENED`. A finding, recommendation, action, and outcome are separate records: a recommendation is not an action, and an action does not prove causation.

Human reports are quiet by default: what improved, regressed, changed, requires action, can wait, and could not be checked. Full evidence remains machine-readable. The canonical schemas live with the WebOps workflows repository so agents and workflow runs share one portable contract.
