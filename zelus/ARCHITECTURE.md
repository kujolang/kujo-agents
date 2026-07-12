# Zelus architecture

```text
packet -> intake -> authorization -> campaign/task graph
       -> recon/source/identity hypotheses -> Workcell reproduction
       -> primitive graph -> chain candidate -> independent verification
       -> CaseFile/report -> disclosure/fix verification -> postmortem
```

The Director owns campaign decisions. Deterministic Kujo modules own execution
and artifact creation. A hypothesis never becomes a finding by prose alone:
source evidence, runtime evidence, primitive evidence, and independent
verification are separate records.

## Kujo composition

- `src/contracts.kujo` defines common record envelopes and state transitions.
- `src/policy.kujo` implements fail-closed scope, action, environment, approval,
  prohibition, and expiry checks.
- `src/evidence.kujo` redacts sensitive values, hashes artifacts, and records
  tool receipts.
- `src/source.kujo` indexes WordPress hooks, REST routes, AJAX actions, inputs,
  capabilities, nonces, and sensitive sinks.
- `src/workcell.kujo` provides a disposable synthetic fixture boundary.
- `src/graph.kujo` composes confirmed primitives conservatively.
- `src/reference.kujo` demonstrates the full deterministic campaign.
- `src/cli.kujo` exposes operator commands.

## Kujo ecosystem seams

Agents SDK provides agent runners, tools, approvals, handoffs, tracing, memory,
and artifacts. Dispatch provides workflow orchestration. Fence provides
architecture-boundary checks. Watchdog provides telemetry. RunLedger and
CaseFile preserve execution evidence. Redact, Scout, Scent, Eval, ShipCheck,
Concord, Workcell, and MCP attach through the contracts in this package.

Zelus owns the security-research domain model and policy boundary; it does not
replace those tools.
