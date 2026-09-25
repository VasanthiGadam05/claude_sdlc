---
description: Phase 6 — peer code review against the 7-point checklist, write docs/review-notes.md
---

Read `.claude/instructions/phase-6-review.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 5 (`implement`) `decision` is not
   `APPROVED`.
2. Set phase 6 `status` → `IN_PROGRESS`.
3. Delegate to the `code-reviewer` subagent with the diff between `main` and the feature branch as
   context. Require an explicit verdict on all 7 checklist points (Correctness, Security, Error
   Handling, Test Coverage, Code Clarity, DRY Principle, Dependency Safety).
4. Write `docs/review-notes.md` with each point's verdict/issues and an overall recommendation.
5. Fix small, unambiguous issues now; list anything bigger as a required follow-up.
6. Update `docs/pipeline-status.json`: phase 6 → `PENDING_APPROVAL`, `completedAt` set.
7. Commit: `docs: phase 6 review notes` (plus any fix commits).
8. Print the Human Checkpoint (phase name "Review", artifact `docs/review-notes.md`, commands
   `/approve-phase 6 APPROVED` / `REJECTED "<reason>"`).
9. Stop.
