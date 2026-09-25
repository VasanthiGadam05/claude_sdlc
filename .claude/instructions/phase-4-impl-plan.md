# Phase 4 — Implementation Planning

## Role
Technical lead breaking the approved design into an executable task list.

## Precondition
Phase 3 (`design-review`) must be `APPROVED`.

## What "done" looks like
1. Read `docs/architecture.md` and `docs/design-review.md`.
2. Break the work into discrete tasks. For each task capture:
   - ID, short title, description.
   - Dependencies (which other task IDs must land first).
   - Files/components it touches.
   - Whether it's currently **blocked** (missing info, unresolved decision) or ready to start.
3. Order tasks so dependencies always precede dependents. Call out anything blocked and why —
   don't silently sequence around a blocker.
4. Write `docs/impl-plan.md` with the ordered task list.
5. Update `docs/pipeline-status.json`: phase 4 → `PENDING_APPROVAL`.
6. Commit and stop for the Human Checkpoint.
