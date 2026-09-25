---
description: Phase 5 — implement the approved plan on a feature branch
---

Read `.claude/instructions/phase-5-implementation.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 4 (`impl-plan`) `decision` is not
   `APPROVED`.
2. Set phase 5 `status` → `IN_PROGRESS`.
3. Check the current git branch. If not already on a `feat/<story-slug>` branch, create one off
   `main` and switch to it. Record the branch name in `docs/pipeline-status.json`'s `repo.branch`.
4. Read `docs/impl-plan.md` and `.claude/instructions/coding.md`.
5. Execute the plan's tasks in dependency order, one at a time. Stop and ask the user if you hit a
   decision the plan doesn't cover — don't guess.
6. Commit implementation work as you go (small, logical commits) following the secret-scan hook's
   constraints (no hardcoded credentials).
7. Update `docs/pipeline-status.json`: phase 5 → `PENDING_APPROVAL`, `completedAt` set. There is no
   `docs/*.md` artifact for this phase.
8. Print the Human Checkpoint (phase name "Implementation", artifact "code on `<branch>`",
   commands `/approve-phase 5 APPROVED` / `REJECTED "<reason>"`).
9. Stop.
