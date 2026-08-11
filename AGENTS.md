# Kujo Agents Agent Instructions

This repository contains reusable KUJO Chain of Command and WebOps agent
packages. Treat role contracts and templates as guidance and review material,
not sandboxing, authorization, or policy enforcement.

## Required Reading

- `README.md`
- `docs/launch-checklist.md`
- `chain-of-command/README.md`
- `chain-of-command/00-chain-of-command.md`
- Relevant agent `AGENT.md` and `SKILL.md`
- `webops/README.md`, `webops/00-permission-model.md`, and `webops/webops-catalog.json` for WebOps changes

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
test "$(cat VERSION)" = "1.1.0"
git diff --check
```

## Evidence Rules

- Preserve inventories, template review notes, and deterministic validation
  output when changing agent contracts.
- Keep tool claims grounded in repository-backed evidence and clearly mark
  inferred behavior.
- Keep authority, stop conditions, and handoff requirements explicit.

## Prohibited Without Approval

Do not use live credentials, publish packages, create public releases, push
final tags, alter branch protection, force-push, rewrite history, or claim that
templates enforce policy or sandboxing.
