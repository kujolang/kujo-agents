# Zelus operator how-to

Zelus is a Kujo package, not a Python application and not a collection of
prompt files. The simplest mental model is:

```text
engagement packet -> Director plan -> Kujo workflow steps -> scoped tools
                   -> evidence ledger -> verification -> report/casefile
```

The package is currently a safe, offline foundation. The reference campaign
proves the handoffs with synthetic WordPress evidence. Live DNS, HTTP,
browser, scanner, and model-provider adapters are integration points; they are
not silently enabled by the package.

## 1. Install and check the package

Build or obtain the Kujo binary, then point `KUJO_BIN` at it:

```bash
export KUJO_BIN=/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/debug/kujo
cd /path/to/kujo-agents/zelus
$KUJO_BIN check zelus.kujo
$KUJO_BIN run zelus.kujo -- doctor
```

`doctor` reports the Kujo entrypoint, agent count, workflow count, skill count,
offline default, and Python-runtime status. A healthy package reports
`"language":"Kujo"`, `"python_runtime":false`, and `"ok":true`.

## 2. Give Zelus an engagement

Start from `examples/sample-wordpress-campaign/` and copy it for a real,
explicitly authorized engagement. At minimum, provide `manifest.json` with an
objective and authorization profile:

```json
{
  "engagement_id": "eng-acme-001",
  "name": "Acme WordPress bounty",
  "objective": "Find and safely validate authorization failures",
  "authorization": {
    "mode": "public_bug_bounty",
    "expires_at": "4102444800",
    "scope_rules": [
      {"pattern":"staging.acme.test", "decision":"allow",
       "actions":["source.read","http.request"], "environments":["staging"]}
    ],
    "prohibited_actions": ["dos", "destructive.delete"],
    "required_approvals": {"exploit.validate":"director"}
  }
}
```

Keep credentials as environment, vault, or encrypted-file references. Do not
put passwords, API keys, cookies, or real user data in the packet.

Validate and ingest the packet:

```bash
$KUJO_BIN run zelus.kujo -- engagement validate examples/my-engagement
$KUJO_BIN run zelus.kujo -- engagement ingest examples/my-engagement \
  --out /tmp/zelus-engagement-manifest.json
$KUJO_BIN run zelus.kujo -- campaign plan /tmp/zelus-engagement-manifest.json \
  --out /tmp/zelus-campaign.json
```

Validation is fail-closed. A newly discovered host is not automatically in
scope; add it to the packet and obtain the required authorization first.

## 3. Send work to the Director and team

For the current deterministic runtime, the operator sends a packet to the
CLI. The Director-shaped intake and planning functions produce the normalized
manifest, campaign objectives, workstreams, and tasks.

For an AI runner built on the Kujo Agents SDK or Dispatch, send the same
packet plus a bounded task request. This is a useful operator message:

```text
Read zelus/HOWTO.md and zelus/agents/director/AGENT.md.
Engagement packet: /path/to/engagement
Objective: test the staging WordPress plugin for low-privilege authorization failures.
Mode: public_bug_bounty
Allowed targets: the scope_rules in manifest.json only.
Allowed actions: source.read, http.request, exploit.validate in the staging Workcell.
Prohibited actions: denial of service, destructive changes, unrelated user data.
Required outputs: task packages, hypothesis cards, evidence references,
primitive/chain records, independent verification, and a draft report.
Stop for human approval before any live exploit validation.
```

The Director should delegate technical work. The source hunter creates a
hypothesis, the identity hunter tests role/object boundaries, the exploit
engineer reproduces in a Workcell, the chain architect evaluates follow-on
capabilities, the verification officer independently challenges it, and the
case officer prepares the disclosure package.

The agent folders are contracts, not hidden workers. Each agent folder has an
`AGENT.md`, `SKILL.md`, and `definition.json`. A Kujo Agents SDK or Dispatch
runner can load those contracts and use the Kujo records as handoff payloads.

## 4. Workflows: how they are managed

Workflows are now Kujo functions in `workflows/catalog.kujo`, not JSON files.
Each workflow returns records like:

```text
workflow id -> ordered steps -> agent + skill + prerequisites + gate
```

Examples include `engagement-intake`, `source-assisted-hunt`,
`role-matrix`, `exploit-development`, `attack-chain-synthesis`,
`independent-verification`, and `responsible-disclosure`.

The registry is inspectable from Kujo code:

```kujo
from workflows.catalog import get_workflow

plan := get_workflow("source-assisted-hunt")
```

The current CLI runs the offline reference path directly. It does not yet
automatically execute arbitrary catalog steps. A Dispatch/Agents SDK adapter
can call `get_workflow`, check each prerequisite, route the step to the named
agent, and persist each result. This explicit boundary prevents a JSON file or
prompt from becoming an unreviewed live action.

