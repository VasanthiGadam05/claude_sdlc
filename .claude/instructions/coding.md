
<!-- applyTo: src/** -->
# Coding Standards — Python Source File Scanner (V2)

Written by `/architecture` (Phase 2) based on the tech stack chosen in `docs/architecture-v2.md`.
Scopes Phase 5 (`/implement`) and anything touching the same paths afterward (Phase 6/7 review and
verification also hold code in these paths to this bar).

## Language & Style

- Python 3.10+, standard library only — no external runtime dependencies.
- Full type hints on all function signatures per PEP 484.
- Use `pathlib.Path` for all filesystem paths — never raw string concatenation.
- Always emit forward-slash relative paths in output Markdown regardless of host OS: convert
  with `path.as_posix()`.
- Use f-strings for all string formatting (no `%` or `.format()`).
- Line length: 100 characters.
- No bare `except:` — catch specific exception types (`OSError`, `PermissionError`, 
  `FileNotFoundError`, `NotADirectoryError`).

## Security Rules

- Never `import`, `exec`, `eval`, or `compile()` scanned `.py` file contents — the scanner
  only reads paths, never executes code.
- Always validate user-provided directory paths with `Path.resolve()` to canonicalize and
  prevent path traversal attacks.
- Never follow symlinks during traversal: use `os.walk(followlinks=False)`.
- Never dereference symlinked files — check `Path.is_symlink()` first and skip them.
- Always resolve discovered paths relative to the scan root with `Path.relative_to()`;
  never let a discovered path escape the root directory into output.
- No secrets, tokens, or credentials in the codebase (repo is public per root `CLAUDE.md`).

## Error Handling Conventions

- Per-file/per-directory failures (permission denied, broken symlink) must be caught at the
  point of failure and logged as warnings — never propagate out of the scanner. A single bad
  file must never fail the whole run.
- Only genuine usage errors (invalid directory, permissions on root) should produce non-zero
  exit codes. Validate directory once, explicitly, before scanning starts.
- Use `print()` for user-facing messages (prompts, status, errors).
- Log skipped directories (hidden) to stdout for informational purposes.
- Error message format: "Error: [brief message]. [Actionable suggestion]"

## Testing Conventions

- Use `unittest` (standard library) with one test module per source module
  (`tests/test_scanner.py`, `tests/test_markdown.py`, `tests/test_writer.py`, `tests/test_ui.py`).
- Use `tempfile.TemporaryDirectory()` for any test touching the filesystem — never write
  fixtures into the real repo tree, never assume a particular OS path separator in assertions.
- Cover at minimum:
  - Recursive discovery with mixed file types.
  - Hidden directory exclusion (`.git`, `.github`, `__pycache__`).
  - Empty directory (no Python files found).
  - Permission denied case (should skip with warning).
  - Valid directory with nested structure.
  - Nonexistent directory (should raise `FileNotFoundError`).
- Run tests with: `python -m unittest discover tests/ -v`

## Code Organization

- Module files in `src/`: `main.py`, `ui.py`, `scanner.py`, `filter.py`, `markdown.py`, `writer.py`.
- Each module has a single responsibility (see `docs/architecture-v2.md` Components section).
- Test files in `tests/`: mirror source structure with `test_` prefix.
- Public interfaces clearly defined; private methods prefixed with `_`.

## Documentation

- Google-style docstrings for all public functions/classes.
- Include: description, Args, Returns, Raises.
- Avoid obvious comments; document WHY for non-obvious logic.
- Module-level docstrings for all modules.
