# Phase 7 — Verify

## Role
QA engineer. Prove the implementation actually works, with real output — not a claim of success.

## Precondition
Phase 6 (`review`) must be `APPROVED`.

## What "done" looks like
1. Delegate to the `qa-verifier` subagent to:
   - Generate/complete unit and integration tests for the changed code, if coverage gaps remain
     from Phase 6.
   - Run the full test suite and capture the **actual** output verbatim (not a paraphrase).
   - Run a content-quality check over every `docs/*.md` artifact produced so far: no missing
     sections, no leftover placeholder text (`TBD`, `TODO`, `[fill in]`), internal consistency
     between `requirements.md` → `architecture.md` → `impl-plan.md`.
2. Write `docs/verification-report.md` with:
   - Test command(s) run and their real output (pass/fail counts, coverage if available).
   - Results of the docs content-quality check.
   - Any gaps found and whether they were fixed or are called out as known limitations.
3. Update `docs/pipeline-status.json`: phase 7 → `PENDING_APPROVAL`.
4. Commit and stop for the Human Checkpoint.
