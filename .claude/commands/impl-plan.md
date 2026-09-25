---
description: Phase 4 — break the design into a dependency-ordered task list, write docs/impl-plan.md
---

Read `.claude/instructions/phase-4-impl-plan.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 3 (`design-review`) `decision` is
   not `APPROVED`.
2. Set phase 4 `status` → `IN_PROGRESS`.
3. Read `docs/architecture.md` and `docs/design-review.md`.
4. Break the work into tasks (ID, title, description, dependencies, files touched, blocked or
   ready) and order them so dependencies precede dependents.
5. Write `docs/impl-plan.md`.
6. Update `docs/pipeline-status.json`: phase 4 → `PENDING_APPROVAL`, `completedAt` set.
7. Commit: `docs: phase 4 implementation plan`.
8. Print the Human Checkpoint (phase name "Implementation Planning", artifact `docs/impl-plan.md`,
   commands `/approve-phase 4 APPROVED` / `REJECTED "<reason>"`).
9. Stop.
