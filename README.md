# Kujo Agents

Reusable agent packages, including universal project agents and KUJO-specific variants.

This repository currently contains:

- `archivist/` - universal source-bound project researcher and handoff dossier builder for any repository, product, workflow, research, documentation, or implementation project.
- `kujo-archivist/` - KUJO-specific Archivist variant customized for KUJO repos, tools, skills, workflows, docs, examples, and related local sources.
- `agents/` - KUJO agent chain of command, role contracts, tool-to-agent map, and reusable specialist agents for strategy, planning, execution, verification, knowledge, and routine worker tasks.

## Purpose

`kujo-agents` is a home for agent definitions, reusable agent skills, and reference material that help future agents work with clear scope, evidence rules, and handoff behavior.

Agents in this repository should be:

- Source-grounded.
- Reusable across future project updates.
- Clear about goals, non-goals, evidence requirements, and output contracts.
- Small enough to inspect and adapt.

## Structure

Each agent package should keep its own instructions and references together:

```text
agent-name/
  AGENT.md
  SKILL.md
  references/
```

The command-chain agents live under `agents/` and follow the same package convention:

```text
agents/
  README.md
  00-chain-of-command.md
  00-tool-agent-map.md
  agent-name/
    AGENT.md
    SKILL.md
```

Existing Archivist packages remain at the repository root because they predate the command-chain folder and are reusable outside the KUJO-specific hierarchy.

## License

MIT. See `LICENSE`.
