<!-- applyTo: docsync/**, tests/**, .githooks/**, scripts/** -->
# Coding Standards — Automated Documentation Sync (Python Source Listing)

Written by `/architecture` (Phase 2) based on the tech stack chosen in `docs/architecture.md`.
Scopes Phase 5 (`/implement`) and anything touching the same paths afterward (Phase 6/7 review and
verification also hold code in these paths to this bar).

## Language & Style

- Python 3.11+, standard library only at runtime — no third-party runtime dependencies. `pytest`
  is a dev/test-only dependency.
- Full type hints on all function signatures (`from __future__ import annotations` at the top of
  each module if needed for forward references).
- Use `pathlib.Path` for all filesystem paths — never raw string concatenation. Always emit
  forward-slash relative paths in `SOURCE_FILES.md` output regardless of host OS (NFR4): convert
  with `path.as_posix()`, not manual string replacement.
- No bare `except:` — catch the specific exception types you expect (`OSError`,
  `UnicodeDecodeError`, `PermissionError`), per the two-tier error model in `docs/architecture.md`.
- Keep `docsync/render.py` a pure function module: no filesystem or logging calls in it, so it
  stays trivially unit-testable and guarantees the determinism required by NFR1.

## Security Rules

- Never `import`, `exec`, `eval`, or `compile()` a scanned `.py` file's contents (NFR3) — the
  scanner only opens files to path-check/read-check them, never to parse or run them as code.
- Never use `subprocess` with `shell=True`. The `.githooks/pre-commit` hook and
  `scripts/install_git_hooks.py` invoke `python` / `git` via argument lists, not shell strings.
- Always resolve discovered paths relative to the scan root with `Path.relative_to`; never let a
  discovered path escape `root` into the listed output.
- No secrets, tokens, or credentials anywhere in this codebase (this repo is public — see root
  `CLAUDE.md`). This tool has no reason to ever need one.

## Error Handling Conventions

- Per-file/per-directory failures (unreadable file, permission error walking a subdirectory,
  broken symlink) must be caught at the point of failure, converted to a warning string, and must
  never propagate out of `scanner.scan` — a single bad file must never fail the whole run (FR8,
  NFR2).
- Only a genuine usage error — `root` doesn't exist or isn't a directory — should produce a
  non-zero exit code from `cli.main`. Validate this once, explicitly, before scanning starts;
  don't let it surface as an unhandled exception.
- Use the standard `logging` module (`WARNING` for per-file skips, `INFO` for the final summary
  line) — no print-based debugging left in committed code.

## Testing Conventions

- `pytest`, with one test module per source module (`tests/test_scanner.py`,
  `tests/test_render.py`, `tests/test_cli.py`).
- Use `tmp_path` for any test that touches the filesystem — never write test fixtures into the
  real repo tree, and never assume a particular OS path separator in assertions.
- Cover at minimum: recursive discovery, each default-excluded directory name, the "zero files
  found" case (FR9), an unreadable-file case that still returns the other files with a warning
  (FR8), and a byte-identical-rerun determinism check (NFR1).
- No network access and no dependency on the real `.git` directory in unit tests; hook-level
  behavior (staging via `git add`) is covered as an integration test that inits a throwaway repo
  under `tmp_path`.
