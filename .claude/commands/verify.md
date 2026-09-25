---
description: Phase 7 — run tests and a docs content-quality check, write docs/verification-report.md
---

Read `.claude/instructions/phase-7-verify.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 6 (`review`) `decision` is not
   `APPROVED`.
2. Set phase 7 `status` → `IN_PROGRESS`.
3. Delegate to the `qa-verifier` subagent to fill test gaps, run the full suite, and check every
   `docs/*.md` artifact for missing sections/placeholder text/consistency.
4. Write `docs/verification-report.md` with real command output (not paraphrased) and the
   docs-quality findings.
5. Update `docs/pipeline-status.json`: phase 7 → `PENDING_APPROVAL`, `completedAt` set.
6. Commit: `docs: phase 7 verification report`.
7. Print the Human Checkpoint (phase name "Verify", artifact `docs/verification-report.md`,
   commands `/approve-phase 7 APPROVED` / `REJECTED "<reason>"`).
8. Stop.
