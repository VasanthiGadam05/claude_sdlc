---
description: Phase 2 — design the system, write docs/architecture.md and .claude/instructions/coding.md
---

Read `.claude/instructions/phase-2-architecture.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 1 (`requirements`) `decision` is not
   `APPROVED` — tell the user to run `/approve-phase 1 APPROVED` first.
2. Set phase 2 `status` → `IN_PROGRESS`.
3. Read `docs/requirements.md`.
4. Produce the architecture per the instructions file (components, data flow, tech stack + why,
   interfaces, security, error handling/observability).
5. Write `docs/architecture.md`.
6. Write `.claude/instructions/coding.md` (tech-stack-specific coding standards for Phase 5,
   scoped with an `applyTo`-style header).
7. Update `docs/pipeline-status.json`: phase 2 → `PENDING_APPROVAL`, `completedAt` set.
8. Commit: `docs: phase 2 architecture`.
9. Print the Human Checkpoint (same format as Phase 1, phase name "Architecture", artifact
   `docs/architecture.md`, commands `/approve-phase 2 APPROVED` / `REJECTED "<reason>"`).
10. Stop.
