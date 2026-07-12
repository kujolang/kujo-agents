# Zelus workflows

Workflows are executable Kujo data in [`catalog.kujo`](catalog.kujo). Each
workflow returns ordered steps with an agent, skill, prerequisites, gate, and
evidence requirement. A runner can call `get_workflow("engagement-intake")`,
validate it, and dispatch each step through the authorization gate.

The catalog is intentionally small and readable. The Kujo runtime owns the
contracts and the offline reference campaign; Dispatch or an Agents SDK runner
can execute the same records when live adapters are installed.

Try it from the package directory:

```bash
$KUJO_BIN check workflows/catalog.kujo
```
