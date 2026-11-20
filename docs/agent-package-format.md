# Kujo Agent Package Format

Every role is a provider-neutral package. The canonical role files are:

```text
AGENT.md             human-readable contract
SKILL.md             invocation and routing contract
manifest.json        machine-readable identity and capability contract
input.schema.json    accepted structured input shape
output.schema.json   produced structured output shape
```

The manifest is intentionally descriptive. Its `permissions.maximum` value is
an upper bound that a runtime adapter must enforce; it is not authorization by
itself. `AGENT.md` and `SKILL.md` remain the source documents for role intent,
workflow, evidence, escalation, and stop conditions.

Shared handoff, artifact, approval, and receipt schemas live in [`../schemas/`](../schemas/)
because they are cross-agent protocols, not role-specific prompts.

## Runtime use

Generate the complete registry first:

```bash
python3 scripts/generate_agent_manifests.py
```

Then render a credential-free adapter package:

```bash
python3 scripts/generate_runtime_adapters.py --target hermes --output dist/hermes
python3 scripts/generate_runtime_adapters.py --target paperclip --output dist/paperclip
```

The generated outputs are deployment inputs, not authority. The target runtime
must still provide credentials, tools, sandboxing, approvals, persistence, and
external-effect enforcement.

## Collaboration compatibility

The optional [collaboration integrations index](../collaboration-integrations.json) joins on canonical agent IDs. Version 1 entries specify a platform, host, protocol major, qualification status and supported operations. The index is separate from the strict agent manifest. A profile or adapter descriptor does not install a runtime, grant authority or authorize a connection.

Fixture-only entries describe a test and do not permit active public setup links. A qualified entry must include a separately reviewed HTTPS setup URL and qualification receipt. Provider credentials, workspace IDs and grants belong to the installed operator environment.
