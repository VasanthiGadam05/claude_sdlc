---
description: Phase 1 — turn the Confluence user story into docs/requirements.md
---

Read `.claude/instructions/phase-1-requirements.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Phase 1 has no precondition (it's the first phase), but if
   its `status` is already `PENDING_APPROVAL` or its `decision` is `APPROVED`, tell the user and
   ask whether they want to re-run it (re-running overwrites `docs/requirements.md`).
2. Check for `.claude/local-config.json` and its `confluenceRef` field. If missing (file absent,
   or the field is empty), ask the user for the Confluence page URL or ID now — do not guess, and
   never write the real value into `docs/pipeline-status.json` or any other tracked file (this
   repo is public — see `CLAUDE.md`'s Sources section). If the user gives you a new value, save it
   into `.claude/local-config.json` (creating it if needed) rather than a tracked file.
3. Set phase 1 `status` → `IN_PROGRESS`, `startedAt` → current time (ask the user for today's
   date/time if you have no other source, or use the `git log` clock — do not fabricate a
   timestamp silently without a real source).
4. Use the `confluence-fetch` skill to pull the story content.
5. Ask the clarifying questions required by the instructions file. Wait for the user's answers.
6. Write `docs/requirements.md` per the instructions file's required sections.
7. Update `docs/pipeline-status.json`: phase 1 `status` → `PENDING_APPROVAL`, `completedAt` set.
   Do **not** write the real Confluence URL into `userStory.ref` — leave it `null` and rely on
   `.claude/local-config.json` (gitignored) as the source of truth.
8. `git add docs/requirements.md docs/pipeline-status.json` and commit:
   `docs: phase 1 requirements`.
9. Print the Human Checkpoint:
   ```
   ┌─ Human Checkpoint: Phase 1 (Requirements) ─────────────┐
   │ Status: PENDING_APPROVAL                                │
   │ Artifact: docs/requirements.md                          │
   ├───────────────────────────────────────────────────────┤
   │ Review the artifact, then run one of:                   │
   │   /approve-phase 1 APPROVED                              │
   │   /approve-phase 1 REJECTED "<reason>"                   │
   └───────────────────────────────────────────────────────┘
   ```
10. Stop. Do not run `/architecture` yourself.
