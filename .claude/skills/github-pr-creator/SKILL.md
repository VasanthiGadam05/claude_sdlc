---
name: github-pr-creator
description: Push the current feature branch and open a GitHub pull request via the gh CLI, given a filled PR body. Use this in Phase 8 (/create-pr) instead of calling gh directly, so the confirmation/body-file plumbing stays consistent.
---

# GitHub PR Creator

Given a completed PR body (the 5-section content: Summary, Changes Made, Test Evidence, Known
Limitations, Reviewer Checklist), push the branch and open the PR.

## Steps

1. Confirm `origin` is configured (`git remote -v`). If not, stop — the calling command is
   responsible for getting the URL from the user first; this skill never guesses a remote.
2. Confirm all work is committed (`git status --porcelain` empty on the feature branch). If not,
   stop and report what's uncommitted rather than committing on the skill's own judgement.
3. **Stop and let the calling command get explicit user confirmation before continuing** — this
   skill does not ask the user itself; it trusts the caller already did, per
   `.claude/instructions/phase-8-pr.md`.
4. Push the branch: `git push -u origin <branch>`.
5. Write the PR body to a temp file and run:
   `gh pr create --title "<title>" --body-file <tempfile> --base main --head <branch>`.
6. Capture and return the PR URL from `gh pr create`'s output.
7. Clean up the temp file.

## Notes

- Never use `--force` on the push.
- Never fabricate a title/body section that the caller didn't supply — if a required section
  (e.g. Test Evidence) is missing content, report that back rather than inventing filler text.
