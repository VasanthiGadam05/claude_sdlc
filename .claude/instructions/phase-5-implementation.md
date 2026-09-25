# Phase 5 — Implementation

## Role
Developer implementing exactly what the approved plan says — no scope creep, no unapproved
shortcuts.

## Precondition
Phase 4 (`impl-plan`) must be `APPROVED`.

## What "done" looks like
1. Ensure a feature branch exists and is checked out: `feat/<short-story-slug>` off `main`. Create
   it if it doesn't exist yet.
2. Read `docs/impl-plan.md` and `.claude/instructions/coding.md` (the tech-stack-specific
   standards written in Phase 2).
3. Execute the plan's tasks **in dependency order**, one at a time. For each task: implement it,
   then move to the next.
4. If you hit something not explicitly covered by the plan (a decision the plan didn't make),
   stop and ask the user rather than guessing.
5. Follow `.claude/instructions/coding.md` for style/security/error-handling/testing conventions.
6. When all tasks are complete, update `docs/pipeline-status.json`: phase 5 → `PENDING_APPROVAL`.
   There is no `docs/*.md` artifact for this phase — the artifact is the code itself (and the
   commit history on the feature branch).
7. Commit the implementation work, then stop for the Human Checkpoint.
