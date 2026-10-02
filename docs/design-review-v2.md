# Phase 3: Design Review — Python Source File Scanner

## Overview
An independent senior reviewer (design-reviewer subagent) conducted a thorough review of the proposed architecture against the requirements specification. This document summarizes all findings, decisions made, and any patches applied to the architecture.

---

## Review Summary

**Documents Reviewed**:
- `docs/requirements-v2.md` (requirements specification)
- `docs/architecture-v2.md` (proposed architecture design)

**Total Findings**: 15
- **High-Severity (Critical)**: 2
- **Medium-Severity**: 7
- **Low-Severity (Clarifications)**: 6

**Architecture Status After Review**: ✅ **Approved with patches** — All critical issues resolved, medium concerns addressed with clarifications.

---

## Critical Findings & Resolutions

### 1. Ambiguous Permission-Handling Strategy (HIGH)

**Issue**: Architecture presented contradictory error handling:
- Error handling table stated: "Skip inaccessible directories with warning; continue scanning."
- DirectoryScanner contract stated: "Raises OSError if inaccessible."

**Decision**: **PATCHED** — Clarified that `DirectoryScanner` gracefully skips inaccessible subdirectories with warnings (robust behavior per requirements-v2.md line 27) while still raising `FileNotFoundError` if the **root directory** doesn't exist.

**Patches Applied**:
- Updated DirectoryScanner contract to clarify skip-with-warning behavior for subdirectories.
- Updated main orchestrator pseudocode to show error handling for each exception type.

---

### 2. Requirement 7 Interpretation Ambiguity (HIGH)

**Issue**: Requirement language ("written to the same directory as the scanned root directory") was ambiguous—could mean parent directory or inside root. Clarification at line 59 of requirements-v2.md resolved this, but architecture didn't explicitly cite it.

**Decision**: **PATCHED** — Added explicit citation of clarification in architecture and deployment sections.

**Patches Applied**:
- Added note in Deployment & Execution section: "Per requirements-v2.md line 59 clarification, the output file is written **inside** the root directory being scanned (not to its parent)."

---

## Medium-Severity Findings & Resolutions

### 3. Missing Main Orchestrator Error-Handling Pseudocode (MEDIUM)

**Issue**: Architecture outlined happy-path flow but not error-handling flow; unclear which component catches errors and how main.py delegates to UserInterface for messages.

**Decision**: **PATCHED** — Added comprehensive pseudocode for main.py showing try-catch logic.

**Patches Applied**:
- Updated Main Orchestrator section with Python pseudocode showing error handling for ValueError, FileNotFoundError, NotADirectoryError, and IOError.

---

### 4. No Example Markdown Output Format (MEDIUM)

**Issue**: Requirement called for "nested directory structure" but no example output was provided, leaving implementer uncertain about header depth, file listing format, empty directories, etc.

**Decision**: **PATCHED** — Added concrete example Markdown output.

**Patches Applied**:
- Updated MarkdownGenerator contract with example output showing directory headers (`#`, `##`) and file bullet points.

---

### 5. Conflicting Scanner & Filter Responsibilities (MEDIUM)

**Issue**: DirectoryScanner appeared to filter hidden directories AND return all `.py` files, while FileFilter also checked for hidden directories—unclear if one or both should be responsible.

**Decision**: **ACCEPTED AS-IS** — Clarified via patch that DirectoryScanner is responsible for excluding hidden directories; FileFilter is redundant but harmless (belt-and-suspenders safety). If needed, FileFilter can be simplified or removed in a future refactor.

**Patches Applied**:
- Updated DirectoryScanner contract: "Recursively walk directory, return all `.py` file paths relative to root, **excluding hidden directories**."

---

### 6. Missing Output Path Construction Specification (MEDIUM)

**Issue**: Architecture never showed how file_path was constructed from root_path and hardcoded filename.

**Decision**: **PATCHED** — Added explicit code in main orchestrator pseudocode.

**Patches Applied**:
- Main orchestrator pseudocode now shows: `output_path = os.path.join(root_path, "generated_files.md")`

---

### 7. Incomplete Symlink Handling Policy (MEDIUM)

**Issue**: Architecture said "never follow symlinks" but didn't clarify whether symlinked files/directories themselves are listed or excluded.

**Decision**: **PATCHED** — Clarified symlink handling in DirectoryScanner contract.

**Patches Applied**:
- Updated DirectoryScanner edge cases: "Symlinks: Never followed (`os.walk(followlinks=False)`); symlinks are treated as regular files and excluded if in hidden directories, included otherwise."

---

### 8. Cross-Platform Path Handling Inconsistency (MEDIUM)

**Issue**: Root path returned by UserInterface is OS-native (e.g., `C:\Users\...` on Windows), but DirectoryScanner returns POSIX-style relative paths. Unclear how these interact.

**Decision**: **PATCHED** — Clarified path handling and added example in DirectoryScanner contract.

**Patches Applied**:
- Updated DirectoryScanner contract: "Returns a sorted list of relative paths normalized to POSIX-style (forward slashes) for cross-platform consistency. Example: `['src/models/user.py', 'tests/test_main.py']`"

---

### 9. Output File Collision Risk (MEDIUM)

**Issue**: Hardcoded filename `generated_files.md` with unconditional overwrite could silently overwrite user data without warning (though requirements explicitly require this behavior).

