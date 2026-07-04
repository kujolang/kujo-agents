# Source Audit Rules

## Core Rule

Do not convert a claim into a fact unless the inspected source supports it. If support is weak, partial, future-facing, or missing, mark the claim as inferred, planned, or unknown.

## Evidence Categories

- Confirmed: Directly stated or implemented in inspected current sources.
- Inferred: Reasonable interpretation from multiple confirmed observations, but not explicitly stated.
- Planned: Roadmap, TODO, proposal, issue note, planning document, or future-oriented comment.
- Unknown: Not found, conflicting, ambiguous, stale, inaccessible, or outside the inspection scope.

## README Files

README files are high-signal project summaries.

Use README files for:

- Project purpose.
- Installation and usage claims.
- Supported commands.
- Stated audience.
- Current positioning.

Treat README claims as confirmed only for what the README states. Verify behavior against source, tests, or CLI output when accuracy matters.

## Docs

Docs can support conceptual, user-facing, and operational claims.

Use docs for:

- Concepts and architecture.
- Workflow descriptions.
- User guides.
- Integration descriptions.
- Public terminology.

Mark docs as planned or uncertain when they contain roadmap language, TODOs, draft labels, outdated version notes, or contradictions with current source code.

## Examples

Examples show intended usage patterns.

Use examples for:

- Common workflows.
- Input and output formats.
- Supported syntax or command usage.
- Integration patterns.

Do not infer full product scope from one example. Phrase broad claims as inferred unless supported elsewhere.

## Tests

Tests are strong evidence for expected behavior.

Use tests for:

- Supported edge cases.
- Command behavior.
- File format contracts.
- Regression-sensitive behavior.

Tests may describe expected behavior better than docs. If tests and docs conflict, report the conflict.

## Source Code

Source code is strong evidence for implemented behavior.

Use source code for:

- Actual commands, APIs, parsers, runners, integrations, and outputs.
- Default values.
- Error handling.
- File paths and artifact formats.

Do not overstate internal implementation details as public product promises unless public docs or CLI help also support them.

## CLI Help Output

CLI help output is strong evidence for current command surface when generated from the local executable.

Use CLI help output for:

- Command names.
- Flags.
- Argument expectations.
- Short command descriptions.

Record the exact command used. If the command fails, record the failure as an audit note rather than inventing behavior.

## Package Metadata

Package metadata supports project identity and distribution facts.

Use metadata for:

- Package name.
- Version.
- Entry points.
- Dependencies.
- Scripts.
- Declared license or repository fields.

Do not treat dependency presence as proof of runtime behavior without supporting code or docs.

## Comments

Comments are weak-to-medium evidence.

Use comments for:

- Implementation intent.
- Warnings.
- Local context.

Mark comments as planned when they describe TODOs, future work, or intended changes. Do not treat comments as shipped behavior if code contradicts them.

## Scripts

Scripts support operational workflows.

Use scripts for:

- Build, test, release, validation, migration, and local automation behavior.
- Required environment variables.
- Generated artifacts.

If scripts are helper-only or obsolete, mark claims cautiously and cite the script path.

## Workflows

Workflow files support automation and process claims.

Use workflows for:

- CI checks.
- Release gates.
- Dogfood runs.
- Cross-repository automation.
- Agent or task orchestration.

Separate workflow intent from successful execution unless logs or artifacts confirm runs.

## Local Skills

Local skills are evidence for agent workflow expectations.

Use skills for:

- Trigger conditions.
- Required procedures.
- Validation rules.
- Repo-specific agent behavior.

Do not treat a skill as proof that the underlying repository supports a feature unless repository sources corroborate it.

## Issue Notes Or Planning Docs

Issue notes, planning docs, roadmaps, and backlog files are planning evidence.

Use them for:

- Proposed features.
- Known gaps.
- Future sequencing.
- Design intent.

Mark these claims as planned unless current source, docs, examples, or tests confirm implementation.

## Marking Uncertain Claims

Use explicit labels:

- Confirmed: "The repository implements..."
- Inferred: "The sources suggest..."
- Planned: "The planning notes propose..."
- Unknown: "The inspected sources do not establish..."

When uncertainty remains, keep the uncertainty in the final dossier.

