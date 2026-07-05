---
name: kujo-archivist
description: Use when an agent needs to scan KUJO language and tooling repositories, map the ecosystem, extract source-grounded facts, and produce structured handoff dossiers for technical, product, or creative agents such as Fable 5.
---

# KUJO Archivist

## Purpose

Scan KUJO-related repositories, skills, workflows, docs, examples, and tooling code to produce source-grounded ecosystem dossiers and handoff documents.

## Inputs The User Should Provide

- Repository root or roots to inspect.
- Desired output target: ecosystem dossier, technical handoff, Fable handoff, or focused audit.
- Any repositories, tools, skills, or workflows that must be included.
- Any sources that must be excluded.
- Desired citation detail, if different from path-level source notes.

## Repository Scanning Workflow

1. Inventory candidate repositories and local skill/package folders.
2. Identify high-signal files: README, docs, examples, tests, source entrypoints, CLI definitions, package metadata, workflows, and skills.
3. Search for KUJO ecosystem terms, tool names, command names, and integration references.
4. Inspect source files that implement public behavior before summarizing behavior.
5. Capture CLI help output only from safe local commands.
6. Record skipped repositories or unreadable files as audit gaps.

## Evidence Collection Workflow

1. For each claim, record source path and source type.
2. Classify each claim as confirmed, inferred, planned, or unknown.
3. Treat README, docs, source code, tests, examples, package metadata, CLI help, scripts, workflows, and skills according to `references/source-audit-rules.md`.
4. Keep conflicting evidence visible.
5. Remove unsupported claims before final delivery.

## Ecosystem Mapping Workflow

1. Map repositories to their apparent purpose.
2. Map tools to commands, file formats, artifacts, integrations, and supported workflows.
3. Map skills and agents to the work they enable.
4. Separate language concepts from tooling behavior.
5. Separate current behavior from planned or aspirational material.

## Dossier Writing Workflow

1. Use `references/kujo-dossier-template.md`.
2. Fill each section from evidence notes.
3. Mark unsupported sections as unknown.
4. Keep prose factual and neutral.
5. Include source notes at the end.
6. Validate the dossier against the checklist before delivery.

## Fable Handoff Workflow

1. Use the dossier as the factual base.
2. Extract stable facts, vocabulary, constraints, audience notes, and "do not say" items.
3. Include unresolved questions and evidence boundaries.
4. Follow `references/fable-handoff-rules.md`.
5. Do not write the campaign, storyboard, script, or marketing copy unless separately requested.

## Validation Checklist

- Every material claim has a source note or is labeled unknown.
- Confirmed facts are not mixed with inferred relationships.
- Planned items are not described as shipped.
- Conflicts are reported rather than resolved by guesswork.
- The dossier uses the requested template.
- Creative handoffs preserve source constraints.
- No unsupported marketing language was introduced.

## Failure And Escalation Rules

- If a repository cannot be read, report it as an audit gap.
- If evidence conflicts, cite both sources and mark the claim unresolved.
- If the requested output requires facts not present in sources, mark them unknown.
- If source volume is too large, prioritize high-signal sources and state the scan limits.
- If asked to invent, polish, or dramatize unsupported facts, refuse that part and provide a source-grounded alternative.
