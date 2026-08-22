# Deferred Agent Opportunities

This record captures credible new-agent candidates discovered during periodic audits. It is intentionally conservative: do not scaffold or register these agents without separate human approval and repository-backed contracts.

## 2026-08-22 Audit

### Source Work Coordinator

- Proposed role: Source Work Coordinator.
- Problem or gap: `source` provides an agent-first Git collaboration lifecycle for work items, sessions, changes, evidence, decisions, canonical Git state, capability-gated API/Git transport, `source submit`, tenant-scoped org/project routes, rate limiting, and credential scanning.
- Repository-backed evidence: `../../source/README.md`, `../../source/package.json`, `../../source/docs/source/`.
- Relevant tools/skills/repositories: Source, Git, Eval/Spec/ShipCheck evidence ingestion, Systems Architect, Integration Engineer, Tooling Developer, Security Reviewer, Code Reviewer, QA Lead, Risk Officer, Release Verifier, Receipt Collector.
- Expected inputs: Source org/project/repository identity, work/change IDs, capability grant boundary, Git transport policy, required evidence policy, credential policy, store backend, and verification commands.
- Expected outputs: normalized work/change/evidence records, submitted change packet, capability audit notes, Git transport result, credential-scan result, decision boundary, and unresolved approval or policy blockers.
- Overlap: Systems Architect, Integration Engineer, Tooling Developer, Security Reviewer, Code Reviewer, QA Lead, Risk Officer, Release Verifier, Receipt Collector, and existing GitHub/GitLab workflows.
- Why not add now: Existing roles can inspect or modify Source when explicitly assigned, and no dedicated `kujo-skills` chain skill or `kujo-workflows` contract exists for routine Source delegation, accept authority, policy mutation, or credential use.
- Required authority boundaries: no live Source server mutation, capability issuance, Git push, change acceptance, policy modification, org/project administration, credential use, or canonical-state decision without explicit human approval and least-privilege credentials.
- Verification requirements: `npm test`, CLI/API contract smoke, auth and Git-transport tests, credential-scan tests, store-backend tests, tenant-isolation tests, and independent security/release review.
- Risks/costs/token impact: a standalone coordinator could duplicate issue hygiene, integration, code review, QA, and release roles while creating unclear authority over Git canonical state and human approval.
- Recommendation: defer.
- Evidence still required: stable chain skill or workflow contract, repeated Source operating workload, governance decision on Source versus existing GitHub/GitLab/Paperclip workflows, and explicit credential/capability policy.

## 2026-08-15 Audit

### Static Commerce Operator

- Proposed role: Static Commerce Operator.
- Problem or gap: `commerce` adds catalog validation, browser cart state, normalized commerce events, SSG integration, and optional provider checkout runtime for static Kujo sites.
- Repository-backed evidence: `../../commerce/README.md`, `../../commerce/AGENTS.md`, `../../commerce/package.json`, `../../commerce/schemas/catalog.schema.json`, `../../commerce/schemas/cart.schema.json`, `../../commerce/schemas/event.schema.json`.
- Relevant tools/skills/repositories: Commerce, SSG, Frontend Developer, Backend Developer, Integration Engineer, Security Reviewer, QA Lead, Release Verifier.
- Expected inputs: site path, `kujo-commerce.yml`, product metadata, provider policy, checkout runtime boundary, credential policy, and verification commands.
- Expected outputs: validated catalog, generated static assets, cart/runtime contract evidence, provider preflight status, security notes, and release blockers.
- Overlap: Frontend Developer, Backend Developer, Integration Engineer, Security Reviewer, QA Lead, Release Verifier.
- Why not add now: Existing roles can cover Commerce work when explicitly assigned, and no dedicated chain skill/workflow exists for payment-provider authority, checkout effects, or order-data boundaries.
- Required authority boundaries: no provider credentials, checkout mutation, payment setup, order/customer data handling, deployment, or production release without explicit approval and least-privilege runtime configuration.
- Verification requirements: `npm run validate`, schema checks, SSG integration build, browser cart smoke, provider fixture/runtime tests, secret review, and release gate.
- Risks/costs/token impact: a standalone commerce operator could duplicate frontend, backend, integration, security, and release responsibilities while increasing credential and money-movement risk.
- Recommendation: defer.
- Evidence still required: stable Kujo skill or workflow contract, repeated commerce workload, provider credential model, and independent security/release review requirements.

### Image Authenticity Analyst

- Proposed role: Image Authenticity Analyst.
- Problem or gap: `truthlens` labels visible web images with local AI-confidence scores inside a Chrome extension.
- Repository-backed evidence: `../../truthlens/README.md`, `../../truthlens/package.json`, `../../truthlens/eval.json`.
- Relevant tools/skills/repositories: TruthLens, Chrome extension QA, Frontend Developer, Security Reviewer, Visual QA Agent, QA Lead, Release Verifier.
- Expected inputs: extension build, model artifact, benchmark fixture, target browser, calibration policy, and privacy/security review scope.
- Expected outputs: validation report, browser smoke evidence, model digest proof, limitation notes, and security/privacy findings.
- Overlap: Frontend Developer, Visual QA Agent, Security Reviewer, QA Lead, Release Verifier, Content Accuracy Reviewer where media claims are in scope.
- Why not add now: TruthLens is a product/browser-extension target, not a general evidence authority. Existing roles can review and maintain it without granting editorial fact-checking or WebOps verification authority.
- Required authority boundaries: no authorship claims, deception claims, moderation action, evidence certification, network upload, or publication decision based only on a probabilistic score.
- Verification requirements: `npm run check`, `npm run package`, Chrome extension smoke, model digest verification, benchmark evidence, and privacy review.
- Risks/costs/token impact: a dedicated role would likely overstate model authority and duplicate existing frontend, security, QA, and release lanes.
- Recommendation: reject.
- Evidence still required: none unless the project becomes a broader maintained media-forensics workflow with stable contracts and explicit human-review boundaries.

