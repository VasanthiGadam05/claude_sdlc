---
description: Record a human APPROVED/REJECTED decision for a phase — the only command allowed to write decisions
argument-hint: <phase-number> <APPROVED|REJECTED> ["reason"]
---

This is the **only** command allowed to write a phase's `decision` field in
`docs/pipeline-status.json`. No phase command may set its own `decision`.

Arguments: `$ARGUMENTS` — expected as `<phase-number> <APPROVED|REJECTED> [reason]`.

Steps:
1. Parse the phase number and decision from `$ARGUMENTS`. Validate:
   - Phase number is 1-8.
   - Decision is exactly `APPROVED` or `REJECTED`.
   - If `REJECTED`, a reason string should be present; if missing, ask the user for one before
     proceeding.
2. Read `docs/pipeline-status.json`. Confirm the target phase's `status` is `PENDING_APPROVAL` —
   if it's `NOT_STARTED`, tell the user the phase hasn't run yet; if it's already decided, ask
   whether they want to overwrite the decision.
3. Set the phase's `decision` to `APPROVED` or `REJECTED`, `decidedAt` to now, and `reason` (null
   if approved and no reason given).
4. If `REJECTED`, also reset the phase's `status` back to `NOT_STARTED` so it can be re-run.
5. Commit: `chore: approve-phase <n> <decision>` (or `reject-phase`).
6. Report the outcome and the next action:
   - If `APPROVED` and phase < 8: name the next slash command to run (phase 1 → `/architecture`,
     phase 2 → `/design-review`, phase 3 → `/impl-plan`, phase 4 → `/implement`,
     phase 5 → `/review`, phase 6 → `/verify`, phase 7 → `/create-pr`).
   - If `APPROVED` and phase == 8: report "Pipeline complete."
   - If `REJECTED`: name the same phase's command to re-run once addressed.
