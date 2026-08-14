# Publishing House Quality Calibration

This corpus tests whether Publishing House reviewers can distinguish premium editorial judgment from work that is competent but generic. It is a calibration set, not proof that taste has been automated.

## What Is Included

- `quality-rubric.json` defines the eight quality dimensions, rating language, classifications, and blocking rule.
- `cases/` contains 18 blind A/B comparisons spanning all 23 Publishing House roles.
- `expected/` contains the reviewed reference judgment for each comparison.
- `judge-prompt.md` is the fixed semantic-review protocol.
- `judge-output.schema.json` defines the review record expected from a human or model judge.
- `evaluation-manifest.json` binds case IDs, role coverage, paths, and fixture checksums.
- `eval.json` runs deterministic corpus and repository checks with Kujo Eval.

## Blind Review Protocol

1. Give the judge `quality-rubric.json`, `judge-prompt.md`, and exactly one file from `cases/`.
2. Do not reveal or load the matching file from `expected/` until the judge has returned a final JSON judgment.
3. Validate the result against `judge-output.schema.json`.
4. Compare preferred candidate, classifications, blockers, decisive dimensions, and cited generic signals with the reference judgment.
5. Record disagreements for human calibration. Do not silently tune the fixture or expected answer to match a model.

Candidate labels are intentionally mixed across the corpus. Length, polish, certainty, model identity, and candidate position are not quality signals.

## Interpretation

The deterministic layer verifies corpus integrity, blind labels, hashes, schema shape, complete dimension ratings, role coverage, and repository contracts. The semantic layer still requires judgment. A passing structural run does not establish that a model can reliably recognize premium work.

Use this corpus to calibrate prompts and reviewers, inspect disagreement patterns, and prevent “competent but generic” from becoming the default acceptance bar. Add new fixtures only after human review, with a concrete distinction that the current corpus does not already test.

## Run The Deterministic Gate

From the repository root:

```bash
python3 scripts/validate_publishing_house.py

KUJO=/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/release/kujo
EVAL=/Users/robertdevore/2026/Kujolang/kujo-repos/eval/main.kujo
"$KUJO" run "$EVAL" lint publishing-house/evals/eval.json
"$KUJO" run "$EVAL" run publishing-house/evals/eval.json \
  --output-dir /tmp/kujo-agents-publishing-house-eval --json
```

Tool inventory, runtime bindings, and composed publishing workflows remain outside this step.
