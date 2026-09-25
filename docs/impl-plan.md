# Implementation Plan — Automated Documentation Sync

Derived from `docs/architecture.md` (as patched by `docs/design-review.md`) and
`.claude/instructions/coding.md`. Tasks are ordered so every dependency precedes its dependents.
None are blocked — Phase 3 resolved all open design questions, so Phase 5 (`/implement`) can run
this list straight through.

| ID | Title | Description | Depends on | Files touched | Status |
|---|---|---|---|---|---|
| T1 | Scaffold `docsync` package | Create `docsync/` as an importable package (`__init__.py`), empty `scanner.py`/`render.py`/`cli.py`/`__main__.py` stubs. | — | `docsync/__init__.py`, `docsync/scanner.py`, `docsync/render.py`, `docsync/cli.py`, `docsync/__main__.py` | Ready |
| T2 | Implement `scanner.scan` | `ScanResult` dataclass (`paths: list[str]`, `warnings: list[str]`); recursive `os.walk` from `root`; `DEFAULT_EXCLUDES` matched by exact name for fixed dirs and `fnmatch` for the `*.egg-info` glob (design-review G1); per-file read-check probe (open + confirm UTF-8-decodable prefix); skip symlinked files without dereferencing, recorded as a warning (design-review R8); permission errors on any directory — including the root's own top-level listing (design-review G6) — caught as tier-1 warnings, never raised past `scan`; paths returned sorted and POSIX-style via `Path.relative_to(root).as_posix()` (FR1, FR2, FR3, FR8, NFR1, NFR4). | T1 | `docsync/scanner.py` | Ready |
| T3 | Implement `render.render_markdown` | Pure function `(root, paths) -> str`; standard listing for non-empty `paths`; explicit "no Python source files were found" variant when `paths` is empty (FR3, FR9); no I/O, no logging (NFR1). | T1 | `docsync/render.py` | Ready |
| T4 | Implement `cli.main` | Parse `argv` (`ROOT` optional, defaults to cwd); validate `ROOT` exists and is a directory — the one genuine tier-2 usage error, non-zero exit (architecture Error Handling tier 2); call `scanner.scan`, log each warning at `WARNING`; call `render.render_markdown`; write `SOURCE_FILES.md` at `ROOT`, catching write failures (`OSError`/`PermissionError`) as the tier-3 error from design-review G3 — non-zero exit, no silent swallow; log the final one-line `INFO` summary; return `0` on success (including zero-files/some-skipped cases) (FR4, FR5, NFR2, NFR3). | T2, T3 | `docsync/cli.py` | Ready |
| T5 | Implement `__main__` shim | Thin `python -m docsync` entry point delegating to `cli.main()` and calling `sys.exit` with its return code. | T4 | `docsync/__main__.py` | Ready |
| T6 | Unit tests — scanner | `tests/test_scanner.py` using `tmp_path`: recursive discovery; each default-excluded directory name individually, plus the `*.egg-info` glob case; zero-`.py`-files case; an unreadable file still returns the rest with a warning; a symlinked file is skipped with a warning and its target is never read; sorted/POSIX-path output. | T2 | `tests/test_scanner.py` | Ready |
| T7 | Unit tests — render | `tests/test_render.py`: deterministic output for a fixed path list; the empty-`paths` "no files found" variant (FR9); byte-identical output across two calls with the same input (NFR1). | T3 | `tests/test_render.py` | Ready |
| T8 | Unit tests — cli | `tests/test_cli.py` using `tmp_path`: invalid root returns non-zero exit code with a clear stderr message; a normal run writes `SOURCE_FILES.md` with expected content and returns `0`; a simulated write failure (e.g. root replaced with a read-only target, or monkeypatched write) returns non-zero per the tier-3 rule. | T4, T5 | `tests/test_cli.py` | Ready |
| T9 | `.githooks/pre-commit` | POSIX shell script: resolve repo root via `git rev-parse --show-toplevel` (design-review G2); resolve interpreter, trying `python3` then falling back to `python`, failing clearly only if neither exists (design-review R2); run `<interpreter> -m docsync <repo-root>`; on a non-zero `docsync` exit, block the commit (tier 2/3 errors); otherwise `git add SOURCE_FILES.md` (FR7) and exit `0`. | T5 | `.githooks/pre-commit` | Ready |
| T10 | `scripts/install_git_hooks.py` | One-time setup script: if `.git/hooks/pre-commit` already exists, copy it to `.git/hooks/pre-commit.bak` and print a warning before overwriting (design-review R3); copy `.githooks/pre-commit` into `.git/hooks/pre-commit`; mark it executable (`os.chmod`). | T9 | `scripts/install_git_hooks.py` | Ready |
| T11 | `.gitattributes` entry | Add `SOURCE_FILES.md -text` so Git never renormalizes the generated file's line endings across platforms (design-review R6 / NFR1, NFR4). | — | `.gitattributes` | Ready |
| T12 | Integration test — hook | `tests/test_hook_integration.py`: `git init` a throwaway repo under `tmp_path`, run `scripts/install_git_hooks.py` against it (including the backup-existing-hook path), create a `.py` file, `git commit`, assert `SOURCE_FILES.md` exists and was staged into that commit. No network access, no dependency on the real repo's `.git` (coding.md Testing Conventions). | T9, T10 | `tests/test_hook_integration.py` | Ready |
| T13 | Full-suite verification pass | Run the complete `pytest` suite; manually re-run `python -m docsync` twice against an unchanged tree and diff the two `SOURCE_FILES.md` outputs to confirm byte-identical (NFR1); confirm each `DEFAULT_EXCLUDES` entry (including `*.egg-info`) is actually excluded end-to-end. This is validation, not new code — feeds directly into Phase 7 (`/verify`). | T6, T7, T8, T12 | — | Ready |

## Execution order

T1 → T2, T3 (parallel-safe, both only depend on T1) → T4 → T5 → T6, T7 (parallel-safe) → T8 → T9 →
T10, T11 (parallel-safe) → T12 → T13.

## Notes for Phase 5 (`/implement`)

- Branch: create/switch to `feat/docsync` before touching any files (per `.claude/instructions/phase-5-implement.md`).
- Every rule cited above by design-review ID (R2, R3, R6, R8, G1, G2, G3, G6) is also already
  encoded in `.claude/instructions/coding.md` — that file is the binding spec if this plan and
  `coding.md` ever appear to disagree.
- No task is blocked; if Phase 5 discovers a need to deviate from this task list, it should pause
  and flag it rather than silently improvising (per the coding.md / phase-5 instructions).
