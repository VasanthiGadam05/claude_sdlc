# Phase 6 — Review

## Role
Peer reviewer of the implementation — independent from the agent that wrote the code.

## Precondition
Phase 5 (`implement`) must be `APPROVED`.

## What "done" looks like
1. Delegate to the `code-reviewer` subagent (fresh context) to review the diff between `main` and
   the feature branch against this exact 7-point checklist — every point must get an explicit
   verdict, not a skip:
   1. **Correctness** — does the code do what `docs/impl-plan.md` / `docs/requirements.md` says?
   2. **Security** — secrets, injection, unsafe input handling, auth gaps.
   3. **Error Handling** — failure paths handled, no silent swallowing.
   4. **Test Coverage** — are the changed code paths actually tested?
   5. **Code Clarity** — naming, structure, readability.
   6. **DRY Principle** — unnecessary duplication.
   7. **Dependency Safety** — new/changed dependencies justified and not obviously risky.
2. Write `docs/review-notes.md`: one section per checklist point with the verdict and any issues
   found, plus an overall recommendation (approve / needs changes).
3. If issues are found, fix them now (before stopping) if they're small and unambiguous;
   otherwise list them as required follow-ups in `review-notes.md`.
4. Update `docs/pipeline-status.json`: phase 6 → `PENDING_APPROVAL`.
5. Commit and stop for the Human Checkpoint.
