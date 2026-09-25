---
description: Phase 1 — turn the Confluence user story into docs/requirements.md
---

Read `.claude/instructions/phase-1-requirements.md` and follow it exactly.

Steps:
1. Read `docs/pipeline-status.json`. Phase 1 has no precondition (it's the first phase), but if
   its `status` is already `PENDING_APPROVAL` or its `decision` is `APPROVED`, tell the user and
   ask whether they want to re-run it (re-running overwrites `docs/requirements.md`).
2. Check `userStory.ref` in `docs/pipeline-status.json` and `CLAUDE.md`'s Sources section. If
   still `TBD`/`null`, ask the user for the Confluence page URL or ID now — do not guess.
3. Set phase 1 `status` → `IN_PROGRESS`, `startedAt` → current time (ask the user for today's
   date/time if you have no other source, or use the `git log` clock — do not fabricate a
   timestamp silently without a real source).
4. Use the `confluence-fetch` skill to pull the story content.
5. Ask the clarifying questions required by the instructions file. Wait for the user's answers.
6. Write `docs/requirements.md` per the instructions file's required sections.
7. Update `docs/pipeline-status.json`: phase 1 `status` → `PENDING_APPROVAL`, `completedAt` set,
   `userStory.ref` set to the Confluence reference used.
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
