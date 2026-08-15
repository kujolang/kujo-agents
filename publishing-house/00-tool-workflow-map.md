# Publishing House Tool And Workflow Map

This map binds each role to the narrowest implemented tools and composed workflows. A binding is capability scope, not approval or permission. The selected workflow may narrow it further.

## Tool ownership

| Tool | Owns | Never substitutes for |
| --- | --- | --- |
| StoryDesk | Ideas, campaigns, commissions, assignments, queue state, packets, handoffs | Editorial judgment, approval, publication |
| Dossier | Claims, sources, captured evidence, conflicts, quotations, consent, rights, freshness | Legal advice, approval, publication |
| GalleyPack | Exact artifact versions, lineage, evidence/review attachments, frozen packages, checksums | Review judgment, approval, publication |
| BluePencil | Structured editorial reviews, blockers, disagreement, quality calibration | Human approval or source rewriting |
| AssetWorks | Media plans, supported transforms, accessibility artifacts, provenance, manifests | Rights, consent, approval, publication |
| VersionSeal | Exact-version human approval decisions, revocation, expiry, verification | Content creation or publication effect |
| PressWire | Approval-gated schedule/publish/correct/unpublish effects and receipts | Approval, indexing, delivery, audience outcome |
| ReaderSignal | Privacy-bounded measurements, feedback, comparisons, learning, follow-up recommendations | Causation, commissioning, approval |

## Role bindings

| Role | Allowed Publishing House tools | Composed workflows |
| --- | --- | --- |
| Publisher | StoryDesk, Dossier | House Governance |
| Editor-in-Chief | StoryDesk, BluePencil, GalleyPack | House Governance, Editorial Review |
| Managing Editor | StoryDesk | House Governance, Daily Desk, Post-Publication Learning |
| Editorial Strategy Director | StoryDesk, Dossier, ReaderSignal | Commissioning, Post-Publication Learning |
| Brand Strategy Director | StoryDesk, Dossier, BluePencil | Commissioning, Editorial Review |
| Director of Editorial Intelligence | Dossier, ReaderSignal, StoryDesk | Evidence Dossier |
| Creative Director | StoryDesk, GalleyPack, AssetWorks | Commissioning, Primary Piece, Adaptation |
| Commissioning Editor | StoryDesk, Dossier | Daily Desk, Commissioning |
| Features Writer | StoryDesk, Dossier, GalleyPack | Primary Piece |
| Technical Editor & Writer | StoryDesk, Dossier, GalleyPack | Primary Piece |
| Campaign Copywriter | StoryDesk, Dossier, GalleyPack | Primary Piece |
| Art Director | AssetWorks, Dossier, GalleyPack | Asset Production, Adaptation, Format Production |
| Developmental Editor | BluePencil, GalleyPack, StoryDesk | Primary Piece, Editorial Review |
| Copy Chief | BluePencil, GalleyPack, StoryDesk | Editorial Review, Adaptation, Format Production |
| Standards & Evidence Editor | Dossier, BluePencil, GalleyPack | Evidence Dossier, Editorial Review, Adaptation, Format Production |
| Franchise & Adaptation Editor | StoryDesk, Dossier, GalleyPack, BluePencil | Adaptation |
| Audience Development Director | StoryDesk, ReaderSignal, PressWire | Post-Publication Learning, Adaptation |
| Production Editor | GalleyPack, AssetWorks, Dossier, BluePencil, VersionSeal | Daily Desk, Asset Production, Adaptation, Format Production, Approval and Publication |
| Publishing Operations Director | VersionSeal, PressWire, GalleyPack, StoryDesk | Approval and Publication |
| Newsletter Editor | StoryDesk, Dossier, GalleyPack, BluePencil | Format Production |
| Social & Community Editor | StoryDesk, Dossier, GalleyPack, BluePencil, ReaderSignal | Format Production, Post-Publication Learning |
| Case Study Editor | StoryDesk, Dossier, GalleyPack, BluePencil | Format Production |
| Video & Audio Producer | AssetWorks, Dossier, GalleyPack, BluePencil | Asset Production, Format Production |

## Lifecycle

```text
House Governance -> Daily Desk -> Commissioning -> Evidence Dossier -> Primary Piece
Primary Piece -> Asset Production
Primary Piece + Asset Production -> Editorial Review
Reviewed primary work -> Adaptation -> Format Production -> Editorial Review as required
Editorial Review -> Approval and Publication -> Post-Publication Learning
Post-Publication Learning -> future StoryDesk input
```

The runnable kits and exact bindings live in `../kujo-workflows/publishing-house-*/workflow.json`. Resolve and validate the selected workflow before acting. Fixture proof demonstrates deterministic integration; live adapters remain operator-configured and must fail closed when unavailable.