## 2026-08-08 Audit

### Context Ingestion Steward

- Proposed role: Context Ingestion Steward.
- Problem or gap: `totalrecall` can ingest Fathom meetings, chat exports, Slack threads, and GitHub activity into Strata, markdown folders, static HTML, or local JSON indexes.
- Repository-backed evidence: `../../totalrecall/README.md`, `../../totalrecall/docs/GETTING_STARTED.md`, `../../totalrecall/docs/SECRETS_AND_KEYCHAIN.md`.
- Relevant tools/skills/repositories: TotalRecall, Strata destination, local export providers, Fathom provider, Slack and GitHub activity imports, Context Packager, Research Analyst, SITREP Agent, Receipt Collector.
- Expected inputs: provider/export source, destination policy, deduplication mode, sync-state location, redaction policy, credential boundary, and retention target.
- Expected outputs: import plan, normalized artifacts, destination records, report JSON, audit log, duplicate/reconciliation status, and unresolved credential or retention boundary.
- Overlap: Research Analyst, Context Packager, SITREP Agent, Receipt Collector.
- Why not add now: Existing knowledge/context roles can inspect TotalRecall artifacts when assigned, and no dedicated chain skill or workflow contract was verified for routine delegation.
- Required authority boundaries: no live provider pull, API-key use, Strata writes, filesystem export, or cross-system learning ingestion without explicit scope and retention approval.
- Verification requirements: `./scripts/totalrecall config validate`, dry-run provider import, destination-specific contract harness, duplicate/idempotency proof, and secrets/keychain review.
- Risks/costs/token impact: broad ingestion could duplicate Research Analyst and Context Packager while increasing private-context retention risk.
- Recommendation: defer.
- Evidence still required: stable `kujo-skills` or `kujo-workflows` contract plus repeated workload showing existing knowledge roles need a specialized ingestion owner.

### Dependabot Security Coordinator

- Proposed role: Dependabot Security Coordinator.
- Problem or gap: `ward` can collect Dependabot security alerts, plan remediation, generate reports/dashboards, and prepare safe fix branches with read-only defaults.
- Repository-backed evidence: `../../ward/README.md`, `../../ward/SECURITY.md`, `../../ward/LAUNCH_READINESS.md`.
- Relevant tools/skills/repositories: Ward, GitHub Dependabot alerts, Dependency Scanner, Security Reviewer, Issue Hygiene Worker, Risk Officer, Release Verifier.
- Expected inputs: repository config, GitHub token boundary, alert query, planning policy, allowed fix mode, verification commands, and reporting target.
- Expected outputs: normalized alert report, remediation plan, dashboard/report artifacts, fix dry-run or explicit apply evidence, unresolved risk and token-exposure notes.
- Overlap: Dependency Scanner, Security Reviewer, Issue Hygiene Worker, Risk Officer, Release Verifier.
- Why not add now: Ward requires GitHub credentials for live collection, currently has no dedicated chain skill/workflow, and existing security/dependency agents can review its reports when explicitly assigned.
- Required authority boundaries: no token use, live alert collection, fix application, branch creation, PR creation, alert dismissal, or remote mutation without explicit approval and least-privilege credentials.
- Verification requirements: `ward doctor`, `ward collect --all` with approved credentials, `ward plan --unplanned`, `ward report --since 7d`, policy tests, and secret/process-list exposure review.
- Risks/costs/token impact: could blur dependency scanning, security review, issue hygiene, and release-risk ownership while adding credential-handling risk.
- Recommendation: defer.
- Evidence still required: stable chain skill/workflow and repeated Dependabot operations that cannot be handled by existing dependency/security roles.

### Mobile Agent Supervisor

- Proposed role: Mobile Agent Supervisor.
- Problem or gap: `leash` supervises local AI agents from a mobile control plane with policy-as-code risk classification, tmux/agent adapters, JWT auth, audit trails, and approval flows.
- Repository-backed evidence: `../../leash/README.md`, `../../leash/SECURITY.md`, `../../leash/docs/PRODUCTION_CHECKLIST.md`.
- Relevant tools/skills/repositories: Leash, Dispatch, Spec, Eval, Scout, Strata integration docs, Integration Engineer, Security Reviewer, Risk Officer, Receipt Collector.
- Expected inputs: supervised session list, policy file, device registration, auth configuration, adapter scope, allowed actions, and approval boundary.
- Expected outputs: approval/audit event record, policy decision, adapter event, security review notes, and unresolved device/runtime proof.
- Overlap: Integration Engineer, Security Reviewer, Risk Officer, Chief of Staff, Dispatch-oriented agents, Receipt Collector.
- Why not add now: Leash is v0.1.0 hardening with Android/device runtime limitations and no dedicated chain skill/workflow; current agents can review Leash as a product/tool repo when assigned.
- Required authority boundaries: no unattended approvals, remote input, biometric-sensitive action claims, production push, device registration, or live agent control without explicit human authorization.
- Verification requirements: daemon health/API smoke, policy tests, adapter tests, Android/device runtime validation where claims require it, audit trail review, and credential/token handling review.
- Risks/costs/token impact: could centralize human approval authority in an agent role and blur chain-of-command governance if activated prematurely.
- Recommendation: defer.
- Evidence still required: validated mobile/runtime proof, stable skill/workflow contract, and governance decision on whether this belongs as an agent role or remains an external control plane.

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
