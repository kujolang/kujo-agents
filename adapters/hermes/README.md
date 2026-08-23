# Hermes Adapter

Render provider-neutral Kujo manifests into Hermes profile bundles:

```bash
python3 scripts/generate_runtime_adapters.py --target hermes --output dist/hermes
```

Each rendered profile contains a generated `SOUL.md`, a profile manifest, and
an example configuration. Tokens and model credentials are intentionally not
generated. Configure those through Hermes' own profile setup and environment
files.

The generated SOUL is an adapter view of `AGENT.md` and `SKILL.md`; it is not a
replacement for the canonical Kujo contract.
