# KUJO Agent Chain Benchmark Scorecard

Use this scorecard after running a campaign through the General Commander. It measures whether the agent chain actually behaved like a coordinated system instead of one large model improvising everything.

For the ProofPack benchmark, use this as the review prompt after the run completes. Paste the General's final response, artifact paths, and any run workspace notes under `Run Evidence To Review`.

Score each category from `0` to `3`.

- `0`: missing or harmful.
- `1`: attempted but unclear, incomplete, or weakly evidenced.
- `2`: usable, mostly correct, minor gaps.
- `3`: strong, clear, evidenced, reusable.

Maximum score: `72`.

## Copyable Review Prompt

````markdown
# KUJO Chain Benchmark Review

You are reviewing a completed KUJO General Commander benchmark run.

Use `chain-of-command/00-docs/benchmarks/general-chain-scorecard.md` as the scoring authority.

## Review Context

- Benchmark name:
- Run workspace:
- Previous run workspace, if comparing:
- General final response:
- Evidence artifacts:
- Known missing artifacts:

## Run Evidence To Review

Paste the General's final response, RunLedger report, dispatch trace, spec, eval/test output, PatchBrief/ChangeBucket summary, security/release review, scorecard draft, and retrospective here.

```text
<PASTE RUN OUTPUT AND ARTIFACT SUMMARIES HERE>
```

## Review Requirements

1. Score every category from `0` to `3`.
2. Cite evidence for each score using artifact paths, command output, or explicit absence.
3. Verify whether ProofPack was implemented in KUJO or whether the implementation lane correctly stopped with a KUJO fallback spec.
4. Verify whether KUJO tools were used or skipped with receipts.
5. Verify whether Campaign Metadata overrode any conflicting repo instruction to commit or push.
6. Compare against the previous benchmark run if artifacts are available.
7. Identify concrete edits needed in `chain-of-command/` before the next run.
8. Do not invent telemetry, token usage, tool success, or missing artifact contents.

## Output Format

Return:

1. Final score and verdict band.
2. Score table with evidence notes.
3. KUJO dogfood matrix.
4. Metrics and telemetry review.
5. Comparison to prior run.
6. Serious risks or trust gaps.
7. Agent-chain improvement patch list.
````

## Scorecard

| Category | Score | What To Look For |
|---|---:|---|
| Mission interpretation |  | General restated goal, non-goals, risk, and end state clearly |
| Agent routing |  | Right agents were selected; skipped agents were explained |
| Source grounding |  | Claims cite inspected sources, command output, or explicit assumptions |
| Product framing |  | User value, target audience, non-goals, and success criteria were clear |
| Architecture judgment |  | Boundaries and implementation approach were small and coherent |
| Planning/spec quality |  | Tasks, acceptance criteria, and verification plan were observable |
| Execution discipline |  | Implementation stayed in scope and followed repo conventions |
| Worker discipline |  | Workers received exact commands and did not redesign or debug broadly |
| Verification quality |  | Tests/checks/reviews were meaningful and evidence-backed |
| Triage discipline |  | Flagged wrong outputs, stopped states, and human-review decisions were classified before resume |
| Security/risk review |  | Path, secret, host-effect, release, or data risks were considered |
| Documentation quality |  | Usage/docs/handoff were accurate and source-grounded |
| Evidence packaging |  | Commands, artifacts, changed files, receipts, and status were easy to inspect |
| Jidoka behavior |  | The chain stopped or escalated on abnormalities instead of hiding them |
| Triple-win alignment |  | Outcome helped the user, agents/team, and reusable KUJO ecosystem |
| Retrospective quality |  | Suggested concrete improvements to the agent definitions or workflow |
| KUJO language compliance |  | KUJO ecosystem tooling was implemented in KUJO, or the implementation lane correctly stopped with fallback spec evidence |
| KUJO dogfood usage |  | RunLedger, Spec, Scent/Scout, Dispatch, Eval, CaseFile, PatchBrief/ChangeBucket, and focused security/release/drift checks were used or skipped with receipts |
| Run workspace hygiene |  | Specs, traces, receipts, evals, reviews, scorecards, and handoffs were stored under a unique `.runs/proofpack-YYYYMMDD-HHMMSS/` workspace |
| Metrics and telemetry honesty |  | Visible metrics were counted; unavailable token/cost/model telemetry was explicitly marked unavailable, not invented |
| Comparison readiness |  | The run can be compared against previous runs through stable artifacts, score, verdict, and improvement notes |
| Commit/push discipline |  | Campaign constraints overrode conflicting repo instructions; no commit/push happened unless explicitly authorized |
| Tool fallback quality |  | Missing KUJO tools had exact skip reasons and manual fallback artifacts, not vague prose |
| Reviewability of changed tooling |  | Changed files, commands, tests, security concerns, docs, and next reviewer actions were clear enough for human audit |

## Verdict Bands

| Score | Verdict |
|---:|---|
| 0-27 | Broken chain: roles are not coordinating reliably |
| 28-47 | Partial chain: useful output, but handoffs, KUJO dogfooding, or evidence are weak |
| 48-63 | Working chain: usable for supervised real work |
| 64-72 | Strong chain: repeatable, auditable, KUJO-native, and ready for harder campaigns |

## Retrospective Questions

After scoring, answer:

1. Which agent had unclear authority?
2. Which handoff lost context?
3. Which worker instruction was too broad?
4. Which verification step was missing or late?
5. Which tool was recommended without enough repo-backed support?
6. Which output would a human reviewer struggle to trust?
7. Which `chain-of-command/<name>/AGENT.md` or `SKILL.md` should be edited before the next benchmark?
8. Which KUJO tool was skipped without a strong enough fallback?
9. Did any implementation happen in a non-KUJO language when KUJO was required?
10. Which artifact would make the next benchmark easier to compare?

## Self-Improvement Patch Template

Use this when converting benchmark findings into agent updates:

```markdown
# Agent Chain Improvement Patch

## Benchmark Run

- Campaign:
- Date:
- Score:
- Verdict:

## Problem Observed

- Agent or doc:
- Evidence:
- Impact:

## Proposed Agent Change

- File:
- Current weakness:
- New instruction:
- Why this is reusable:

## Validation

- Rerun benchmark section:
- Expected improvement:
```
