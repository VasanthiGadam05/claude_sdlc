# Phase 2 — Architecture

## Role
Senior software architect. Turn approved requirements into a concrete technical design.

## Precondition
`docs/pipeline-status.json` phase 1 (`requirements`) must have `decision == "APPROVED"`. If not,
refuse to proceed and tell the user to run `/approve-phase 1 APPROVED` first.

## What "done" looks like
1. Read `docs/requirements.md`.
2. Propose:
   - Components/modules and their responsibilities.
   - A data-flow description (text is fine; ASCII/mermaid diagram if it clarifies).
   - Tech stack choices with a one-line rationale each (language, frameworks, storage, external
     APIs).
   - Key interfaces/contracts between components.
   - Security considerations (auth, secret handling, input validation at boundaries).
   - Error handling strategy and observability (logging).
3. Write `docs/architecture.md` with the above.
4. Write `.claude/instructions/coding.md` — a scoped coding-standards file (language/style,
   security rules, error-handling conventions, testing conventions) for whatever gets built in
   Phase 5, based on the tech stack chosen here. Give it an `applyTo`-style header comment noting
   which paths it governs (e.g. `src/**`).
5. Update `docs/pipeline-status.json`: phase 2 → `PENDING_APPROVAL`.
6. Commit and stop for the Human Checkpoint.
