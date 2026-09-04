# Kujo VideoOps

VideoOps is a file-contract-driven team of five production roles for turning structured intake into an executable plan, rights-aware assets, a HyperFrames composition, independent review, and a bounded revision handoff.

It follows the WebOps packaging model: the agent is the primitive, workflows compose agents, shared standards are read-only context, and a runtime adapter enforces permissions. The five packages are Creative Director, Asset Scout, Media Generator, HyperFrames Editor, and Video Critic.

PackWrite owns intake normalization. VideoOps consumes its `intake/` artifacts and does not reimplement it. A production master orchestrator is intentionally deferred until the five stage contracts are stable; the sibling `kujo-workflows` fixture driver is proof code, not an autonomous production orchestrator.

Start with [`00-agent-map.md`](00-agent-map.md), [`00-production-standard.md`](00-production-standard.md), [`00-permission-model.md`](00-permission-model.md), and [`00-model-routing.md`](00-model-routing.md). The machine-readable source is [`videoops-catalog.json`](videoops-catalog.json).

Every run uses workspace-relative artifacts under `intake/`, `planning/`, `assets/`, `production/`, `review/`, and `output/`. Required decisions are written to files; downstream roles never depend on hidden conversation state.

No contract is permanently coupled to a provider or named model. Mechanical stages are economical-first, deterministic checks precede semantic judgment, economical attempts are capped at two, and escalation is local to the failing stage. Live provider, paid generation, cloud render, or publication actions require separate operator approval.
