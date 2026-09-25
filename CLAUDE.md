# Agentic SDLC Capstone — Automated Documentation Sync

This repo is a Claude Code implementation of the "Automated Documentation Sync" capstone: an
8-phase agentic SDLC pipeline — requirements → architecture → design review → implementation
planning → implementation → review → verify → PR — with a mandatory human-review checkpoint
after every phase. The assignment was originally written for GitHub Copilot; everything here is
built from scratch for Claude Code, project-local (nothing depends on globally installed agents
or plugins).

## Copilot → Claude Code concept mapping

| GitHub Copilot capstone concept | Claude Code equivalent |
|---|---|
| Copilot Chat/CLI | Claude Code interactive session (this CLI) |
| Custom chat modes / agents | Project subagents in `.claude/agents/*.md` (peer-reviewer personas) |
| Prompts (reusable prompt files) | Project slash commands in `.claude/commands/*.md` |
| Instructions (`copilot-instructions.md` + scoped `*.instructions.md`) | This file (always-on) + `.claude/instructions/phase-N-*.md` (per-phase rules) |
| Agent Mode (autonomous edit+run, PR creation) | Normal Claude Code tool use (Read/Edit/Bash) + `gh` CLI, wrapped by the `github-pr-creator` skill |
| Hooks | `.claude/settings.json` hooks calling PowerShell scripts in `.claude/hooks/*.ps1` |
| Skills | `.claude/skills/*/SKILL.md` — reusable mechanics not tied to one phase |

## Pipeline state

`docs/pipeline-status.json` is the single source of truth for where the pipeline is. Each of the
8 phases has a `status` (`NOT_STARTED` → `IN_PROGRESS` → `PENDING_APPROVAL` → `APPROVED`/`REJECTED`)
and a `decision`/`decidedAt`/`reason` recorded once a human reviews it.

## THE HARD RULE

**Every phase produces exactly one artifact and then stops.** Do not start the next phase until
`docs/pipeline-status.json` shows the previous phase's `decision` as `APPROVED`. This is enforced
two ways:
1. Each phase command checks the previous phase's status itself before doing any work.
2. `.claude/hooks/phase-gate.ps1` (wired via `PreToolUse` in `.claude/settings.json`) blocks the
   `Write`/`Edit` of a phase artifact, or `gh pr create`, if the gate isn't satisfied — even if a
   command forgets to check.

Never skip this gate, and never edit `pipeline-status.json` to fake an approval — only
`/approve-phase` (a real human decision) may flip a phase to `APPROVED`/`REJECTED`.

## Commands

- `/requirements`, `/architecture`, `/design-review`, `/impl-plan`, `/implement`, `/review`,
  `/verify`, `/create-pr` — one per phase. Each reads its matching
  `.claude/instructions/phase-N-*.md` for detailed rules.
- `/pipeline [--from N] [--to N]` — runs phases in sequence, still stopping for a real human
  checkpoint after every phase.
- `/approve-phase N [APPROVED|REJECTED] [reason]` — the only command allowed to advance
  `pipeline-status.json`.

## Docs layout

- `docs/requirements.md`, `docs/architecture.md`, `docs/design-review.md`, `docs/impl-plan.md`,
  `docs/review-notes.md`, `docs/verification-report.md` — one per phase artifact.
- `docs/pipeline-status.json` — orchestration state (see above).
- `docs/README.md` — pipeline index.
- `.claude/instructions/coding.md` — written by `/architecture` once a tech stack is chosen;
  scopes language/security/testing rules for whatever gets implemented in Phase 5.

## Sources (fill in when known — never guess these)

- **User story**: Confluence — page link: `TBD`
- **GitHub remote**: `TBD` (set via `git remote add origin <url>` once provided)

## Security

Never hardcode credentials. Secrets come from environment variables only. `git commit` is gated
by `.claude/hooks/secret-scan.ps1`, which blocks commits containing obvious secret patterns — but
that is a backstop, not a substitute for care.
