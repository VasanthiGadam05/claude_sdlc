# Architecture — Automated Documentation Sync (Python Source Listing)

Based on `docs/requirements.md` (FR1–FR9, NFR1–NFR5). This is a small, dependency-free local tool
plus a Git hook — there is no server, database, or external API in this design, so several of the
usual architecture sections (data storage, external integrations) are intentionally thin.

## Components

- **`docsync/scanner.py`** — walks a root directory, applies the default exclusion list (FR2),
  and returns a sorted list of relative `.py` paths plus a list of warnings for files that
  couldn't be read (FR8). Owns all filesystem-walking and per-file error handling.
- **`docsync/render.py`** — pure function that turns `(root, sorted relative paths)` into the
  exact Markdown text for `SOURCE_FILES.md` (FR3, FR9). No I/O — just string building, which makes
  it trivially unit-testable and guarantees determinism (NFR1).
- **`docsync/cli.py`** — entry point (`python -m docsync [ROOT]`). Validates `ROOT` is a real
  directory (a genuine usage error, unlike per-file errors), calls the scanner then the renderer,
  writes `SOURCE_FILES.md` at `ROOT` (FR4, FR5), logs warnings, and prints a one-line summary.
- **`docsync/__main__.py`** — thin `python -m docsync` shim delegating to `cli.main()`.
- **`.githooks/pre-commit`** — the Git pre-commit hook script (FR6). Runs
  `python -m docsync <repo-root>`, then `git add SOURCE_FILES.md` (FR7) so the regenerated
  listing is staged into the same commit, then exits 0 so the commit always proceeds — per-file
  scan failures are already absorbed inside `docsync` (FR8/NFR2), so the hook itself has nothing
  left to fail on except "Python isn't on PATH", which is a genuine environment problem worth
  blocking on.
- **`scripts/install_git_hooks.py`** — one-time setup script a developer runs after cloning; copies
  `.githooks/pre-commit` into `.git/hooks/pre-commit` and marks it executable. Resolves Open
  Question #3 from `docs/requirements.md`: hook installation is an explicit opt-in script rather
  than something that runs automatically on clone (Git has no reliable "on clone" hook point, and
  silently installing a hook that intercepts every commit without the developer's knowledge would
  be surprising).

## Data Flow

```
developer runs `git commit`
        │
        ▼
.git/hooks/pre-commit  (installed copy of .githooks/pre-commit)
        │  invokes
        ▼
python -m docsync <repo-root>
        │
        ├─ cli.main(root)
        │     ├─ validate root is an existing directory  ──(fails)──▶ exit 1, commit blocked
        │     │                                                        (genuine usage error)
        │     ├─ scanner.scan(root, DEFAULT_EXCLUDES)
        │     │     → sorted relative .py paths, warnings[]
        │     ├─ log warnings[] to stderr (non-fatal, FR8/NFR2)
        │     ├─ render.render_markdown(root, paths) → markdown text
        │     └─ write markdown text to <root>/SOURCE_FILES.md  (full overwrite, FR5)
        │
        ▼
hook runs `git add SOURCE_FILES.md`   (FR7)
        │
        ▼
hook exits 0  →  commit proceeds with the regenerated, staged SOURCE_FILES.md
```

## Tech Stack

| Choice | Rationale |
|---|---|
| Python 3.11+, standard library only (`pathlib`, `os`, `argparse`, `logging`) | The tool's whole job is to describe a Python project's source files; zero runtime dependencies means nothing to pin, vendor, or audit, and keeps NFR3 (no code execution) trivially true — there's no import machinery involved at all. |
| `pytest` (dev/test dependency only, not a runtime dependency) | Standard, minimal-boilerplate test runner; matches the testing conventions in `.claude/instructions/coding.md`. |
| Plain POSIX shell script for `.githooks/pre-commit` | Git for Windows ships Git Bash, so a `#!/usr/bin/env sh` hook runs unmodified on Windows, macOS, and Linux (NFR4) without needing a compiled launcher. |
| No packaging/distribution (no `pip install`, no PyPI publish) | Out of scope per `docs/requirements.md`; this is a single-repo tool invoked via `python -m docsync`, not a distributed package. |

## Key Interfaces

- `scanner.scan(root: Path, exclude_dirs: frozenset[str] = DEFAULT_EXCLUDES) -> ScanResult`
  where `ScanResult` is a small dataclass: `paths: list[str]` (sorted, POSIX-style relative paths,
  NFR1/NFR4) and `warnings: list[str]` (one per skipped file, human-readable).
- `render.render_markdown(root: Path, paths: list[str]) -> str` — pure, deterministic; returns the
  "no files found" variant (FR9) when `paths` is empty.
- `cli.main(argv: list[str] | None = None) -> int` — returns a process exit code; `0` on success
  (including the zero-files and some-files-skipped cases), non-zero only if `root` itself is not a
  valid directory.
- CLI surface: `python -m docsync [ROOT]` — `ROOT` optional, defaults to the current working
  directory.

## Security Considerations

- **No code execution (NFR3).** The scanner only uses `pathlib`/`os` filesystem calls to find and
  read-check `.py` files; it never `import`s, `exec`s, or otherwise runs any scanned file's
  content. This matters because the whole point of the tool is to walk arbitrary, possibly
  untrusted source trees.
- **Read-check, not content parsing.** "Unreadable/undecodable" (FR8) is detected by attempting to
  open and read the file's bytes and confirm UTF-8 decodability of a small prefix — never by
  parsing it as Python (no `ast.parse`, no `compile`).
- **Path containment.** All discovered paths are computed relative to `root` via
  `Path.relative_to`; the scanner never follows a discovered path outside `root` (guards against a
  symlink inside the tree pointing elsewhere and leaking unrelated filesystem structure into the
  committed `SOURCE_FILES.md`).
- **No secrets in scope.** The tool touches only file *paths*, never file *contents* of the
  scanned files beyond a read-access probe — so there's no scenario where secret material embedded
  in a `.py` file ends up copied into `SOURCE_FILES.md`.

## Error Handling & Observability

- **Two error tiers, matching FR8/NFR2:**
  1. *Per-file/per-directory errors* (permission denied on a subdirectory, an unreadable file,
     a broken symlink) are caught at the point of failure, turned into a warning string, and
     scanning continues. These never raise past `scanner.scan`.
  2. *Tool-level usage errors* (root path doesn't exist or isn't a directory) are real failures:
     `cli.main` returns a non-zero exit code and prints a clear message to stderr. This is the only
     case where the pre-commit hook should actually block a commit.
- **Logging.** Uses the standard `logging` module: warnings (tier 1) at `WARNING` level to
  stderr; a final one-line summary ("Wrote SOURCE_FILES.md: N files listed, M skipped") at `INFO`
  level. No logging framework/config beyond `logging.basicConfig` — this is a short-lived CLI
  invocation, not a long-running service.
- **Idempotency check.** Because `render.render_markdown` is a pure function over a sorted input
  list, NFR1 (byte-identical re-runs) falls out of the design rather than needing special-casing.
