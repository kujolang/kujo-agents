# Launch Checklist

Current launch scope: `locally verified support/distribution technical preview`. Agent/template inventory and deterministic Zelus validation pass locally. Template enforcement, third-party platform behavior, live offensive testing, and Workcell proof are not complete.

## Local Gates

- [x] Template inventory checked with `find . -maxdepth 3 \( -name AGENT.md -o -name SKILL.md -o -name README.md \) | sort`.
- [x] Zelus doctor checked with `$KUJO_BIN run zelus.kujo -- doctor`.
- [x] Zelus reference campaign checked with `$KUJO_BIN run zelus.kujo -- campaign reference examples/sample-wordpress-campaign --out /tmp/zelus-next-batch-reference`.
- [x] Zelus contract tests checked with `$KUJO_BIN run tests/zelus_contract_tests.kujo --interpreter`.
- [x] Zelus CLI tests checked with `$KUJO_BIN run tests/zelus_cli_tests.kujo --interpreter`.
- [x] Zelus registry tests checked with `$KUJO_BIN run tests/zelus_registry_tests.kujo --interpreter`.
- [x] Formatting checked with `git diff --check`.
- [ ] Workcell proof checked with `workcell run --file docs/workcell-launch-gate.json --repo .`.
- [ ] Independent review of public install/adaptation instructions.

## Current External Blocker

Workcell proof is blocked by the local Docker image build/pull path. The Workcell base image could not be fetched from Docker Hub because `auth.docker.io` timed out.

Closest equivalent proof: agent/template inventory plus deterministic Zelus local proof.

Safe resume command:

```bash
cd /Users/robertdevore/2026/Kujolang/kujo-repos/workcell
DOCKER_HOST=unix:///Users/robertdevore/.colima/kujo-workcell/docker.sock docker build --tag kujolang/workcell-base:local docker/
cd /Users/robertdevore/2026/Kujolang/kujo-repos/kujo-agents
workcell run --file docs/workcell-launch-gate.json --repo .
```

## Forbidden Launch Actions

Live offensive testing, live credentials, package publication, public releases, final release tags, hosted deployment, branch-protection changes, force-pushes, and claims that templates enforce sandboxing or policy remain out of scope.
