# VideoOps Production Request

Use the VideoOps Producer at `/absolute/path/to/kujo-agents/videoops/producer/AGENT.md`.

Read the complete `videoops/` package before acting, including the shared `00-*.md` standards, the Producer contract, and each specialist `AGENT.md` and `SKILL.md` when that role begins. If `kujo-videoops-workflows` is installed, use it. Treat the five `kujo-workflows/videoops-*` fixture commands as acceptance tests only; do not use fixture content for this production.

Execute this request end to end through Creative Director, Asset Scout, Media Generator only where the manifest says `GENERATE`, HyperFrames Editor, and independent Video Critic. Use native subagents when the harness supports them. Otherwise assume one role at a time and use the required workspace artifacts and handoffs as context boundaries. Do not stop at a plan or draft unless a real blocker requires operator action.

## Production request

<Describe the release, demo, explainer, social clip, or other video you want. Include the product or subject, source material, required claims, target audience, CTA, desired tone, and anything that must or must not appear.>

## Workspace

- Target workspace: `/absolute/path/to/new-video-workspace`
- Source repositories/files: `<absolute paths or none>`
- Reference URLs/files: `<references or none>`

## Delivery contract

- Format/platform: `<for example, 1920x1080 landscape product demo>`
- Target duration: `<duration or bounded range>`
- FPS: `<FPS or let Creative Director choose and record>`
- Audio/captions: `<requirements>`
- Deadline: `<deadline or none>`
- Quality mode: `<economy, standard, or flagship>`

## Authority and cost

- Filesystem scope: target workspace plus the named read-only source paths.
- Authenticated capture allowed: `<yes/no; no by default>`
- Paid generation allowed: `<yes/no and maximum approved amount; no by default>`
- Publication allowed: `<yes/no and exact destination/action; no by default>`

## Completion

Finish only after the Critic passes the exact final candidate and deterministic render checks pass. Return the final video path, checksum, dimensions, FPS, duration, audio status, revision count, approval evidence, external effects, recorded model/token/cost evidence when available, and any unresolved blocker. Never invent evidence for unavailable tools or providers.
