# Kujo Agents Agent Instructions

This repository contains reusable agent packages and templates. Treat templates as guidance and review material, not sandboxing or policy enforcement.

## Required Reading

- `README.md`
- `docs/launch-checklist.md`
- Relevant agent `AGENT.md`, `SKILL.md`, and package `README.md`
- `zelus/README.md` and `zelus/SECURITY.md` before touching Zelus

## Validation

```bash
find . -maxdepth 3 \( -name AGENT.md -o -name SKILL.md -o -name README.md \) | sort
cd zelus
"$KUJO_BIN" run zelus.kujo -- doctor
"$KUJO_BIN" run zelus.kujo -- campaign reference examples/sample-wordpress-campaign --out /tmp/zelus-reference
"$KUJO_BIN" run tests/zelus_contract_tests.kujo --interpreter
"$KUJO_BIN" run tests/zelus_cli_tests.kujo --interpreter
"$KUJO_BIN" run tests/zelus_registry_tests.kujo --interpreter
cd ..
git diff --check
```

## Evidence Rules

- Preserve inventories, template review notes, and deterministic Zelus proof logs for launch evidence.
- Keep offensive-security wording explicitly authorized/research-only.
- Workcell proof is required for this launch batch unless a blocker receipt documents the Docker/host blocker and closest equivalent proof.

## Prohibited Without Approval

Do not run live offensive testing, use live credentials, publish packages, create public releases, push final tags, alter branch protection, force-push, rewrite history, or claim templates enforce policy/sandboxing.
