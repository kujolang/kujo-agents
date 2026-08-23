# Launch Checklist

Current release: `v1.2.0`; the tagged `v1.0.0` Chain of Command baseline remains preserved.

Public scope: independent reusable Chain of Command, WebOps, and Publishing
House agent contracts, their shared maps, and evidence and authority boundaries.

## Local Gates

- [x] Each first-class agent set remains independently installable and usable.
- [x] Every role package contains both `AGENT.md` and `SKILL.md`.
- [x] Root and package documentation describe separate authority boundaries.
- [x] `VERSION`, README badge, changelog, tag intent, and release notes agree on
  `1.2.0`.
- [x] Publishing House includes a validated 18-case blind quality-calibration
  corpus covering all 23 roles without treating semantic judgment as a score.
- [x] Publishing House declares the eight implemented tools, eleven lifecycle
  workflows, tool ownership boundaries, and all 23 role bindings.
- [x] Tool-to-agent relationships remain source-grounded or explicitly marked
  as inferred.
- [x] All 79 roles expose provider-neutral manifests and I/O schemas, with a
  checked-in registry and credential-free Hermes/Paperclip renderers.
- [x] Templates retain explicit authority, handoff, evidence, and stop
  conditions.
- [x] Repository formatting passes `git diff --check`.
- [x] Public use and adaptation instructions were reviewed for the `v1.2.0`
  baseline.
- [x] `docs/webops-toolchain-contract.json` pins the three WebOps tools at
  `0.1.0`, their v1 artifact schemas, read-only boundaries, budgets, and the
  explicit SearchBridge submission authorization tuple.

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
python3 scripts/validate_publishing_house.py
test "$(cat VERSION)" = "1.2.0"
rg -n '1\.0\.0' README.md CHANGELOG.md docs/launch-checklist.md
git diff --check
```

## Release Evidence

- Agent inventory: 28 paired `AGENT.md` and `SKILL.md` packages under
  `chain-of-command/`.
- Release inventory: 23 paired Publishing House `AGENT.md` and `SKILL.md`
  packages plus UI metadata and 18 blind calibration pairs.
- Release metadata: `VERSION`, README badge, changelog, tag, and release name
  use `1.2.0` / `v1.2.0` consistently.
- Local artifact guard: `.github/scripts/check-kujo-tool-artifacts.sh`.
- Bounded execution proof: `docs/workcell-launch-gate.json`.
- Hosted CI remains environment-dependent and must not be represented as
  passing when GitHub does not start the workflow.

## Out Of Scope

The role templates do not themselves enforce sandboxing, permissions, policy,
or third-party platform behavior. Package publication, later public releases,
hosted deployment, branch-protection changes, force-pushes, and live credential
use require separate approval.
