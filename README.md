# Kujo Agents

Reusable agent packages, including universal project agents and KUJO-specific variants.

This repository currently contains:

- `archivist/` - universal source-bound project researcher and handoff dossier builder for any repository, product, workflow, research, documentation, or implementation project.
- `kujo-archivist/` - KUJO-specific Archivist variant customized for KUJO repos, tools, skills, workflows, docs, examples, and related local sources.
- `chain-of-command/` - coordinated KUJO agent chain of command, role contracts, tool-to-agent map, campaign templates, benchmarks, and reusable specialist agents for strategy, planning, execution, verification, knowledge, and routine worker tasks.
- `zelus/` - Kujo-native offensive-security research team and bug-bounty agent roster.

## Zelus

`zelus/` is a separate Kujo-native offensive security research team for
authorized WordPress bug bounty and vendor-approved research. It showcases
Kujo contracts, policy gates, evidence receipts, Workcell fixtures, agent
roster, skills, workflows, and deterministic tests without adding a Python
runtime.

```bash
export KUJO_BIN=/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/debug/kujo
cd zelus
$KUJO_BIN run zelus.kujo -- doctor
$KUJO_BIN run zelus.kujo -- campaign reference examples/sample-wordpress-campaign --out /tmp/zelus-reference
$KUJO_BIN run tests/zelus_contract_tests.kujo
```

See [zelus/README.md](zelus/README.md) for the package layout and integration
boundaries.

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

The command-chain agents live under `chain-of-command/` and follow the same package convention:

```text
chain-of-command/
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
