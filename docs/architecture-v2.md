# Phase 2: Architecture — Python Source File Scanner

## Overview
The Python Source File Scanner is a standalone CLI application that scans a user-specified directory tree, discovers all `.py` files (excluding hidden directories), and generates a Markdown document with a hierarchical listing.

---

## System Architecture

### Components & Responsibilities

#### 1. **UserInterface Module** (`ui.py`)
- **Responsibility**: Handle all user interactions.
- **Methods**:
  - `get_directory_path() -> str`: Prompt user for directory and validate it exists.
  - `display_error(message: str)`: Display error messages to user.
  - `display_success(message: str)`: Display success/completion messages.
- **Key Contract**: Returns an absolute path string or raises `ValueError` if invalid.

#### 2. **DirectoryScanner Module** (`scanner.py`)
- **Responsibility**: Recursively traverse directory tree and collect file paths.
- **Methods**:
  - `scan_directory(root_path: str) -> List[str]`: Recursively walk directory, return all `.py` file paths relative to root.
  - `is_hidden_directory(path: str) -> bool`: Check if a directory name starts with `.` or is `__pycache__`.
- **Key Contract**: Returns a sorted list of relative paths (forward slashes, POSIX-style).
- **Edge Cases**: Handles permission errors, symlink loops, non-existent directories.

#### 3. **FileFilter Module** (`filter.py`)
- **Responsibility**: Filter files based on criteria (extension, hidden status).
- **Methods**:
  - `is_valid_file(path: str) -> bool`: Return True if file is a `.py` file in a non-hidden directory.
- **Key Contract**: Reusable predicate for filtering.

#### 4. **MarkdownGenerator Module** (`markdown.py`)
- **Responsibility**: Transform file list into hierarchical Markdown structure.
- **Methods**:
  - `generate_markdown(file_list: List[str]) -> str`: Build Markdown content with nested headers by directory depth.
  - `build_hierarchy(files: List[str]) -> Dict`: Create a nested dictionary structure representing the directory tree.
- **Key Contract**: Returns a formatted Markdown string with proper headers, indentation, and links.
- **Format**:
  - Use `#` for top-level directories.
  - Use `##`, `###`, etc., for subdirectories.
  - List files as bullet points under their parent directory.

#### 5. **FileWriter Module** (`writer.py`)
- **Responsibility**: Write Markdown content to disk safely.
- **Methods**:
  - `write_markdown(file_path: str, content: str)`: Write content, overwrite without prompting.
- **Key Contract**: Raises `IOError` if write fails; no warnings for overwrite.

#### 6. **Main Orchestrator** (`main.py`)
- **Responsibility**: Coordinate workflow and error handling.
- **Flow**:
  1. Get directory from user via `UserInterface`.
  2. Scan directory via `DirectoryScanner`.
  3. Filter files via `FileFilter`.
  4. Generate Markdown via `MarkdownGenerator`.
  5. Write to file via `FileWriter`.
  6. Report success to user.

---

## Data Flow Diagram

```
User Input (Directory Path)
         ↓
  [UserInterface.get_directory_path()]
         ↓
  Path Validation (exists, is_dir)
         ↓
  [DirectoryScanner.scan_directory()]
         ↓
  Raw File List (all .py files)
         ↓
  [FileFilter.is_valid_file()]
         ↓
  Filtered File List (excludes hidden dirs)
         ↓
  [MarkdownGenerator.generate_markdown()]
         ↓
  Markdown Content (hierarchical)
         ↓
  [FileWriter.write_markdown()]
         ↓
  Output File (root_dir/generated_files.md)
         ↓
  Success Message to User
```

---

## Tech Stack Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Language** | Python 3.10+ | Standard for scripting and file operations; no external dependencies required. |
| **Directory Walking** | `os.walk()` | Standard library, efficient, handles directory traversal natively. |
| **Path Handling** | `pathlib.Path` | Modern, cross-platform path handling; cleaner API than `os.path`. |
| **CLI Framework** | Standard `input()` | MVP only; no heavy framework like Click/Typer needed. |
| **Markdown Generation** | String templates | Simple, no external library needed for static structure. |
| **Output Format** | Markdown (`.md`) | Human-readable, Git-friendly, widely supported. |

---

## Security Considerations

1. **Path Traversal Prevention**:
   - Validate user input directory exists and is accessible before scanning.
   - Use `pathlib.Path.resolve()` to canonicalize paths and prevent symlink attacks.
   - Do not follow symlinks during traversal (use `os.walk(followlinks=False)`).

2. **Input Validation**:
   - Check that user-provided directory path is a valid directory (not a file).
   - Reject empty or whitespace-only paths.
   - Handle permission errors gracefully without exposing system details.

3. **File Overwrite Safety**:
   - Per requirements, overwrite without prompting (behavior is explicit).
   - Ensure output file path is valid before writing.

4. **No Code Injection**:
   - Do not execute or evaluate file contents.
   - Treat all paths as data, not code.

---

## Error Handling Strategy

| Error Scenario | Handling |
|---|---|
| Invalid/non-existent directory | Display user-friendly message, re-prompt or exit. |
| Permission denied on directory | Skip inaccessible directories with warning; continue scanning accessible ones. |
| Write failure (disk full, no perms) | Display error and exit; do not partially create file. |
| Symlink loops | Use `os.walk(followlinks=False)` to avoid infinite loops. |
| Empty directory | Generate Markdown with message "No Python files found." |

---

## Observability & Logging

1. **User-Visible Output**:
   - Clear prompts for directory input.
   - Status messages: "Scanning directory...", "Found N Python files.", "Generated: <output_file>".
   - Error messages with actionable guidance (e.g., "Directory not found. Please check the path.").

2. **Internal Logging** (optional for MVP):
   - Log directory traversal events to stdout (can be toggled via verbose flag later).
   - Log skipped directories (hidden) for debugging.

---

## Interfaces & Contracts

### UserInterface
```python
def get_directory_path() -> str:
    """
    Prompt user for directory path.
    Returns: Absolute path as string.
    Raises: ValueError if path is invalid.
    """

def display_error(message: str) -> None:
    """Display error message to user."""

def display_success(message: str) -> None:
    """Display success message to user."""
```

### DirectoryScanner
```python
def scan_directory(root_path: str) -> List[str]:
    """
    Recursively scan directory for .py files.
    Returns: List of relative paths (POSIX-style, forward slashes).
    Raises: OSError if directory doesn't exist or is inaccessible.
    """
```

### MarkdownGenerator
```python
def generate_markdown(file_list: List[str]) -> str:
    """
    Generate Markdown content from file list.
    Returns: Markdown string with hierarchical structure.
    """
```

### FileWriter
```python
def write_markdown(file_path: str, content: str) -> None:
    """
    Write Markdown content to file.
    Raises: IOError if write fails.
    """
```

---

## Deployment & Execution

**Entry Point**: `python main.py`

**Output**: `<user_specified_directory>/generated_files.md`

**Dependencies**: None (uses standard library only).

---

## Future Enhancements (Out of Scope)

- Support for multiple file extensions (`.js`, `.ts`, etc.).
- Filtering by file size, modification date.
- Integration with GitHub/GitLab for automated scanning.
- Parallel directory scanning for large codebases.
- Configuration file support.

---

## Document Metadata

- **Written by**: Claude Haiku 4.5
- **Date**: 2026-10-02
- **Phase**: 2 (Architecture)
- **Status**: Pending Approval
