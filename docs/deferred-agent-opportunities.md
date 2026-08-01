# Deferred Agent Opportunities

This record captures credible new-agent candidates discovered during periodic audits. It is intentionally conservative: do not scaffold or register these agents without separate human approval and repository-backed contracts.

## 2026-08-01 Audit

### Intake Coordinator

- Proposed role: Intake Coordinator.
- Problem or gap: `intake` normalizes inbound work across manual, file, webhook, Slack, GitHub, Jira, Linear, ClickUp, and email sources, then proposes policy-gated actions with local audit logs.
- Repository-backed evidence: `../../intake/README.md`, `../../intake/package.json`.
- Relevant tools/skills/repositories: Intake, Strata export, TotalRecall-compatible export, source adapters, dashboard, policy gates.
- Expected inputs: source configuration, incoming item, queue policy, approval policy, action target, retention rules.
- Expected outputs: normalized `IntakeItem`, draft/action record, approval/audit evidence, learning export, unresolved approval boundary.
- Overlap: Chief of Staff, Triage Agent, Issue Hygiene Worker, General Commander, Receipt Collector.
- Why not add now: No dedicated `kujo-skills` entry or `kujo-workflows` contract was verified for routine chain delegation. Existing strategic/triage/issue roles can evaluate Intake outputs when explicitly assigned.
- Required authority boundaries: no unattended remote sends, mailbox mutation, issue comments, credential use, non-local dashboard exposure, or learning export without policy and human approval where required.
- Verification requirements: `npm run verify`, `intake doctor`, `intake shipcheck`, dashboard/API smoke, source-specific webhook or mailbox readiness checks.
- Risks/costs/token impact: could become a broad routing agent that duplicates Chief of Staff and Triage Agent; live adapters can involve credentials and external mutations.
- Recommendation: defer.
- Evidence still required: stable chain skill/workflow contract and repeated workload showing existing routing roles cannot manage Intake handoffs safely.

### Cinch Workspace Operator

- Proposed role: Cinch Workspace Operator.
- Problem or gap: `cinch` is a local desktop harness that can coordinate workspaces, file edits, git diffs, commands, MCP, proof artifacts, and Trail export.
- Repository-backed evidence: `../../cinch/README.md`, `../../cinch/package.json`.
- Relevant tools/skills/repositories: Cinch, PatchBrief, ShipCheck, Lens, RunLedger/Trail, MCP, Workcell registry, desktop smoke evidence.
- Expected inputs: workspace path, command/tool policy, approval profile, proof target, git operation scope.
- Expected outputs: Trail export, proof artifacts, command/diff evidence, unresolved approval or desktop-platform boundary.
- Overlap: Tooling Developer, Frontend Developer, Integration Engineer, QA Lead, Visual QA Agent, Receipt Collector.
- Why not add now: Cinch is a product/tool surface and macOS-first hardened alpha, not a chain runtime contract. Existing agents can work on Cinch when assigned without creating a broad operator role.
- Required authority boundaries: no unapproved shell, write, git, push, PR, MCP, network, external-adapter, or desktop automation actions.
- Verification requirements: `pnpm verify`, `pnpm release:readiness` for distribution claims, Tauri/browser smoke, Cargo tests, platform-specific desktop evidence.
- Risks/costs/token impact: a broad workspace operator could duplicate most execution and worker roles while increasing approval complexity.
- Recommendation: defer.
- Evidence still required: a narrow chain skill/workflow and repeated cross-tool workspace operations that current agents cannot handle through existing roles.

### Diff Review Fixture Steward

- Proposed role: Diff Review Fixture Steward.
- Problem or gap: `diff-viewer-demo`, `diff-viewer-demo-fresh`, and `diff-viewer-verified` are small repositories for testing workspace diff and inline review behavior.
- Repository-backed evidence: `../../diff-viewer-demo/README.md`, `../../diff-viewer-demo-fresh/README.md`, `../../diff-viewer-verified/README.md`.
- Relevant tools/skills/repositories: fixture repos, Code Reviewer, QA Lead, Cinch or Codex diff-review surfaces.
- Expected inputs: fixture scenario, expected diff/review behavior, target review UI.
- Expected outputs: small fixture diff, test result, review-surface evidence.
- Overlap: Code Reviewer, QA Lead, Visual QA Agent.
- Why not add now: These are fixtures, not durable Kujo tools, workflows, or product capabilities.
- Required authority boundaries: no broad source changes or tool claims from fixture behavior.
- Verification requirements: fixture-specific Node tests where present and target review UI proof.
- Risks/costs/token impact: unnecessary agent proliferation for throwaway test data.
- Recommendation: reject.
- Evidence still required: none unless the fixtures become a maintained review harness with a stable contract.
