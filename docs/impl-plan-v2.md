# Phase 4: Implementation Plan — Python Source File Scanner

## Overview
This document breaks down the Python Source File Scanner implementation into discrete, ordered tasks with clear dependencies, file locations, and completion criteria.

**Target Completion**: Phase 5 (Implementation)  
**Tech Stack**: Python 3.10+, standard library only  
**Coding Standards**: See `.claude/instructions/coding.md`

---

## Task Dependency Graph

```
TASK-1: Project Setup & Module Structure
    ↓
TASK-2: UserInterface Module
TASK-3: DirectoryScanner Module
TASK-4: MarkdownGenerator Module
TASK-5: FileWriter Module
    ↓ (all depend on TASK-1)
TASK-6: Main Orchestrator & Error Handling
    ↓ (depends on all utility modules)
TASK-7: End-to-End Testing
    ↓
TASK-8: Documentation & Code Quality
```

---

## Detailed Task List

### TASK-1: Project Setup & Module Structure

**ID**: TASK-1  
**Title**: Initialize project structure and base modules  
**Description**:  
Create the project directory structure, set up module files, and establish the base framework for the implementation.

**Deliverables**:
- Create `src/` directory
- Create empty module files: `src/main.py`, `src/ui.py`, `src/scanner.py`, `src/markdown.py`, `src/writer.py`
- Create `tests/` directory for test modules
- Add module-level docstrings to all modules
- Add Python 3.10+ shebang and future imports where needed

**Files Touched**:
- `src/main.py`
- `src/ui.py`
- `src/scanner.py`
- `src/markdown.py`
- `src/writer.py`
- `tests/` (new directory)

**Dependencies**: None  
**Blocked**: No  
**Estimated Complexity**: Low  

**Acceptance Criteria**:
- [ ] All source files exist in `src/`
- [ ] All test files created in `tests/`
- [ ] Each module has a module-level docstring
- [ ] Directory structure matches architecture specification

---

### TASK-2: UserInterface Module

**ID**: TASK-2  
**Title**: Implement user interaction (prompts, error/success messages)  
**Description**:  
Implement the `UserInterface` class with methods for directory input, error/success messaging. Must validate directory existence and type.

**Deliverables**:
- `UserInterface.get_directory_path() -> str`: Prompt user for directory path, validate it exists and is a directory, return absolute path. Re-prompt on invalid input (loop until valid or user interrupts).
- `UserInterface.display_error(message: str) -> None`: Print error with "Error:" prefix.
- `UserInterface.display_success(message: str) -> None`: Print success with "✓" prefix.
- Full type hints and docstrings per coding standards

**Files Touched**:
- `src/ui.py`

**Dependencies**: TASK-1  
**Blocked**: No  
**Estimated Complexity**: Low  

**Acceptance Criteria**:
- [ ] `get_directory_path()` validates existence and type
- [ ] Re-prompts on invalid input
- [ ] Error and success messages formatted correctly
- [ ] All methods have type hints and docstrings
- [ ] Handles edge cases: empty input, whitespace-only input, symlinks

---

### TASK-3: DirectoryScanner Module

**ID**: TASK-3  
**Title**: Implement recursive directory scanning for Python files  
**Description**:  
Implement the `DirectoryScanner` class with recursive directory walk. Must exclude hidden directories, skip inaccessible directories with warnings, never follow symlinks, and normalize paths to POSIX format.

**Deliverables**:
- `DirectoryScanner.scan_directory(root_path: str) -> List[str]`: Recursively walk directory, return all `.py` files relative to root (POSIX-style), exclude hidden dirs, skip inaccessible with warnings. Raise `FileNotFoundError` if root doesn't exist.
- `DirectoryScanner.is_hidden_directory(path: str) -> bool`: Return True if directory name starts with `.` or is `__pycache__`.
- Error handling: Catch `OSError`/`PermissionError` on subdirectories, log warning, continue scanning.
- Full type hints and docstrings

**Files Touched**:
- `src/scanner.py`

**Dependencies**: TASK-1  
**Blocked**: No  
**Estimated Complexity**: Medium  

**Acceptance Criteria**:
- [ ] Recursively discovers all `.py` files
- [ ] Excludes hidden directories (`.git`, `.github`, `__pycache__`)
- [ ] Returns POSIX-style relative paths (forward slashes)
- [ ] Handles permission errors gracefully (skip with warning, continue)
- [ ] Raises `FileNotFoundError` for nonexistent root
- [ ] Uses `os.walk(followlinks=False)` to avoid symlink loops
- [ ] Paths sorted for consistent output

---

### TASK-4: MarkdownGenerator Module

**ID**: TASK-4  
**Title**: Implement Markdown generation with hierarchical structure  
**Description**:  
Implement the `MarkdownGenerator` class to transform a flat list of Python file paths into hierarchical Markdown with nested headers by directory depth.

