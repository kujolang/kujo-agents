# VideoOps Production Standard

## File contract

Agents work only inside their assigned stage and write inspectable artifacts. The canonical workspace is `intake/`, `planning/`, `assets/{source,captured,generated,normalized,audio,fonts}`, `production/hyperframes/`, `review/evidence/`, and `output/`.

No stage may hide missing dependencies, invent product claims, rewrite another role's decision, or declare success before required outputs validate. Shared standards are read-only during a run.

## Creative and motion language

Communicate one strong idea. Favor direct copy, authentic product evidence, hard cuts, punch-ins, micro-inserts, kinetic typography, temporal contrast, and semantic timing. Glitch is punctuation, not wallpaper. References supply general principles rather than shot-for-shot imitation. Avoid generic AI brains, robots, neon cyberpunk, fake dashboards, purple SaaS gradients, and meaningless filler unless explicitly justified.

## Assets and rights

Source priority is first-party existing media, first-party capture, clearly reusable external media, then custom generation. Publicly viewable media is discovery-only unless actual reuse rights are documented. Unknown rights means `reference-only`. Preserve originals; normalize copies separately. Every production asset maps to provenance and shot IDs.

Every requirement terminates as `FOUND`, `CAPTURED`, `GENERATE`, `NOT_REQUIRED`, or `BLOCKED`. Never guess a license.

## Audio and typography

Use the current Kujo brand type system and licensed fonts. Critical copy must remain readable at target size. Audio should reinforce edit rhythm, preserve clear speech, and avoid clipping, competing music, or unlicensed material.

## Quality

Review narrative clarity, hook, pacing, hierarchy, motion, brand fit, audio sync, transcript fidelity, technical render quality, and CTA. Mandatory defects use `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW` with timestamp/frame range, problem, impact, required change, and acceptance criteria. Preference alone cannot fail a video.
