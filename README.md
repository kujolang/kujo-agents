# Kujo Agents

[![Version](https://img.shields.io/badge/version-1.2.0-black)](https://github.com/kujolang/kujo-agents)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![built with Kujo](https://img.shields.io/badge/built%20with-Kujo-white.svg)](https://github.com/kujolang/kujo)

Reusable role contracts for KUJO agent sets.

The public repository contains three independent first-class packages:

- [`chain-of-command/`](chain-of-command/) — coordinated roles for strategy, planning, execution, verification, knowledge, and bounded worker tasks.
- [`webops/`](webops/) — 28 peer website operators for research, measurement, audit, maintenance, optimization, and improvement.
- [`publishing-house/`](publishing-house/) — 23 editorial roles for strategy, creative development, writing, independent review, production, approval packaging, and bounded publishing operations.

## Start Here

Read these files before running or adapting an agent set:

1. [`chain-of-command/README.md`](chain-of-command/README.md) — role selection, handoffs, model tiers, and campaign guidance.
2. [`chain-of-command/00-chain-of-command.md`](chain-of-command/00-chain-of-command.md) — authority layers and escalation paths.
3. [`chain-of-command/00-tool-agent-map.md`](chain-of-command/00-tool-agent-map.md) — supported tool-to-role relationships.
4. [`chain-of-command/general-commander/AGENT.md`](chain-of-command/general-commander/AGENT.md) — top-level mission routing contract.
5. [`webops/README.md`](webops/README.md) — direct specialist selection, capabilities, permissions, history, and workflow composition.
6. [`webops/00-agent-map.md`](webops/00-agent-map.md) — the complete WebOps roster.
7. [`publishing-house/README.md`](publishing-house/README.md) — standalone operation, desks, review boundary, and current implementation scope.
8. [`publishing-house/00-publishing-house.md`](publishing-house/00-publishing-house.md) — constitution, authority layers, productive tension, and interoperability rules.
9. [`publishing-house/00-quality-standard.md`](publishing-house/00-quality-standard.md) — the premium editorial bar and generic-work warning signals.
10. [`publishing-house/00-shared-contracts.md`](publishing-house/00-shared-contracts.md) — briefs, evidence, artifacts, reviews, approvals, receipts, and handoffs.
11. [`publishing-house/00-tool-workflow-map.md`](publishing-house/00-tool-workflow-map.md) — canonical tool ownership, role bindings, and lifecycle workflow routing.
12. [`publishing-house/evals/README.md`](publishing-house/evals/README.md) — blind quality calibration, deterministic integrity checks, and semantic judging protocol.

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
webops/
  README.md
  00-agent-map.md
  00-tool-agent-map.md
  00-capability-integration-map.md
  00-permission-model.md
  00-history-and-reporting.md
  00-workflow-map.md
  webops-catalog.json
  agent-name/
    AGENT.md
    SKILL.md
publishing-house/
  README.md
  00-publishing-house.md
  00-quality-standard.md
  00-shared-contracts.md
  00-permission-model.md
  00-agent-map.md
  00-tool-workflow-map.md
  publishing-house-catalog.json
  evals/
    README.md
    quality-rubric.json
    evaluation-manifest.json
    judge-prompt.md
    judge-output.schema.json
    eval.json
    cases/
    expected/
  agent-name/
    AGENT.md
    SKILL.md
    agents/openai.yaml
```

Each agent package keeps its role contract and operating skill together. The
templates are guidance and review material; they do not provide sandboxing,
authorization, or policy enforcement by themselves.

## Release Status

`v1.2.0` preserves the stable Chain of Command and WebOps baselines while
integrating the 23 Publishing House roles with eight local-first tools and an
eleven-workflow lifecycle map. The 18-case blind quality corpus remains a
calibration surface rather than an automated editorial-taste claim. Runtime
packages and operator-configured adapters remain responsible for enforcement
and external effects.

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
python3 scripts/validate_webops.py
python3 scripts/validate_publishing_house.py
test "$(cat VERSION)" = "1.2.0"
git diff --check
```

## License

MIT. See [`LICENSE`](LICENSE).