**Deliverables**:
- `MarkdownGenerator.generate_markdown(file_list: List[str]) -> str`: Input is sorted list of relative paths (POSIX-style). Output is formatted Markdown with nested headers (`#`, `##`, `###`, etc.) organized by directory, files listed as bullet points.
- `MarkdownGenerator.build_hierarchy(files: List[str]) -> Dict`: Build intermediate nested dictionary structure from file list.
- Example output format (from architecture):
  ```markdown
  # src
  
  ## models
  - user.py
  - product.py
  
  # tests
  - test_main.py
  ```
- Handle edge case: empty file list → return Markdown header "# Python Files" with message "No Python files found."
- Full type hints and docstrings

**Files Touched**:
- `src/markdown.py`

**Dependencies**: TASK-1  
**Blocked**: No  
**Estimated Complexity**: Medium  

**Acceptance Criteria**:
- [ ] Generates hierarchical headers based on directory depth
- [ ] Files listed as bullet points under parent directory
- [ ] Output matches example format from architecture
- [ ] Handles empty file list gracefully
- [ ] Handles deeply nested directories (maintains header depth correctly)
- [ ] No hardcoded paths or OS-specific separators in output

---

### TASK-5: FileWriter Module

**ID**: TASK-5  
**Title**: Implement safe Markdown file output  
**Description**:  
Implement the `FileWriter` class to write Markdown content to disk safely, with unconditional overwrite per requirements.

**Deliverables**:
- `FileWriter.write_markdown(file_path: str, content: str) -> None`: Write content to file_path. Overwrite existing files without prompting. Raise `IOError` if write fails (permissions, disk full, invalid path).
- Use context managers (`with` statements) for safe file handling
- Ensure absolute path is passed; validate before writing
- Full type hints and docstrings

**Files Touched**:
- `src/writer.py`

**Dependencies**: TASK-1  
**Blocked**: No  
**Estimated Complexity**: Low  

**Acceptance Criteria**:
- [ ] Writes Markdown content to specified file path
- [ ] Overwrites existing files without prompting
- [ ] Uses context managers for safe file handling
- [ ] Raises `IOError` on write failure
- [ ] Handles edge cases: invalid paths, permission denied

---

### TASK-6: Main Orchestrator & Error Handling

**ID**: TASK-6  
**Title**: Implement main orchestrator and error handling flow  
**Description**:  
Implement the `main()` function that orchestrates the workflow (from architecture pseudocode) with comprehensive error handling per the design review.

**Deliverables**:
- `main()` function that:
  1. Instantiates all modules (UserInterface, DirectoryScanner, MarkdownGenerator, FileWriter)
  2. Calls `ui.get_directory_path()` to get root directory
  3. Calls `scanner.scan_directory(root)` to get file list
  4. Calls `generator.generate_markdown(files)` to generate content
  5. Constructs output path: `os.path.join(root, "generated_files.md")`
  6. Calls `writer.write_markdown(output_path, content)` to write file
  7. Calls `ui.display_success(...)` with full path to output file
- Error handling per pseudocode from design review:
  - `ValueError` from `get_directory_path()`: Display error, re-prompt or exit (per team decision)
  - `FileNotFoundError`/`NotADirectoryError`: Display error, exit with code 1
  - `IOError` from `write_markdown()`: Display error, exit with code 1
- Module instantiation at top of main()
- All error messages user-friendly (no raw exception traces)

**Files Touched**:
- `src/main.py`

**Dependencies**: TASK-2, TASK-3, TASK-4, TASK-5 (all utility modules must exist)  
**Blocked**: No  
**Estimated Complexity**: Medium  

**Acceptance Criteria**:
- [ ] Instantiates all modules correctly
- [ ] Follows exact flow from architecture pseudocode
- [ ] Error handling matches design review pseudocode
- [ ] Output path construction correct: `os.path.join(root, "generated_files.md")`
- [ ] Success message includes full output file path
- [ ] Exit codes: 0 on success, 1 on unrecoverable error
- [ ] No bare `except:` clauses

---

### TASK-7: Comprehensive Test Suite

**ID**: TASK-7  
**Title**: Write unit and integration tests  
**Description**:  
Implement test modules using `unittest` framework with coverage of all components and integration scenarios.

**Deliverables**:
- **tests/test_ui.py**: Test UserInterface
  - Valid directory input
  - Nonexistent directory (should re-prompt or raise)
  - Empty/whitespace input (should re-prompt)
  
- **tests/test_scanner.py**: Test DirectoryScanner
  - Recursive discovery of `.py` files in nested structure
  - Exclusion of hidden directories (`.git`, `.github`, `__pycache__`)
  - Exclusion of files in hidden directories
  - Empty directory (no files found) returns empty list
  - Nonexistent root raises `FileNotFoundError`
  - Permission denied on subdirectory: skip with warning, continue
  - Symlinks: not followed, treated as regular files
  - Sorted output (consistent ordering)
  - POSIX-style relative paths (forward slashes)

