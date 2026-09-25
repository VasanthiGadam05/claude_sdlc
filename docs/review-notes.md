# Phase 6 — Review Notes

Reviewer: `code-reviewer` subagent (independent, fresh context — did not write the implementation).
Scope: `git diff main feat/docsync` (9 commits, merge-base `bc3f34a`), full reads of `docsync/*.py`,
`.githooks/pre-commit`, `scripts/install_git_hooks.py`, `.gitattributes`, and all four test modules.
Verified against `docs/requirements.md`, `docs/architecture.md`, `docs/design-review.md`,
`docs/impl-plan.md`, and `.claude/instructions/coding.md`. The reviewer ran the real test suite and
a manual two-run idempotency check rather than assuming correctness from reading code alone.

## 1. Correctness — Pass (one minor gap, fixed)

Traced the full happy path end to end: `cli.main` validates root (tier 2) → `scanner.scan` walks
with `os.walk(onerror=...)`, applies `DEFAULT_EXCLUDES` (exact match) + `fnmatch(*.egg-info)`, skips
symlinked files without dereferencing (`is_symlink()` checked before any read), probes
readability/UTF-8 decodability, sorts and returns POSIX-relative paths → `render.render_markdown`
(pure, no I/O) produces the FR9 "no files found" variant when empty → `cli.main` writes
`SOURCE_FILES.md` with tier-3 write-failure handling → returns 0.

All of FR1–FR9 are satisfied. FR4/FR5 (fixed filename, full regeneration) were manually verified
byte-identical across two consecutive runs (`diff run1.md run2.md` → identical), confirming NFR1.
The three error tiers match `docs/architecture.md` exactly. The hook's interpreter fallback
(`.githooks/pre-commit`) probes that a candidate interpreter actually *runs* (not just that it's on
PATH) — stricter than the spec required.

**Gap found and fixed during this review:** `.githooks/pre-commit`'s `git add
"$REPO_ROOT/SOURCE_FILES.md"` call did not check its own exit status before `exit 0`. A failed
staging attempt (e.g. an index lock held by another process) would have silently violated FR7 —
the doc would regenerate but not be staged into the triggering commit, exactly the drift FR7 exists
to prevent. **Fixed**: the hook now captures `$?` after `git add` and blocks the commit with a
clear stderr message if staging failed. Re-ran `tests/test_hook_integration.py` after the fix — both
tests still pass.

## 2. Security — Pass

- No hardcoded secrets in the diff (grepped for password/secret/token/api-key/private-key patterns;
  only hit was the string `secret.py`, a test fixture filename, not a credential).
- No `shell=True` anywhere; `scripts/install_git_hooks.py` uses `subprocess.run` with an argument
  list.
- `scanner.py` never executes or imports scanned file content — only a bounded 8KB binary
  read-probe (NFR3).
- All output paths are contained via `Path.relative_to(root)` — no path can escape `root` in the
  report.
- Symlinked files are skipped before any read is attempted; `os.walk`'s default
  `followlinks=False` means symlinked directories are never recursed into either.
- Shell hook variables are all quoted (`"$REPO_ROOT"`, `"$PYTHON"`, `"$DOCSYNC_EXIT"`); the
  interpreter loop only iterates a fixed literal list, so there's no injection surface.
- No sensitive/gitignored file (e.g. `.claude/local-config.json`) appears in this diff.

## 3. Error Handling — Pass

Tier 1 (`os.walk(onerror=...)` + narrow per-file `except (OSError, UnicodeDecodeError)`), tier 2
(`cli.py` root-is-directory check), and tier 3 (`cli.py`'s `write_text` wrapped in `except OSError`)
all match the architecture doc, with no bare `except:` and no silent swallowing. The hook correctly
captures and propagates `docsync`'s real exit code rather than collapsing it to a generic failure.
The one unhandled failure path (`git add`'s exit status, see §1) has been fixed.

## 4. Test Coverage — Pass

Real suite run: **20 passed, 2 skipped** (`python -m pytest -v`).

- `tests/test_scanner.py`: recursive discovery, each of the 7 `DEFAULT_EXCLUDES` entries
  individually (parametrized), the `*.egg-info` glob, the zero-files case, and sorted/POSIX-path
  output. Assertions check actual exclusion (file absent from result), not just "didn't crash."
- The 2 skips are legitimate environment gates, not disabled coverage: the chmod-based unreadable-file
  test skips only on `win32` (Windows ACLs don't map to POSIX chmod bits); the symlink test attempts
  the real `symlink_to` first and only skips if the environment actually lacks the privilege.
- `tests/test_cli.py` exercises all three tiers, including a monkeypatched `Path.write_text` failure
  that actually drives the tier-3 except branch.
- `tests/test_render.py` covers non-empty/empty output, byte-identical determinism, and confirms
  `render_markdown` never touches the filesystem.
- `tests/test_hook_integration.py` runs a real `git init` + real commit end-to-end and asserts both
  file content and that it was actually staged (`git show --stat HEAD`) — a genuine integration
  check of FR6/FR7, not a mock.

**Follow-up (non-blocking):** no test exercises `scanner.py`'s `os.walk(onerror=...)` tier-1
directory-permission-error path (design-review G6's specific scenario — an unlistable
subdirectory). Recommend adding a Windows-skippable test that makes a subdirectory unlistable and
asserts a warning is produced without aborting the scan.

## 5. Code Clarity — Pass

Files are small and single-purpose; names match their architectural roles (`scan`,
`render_markdown`, `main`, `_is_excluded_dir`, `_confirm_readable_text`). `render.py`'s `del root`
(kept for interface symmetry with `scanner.scan`, but unused since content is paths-only per FR3)
is called out with a one-line comment that makes the intent immediately clear. `cli.py` reads
top-to-bottom exactly like the architecture doc's data-flow diagram. No unnecessary or misleading
comments anywhere in the diff.

## 6. DRY Principle — Pass

No meaningful duplication in production code — `scanner.py`, `render.py`, `cli.py` each own a
distinct, non-overlapping responsibility.

**Follow-up (non-blocking):** the "try `python3`, probe it actually runs, fall back to `python`"
logic exists once in the shell hook and once (independently, in Python) in
`tests/test_hook_integration.py::_require_working_hook_interpreter`. Not practical to share across
languages, but the two could drift if the hook's probe logic changes without updating the test
guard to match.

## 7. Dependency Safety — Pass

Confirmed via imports in every touched file: stdlib only (`os`, `fnmatch`, `pathlib`, `dataclasses`,
`argparse`, `logging`, `shutil`, `stat`, `subprocess`, `sys`). No `requirements.txt`,
`pyproject.toml`, or `setup.py`/`setup.cfg` exists in the repo or was added by this branch. `pytest`
remains an ambient dev-tool, never declared as a runtime dependency, consistent with
`docs/architecture.md`'s Tech Stack table. No new third-party dependency was introduced.

## Overall Recommendation: **Approve**

All 7 checklist points pass. FR1–FR9 and the three-tier error model are correctly implemented and
match the approved architecture/design-review/impl-plan documents. The one issue found
(`git add` exit status unchecked in the pre-commit hook) was small and unambiguous, and has been
fixed and re-verified in this same review pass.

**Required follow-ups** (do not block this approval, but should be addressed before the feature is
considered fully hardened):
- Add a test for `scanner.py`'s `os.walk(onerror=...)` tier-1 directory-permission-error path
  (design-review G6).

**Non-blocking notes:**
- Minor, unavoidable duplication of interpreter-probe logic between `.githooks/pre-commit` and
  `tests/test_hook_integration.py`.