## 5. Skills: how they are managed

Skills are now Kujo records in `skills/catalog.kujo`. The catalog answers:

- Which agent owns a skill?
- Which tool family may it request?
- What evidence must it produce?
- What version of the contract is in force?

For example, `wordpress_object_authorization_test` belongs to the
identity/authorization agent and may use the RoleMatrix, request replay,
Workcell, and evidence-ledger tool families. The catalog is a registry; the
agent `SKILL.md` is the human-readable procedure, and the Kujo source modules
perform deterministic behavior where implemented.

```kujo
from skills.catalog import get_skill

skill_record := get_skill("wordpress_object_authorization_test")
```

Skills are not unrestricted plugin loading. A runner must still enforce the
engagement policy, tool permissions, approvals, rate limits, environment, and
expiration on every invocation.

## 6. Tools, scanners, and custom adapters

Yes, Zelus can use large security tools and custom tools, but each one must be
wrapped by a Kujo adapter under `zelus/tools/`. The adapter is responsible for
the operational boundary:

```text
task -> policy.evaluate -> authorized argv/API call -> tool receipt
     -> redacted evidence -> parsed result -> task handoff
```

Potential adapters include `subfinder`, `amass`, `assetfinder`, `httpx`,
`katana`, `gau`, `waybackurls`, `ffuf`, `nuclei`, `wpscan`, browser
automation, a private scanner, or a vendor API. The repository does not claim
these tools are installed or authorized. Add one only after confirming the
program policy and adding an offline fixture test.

`tools/adapter_contract.kujo` demonstrates the full receipt/evidence path with
a deterministic fixture. A live adapter should:

1. Accept structured arguments, preferably an argv array or typed API request.
2. Refuse missing or expired authorization.
3. Avoid shell interpolation of target-controlled values.
4. Capture tool version, command/request hash, target, timestamps, and exit state.
5. Store raw output through redaction and link it to parsed records.
6. Enforce rate limits and cleanup.

To add a custom scanner, create an adapter, add its action to the authorization
profile, map the action to the owning skill, and add a fixture test. Do not
give an agent a generic “run anything” shell tool.

## 7. Run the reference campaign

This demonstrates the complete offline path:

```bash
$KUJO_BIN run zelus.kujo -- campaign reference \
  examples/sample-wordpress-campaign --out /tmp/zelus-reference
```

Inspect the generated directory:

```bash
find /tmp/zelus-reference -maxdepth 2 -type f | sort
cat /tmp/zelus-reference/casefile.json
```

The run produces hypothesis records, primitive records, a chain record,
verification, redacted evidence, Workcell cleanup, and a CaseFile/report
readiness artifact. The evidence ledger keeps raw receipts and hashes so a
claim is not supported by agent prose alone.

For source-only analysis of a supplied plugin:

```bash
$KUJO_BIN run zelus.kujo -- hypotheses source \
  examples/sample-wordpress-campaign/targets/source/zelus-fixture.php \
  --engagement eng-local --campaign campaign-local \
  --target staging.acme.test --out /tmp/hypotheses.json
```

## 8. Review results and build a report

The operator reviews the output directory and only submits after independent
verification. A report readiness check requires the finding and verification
records to agree on prerequisites, affected behavior, evidence, and status:

```bash
$KUJO_BIN run zelus.kujo -- report validate \
  /tmp/zelus-reference/finding.json \
  /tmp/zelus-reference/verification.json
```

The intended submission targets are HackerOne, Bugcrowd, Wordfence,
Patchstack, direct vendor disclosure, or an internal remediation ticket. The
case officer must label observed facts, supported inferences, and unverified
possibilities separately and redact secrets before export.

## 9. What is implemented versus next

Implemented now:

- Kujo-native contracts, policy gate, evidence receipts, redaction, source
  hypotheses, Workcell fixture, primitive/chain graph, verification gate,
  casefile, CLI, tests, and offline reference campaign.
- Ten organized Zelus agent contracts and a Kujo skill/workflow registry.
- A scoped adapter contract for adding scanners without a root Python tools
  directory.

Next integration work:

- Wire the Kujo Agents SDK or Dispatch to execute catalog steps with model
  providers and persistent handoffs.
- Add approved, sandboxed adapters for DNS/HTTP/browser/scanner tools.
- Add a real disposable WordPress container provider and browser replay.
- Add vendor-specific submission transports and fix-verification polling.

Until those adapters are installed and tested, Zelus will not probe a live
target. That is an intentional safety boundary, not a missing prompt.
