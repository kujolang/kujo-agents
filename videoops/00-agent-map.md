# VideoOps Agent Map

| Stage | Agent | Owns | Does not own |
|---|---|---|---|
| Planning | Creative Director | thesis, transcript, pacing, shots, asset requirements | sourcing, generation, editing, approval |
| Asseting | Asset Scout | discovery, capture, rights, provenance, normalization | narrative, generation, editing |
| Asseting | Media Generator | explicit `GENERATE` items and manifest updates | unrelated filler, sourcing, final edit |
| Production | HyperFrames Editor | composition, render, technical QA, fix application | sourcing, creative approval |
| Review | Video Critic | independent PASS/FAIL and actionable defects | editing, sourcing, silent repair |

PackWrite is the upstream intake boundary. The supported stage workflows are `videoops-creative-planning`, `videoops-asset-resolution`, `videoops-media-generation`, `videoops-hyperframes-edit`, and `videoops-quality-review`.
