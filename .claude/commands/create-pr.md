---
description: Phase 8 — push the branch and open the pull request
---

Read `.claude/instructions/phase-8-pr.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Refuse and stop if phase 7 (`verify`) `decision` is not
   `APPROVED`.
2. Check `git remote -v` for `origin`. If not set, check `.claude/local-config.json`'s
   `githubRemote` field; if that's also missing, ask the user for the GitHub repo URL now — do not
   guess. Run `git remote add origin <url>` if not already configured. Never write the real remote
   URL into `docs/pipeline-status.json` or any other tracked file (this repo is public).
3. Set phase 8 `status` → `IN_PROGRESS`.
4. Build the PR body with the 5 required sections (Summary, Changes Made, Test Evidence, Known
   Limitations, Reviewer Checklist) from the accumulated `docs/*.md` artifacts, following
   `.github/PULL_REQUEST_TEMPLATE.md`.
5. **Ask the user for explicit confirmation** before creating the PR — a second, independent
   check on top of the phase 7→8 approval gate.
6. On confirmation, use the `github-pr-creator` skill to push the branch and run
   `gh pr create --body-file`.
7. Update `docs/pipeline-status.json`: phase 8 → `PENDING_APPROVAL`, `completedAt` set, record the
   PR URL somewhere visible (e.g. echo it back to the user and note it in the checkpoint).
8. Commit the status update: `docs: phase 8 pr opened`.
9. Print the Human Checkpoint (phase name "PR", artifact "PR <url>", commands
   `/approve-phase 8 APPROVED` / `REJECTED "<reason>"`). Note that approving phase 8 marks the
   whole pipeline complete.
10. Stop.
