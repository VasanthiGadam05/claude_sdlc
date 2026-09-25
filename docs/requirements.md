# Requirements — Automated Documentation Sync (Python Source Listing)

## Source

Confluence, page title **"User Story"**. The real page link is not committed to this public
repo — see `.claude/local-config.json` (`confluenceRef`, gitignored) and `CLAUDE.md`'s Sources
section for how to resolve it.

**Story:** As a developer, I want the application to scan Python source files and generate a
Markdown document listing them, so that I can quickly understand what source files are present
in the project.

This requirements document expands that one-line story into a concrete, testable spec, based on
clarifying answers from the human product owner (recorded under Open Questions below).

## Functional Requirements

1. **FR1 — Recursive scan.** The tool SHALL recursively scan a given root directory for all files
   ending in `.py`.
2. **FR2 — Default exclusions.** The tool SHALL exclude files located under conventional
   non-source directories by default, at minimum: `.venv/`, `venv/`, `__pycache__/`, `.git/`,
   `node_modules/`, `build/`, `dist/`, `*.egg-info/`.
3. **FR3 — Markdown listing content.** The tool SHALL generate a Markdown document listing the
   path of each discovered `.py` file, relative to the scanned root. Only the relative path is
   listed per entry — no line counts, docstrings, or other metadata (explicitly deferred, see
   Out of Scope).
4. **FR4 — Fixed output location.** The tool SHALL write the generated Markdown document to a
   fixed filename, `SOURCE_FILES.md`, at the root of the scanned directory.
5. **FR5 — Full regeneration.** Every run SHALL fully regenerate `SOURCE_FILES.md` from scratch
   (complete overwrite). There is no incremental/append mode; two runs against an unchanged tree
   MUST produce byte-identical output.
6. **FR6 — Pre-commit trigger.** The tool SHALL run automatically via a Git pre-commit hook,
   before each commit is finalized.
7. **FR7 — Auto-stage the regenerated doc.** After regenerating `SOURCE_FILES.md`, the pre-commit
   hook SHALL stage it (`git add`) so the updated listing is included in the same commit that
   triggered the regeneration — otherwise the doc silently drifts out of sync with the commit it
   was meant to describe. (See Open Questions — this was not explicitly asked and is called out
   for reviewer sign-off.)
8. **FR8 — Per-file read failures are non-fatal.** If a discovered `.py` file cannot be read or
   decoded (e.g. permission error, invalid encoding), the tool SHALL skip that file, log a warning
   naming the file and the reason, and continue scanning the rest. It SHALL NOT abort the commit.
9. **FR9 — Empty result is valid.** If zero `.py` files are found under the root after exclusions,
   the tool SHALL still write a valid `SOURCE_FILES.md` that states no Python source files were
   found, rather than erroring out or leaving a stale file in place.

## Non-Functional Requirements

1. **NFR1 — Determinism.** Output ordering must be stable (e.g. sorted paths) so re-runs against
   an unchanged tree are byte-identical (supports FR5's idempotency requirement and makes the hook
   diff-friendly in `git diff`).
2. **NFR2 — Non-blocking on partial failure.** A single unreadable file must never fail the whole
   commit (ties to FR8) — only a failure of the tool itself (e.g. it can't run at all) should
   block a commit.
3. **NFR3 — Local execution, no code execution risk.** The tool only reads file contents to detect
   `.py` files and list their paths; it MUST NOT import, exec, or otherwise execute any scanned
   Python file's code.
4. **NFR4 — Cross-platform paths.** Relative paths in the Markdown output must use a consistent
   separator (forward slash) regardless of host OS, since the hook may run on Windows, macOS, or
   Linux developer machines.
5. **NFR5 — Reasonable performance.** No numeric SLA was specified by the product owner; the tool
   must not introduce a perceptible delay to a normal developer commit for a typical project-sized
   tree (low thousands of files).

## Out of Scope

- Non-Python source files (`.pyi`, `.ipynb`, etc.) — only `.py` is in scope.
- Any per-file metadata beyond the relative path: no line counts, no docstring extraction, no
  last-modified timestamps (explicitly rejected in favor of the simplest listing).
- CI-based triggering (e.g. running in a pipeline on push/PR) — the product owner chose a Git
  pre-commit hook instead; CI execution is not part of this feature.
- User-configurable exclusion lists or output paths — both are fixed/hardcoded per the product
  owner's answers (default exclusion list, fixed `SOURCE_FILES.md` name). Making either
  configurable is a possible future enhancement, not part of this story.
- Hook installation tooling (e.g. auto-installing the hook into `.git/hooks/` on clone) is not
  addressed by this story; only the hook's *behavior* once installed is in scope. (Flagged again
  under Open Questions for Phase 2 to decide how the hook actually gets installed.)

## Open Questions and Resolutions

1. **Should the regenerated `SOURCE_FILES.md` be auto-staged into the triggering commit?** Not
   explicitly asked. Resolved as **yes** (FR7) — an "Automated Documentation Sync" pre-commit hook
   that regenerates a doc but leaves it unstaged would let the doc drift out of sync with the very
   commit it's meant to describe, defeating the point of the story. Flagged for explicit reviewer
   sign-off during `/design-review`, since it's an assumption rather than a direct product-owner
   answer.
2. **Exact output filename.** Not explicitly asked. Resolved as `SOURCE_FILES.md` at the scanned
   root (FR4) as a reasonable, predictable default. Reviewer may rename during design review.
3. **How the hook itself gets installed** (manual copy, a setup script, a packaged hook manager
   like `pre-commit`) is deferred to Phase 2 (`/architecture`), since it's a tech-stack/tooling
   decision rather than a behavioral requirement.
4. All other ambiguities (trigger mechanism, scan depth, default exclusions, output location,
   listing detail, regeneration/error behavior) were resolved directly by the product owner — see
   FR1–FR9 above, which encode those answers.
