# Launch Checklist

Current launch scope: `locally verified support/distribution technical preview`. Agent/template inventory, deterministic Zelus validation, and Workcell proof pass locally. Template enforcement, third-party platform behavior, and live offensive testing are not complete.

## Local Gates

- [x] Template inventory checked with `find . -maxdepth 3 \( -name AGENT.md -o -name SKILL.md -o -name README.md \) | sort`.
- [x] Zelus doctor checked with `$KUJO_BIN run zelus.kujo -- doctor`.
- [x] Zelus reference campaign checked with `$KUJO_BIN run zelus.kujo -- campaign reference examples/sample-wordpress-campaign --out /tmp/zelus-next-batch-reference`.
- [x] Zelus contract tests checked with `$KUJO_BIN run tests/zelus_contract_tests.kujo --interpreter`.
- [x] Zelus CLI tests checked with `$KUJO_BIN run tests/zelus_cli_tests.kujo --interpreter`.
- [x] Zelus registry tests checked with `$KUJO_BIN run tests/zelus_registry_tests.kujo --interpreter`.
- [x] Formatting checked with `git diff --check`.
- [x] Workcell proof checked with `workcell run --file docs/workcell-launch-gate.json --repo . --no-pull`.
- [ ] Independent review of public install/adaptation instructions.

## Workcell Proof Notes

Workcell proof passed after building `kujolang/workcell-base:local` with `DOCKER_BUILDKIT=0`, using the Colima Workcell Docker host, and setting `TMPDIR` to a path under `/Users/robertdevore/2026/Kujolang/kujo-repos/.workcell-host-tmp` so the disposable worktree mount was visible inside the Colima VM.

Resume command:

```bash
export DOCKER_HOST=unix:///Users/robertdevore/.colima/kujo-workcell/docker.sock
export DOCKER_CONFIG=/tmp/kujo-next-batch-docker-config
export TMPDIR=/Users/robertdevore/2026/Kujolang/kujo-repos/.workcell-host-tmp
workcell run --file docs/workcell-launch-gate.json --repo . --no-pull
workcell verify --run .workcell/runs/<run-id> --json
```

## Forbidden Launch Actions

Live offensive testing, live credentials, package publication, public releases, final release tags, hosted deployment, branch-protection changes, force-pushes, and claims that templates enforce sandboxing or policy remain out of scope.
