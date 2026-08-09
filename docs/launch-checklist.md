# Launch Checklist

Current public scope: the reusable KUJO chain-of-command agent contracts,
supporting maps, and campaign templates.

## Local Gates

- [x] Only chain-of-command agent packages are present in the public tree.
- [x] Every agent package contains both `AGENT.md` and `SKILL.md`.
- [x] Root and chain documentation describe the chain-only scope.
- [x] Tool-to-agent relationships remain source-grounded or explicitly marked
  as inferred.
- [x] Templates retain explicit authority, handoff, evidence, and stop
  conditions.
- [x] Repository formatting passes `git diff --check`.
- [ ] Independent review of public use and adaptation instructions.

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
git diff --check
```

## Out Of Scope

The role templates do not themselves enforce sandboxing, permissions, policy,
or third-party platform behavior. Package publication, public releases, final
release tags, hosted deployment, branch-protection changes, force-pushes, and
live credential use require separate approval.
