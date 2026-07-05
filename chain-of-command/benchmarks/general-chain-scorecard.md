# KUJO Agent Chain Benchmark Scorecard

Use this scorecard after running a campaign through the General Commander. It measures whether the agent chain actually behaved like a coordinated system instead of one large model improvising everything.

Score each category from `0` to `3`.

- `0`: missing or harmful.
- `1`: attempted but unclear, incomplete, or weakly evidenced.
- `2`: usable, mostly correct, minor gaps.
- `3`: strong, clear, evidenced, reusable.

Maximum score: `45`.

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
| Security/risk review |  | Path, secret, host-effect, release, or data risks were considered |
| Documentation quality |  | Usage/docs/handoff were accurate and source-grounded |
| Evidence packaging |  | Commands, artifacts, changed files, receipts, and status were easy to inspect |
| Jidoka behavior |  | The chain stopped or escalated on abnormalities instead of hiding them |
| Triple-win alignment |  | Outcome helped the user, agents/team, and reusable KUJO ecosystem |
| Retrospective quality |  | Suggested concrete improvements to the agent definitions or workflow |

## Verdict Bands

| Score | Verdict |
|---:|---|
| 0-17 | Broken chain: roles are not coordinating reliably |
| 18-29 | Partial chain: useful output, but handoffs or evidence are weak |
| 30-39 | Working chain: usable for supervised real work |
| 40-45 | Strong chain: repeatable, auditable, and ready for harder campaigns |

## Retrospective Questions

After scoring, answer:

1. Which agent had unclear authority?
2. Which handoff lost context?
3. Which worker instruction was too broad?
4. Which verification step was missing or late?
5. Which tool was recommended without enough repo-backed support?
6. Which output would a human reviewer struggle to trust?
7. Which `chain-of-command/<name>/AGENT.md` or `SKILL.md` should be edited before the next benchmark?

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
