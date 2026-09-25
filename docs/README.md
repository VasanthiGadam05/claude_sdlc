# Pipeline docs

This folder holds the artifacts produced by each phase of the agentic SDLC pipeline, plus the
pipeline's state file.

## Phase order

| # | Phase | Command | Artifact |
|---|-------|---------|----------|
| 1 | Requirements | `/requirements` | `requirements.md` |
| 2 | Architecture | `/architecture` | `architecture.md` |
| 3 | Design Review | `/design-review` | `design-review.md` |
| 4 | Implementation Planning | `/impl-plan` | `impl-plan.md` |
| 5 | Implementation | `/implement` | (code changes, no doc artifact) |
| 6 | Review | `/review` | `review-notes.md` |
| 7 | Verify | `/verify` | `verification-report.md` |
| 8 | PR | `/create-pr` | (GitHub PR, no doc artifact) |

Run the whole thing with `/pipeline`, or run phases individually. Either way, every phase stops
and waits for a human decision before the next phase is allowed to start.

## `pipeline-status.json`

The state file for the pipeline. Each phase has:
- `status`: `NOT_STARTED` → `IN_PROGRESS` → `PENDING_APPROVAL` → `APPROVED` / `REJECTED`
- `decision`, `decidedAt`, `reason`: set only by a human running `/approve-phase`

Approve a phase: `/approve-phase 1 APPROVED`
Reject a phase: `/approve-phase 2 REJECTED "reason text"` (leaves it re-runnable)

No command other than `/approve-phase` may write a phase's `decision` field.
