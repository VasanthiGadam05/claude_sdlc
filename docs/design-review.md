# Design Review — Automated Documentation Sync

Independent review of `docs/architecture.md` against `docs/requirements.md`, performed by the
`design-reviewer` subagent (fresh context, read-only) as required by Phase 3. Findings below are
grouped by disposition: **Patched** (architecture.md changed as a result), **Hardened** (kept the
same approach, added a safeguard), or **Accepted** (kept as-is; risk/tradeoff documented here
rather than changing the design).

## Risks

| # | Risk | Disposition |
|---|---|---|
| R1 | Scanner walks the raw working tree, not the git index — an untracked or `.gitignore`d `.py` file gets listed in `SOURCE_FILES.md` even though it isn't part of the commit. | **Accepted.** FR1 explicitly says "scan a given root directory," not "scan git-tracked files" — matching git's index would require a runtime dependency on the `git` binary, which the stdlib-only tech-stack choice (architecture.md Tech Stack table) deliberately avoids. Documented as a known limitation rather than a defect. |
| R2 | Hook invokes `python -m docsync`; on many Linux/macOS setups `python` isn't aliased to `python3`, so the hook unconditionally blocks every commit on those machines. | **Patched.** Hook now tries `python3` first, falls back to `python`, and only then treats "neither found" as the genuine environment error that blocks a commit. |
| R3 | `scripts/install_git_hooks.py` overwrites `.git/hooks/pre-commit` with no check for a pre-existing hook (e.g. from another tool), silently destroying it. | **Hardened.** Installer now backs up any existing hook to `pre-commit.bak` before writing, and warns if one was present. |
| R4 | Hook installation is opt-in (per requirements.md Open Question #3); a developer who never runs the installer gets zero enforcement, with no CI backstop (CI triggering is explicitly out of scope). | **Accepted.** This is a direct consequence of a requirements-level scope decision (pre-commit hook, not CI), not something Phase 3 can or should redesign around. |
| R5 | Per-file warnings (FR8) only go to stderr during the local `git commit`; a PR reviewer has no way to see that files were skipped. | **Accepted.** Putting warnings inside `SOURCE_FILES.md` would violate FR3's explicit "only the relative path is listed — no ... other metadata" constraint. stderr-only is the requirements-compliant choice. |
| R6 | `core.autocrlf`/`.gitattributes` text-normalization could rewrite `SOURCE_FILES.md`'s line endings independent of what the tool wrote, muddying NFR1's "byte-identical" claim across platforms. | **Patched.** Architecture now recommends a `SOURCE_FILES.md -text` entry in the project's `.gitattributes` so Git never renormalizes the generated file's line endings. |
| R7 | No discussion of scan cost past "low thousands of files" (NFR5) or an escape hatch for large repos. | **Accepted.** NFR5 sets no numeric SLA and scopes to "low thousands of files"; `git commit --no-verify` is already a standard, always-available Git escape hatch and doesn't need custom design work. |
| R8 | A symlinked *file* (not directory) inside the tree is reported with a safe in-`root` path, but the read-check probe still opens and reads whatever the symlink points to — potentially leaking external file content readability, not just path structure. | **Patched.** Scanner now skips symlinked files (reports them via the same FR8 warning path) instead of dereferencing them for the read-check. |

## Gaps

| # | Gap (→ requirement) | Disposition |
|---|---|---|
| G1 | `DEFAULT_EXCLUDES: frozenset[str]` can't literally match the glob `*.egg-info/` from FR2 via containment. | **Patched.** Key Interfaces now specifies exclusion matching is by exact directory-name match for fixed names, plus `fnmatch`-style suffix matching for the one glob entry (`*.egg-info`) — no third-party glob library needed. |
| G2 | Nothing specifies how the hook determines `<repo-root>` to pass to `python -m docsync`, load-bearing for FR7's staging step. | **Patched.** Hook now resolves the root via `git rev-parse --show-toplevel` before invoking `docsync`. |
| G3 | Only two error tiers are defined; a failure writing `SOURCE_FILES.md` itself (disk full, permission denied, AV lock) isn't covered by either. | **Patched.** Added a third case to the error-handling section: a write failure is a tool-level error (same tier as an invalid root) — non-zero exit, and the hook blocks the commit, since we can't guarantee `SOURCE_FILES.md` is in a valid state. |
| G4 | No performance section addressing NFR5 at all. | **Patched.** Added a short Performance note: single-pass `os.walk` plus one bounded read-probe per discovered file is O(files), which is the right complexity class for NFR5's "low thousands of files" scope — no caching/parallelism needed at this scale. |
| G5 | No design for testing the shell hook / installer script themselves, only the Python modules. | **Already covered** — `.claude/instructions/coding.md`'s Testing Conventions already specifies an integration test that inits a throwaway repo under `tmp_path` to cover hook-level staging behavior. No change needed; noted here so the cross-reference is explicit. |
| G6 | Undefined whether a permission error on the *root* directory's own top-level walk (vs. a subdirectory) is tier-1 (warn, continue) or tier-2 (fail the tool). | **Patched.** Clarified: identical to any subdirectory — tier-1 warning, scan continues with whatever was readable, consistent with FR8's "a single bad file/dir must never fail the whole run." |

## Alternatives considered

- **Hook install mechanism:** `git config core.hooksPath .githooks` (point Git directly at the versioned directory, no copying) was considered as an alternative to the custom installer script. Rejected for now — it's still opt-in (same R4 tradeoff) and it repoints hook lookup for *every* hook in the repo, not just this one, which could silently disable unrelated hooks other tooling installs later. The custom installer, now hardened with a backup (R3), stays.
- **Hook implementation language:** a pure-Python hook file (avoiding the `sh` + `python` two-runtime split behind R2) was considered. Rejected — it trades one interpreter-resolution problem for a different one (the hook file's own shebang still needs a Python interpreter) without removing the underlying risk, and loses the "runs unmodified via Git Bash" simplicity NFR4 relies on.
- **Scan source (working tree vs. git index):** covered under R1/A5 above — rejected in favor of the stdlib-only, git-agnostic design already chosen.

## Architecture changes made

`docs/architecture.md` was patched in place (not left contradicting this document) for: R2, R6, R8,
G1, G2, G3, G4, G6. See that file's Components, Key Interfaces, Security Considerations, and Error
Handling & Observability sections. `.claude/instructions/coding.md` was also updated to encode R2,
R3, R8, G2 as concrete coding rules for Phase 5.
