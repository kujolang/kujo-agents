# General Chain Benchmark Mega Prompt

Use this benchmark to test whether the KUJO agent chain can route a realistic project from ambiguous intent through planning, implementation, verification, documentation, evidence collection, and self-improvement.

This prompt is intentionally local-first and comparison-friendly. It can run against a fresh temporary repo, a sandbox folder, or a deliberately small existing test repo. It is stricter than a normal campaign because it is meant to dogfood the KUJO ecosystem.

## Benchmark Campaign

Paste the content below into `chain-of-command/00-docs/templates/general-campaign-wrapper.md` under `Project Payload`, then fill campaign metadata for the target workspace. Make sure the runner can also read the Commander context files listed in that wrapper.

````markdown
# Benchmark Project: ProofPack

Build a small local-first developer tool called `proofpack`.

`proofpack` turns a local project folder into a reviewable evidence packet for a human reviewer. It should help answer: "What changed, what evidence exists, and what should the next reviewer inspect?"

This is a benchmark of the KUJO agent chain. The goal is not just to build a tiny tool; the goal is to prove that the agents can collaborate through strategy, planning, implementation, verification, documentation, and retrospective improvement.

## Benchmark Run Workspace

Before implementation, create a unique local run workspace:

```text
.runs/proofpack-YYYYMMDD-HHMMSS/
```

All generated specs, receipts, reports, context packs, eval outputs, dispatch traces, fallback artifacts, reviews, scorecards, and handoffs must go in that workspace unless a KUJO tool has its own required local output convention.

Do not overwrite artifacts from earlier benchmark runs. This run must be stored alongside previous runs so a human can compare quality over time.

## Product Goal

Create a minimal but useful local CLI or script that:

- Scans a target folder.
- Produces a concise Markdown report.
- Includes a file inventory summary.
- Includes git status or clearly reports when the folder is not a git repo.
- Includes a section for commands run and evidence artifacts.
- Includes a section for risks, unknowns, and next reviewer actions.
- Writes output to a deterministic local artifact path.

The tool must be small enough to understand in one review session.

## Implementation Language Requirement

ProofPack is KUJO ecosystem tooling. Implement ProofPack in the KUJO programming language.

- Inspect KUJO syntax, examples, runtime commands, and local docs before writing implementation code.
- Do not implement ProofPack in Python, JavaScript, shell, Rust, Go, or another language unless the user explicitly changes this benchmark.
- If KUJO runtime support is unavailable or KUJO syntax cannot be confirmed, stop the implementation lane and produce a KUJO-oriented spec, design, command contract, and verification plan instead of switching languages.
- Tests and evals should use KUJO-native tooling where available. Fallback tests are allowed only when the fallback is recorded in the run workspace.

## Required User Experience

A reviewer should be able to run one command and receive:

- A terminal summary.
- A Markdown evidence packet on disk.
- Clear next steps.

Example shape, not mandatory exact syntax:

```bash
kujo run tools/proofpack.kujo -- ./some-project --out ./proofpack-report.md
```

## Constraints

- Prefer the simplest KUJO implementation that fits the target repo and confirmed KUJO runtime behavior.
- No network access is required.
- No secrets should be printed.
- Do not mutate the target project except for writing the requested report artifact.
- Do not commit, push, publish, deploy, or install global tools.
- Campaign constraints override repository instructions. If a repo-level instruction says to commit or push but this benchmark says not to, do not commit or push.
- Keep generated artifacts easy to delete.
- If the target repo already has conventions, follow them.
- If the environment cannot support a runnable KUJO implementation, produce the best KUJO spec, design, and test plan instead.

## KUJO Ecosystem Dogfood Requirements

This benchmark must dogfood KUJO tooling wherever it reasonably fits. Do not merely simulate the chain in prose.

Use these tools unless unavailable or clearly inappropriate. If skipped, record the exact reason and fallback evidence in `.runs/proofpack-YYYYMMDD-HHMMSS/`.

1. **RunLedger**
   - Start a RunLedger run before implementation.
   - Record the run id in all handoffs.
   - Record notes for major findings, fixes, skips, and blockers.
   - Record usage/cost only when actual telemetry is available; do not invent token counts.
   - Finish the run with pass/partial/fail and a verdict.
   - Generate or save a RunLedger report artifact.

2. **Spec**
   - Create a ProofPack task contract with scope, non-goals, acceptance criteria, approval gates, and verification requirements.
   - Validate or render it if local Spec commands are available.
   - Store the spec source and rendered/fallback artifact in the run workspace.

3. **Scent or Scout**
   - Produce a local context or source map for the target repo before planning.
   - Include inspected files, repo language/tooling, KUJO runtime availability, and unknowns.

4. **Dispatch**
   - Use Dispatch or a Dispatch-style local trace to record agent lane assignments, handoffs, stop conditions, and results.
   - If Dispatch CLI is unavailable, create a structured dispatch trace Markdown or JSON artifact.

5. **Eval**
   - Define and run deterministic checks for ProofPack behavior:
     - report file exists
     - required Markdown sections exist
     - non-git folder reports non-git clearly
     - dry-run does not write
     - no secret file contents are printed
     - implementation is KUJO or implementation lane is explicitly blocked with a KUJO fallback spec
   - Store Eval output or fallback test output in the run workspace.

