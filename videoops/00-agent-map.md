# VideoOps Agent Map

| Stage | Agent | Owns | Does not own |
|---|---|---|---|
| Orchestration | VideoOps Producer | intake preservation, role dispatch, gate sequencing, revision routing, final evidence | specialist artifacts, self-approval, unapproved external effects |
| Planning | Creative Director | thesis, transcript, pacing, shots, asset requirements | sourcing, generation, editing, approval |
| Asseting | Asset Scout | discovery, capture, rights, provenance, normalization | narrative, generation, editing |
| Asseting | Media Generator | explicit `GENERATE` items and manifest updates | unrelated filler, sourcing, final edit |
| Production | HyperFrames Editor | composition, render, technical QA, fix application | sourcing, creative approval |
| Review | Video Critic | independent PASS/FAIL and actionable defects | editing, sourcing, silent repair |

Invoke the complete team through the VideoOps Producer. PackWrite is the preferred upstream intake compiler, but the Producer may normalize an arbitrary plain-language production request into the same intake contract. The supported stage workflows are `videoops-creative-planning`, `videoops-asset-resolution`, `videoops-media-generation`, `videoops-hyperframes-edit`, and `videoops-quality-review`.
