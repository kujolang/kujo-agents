# Kujo Agents

Reusable custom agent packages for the KUJO programming language and tooling ecosystem.

This repository currently contains:

- `archivist/` - source-bound ecosystem researcher and handoff dossier builder for KUJO repos, tools, skills, workflows, docs, examples, and related local sources.

## Purpose

`kujo-agents` is a home for agent definitions, reusable agent skills, and reference material that help future agents work inside the KUJO ecosystem with clear scope, evidence rules, and handoff behavior.

Agents in this repository should be:

- Source-grounded.
- Reusable across future KUJO updates.
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

Future command-chain, role hierarchy, or routing structure can be added here as the agent set grows.

## License

MIT. See `LICENSE`.

