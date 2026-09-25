# Phase 3 — Design Review

## Role
Independent senior reviewer of the architecture — not the same reasoning that wrote it.

## Precondition
Phase 2 (`architecture`) must be `APPROVED`.

## What "done" looks like
1. Delegate to the `design-reviewer` subagent (fresh context, read-only) to review
   `docs/architecture.md` and `docs/requirements.md` for:
   - Risks (scalability, security, single points of failure).
   - Gaps (requirements not addressed by the design).
   - Alternatives worth considering, with tradeoffs.
2. Collect the subagent's findings and decide, for each: accept as-is, patch the architecture, or
   flag as an open risk to carry forward.
3. Write `docs/design-review.md`: findings, decisions made, and rationale.
4. If any finding requires a design change, patch `docs/architecture.md` directly and note the
   change in `design-review.md` (don't leave the two documents contradicting each other).
5. Update `docs/pipeline-status.json`: phase 3 → `PENDING_APPROVAL`.
6. Commit and stop for the Human Checkpoint.
