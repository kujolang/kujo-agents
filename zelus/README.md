# Zelus

Zelus is a Kujo-native AI offensive-security research team for explicitly
authorized WordPress bug bounty, vendor-approved red-team, and internal
adversary simulation work.

The implementation is intentionally written in Kujo. The package showcases
Kujo modules, structured data, file-backed artifacts, deterministic offline
fixtures, CLI parsing, tests, redaction, policy gates, and Agents SDK-shaped
handoffs without requiring Python, provider credentials, or network access.

## Run

```bash
export KUJO_BIN=/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/debug/kujo
cd zelus
$KUJO_BIN check zelus.kujo
$KUJO_BIN run zelus.kujo -- doctor
$KUJO_BIN run zelus.kujo -- engagement validate examples/sample-wordpress-campaign
$KUJO_BIN run zelus.kujo -- campaign reference examples/sample-wordpress-campaign --out /tmp/zelus-reference
$KUJO_BIN test-run tests/zelus_contract_tests.kujo -v
```

## Layout

```text
zelus/
├── zelus.kujo             # thin CLI entrypoint
├── src/                    # Kujo runtime, contracts, policy, evidence, graph
├── agents/                 # Zelus-specific agent contracts and prompts
├── skills/                 # versioned skill catalog
├── workflows/              # declarative campaign definitions
├── schemas/                # machine-readable record contracts
├── examples/               # synthetic engagement packets
└── tests/                  # Kujo-native contract tests
```

The package is an offline foundation. Live HTTP, DNS, browser, container, and
provider adapters must be connected through the scope gate and evidence receipt
contracts before use against any real target.
