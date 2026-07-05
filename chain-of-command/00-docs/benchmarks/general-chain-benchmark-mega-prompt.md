# General Chain Benchmark Mega Prompt

Use this benchmark to test whether the KUJO agent chain can route a realistic project from ambiguous intent through planning, implementation, verification, documentation, evidence collection, and self-improvement.

This prompt is intentionally project-agnostic and local-first. It can run against a fresh temporary repo, a sandbox folder, or a deliberately small existing test repo.

## Benchmark Campaign

Paste the content below into `chain-of-command/00-docs/templates/general-campaign-wrapper.md` under `Project Payload`, then fill campaign metadata for the target workspace. Make sure the runner can also read the Commander context files listed in that wrapper.

````markdown
# Benchmark Project: ProofPack

Build a small local-first developer tool called `proofpack`.

`proofpack` turns a local project folder into a reviewable evidence packet for a human reviewer. It should help answer: "What changed, what evidence exists, and what should the next reviewer inspect?"

This is a benchmark of the KUJO agent chain. The goal is not just to build a tiny tool; the goal is to prove that the agents can collaborate through strategy, planning, implementation, verification, documentation, and retrospective improvement.

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

## Required User Experience

A reviewer should be able to run one command and receive:

- A terminal summary.
- A Markdown evidence packet on disk.
- Clear next steps.

Example shape, not mandatory exact syntax:

```bash
proofpack ./some-project --out ./proofpack-report.md
```

## Constraints

- Prefer the simplest implementation that fits the target repo language and tooling.
- No network access is required.
- No secrets should be printed.
- Do not mutate the target project except for writing the requested report artifact.
- Do not commit, push, publish, deploy, or install global tools.
- Keep generated artifacts easy to delete.
- If the target repo already has conventions, follow them.
- If the environment cannot support a runnable implementation, produce the best spec, design, and test plan instead.

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
- `Documentation Writer`: update or create usage docs.
- `Receipt Collector` or `SITREP Agent`: create final evidence/status summary.
- `Risk Officer` or `Security Reviewer`: inspect risks if secrets, path handling, git commands, or host effects are involved.

If any role is skipped, the General must explain why.

## Acceptance Criteria

- A human can identify what each agent was asked to do.
- Handoffs are explicit and scoped.
- Worker agents receive only exact commands.
- The implementation, if attempted, has at least one verification command.
- The final report includes files changed, commands run, pass/fail status, and remaining gaps.
- Security/path/secret risks are considered.
- The final retrospective proposes improvements to the agent definitions if weaknesses are found.

## Stretch Criteria

- Add a JSON output mode.
- Add a dry-run mode.
- Add a small fixture or example folder.
- Add a test that verifies the Markdown report contains expected sections.
- Use an existing KUJO tool where appropriate, but do not force a tool if a normal repo script is enough.

## Final Benchmark Output Required

Return:

1. Agent lane transcript summary.
2. Deliverables produced.
3. Commands run and results.
4. Evidence artifacts.
5. Acceptance criteria result.
6. Chain performance score using the KUJO Agent Benchmark Scorecard.
7. Recommended edits to `chain-of-command/` for the next run.
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
