# Launch Checklist

Current source version: `1.1.0`; the tagged `v1.0.0` Chain of Command baseline remains preserved.

Public scope: the reusable KUJO chain-of-command agent contracts, supporting
maps, campaign template, and evidence boundaries.

## Local Gates

- [x] Only chain-of-command agent packages are present in the public tree.
- [x] Every agent package contains both `AGENT.md` and `SKILL.md`.
- [x] Root and chain documentation describe the chain-only scope.
- [x] `VERSION`, README badge, changelog, tag intent, and release notes agree on
  `1.1.0`.
- [x] Tool-to-agent relationships remain source-grounded or explicitly marked
  as inferred.
- [x] Templates retain explicit authority, handoff, evidence, and stop
  conditions.
- [x] Repository formatting passes `git diff --check`.
- [x] Public use and adaptation instructions were reviewed for the `v1.1.0`
  baseline.

## Validation Commands

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
rg -n '1\.0\.0' README.md CHANGELOG.md docs/launch-checklist.md
git diff --check
```

## Release Evidence

- Agent inventory: 28 paired `AGENT.md` and `SKILL.md` packages under
  `chain-of-command/`.
- Release metadata: `VERSION`, README badge, changelog, tag, and release name
  use the current source version consistently and distinguish it from the existing `v1.0.0` tag.
- Local artifact guard: `.github/scripts/check-kujo-tool-artifacts.sh`.
- Bounded execution proof: `docs/workcell-launch-gate.json`.
- Hosted CI remains environment-dependent and must not be represented as
  passing when GitHub does not start the workflow.

## Out Of Scope

The role templates do not themselves enforce sandboxing, permissions, policy,
or third-party platform behavior. Package publication, later public releases,
hosted deployment, branch-protection changes, force-pushes, and live credential
use require separate approval.
