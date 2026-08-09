# Kujo Agents

[![Version](https://img.shields.io/badge/version-1.0.0-black)](https://github.com/kujolang/kujo-agents/releases/tag/v1.0.0)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![built with Kujo](https://img.shields.io/badge/built%20with-Kujo-white.svg)](https://github.com/kujolang/kujo)

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
CHANGELOG.md
VERSION
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

## Release Status

`v1.0.0` is the stable baseline for this chain-of-command agent setup. It
includes 28 paired agent packages plus the role map, tool ownership map,
campaign template, and evidence boundaries needed to use the chain as a
reusable starting point.

See [`CHANGELOG.md`](CHANGELOG.md) for release history and
[`docs/launch-checklist.md`](docs/launch-checklist.md) for the verified release
scope.

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

bash .github/scripts/check-kujo-tool-artifacts.sh
test "$(cat VERSION)" = "1.0.0"
git diff --check
```

## License

MIT. See [`LICENSE`](LICENSE).
