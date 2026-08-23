# Runtime Adapters

The agent directories are provider-neutral packages. Their `AGENT.md`,
`SKILL.md`, `manifest.json`, and I/O schemas describe role intent and
contracts; they do not grant permissions, credentials, sandbox access, or
external effects.

Adapters translate those contracts into a runtime's native configuration:

- [`hermes/`](hermes/) renders isolated Hermes profile bundles.
- [`paperclip/`](paperclip/) defines Paperclip registration and heartbeat
  boundaries without calling a live control plane.

Adapters must keep credentials outside the repository, enforce the manifest's
permission ceiling, preserve handoffs and receipts, and fail closed when a
required capability or approval is unavailable.
