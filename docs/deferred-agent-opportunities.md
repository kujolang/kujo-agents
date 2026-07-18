# Deferred Agent Opportunities

This record captures credible new-agent candidates discovered during periodic audits. It is intentionally conservative: do not scaffold or register these agents without separate human approval and repository-backed contracts.

## 2026-07-18 Audit

### Workflow Orchestrator

- Proposed role: Workflow Orchestrator.
- Problem or gap: Relay, Dispatch, PackWrite, RunLedger, ChangeBucket, Eval, and Workcell now form a larger bounded mission lifecycle than any single worker or implementation role owns.
- Repository-backed evidence: `../../relay/README.md`, `../../kujo-workflows/README.md`, `../../dispatch/README.md`, `../../workcell/README.md`.
- Relevant tools/skills/repositories: Relay, Dispatch, PackWrite, RunLedger, ChangeBucket, Eval, Workcell, `kujo-relay-workflows`, `kujo-dispatch-workflows`.
- Expected inputs: mission spec, repo scope, approval policy, budget, verification gates, handoff target.
- Expected outputs: lifecycle plan, run state references, pause/resume/cancel evidence, handoff receipt, unresolved authority decisions.
- Overlap: General Commander, Chief of Staff, Integration Engineer, Triage Agent, Receipt Collector.
- Why not add now: Current roles can consume Relay evidence without needing a separate owner. Relay remains local alpha with live-provider and enterprise-tenancy boundaries.
- Required authority boundaries: no independent approval to deploy, publish, run destructive actions, or bypass human approval.
- Verification requirements: Relay contract tests, workflow catalog validation, RunLedger receipt evidence, ChangeBucket/Eval artifact verification.
- Risks/costs/token impact: potential overlap with General Commander and Chief of Staff; high context load if it tries to own mission strategy.
- Recommendation: defer.
- Evidence still required: repeated multi-agent runs where existing roles fail specifically because lifecycle orchestration lacks a dedicated owner.

### Execution Sandbox Operator

- Proposed role: Execution Sandbox Operator.
- Problem or gap: Workcell adds a bounded local Docker/Podman execution package that could centralize sandbox setup, run evidence, cleanup, and tamper checks.
- Repository-backed evidence: `../../workcell/README.md`, `../../kujo-workflows/README.md`.
- Relevant tools/skills/repositories: Workcell, Eval, CaseFile, RunLedger, `kujo-workcell-workflows`.
- Expected inputs: workcell definition, source repo, declared command, artifact policy, network/secret policy.
- Expected outputs: run receipt, logs, patch/artifact exports, verification result, cleanup status.
- Overlap: Tooling Developer, Routine Worker, Test Runner, QA Lead, Release Verifier, Security Reviewer.
- Why not add now: Existing worker/test/QA roles can run Workcell when explicitly assigned; Workcell's host-trust boundary requires careful operator judgment.
- Required authority boundaries: no unsupervised Docker/Podman host changes, network policy changes, secret injection, or cleanup outside Workcell-owned resources.
- Verification requirements: `workcell validate`, `workcell inspect`, `workcell run`, `workcell verify`, release report evidence when available.
- Risks/costs/token impact: potential overuse for simple tests; Docker environment failures could create noisy triage loops.
- Recommendation: consider later.
- Evidence still required: recurring tasks where safe bounded execution is needed often enough that existing worker roles duplicate setup or skip cleanup.

### Decision Hearing Facilitator

- Proposed role: Decision Hearing Facilitator.
- Problem or gap: Tribunal can produce adversarial decision packets for consequential choices, but final authority and follow-through still belong to humans or strategic/release/security roles.
- Repository-backed evidence: `../../tribunal/README.md`, `../../kujo-workflows/README.md`.
- Relevant tools/skills/repositories: Tribunal, ShipCheck, Fence, RunLedger, CaseFile, `kujo-tribunal-workflows`.
- Expected inputs: consequential proposal, decision context, evidence packet, risk constraints, authority boundary.
- Expected outputs: hearing packet, fatal-flaw result, advisory ruling, dissent/open risks, human decision prompt.
- Overlap: Risk Officer, Product Strategist, Systems Architect, General Commander, Release Verifier.
- Why not add now: Tribunal remains advisory; existing strategic and risk roles can request or interpret packets without a dedicated agent.
- Required authority boundaries: cannot approve release, security, legal, financial, production, or customer-impact decisions.
- Verification requirements: Tribunal local gate evidence, unsigned/signed status, artifact integrity, explicit authority owner.
- Risks/costs/token impact: could formalize too many routine decisions and slow the chain.
- Recommendation: defer.
- Evidence still required: repeated high-impact decisions where existing roles miss adversarial review and a Tribunal packet would materially improve outcomes.

### Design System Steward

- Proposed role: Design System Steward.
- Problem or gap: SiteKit creates a Kujo design-system contract that could benefit from dedicated ownership across frontend, docs, snapshots, accessibility, and consuming-site validation.
- Repository-backed evidence: `../../site-kit/README.md`.
- Relevant tools/skills/repositories: SiteKit, Lens, SSG, CMS Experience, `kujo-sitekit-workflows`, `kujo-lens-workflows`.
- Expected inputs: component contract, consuming layout, token/theme change, docs requirement.
- Expected outputs: build/lint/validate/snapshot evidence, component guidance, browser/accessibility proof handoff.
- Overlap: Frontend Developer, Visual QA Agent, Documentation Writer, Product Strategist.
- Why not add now: SiteKit remains an internal private package and current roles can handle normal usage.
- Required authority boundaries: no unilateral product/design-system policy changes; consuming apps still own layout decisions.
- Verification requirements: SiteKit build/lint/validate/snapshot plus Lens proof for representative consuming layouts.
- Risks/costs/token impact: risk of design-system centralization before adoption volume justifies it.
- Recommendation: consider later.
- Evidence still required: multiple active consuming projects with recurring component drift or duplicated design-system review.

### Steganography Demo Specialist

- Proposed role: Steganography Demo Specialist.
- Problem or gap: StegoCipher Kujo is narrow and educational; it does not create a broad ecosystem ownership gap.
- Repository-backed evidence: `../../stego-cipher-kujo/README.md`.
- Relevant tools/skills/repositories: StegoCipher Kujo, Security Reviewer.
- Expected inputs: demo scenario or security-review request.
- Expected outputs: bounded demo artifact or review note.
- Overlap: Security Reviewer, Research Analyst, Documentation Writer.
- Why not add now: The repository is explicitly not cryptographic encryption and has no recurring agent-chain ownership need.
- Required authority boundaries: never handle real secrecy, credentials, or cryptographic assurance.
- Verification requirements: repo smoke suite and explicit non-crypto disclaimer.
- Risks/costs/token impact: unnecessary agent proliferation for a single-purpose demo.
- Recommendation: reject.
- Evidence still required: none; revisit only if StegoCipher becomes part of a larger supported education/demo workflow.
