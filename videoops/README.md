# Kujo VideoOps

VideoOps is a file-contract-driven team with one Producer and five specialist roles for turning a new video request into structured intake, an executable plan, rights-aware assets, a HyperFrames composition, independent review, and a verified final deliverable.

It follows the WebOps packaging model: the agent is the primitive, workflows compose agents, shared standards are read-only context, and a runtime adapter enforces permissions. Invoke `VideoOps Producer` for an end-to-end production. The Producer coordinates Creative Director, Asset Scout, Media Generator, HyperFrames Editor, and Video Critic without taking over their specialist decisions.

PackWrite remains the preferred intake compiler. When a validated PackWrite pack exists, VideoOps consumes its `intake/` artifacts. When a user supplies an ordinary mega prompt instead, the Producer preserves it and creates the same intake artifact set before dispatching the Creative Director. The sibling `kujo-workflows` fixture driver remains acceptance proof; it is not the only way to use the agents and must not be invoked for a real production request.

## Invoke The Team

Use [`MEGA_PROMPT_TEMPLATE.md`](MEGA_PROMPT_TEMPLATE.md) for a portable request, or tell a file-capable harness:

```text
Use the VideoOps Producer at /absolute/path/to/kujo-agents/videoops/producer/AGENT.md.
Read and follow the complete VideoOps package, then execute my production request
through all five specialist roles. Work in /absolute/path/to/project-video-workspace.

Production request:
<paste the request here>
```

The harness must be able to read the package and write the target workspace. Media generation, authenticated capture, and other provider-backed actions still depend on the harness's available tools and operator approval. A runtime with native subagents may delegate each role; a single-agent runtime may execute the same roles sequentially with the file handoffs as context boundaries.

Start with [`00-agent-map.md`](00-agent-map.md), [`00-production-standard.md`](00-production-standard.md), [`00-permission-model.md`](00-permission-model.md), and [`00-model-routing.md`](00-model-routing.md). The machine-readable source is [`videoops-catalog.json`](videoops-catalog.json).

Every run uses workspace-relative artifacts under `intake/`, `planning/`, `assets/`, `production/`, `review/`, and `output/`. Required decisions are written to files; downstream roles never depend on hidden conversation state.

No contract is permanently coupled to a provider or named model. Mechanical stages are economical-first, deterministic checks precede semantic judgment, economical attempts are capped at two, and escalation is local to the failing stage. Live provider, paid generation, cloud render, or publication actions require separate operator approval.
