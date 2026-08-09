# Kujo Agents

Reusable role contracts for the KUJO agent chain of command.

The public repository is intentionally focused on one package:

- [`chain-of-command/`](chain-of-command/) — coordinated roles for strategy, planning, execution, verification, knowledge, and bounded worker tasks.

## Start Here

Read these files before running or adapting the chain:

1. [`chain-of-command/README.md`](chain-of-command/README.md) — role selection, handoffs, model tiers, and campaign guidance.
2. [`chain-of-command/00-chain-of-command.md`](chain-of-command/00-chain-of-command.md) — authority layers and escalation paths.
3. [`chain-of-command/00-tool-agent-map.md`](chain-of-command/00-tool-agent-map.md) — supported tool-to-role relationships.
4. [`chain-of-command/general-commander/AGENT.md`](chain-of-command/general-commander/AGENT.md) — top-level mission routing contract.

For a reusable campaign intake packet, use
[`chain-of-command/00-docs/templates/general-campaign-wrapper.md`](chain-of-command/00-docs/templates/general-campaign-wrapper.md).

## Repository Layout

```text
chain-of-command/
  README.md
  00-chain-of-command.md
  00-tool-agent-map.md
  00-ecosystem-inventory.md
  00-docs/
  agent-name/
    AGENT.md
    SKILL.md
```

Each agent package keeps its role contract and operating skill together. The
templates are guidance and review material; they do not provide sandboxing,
authorization, or policy enforcement by themselves.

## Validation

```bash
find chain-of-command -mindepth 2 -maxdepth 2 -type f \
  \( -name AGENT.md -o -name SKILL.md \) | sort

for dir in chain-of-command/*/; do
  case "$dir" in
    chain-of-command/00-docs/) continue ;;
  esac
  test -f "${dir}AGENT.md" && test -f "${dir}SKILL.md"
done

git diff --check
```

See [`docs/launch-checklist.md`](docs/launch-checklist.md) for the current
public-scope checks.

## License

MIT. See [`LICENSE`](LICENSE).
