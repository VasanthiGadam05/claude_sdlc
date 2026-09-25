---
description: Phase 3 — independent review of the architecture, write docs/design-review.md
---

Read `.claude/instructions/phase-3-design-review.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 2 (`architecture`) `decision` is not
   `APPROVED`.
2. Set phase 3 `status` → `IN_PROGRESS`.
3. Delegate to the `design-reviewer` subagent (via the Agent tool) with `docs/architecture.md` and
   `docs/requirements.md` as context. Ask it to return risks, gaps, and alternatives.
4. Decide on each finding: accept, patch the architecture, or carry forward as an open risk.
5. Write `docs/design-review.md`. If the architecture changed, patch `docs/architecture.md` too
   and note it in `design-review.md`.
6. Update `docs/pipeline-status.json`: phase 3 → `PENDING_APPROVAL`, `completedAt` set.
7. Commit: `docs: phase 3 design review`.
8. Print the Human Checkpoint (phase name "Design Review", artifact `docs/design-review.md`,
   commands `/approve-phase 3 APPROVED` / `REJECTED "<reason>"`).
9. Stop.