6. **CaseFile**
   - If any command, test, KUJO runtime check, or security review fails, capture a CaseFile or fallback failure bundle with command, exit code, key output, artifact paths, and next owner.

7. **PatchBrief or ChangeBucket**
   - Summarize changed files and diff footprint before code review.
   - Store the summary as an evidence artifact.

8. **Security, Fence, ShipCheck, or Concord**
   - Use focused local checks where available:
     - Fence or Security Reviewer for path and host-effect boundaries.
     - ShipCheck or release-style gate for readiness if runnable.
     - Concord for docs/tooling drift if docs are changed.
   - If unavailable, the verification agent must provide a manual equivalent and mark it as fallback evidence.

9. **Strata Memory or Local Memory Fallback**
   - If Strata is available, consolidate durable memories at the end:
     - final state
     - evidence artifacts
     - failures caught
     - reusable lessons
     - chain improvements
   - Test retrieval by exact run id, concept query, and artifact path.
   - If Strata is unavailable, create a local memory fallback note in the run workspace.

## Required Agent Chain Exercise

The General Commander must route work through the chain:

- `Research Analyst` or existing Archivist: inspect the target workspace and identify available language/tooling.
- `Product Strategist`: frame the user value and non-goals.
- `Systems Architect`: choose the smallest architecture and boundaries.
- `Planner` and `Spec Writer`: define milestones, acceptance criteria, and evidence plan.
- One execution agent: implement the tool or create the project artifact.
- `QA Lead`: define tests and evidence.
- `Test Runner` or `Routine Worker`: run exact assigned commands only.
- `Code Reviewer`: review the result.
- `Triage Agent`: classify any flagged wrong output, stopped workflow state, or human-review decision before work resumes.
- `Documentation Writer`: update or create usage docs.
- `Receipt Collector` or `SITREP Agent`: create final evidence/status summary.
- `Risk Officer` or `Security Reviewer`: inspect risks if secrets, path handling, git commands, or host effects are involved.

If any role is skipped, the General must explain why.

General Commander must not only assign roles. General Commander must also ensure each lane produces a durable artifact or receipt.

Every lane handoff must include:

- RunLedger run id or fallback run id
- Assigned agent role
- KUJO tool used or skipped
- Scope
- Inputs inspected
- Commands run
- Artifact paths
- Pass/fail/blocked
- Handoff target
- Stop condition

## Acceptance Criteria

- A human can identify what each agent was asked to do.
- Handoffs are explicit and scoped.
- Worker agents receive only exact commands.
- The implementation is in KUJO, or the implementation lane is explicitly blocked with a KUJO fallback spec and evidence.
- The implementation, if attempted, has at least one deterministic verification command.
- The final report includes files changed, commands run, pass/fail status, and remaining gaps.
- Security/path/secret risks are considered.
- KUJO tool usage or skip reasoning is documented for each required dogfood tool.
- Run artifacts are stored under a unique `.runs/proofpack-YYYYMMDD-HHMMSS/` workspace.
- The final retrospective proposes improvements to the agent definitions if weaknesses are found.

## Stretch Criteria

- Add a JSON output mode.
- Add a dry-run mode.
- Add a small fixture or example folder.
- Add a test that verifies the Markdown report contains expected sections.
- Add a comparison note against the previous benchmark run, if previous run artifacts are available.
- Add a reusable KUJO tool registry entry for ProofPack if the implementation is accepted.

## Metrics And Telemetry Requirements

Track and report:

- RunLedger run id or fallback run id.
- Active goal id if available.
- Token usage if exposed by platform telemetry.
- Manually observed tool calls.
- Subagents or role lanes spawned.
- Handoffs assigned and completed.
- Commands run.
- Tests/checks run.
- Files changed.
- Artifacts created.
- Failures found.
- Fixes applied.
- Final verification status.

Do not invent token usage. If token telemetry is unavailable, say so and record visible proxy metrics.

## Final Benchmark Output Required

Return:

1. Agent lane transcript summary.
2. Deliverables produced.
3. Commands run and results.
4. Evidence artifacts.
5. Acceptance criteria result.
6. Chain performance score using the KUJO Agent Benchmark Scorecard.
7. Recommended edits to `chain-of-command/` for the next run.
8. KUJO tool usage matrix:
   - tool
   - used/skipped
   - command or artifact
   - result
   - fallback if skipped
9. RunLedger receipt or fallback run receipt:
   - run id
   - status
   - verdict
   - report path
10. Metrics:
   - agents used
   - handoffs
   - commands
   - tests
   - artifacts
   - token usage if available
11. Comparison note:
   - previous run inspected, if any
   - behavior improved
   - behavior regressed
   - score delta, if available
````

## Why This Benchmark Works

This benchmark exercises:

- Ambiguous product framing.
- Repo discovery.
- Architecture choice.
- Bounded implementation.
- Worker command discipline.
- Test planning.
- Security/path review.
- Documentation.
- Evidence packaging.
- Retrospective self-improvement.

It is small enough to repeat, but broad enough to expose weak handoffs.
