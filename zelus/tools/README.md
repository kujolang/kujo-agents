# Zelus tool adapters

Tool adapters belong here, under `zelus/`, rather than in a repository-root
`tools/` directory. An adapter is the narrow Kujo boundary between an agent
skill and a scanner, browser, API client, or local process.

Every adapter must:

1. Receive an engagement, campaign, agent, target, action, environment, and
   approval context.
2. Call the policy gate before touching the target.
3. Use structured argv or an API client; never build a shell command by string
   concatenation.
4. Record a tool receipt with input/output hashes.
5. Capture redacted raw output as evidence.
6. Return a machine-readable result and cleanup status.

`adapter_contract.kujo` contains the deterministic fixture adapter used by
the tests. It demonstrates the complete boundary without running a scanner or
using the network. Real integrations can wrap tools such as `subfinder`,
`amass`, `assetfinder`, `httpx`, `katana`, `gau`, `waybackurls`, `ffuf`,
`nuclei`, or `wpscan`, provided the engagement policy explicitly allows the
action and the adapter preserves the receipt/evidence contract.

Custom tools use the same pattern: create one Kujo adapter, declare its action
in the engagement policy, map it to the owning skill, and add an offline
fixture test before enabling live execution.
