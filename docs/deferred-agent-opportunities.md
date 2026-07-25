# Deferred Agent Opportunities

This record captures credible new-agent candidates discovered during periodic audits. It is intentionally conservative: do not scaffold or register these agents without separate human approval and repository-backed contracts.

## 2026-07-25 Audit

### Context Capsule Steward

- Proposed role: Context Capsule Steward.
- Problem or gap: Capsule can generate deterministic, offline project handoff packages with checksums, manifests, command detection, and validation.
- Repository-backed evidence: `../../benchmarks-capsule-v3/README.md`, `../../kujo-skills/SKILLS_INDEX.md`.
- Relevant tools/skills/repositories: Capsule, Scent, Scout, PackWrite, RunLedger, `kujo-benchmarks-capsule-workflows`.
- Expected inputs: source repo path, include/exclude policy, output path, stable-mode requirement, downstream consumer.
- Expected outputs: `capsule.json`, `capsule.md`, `manifest.json`, validation result, redaction-boundary note.
- Overlap: Context Packager, Research Analyst, QA Lead, Receipt Collector.
- Why not add now: Existing Context Packager and Research Analyst roles can own Capsule use without a new specialized agent. Capsule is a deterministic handoff artifact format, not a broad reasoning or ownership lane.
- Required authority boundaries: no secret assurance beyond Capsule's documented shallow filename/keyword redaction; no mutation outside declared output paths; no context sharing without redaction review.
- Verification requirements: `./bin/capsule make`, `inspect`, `validate`, and repository `scripts/run_checks.sh` when changing Capsule itself.
- Risks/costs/token impact: could duplicate Scout/Scent context workflows if invoked for every task; packages may include bulky previews when source boundaries are weak.
- Recommendation: reject as a new agent; add Capsule to existing Context Packager, Research Analyst, QA Lead, and Receipt Collector guidance.
- Evidence still required: repeated failures where existing context roles misuse or skip Capsule in a way a dedicated owner would prevent.

### Benchmark Operator

- Proposed role: Benchmark Operator.
- Problem or gap: Benchmark System provides portable execution and review prompts for AI Chat pane-profile benchmark runs and PDF-quality review outputs.
- Repository-backed evidence: `../../benchmarks-system/README.md`.
- Relevant tools/skills/repositories: Benchmark System, AI Chat, RunLedger, Eval, CaseFile, QA Lead, Product Strategist.
- Expected inputs: benchmark suite, saved AI Chat pane profile, execution prompt, review kit, output destination.
- Expected outputs: factual review packet, quality/token/cost/time summaries, dream-team review, PDF-ready artifact, unresolved telemetry boundaries.
- Overlap: QA Lead, Product Strategist, General Commander, Receipt Collector.
- Why not add now: The repository is currently a prompt/documentation kit, not a standalone executable CLI or stable agent contract. QA Lead can own benchmark evidence requirements and Product Strategist can consume comparative outcomes.
- Required authority boundaries: no invented model, token, cost, or quality claims; visible telemetry only; no broad approval authority from benchmark scores alone.
- Verification requirements: AI Chat run evidence, generated review artifacts, RunLedger or CaseFile receipt where available, exact telemetry-unavailable notes.
- Risks/costs/token impact: benchmark reviews can be expensive and long-running; a new agent could normalize benchmark theater without executable proof.
- Recommendation: defer.
- Evidence still required: stable executable contract or repeated benchmark workload volume that existing QA/product roles cannot manage.

### Campaign Surface Producer

- Proposed role: Campaign Surface Producer.
- Problem or gap: Kujo Hyperframes is a source-grounded static campaign and video-composition surface with strict claim-map constraints.
- Repository-backed evidence: `../../kujo-hyperframes/README.md`.
- Relevant tools/skills/repositories: Kujo Hyperframes, Archivist dossier, Lens, SiteKit, Documentation Writer, Frontend Developer, Visual QA Agent, Product Strategist.
- Expected inputs: source dossier, claim map, frame or composition brief, browser/video target, approval boundary.
- Expected outputs: static page or rendered composition update, claim-map validation, browser/video proof, source-grounded copy handoff.
- Overlap: Documentation Writer, Frontend Developer, Visual QA Agent, Product Strategist.
- Why not add now: Existing frontend, visual QA, documentation, and product roles naturally cover the work with stricter separation between copy, implementation, and proof.
- Required authority boundaries: no unsupported launch, adoption, enterprise, benchmark, sandbox, AI-vision, or public-registry claims.
- Verification requirements: source claim map, local browser proof for `index.html`, render command evidence for video compositions when changed.
- Risks/costs/token impact: creating a campaign-only agent would add narrow routing overhead and may blur product strategy with implementation.
- Recommendation: reject.
- Evidence still required: none; revisit only if multiple campaign surfaces become recurring production work with independent release gates.

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