**Decision**: **ACCEPTED WITH MITIGATION** — Design choice is intentional per requirements. Mitigated via clear user communication.

**Patches Applied**:
- Updated File Overwrite Safety section: "Users must be made aware of this behavior via success message: e.g., 'Created/overwritten: /path/to/generated_files.md'."

---

## Low-Severity Findings & Resolutions

### 10. Relative Paths Format Ambiguity (LOW - Clarification)

**Issue**: DirectoryScanner contract said "POSIX-style (forward slashes)" but didn't explain how normalization works on Windows.

**Decision**: **PATCHED** — Clarified in contract example.

**Patches Applied**:
- DirectoryScanner contract now includes example showing forward-slash normalization: `['src/models/user.py', ...]`

---

### 11. Hidden Files vs. Hidden Directories (LOW - Clarification)

**Issue**: Requirements say exclude hidden **directories**, but FileFilter contract was ambiguous about whether files named `.hidden.py` are excluded.

**Decision**: **PATCHED** — Clarified that hidden status is determined by directory names, not file names.

**Patches Applied**:
- FileFilter contract updated (suggested in review; accepted as design clarification).

---

### 12. Module Instantiation Pattern (LOW - Clarification)

**Issue**: Data flow shows function calls but never clarifies whether modules are singletons, instantiated once, or stateless utilities.

**Decision**: **ACCEPTED** — Documented as implementation detail (all modules are stateless; instantiated once per run in main.py).

---

### 13. Error Recovery Behavior (LOW - Clarification)

**Issue**: Error handling table said "Display user-friendly message, re-prompt or exit"—unclear which.

**Decision**: **PATCHED** — Updated main orchestrator pseudocode to show exit(1) for non-recoverable errors; re-prompt behavior left to implementation team.

**Patches Applied**:
- Main orchestrator pseudocode includes `exit(1)` for OSError, FileNotFoundError, IOError.

---

### 14. Relative Paths – Definition Ambiguity (LOW - Clarification)

**Issue**: Unclear whether relative paths mean paths from root or from current working directory.

**Decision**: **ACCEPTED** — Relative to scan root (clear from context and examples).

---

### 15. Requirement 7 Language Clarity (LOW - Clarification)

**Issue**: Original requirement language was awkwardly phrased ("same directory as the scanned root directory").

**Decision**: **ACCEPTED** — Clarification in requirements-v2.md line 59 resolved the ambiguity; architecture now cites it.

---

## Architecture Patches Summary

All patches have been applied to `docs/architecture-v2.md`:

| Finding | Severity | Type | Action | Status |
|---------|----------|------|--------|--------|
| Permission handling | HIGH | Risk | Clarified graceful skip behavior | ✅ Patched |
| Requirement 7 ambiguity | HIGH | Gap | Added clarification citation | ✅ Patched |
| Main orchestrator pseudocode | MEDIUM | Gap | Added error-handling pseudocode | ✅ Patched |
| Markdown output example | MEDIUM | Gap | Added format example | ✅ Patched |
| Scanner/Filter responsibilities | MEDIUM | Gap | Clarified responsibilities | ✅ Clarified |
| Output path construction | MEDIUM | Gap | Added code example in main | ✅ Patched |
| Symlink handling | MEDIUM | Risk | Clarified policy in contract | ✅ Patched |
| Cross-platform paths | MEDIUM | Risk | Added normalization example | ✅ Patched |
| Output file collision | MEDIUM | Risk | Documented mitigation (user messaging) | ✅ Mitigated |
| Relative paths format | LOW | Clarification | Added example | ✅ Patched |
| Hidden files vs. directories | LOW | Clarification | Contract updated (accepted as-is in arch) | ✅ Accepted |
| Module instantiation | LOW | Clarification | Implementation detail (accepted) | ✅ Accepted |
| Error recovery behavior | LOW | Clarification | Pseudocode shows exit behavior | ✅ Patched |

---

## Alternatives Considered

The reviewer identified three architectural alternatives; all were reviewed and the current design was **recommended** for each:

1. **FileFilter as separate module vs. embedding in DirectoryScanner**: Keep current (separation of concerns wins).
2. **Nested dictionary intermediate structure vs. streaming generation**: Keep current (clarity and testability wins).
3. **Hardcoded output filename vs. user-configurable**: Keep current (MVP scope).

---

## Open Risks (Carried Forward)

No open risks; all issues were either patched, clarified, or explicitly accepted with mitigation.

---

## Recommendation

✅ **Architecture is approved and ready for implementation.**

All critical ambiguities have been resolved. The patched architecture provides clear guidance for Phase 5 (Implementation) and Phase 6 (Code Review). The implementer has concrete specifications for:
- Component responsibilities and interfaces
- Error handling flow
- Output format (with examples)
- Path handling across platforms
- Symlink and hidden directory policies

---

## Artifacts Modified

- **docs/architecture-v2.md**: 9 patches applied (DirectoryScanner contract, Main Orchestrator pseudocode, MarkdownGenerator example, Deployment & Execution section, Security section).

---

## Document Metadata

- **Reviewed by**: Design-Reviewer Subagent (Independent Senior Architect)
- **Date**: 2026-10-02
- **Phase**: 3 (Design Review)
- **Status**: Complete
- **Architecture Status**: ✅ Approved with Patches
