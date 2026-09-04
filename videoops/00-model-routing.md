# VideoOps Model Routing

VideoOps is economical by default, capability-routed, Eval-gated, and provider-independent.

Logical profiles are `economical-general`, `economical-code`, `economical-multimodal`, `premium-creative`, and `premium-multimodal`. Config supplies provider/model candidates; no role hard-codes one. Mechanical facts such as files, schema, resolution, FPS, duration, streams, asset IDs, provenance fields, and render exit status are determined by software.

Each stage validates, attempts one targeted economical repair, then either passes or records a stage-local escalation. Default maximum economical attempts is two. Default editor/critic revision limit is three. Budget pressure never converts a failed gate into acceptance.

Every escalation records stage, from/to profile, reason, attempts, prior gate result, timestamp, provider/model resolution, usage when known, latency, and cost when known. Never invent usage or cost.

Quality modes are `economy`, `standard`, and `flagship`. Flagship may request earlier creative or final multimodal review, but mechanical stages remain economical. Select future provider defaults from cost per accepted artifact, not headline token price.
