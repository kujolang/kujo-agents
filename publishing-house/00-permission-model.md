# Publishing House Permission Model

Permission is a run input and an upper bound. A role contract may narrow it further.

## OBSERVE

May inspect provided profiles, sources, artifacts, history, and configured read-only evidence. May write its own local evidence and review artifacts. May not change an editorial artifact, status, approval, schedule, or external system.

## PROPOSE

Includes OBSERVE and may create briefs, strategies, drafts, edits, assets, reviews, manifests, and recommended status changes inside the authorized workspace. May not claim human approval or cause an external publication effect.

## ACT

Includes PROPOSE and only the explicitly named role-bounded actions in the run. Publishing Operations is the only current role with a maximum of ACT, and it may act only on an exact human-approved artifact version through a configured adapter. Credentials never imply authority.

Every run records role, mode, assignment ID, target, allowed actions, artifact versions, approval boundary, external effects, and receipts. Missing capability or authority produces one bounded blocker rather than repeated requests or silent degradation.