- **tests/test_markdown.py**: Test MarkdownGenerator
  - Flat directory structure (single `#` header, files as bullets)
  - Nested directory structure (multiple header levels)
  - Empty file list (no Python files found message)
  - Deeply nested directories (header depth correct)
  - Files with special characters in names
  - Example output matches architecture spec

- **tests/test_writer.py**: Test FileWriter
  - Write to valid path
  - Overwrite existing file (no prompt)
  - Write to directory with no permissions (raise `IOError`)
  - Write to full disk (simulate with mock)

- **tests/test_integration.py** (optional): End-to-end test
  - Create temporary directory with mixed files
  - Run full scan→generate→write flow
  - Verify output file exists and contains expected content

**Files Touched**:
- `tests/test_ui.py`
- `tests/test_scanner.py`
- `tests/test_markdown.py`
- `tests/test_writer.py`
- `tests/test_integration.py` (optional)

**Dependencies**: TASK-2, TASK-3, TASK-4, TASK-5  
**Blocked**: No  
**Estimated Complexity**: High  

**Acceptance Criteria**:
- [ ] All tests run: `python -m unittest discover tests/ -v`
- [ ] Test coverage >80% (use `coverage` tool if available)
- [ ] No skipped tests
- [ ] All edge cases from requirements/architecture covered
- [ ] Tests use `tempfile.TemporaryDirectory()` for filesystem tests
- [ ] No hardcoded OS paths in assertions
- [ ] Mocking used for permission errors, disk-full scenarios

---

### TASK-8: Documentation & Code Quality

**ID**: TASK-8  
**Title**: Final code review, documentation, and quality checks  
**Description**:  
Verify code quality, completeness of docstrings, adherence to coding standards, and overall readiness for Phase 5 code review.

**Deliverables**:
- **Code Quality Checks**:
  - All functions have type hints (PEP 484)
  - All public functions have Google-style docstrings
  - No bare `except:` clauses
  - No hardcoded paths or magic numbers
  - Line length ≤100 characters
  - PEP 8 compliance
  - No unused imports or variables

- **Security Verification**:
  - No `eval()`, `exec()`, `compile()` on file contents
  - `os.walk(followlinks=False)` used
  - Symlinks handled per spec
  - User input validated at boundaries
  - No subprocess with `shell=True`

- **Testing Verification**:
  - All tests pass
  - Coverage >80%
  - Edge cases covered

- **Documentation**:
  - README.md (if not already present) with usage instructions
  - All modules have docstrings
  - Comments only for non-obvious logic

**Files Touched**:
- All files in `src/` and `tests/`
- `README.md` (if needed)

**Dependencies**: TASK-1 through TASK-7  
**Blocked**: No  
**Estimated Complexity**: Low–Medium  

**Acceptance Criteria**:
- [ ] All code quality checks pass
- [ ] All tests pass with >80% coverage
- [ ] Security checks complete
- [ ] Documentation complete
- [ ] Code ready for Phase 5 peer review

---

## Summary

| Task ID | Title | Status | Complexity | Dependencies |
|---------|-------|--------|-----------|--------------|
| TASK-1 | Project Setup & Module Structure | Ready | Low | None |
| TASK-2 | UserInterface Module | Ready | Low | TASK-1 |
| TASK-3 | DirectoryScanner Module | Ready | Medium | TASK-1 |
| TASK-4 | MarkdownGenerator Module | Ready | Medium | TASK-1 |
| TASK-5 | FileWriter Module | Ready | Low | TASK-1 |
| TASK-6 | Main Orchestrator & Error Handling | Ready | Medium | TASK-2,3,4,5 |
| TASK-7 | Comprehensive Test Suite | Ready | High | TASK-2,3,4,5 |
| TASK-8 | Documentation & Code Quality | Ready | Low–Medium | TASK-1–7 |

---

## Blocked Tasks

**None.** All tasks are ready to begin. No missing information or unresolved design decisions remain.

---

## Implementation Notes

1. **Sequential Dependencies**: Tasks should be completed in order. TASK-1 must complete before any other task starts. Tasks 2–5 are independent of each other but all depend on TASK-1. TASK-6 depends on all of 2–5.

2. **Testing Strategy**: Tests should be written alongside implementation (TDD encouraged). Tests for TASK-3 (DirectoryScanner) will be most complex due to filesystem mocking.

3. **Code Organization**: All production code in `src/`, all tests in `tests/`. Use absolute imports from `src/` modules.

4. **Coding Standards**: All code must comply with `.claude/instructions/coding.md`. No exceptions.

5. **Estimated Duration**: ~1–2 hours of focused development, depending on implementation experience and testing rigor.

---

## Document Metadata

- **Written by**: Claude Haiku 4.5
- **Date**: 2026-10-02
- **Phase**: 4 (Implementation Planning)
- **Status**: Pending Approval
