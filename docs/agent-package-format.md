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
