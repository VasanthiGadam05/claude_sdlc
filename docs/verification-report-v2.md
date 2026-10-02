# Phase 7: Verification Report (v2)

Branch: `feat/docsync-v2`. Python 3.12.5, pytest 8.3.5 on Windows.

## 1. Test run history

The v2 suite had never been run before this phase. Two earlier attempts hung and were stopped by their timeouts.

**Root cause of the hang:** `tests/test_cli.py::test_main_with_nonexistent_directory` patched `input` with a fixed `return_value`. `UserInterface.get_directory_path()` correctly re-prompts on an invalid path, so it looped forever on the same bad path.

**Defects found by actually running the suite (all fixed in this phase):**

| # | Defect | Fix |
|---|--------|-----|
| 1 | Hanging CLI test (above) | Replaced with `test_main_reprompts_on_nonexistent_then_succeeds`; added EOF and scanner-error exit-code tests |
| 2 | `display_success` raised `UnicodeEncodeError` on cp1252/piped stdout, so `main()` returned 1 after a successful write | `src/ui.py` falls back to `[OK]`; test added |
| 3 | `MarkdownGenerator` printed root-level files after sub-directory headings, so they appeared to belong to the wrong directory | `src/markdown.py` lists a level's files before its sub-directories; test added |
| 4 | No test for the permission-denied path | `test_scan_directory_permission_denied_subdir_is_skipped` added |

## 2. Final test run (verbatim)

Command: `python -m pytest tests -v -p no:cacheprovider`

```
collected 37 items
... (36 PASSED, 1 SKIPPED; full per-test listing reproduced by the command above)
tests/test_scanner.py::TestDirectoryScanner::test_scan_directory_skips_symlinked_files SKIPPED
======================== 36 passed, 1 skipped in 2.70s ========================
```

Coverage, command `python -m pytest tests -q --cov=src --cov-report=term-missing`:

```
Name              Stmts   Miss  Cover   Missing
src\main.py          32      3    91%   42-43, 50
src\markdown.py      31      0   100%
src\scanner.py       31      4    87%   56-57, 61-62
src\ui.py            27      5    81%   23-24, 39-41
src\writer.py         9      0   100%
TOTAL               130     12    91%
36 passed, 1 skipped in 4.15s
```

The 36 passed include 2 legacy `tests/test_hook_integration.py` tests, which target the old `docsync/` package. That file is pytest-style, so `python -m unittest` reports 0 tests for it.

## 3. Docs content-quality check

- Required sections: none missing across the five v2 docs.
- Placeholders: one `TBD` in `architecture-v2.md` (re-prompt vs. exit). The code re-prompts inside `UserInterface`.

**Discrepancies not fixed in this phase (earlier phases' approved artifacts):**

- `architecture-v2.md` and `design-review-v2.md` describe a `FileFilter` module (`filter.py`). It was never implemented and has no task in `impl-plan-v2.md`; the scanner does the filtering.
- `architecture-v2.md` main pseudocode catches `ValueError` and prints the check mark itself. The code has no such handler, and `display_success` adds the mark.
- Symlink policy conflicts: architecture and design review say symlinked files are "included otherwise"; `coding.md` and the code skip them with a warning.
- `review-notes-v2.md` overstated its claims. It said mixed root/sub-directory Markdown was "tested and verified" (it was wrong, defect 3), that permission-denied was covered by tests (there was none), and that all acceptance criteria were met without a test run. Treat the Phase 6 verdict as superseded by this report.
- `coding.md` names `tests/test_markdown.py`; the file is `tests/test_render.py`.

## 4. Known limitations

- A directory named `_files` crashes `generate_markdown` (`TypeError`), because `build_hierarchy` uses `"_files"` as a reserved key. `main()` returns 1 with "Unexpected error".
- The symlink test is skipped on this machine, so symlink skipping has no executed coverage.
- `EOFError` produces `Error: Unexpected error: ` with an empty detail. The exit code is correct.
- `scanner.py` wraps the walk in `except Exception`, against the `coding.md` rule to catch specific exceptions.
- Uncovered lines: `ui.py` 23-24, 39-41 (path-resolution error branches); `scanner.py` 56-57, 61-62 (symlink and broad-exception branches); `main.py` 42-43, 50.
