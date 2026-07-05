# Project Dossier Template

## Executive Summary

Brief factual summary of the inspected project.

Evidence status: confirmed / inferred / planned / unknown.

## One-Sentence Description

A single source-grounded sentence describing the project.

Evidence status: confirmed / inferred / planned / unknown.

## What The Project Is

Describe the project based on inspected sources.

Include:

- Project identity.
- Main product, library, service, dataset, content system, research effort, workflow, or artifact type.
- Runtime, platform, framework, or operational context when applicable.
- Boundaries between product behavior, implementation behavior, docs, examples, and planning material.

## Why The Project Exists

Summarize source-supported motivations, problems, goals, or design constraints.

If motivation is not explicit, mark it unknown or inferred.

## Core Concepts

List source-supported project concepts, domain terms, data models, syntax, runtime behavior, workflows, or user-facing ideas.

For each concept:

- Name.
- Description.
- Source note.
- Evidence status.

## Architecture And Implementation Map

Map implemented components and their supported behavior.

For each component:

- Component name.
- Location.
- Purpose.
- Main APIs, commands, entrypoints, routes, jobs, screens, or documents.
- Inputs and outputs.
- Dependencies or integration points.
- Evidence status.

## Tooling And Workflow Map

Map tools, scripts, automation, operational processes, and workflow packs.

For each workflow or tool:

- Name.
- Location.
- Purpose.
- Inputs.
- Outputs or generated artifacts.
- Required commands, services, or dependencies.
- Evidence status.

## Interfaces, Commands, And Artifacts

Map externally meaningful surfaces.

Include when present:

- CLI commands and flags.
- Public APIs, routes, events, schemas, or configuration files.
- UI surfaces.
- File formats.
- Generated artifacts.
- Data stores.
- Integration boundaries.

## Repository And Source Map

List inspected repositories, packages, folders, documents, and artifacts.

For each source area:

- Path.
- Apparent purpose.
- High-signal files inspected.
- Important commands, APIs, concepts, or artifacts.
- Open questions.
- Evidence status.

## Positioning Or Public Claims

Record only source-supported positioning language.

Include:

- Phrases used by the project itself.
- Where the phrase appears.
- Whether it is current, historical, planned, or uncertain.

Avoid rewriting positioning as marketing copy.

## Audience, Users, Or Stakeholders

Describe source-supported target users, audiences, stakeholders, or use cases.

Separate:

- Explicit audience claims.
- Inferred users based on examples, docs, workflows, or implementation.
- Unknown audience gaps.

## What Is Confirmed

Bullet list of facts directly supported by inspected sources.

Each bullet must include a source note.

## What Is Inferred

Bullet list of relationships or interpretations that are plausible but not directly stated.

Each bullet must include the evidence behind the inference.

## What Is Planned

Bullet list of roadmap, TODO, proposal, issue note, comment, or future-facing items.

Each bullet must identify the planning source.

## What Is Unknown

Bullet list of gaps, conflicts, missing sources, unclear ownership, or unverified claims.

## What To Avoid Saying

List claims that should not be made because they are unsupported, misleading, outdated, too broad, or contradicted by inspected sources.

## Glossary

Define source-supported project terms.

For each term:

- Term.
- Definition.
- Source note.
- Evidence status.

## Source Notes

Use this format:

- `[S1]` Path: `path/to/source`
  Type: README / docs / example / test / source / CLI output / metadata / script / workflow / skill / planning note / design note / research note / data artifact.
  Detail: section, command, symbol, route, schema, line reference, or artifact name when available.
  Supports: short description of the supported claim.
  Evidence status: confirmed / inferred / planned / unknown.
