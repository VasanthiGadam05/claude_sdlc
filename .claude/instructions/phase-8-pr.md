# Phase 8 — PR

## Role
PR author, using Agent Mode-equivalent autonomy (Claude Code tool use + `gh` CLI) to open the pull
request against the existing target GitHub repo.

## Precondition
Phase 7 (`verify`) must be `APPROVED`. The GitHub remote must be configured (`git remote -v` shows
`origin`) — if not, check `.claude/local-config.json`'s `githubRemote` field; if that's also
missing, stop and ask the user for the repo URL rather than guessing it. Never write the real
remote URL into `docs/pipeline-status.json` or any other tracked file — this repo is public.

## What "done" looks like
1. Confirm the feature branch (from Phase 5) has all work committed; push it to `origin`.
2. Build the PR body from the accumulated docs artifacts, with these 5 sections **exactly**:
   - **Summary** — what this PR does and why (from `requirements.md`).
   - **Changes Made** — key changes (from `impl-plan.md` + the actual diff).
   - **Test Evidence** — real output from `verification-report.md`.
   - **Known Limitations** — anything called out in `review-notes.md` / `verification-report.md`.
   - **Reviewer Checklist** — the 7-point checklist from `review-notes.md`, each with its verdict.
3. Use the `github-pr-creator` skill to run `gh pr create --body-file`, but **ask the user for
   explicit confirmation before that call runs** — this is a second, independent confirmation on
   top of the Phase 7→8 approval gate, because creating a PR is a hard-to-reverse, externally
   visible action.
4. Capture the PR URL. Update `docs/pipeline-status.json`: phase 8 → `PENDING_APPROVAL`.
5. Commit and present the final Human Checkpoint. After phase 8 is approved, the pipeline is
   complete.
