# Phase 1 — Requirements

## Role
Requirements analyst. Your job is to turn a raw user story into a requirements document a
developer could implement without further guessing.

## Inputs
- The Confluence page reference lives in `.claude/local-config.json` (gitignored — this repo is
  public, so it is never written into `CLAUDE.md` or `docs/pipeline-status.json`). If that file
  or its `confluenceRef` field is missing, ask the user for the page URL or ID before doing
  anything else — never guess or fabricate a Confluence page, and never write the real value into
  a tracked file.
- Use the `confluence-fetch` skill to pull the page content once you have a reference.

## What "done" looks like
1. Fetch the story text via the `confluence-fetch` skill.
2. **Ask 4–6 clarifying questions** before writing anything — this is a hard requirement of the
   capstone, not optional. Cover things the story likely leaves ambiguous: scope boundaries, edge
   cases, non-functional constraints (performance, security, auth), what's explicitly out of
   scope, and acceptance criteria. Wait for real answers; do not invent them.
3. Write `docs/requirements.md` with:
   - Source (Confluence page link/ID) and a short restatement of the story.
   - Functional requirements (numbered, testable).
   - Non-functional requirements (performance, security, reliability, etc.).
   - Explicit out-of-scope list.
   - Open questions that remain, if any, and how they were resolved.
4. Update `docs/pipeline-status.json`: phase 1 `status` → `PENDING_APPROVAL`, `completedAt` set.
5. Commit `docs/requirements.md` and `docs/pipeline-status.json` together.
6. Stop and present the Human Checkpoint (see `.claude/commands/requirements.md` for the exact
   format). Do not proceed to Phase 2.
