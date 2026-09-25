---
description: Orchestrate the SDLC phases in sequence, stopping for a human checkpoint after each one
argument-hint: "[--from N] [--to N]"
---

Runs phases in order, but **never skips the human checkpoint** — this command still stops after
every phase for a real `/approve-phase` decision; it does not auto-approve anything.

Arguments: `$ARGUMENTS` — optional `--from N` / `--to N` to bound the range (default: from the
first `NOT_STARTED`/not-yet-approved phase, through phase 8).

Steps:
1. Read `docs/pipeline-status.json`.
2. Validate `--from`/`--to` if given (1-8, from <= to).
3. Determine the starting phase: the lowest-numbered phase in range whose `decision` is not
   `APPROVED` (resume logic — skip already-approved phases silently, just note them as "already
   approved, skipping").
4. Run that phase's command logic in-line (i.e. do exactly what `/requirements`, `/architecture`,
   etc. would do for that phase number — reuse the same steps, don't duplicate divergent logic).
5. After writing the artifact and setting `status` → `PENDING_APPROVAL`, **stop** and print the
   Human Checkpoint exactly as that phase's command would.
6. Do not proceed to the next phase automatically. The user must run `/approve-phase` (or
   re-invoke `/pipeline` after approving, which will then pick up the next unapproved phase).
7. If invoked after all phases in range are `APPROVED`, report "Range complete" (if `--to` given)
   or "Pipeline complete" (if range covers through phase 8).
