from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES: frozenset[str] = frozenset(
    {".venv", "venv", "__pycache__", ".git", "node_modules", "build", "dist"}
)
_EGG_INFO_GLOB = "*.egg-info"

_READ_PROBE_BYTES = 8192


@dataclass
class ScanResult:
    paths: list[str]
    warnings: list[str]


def _is_excluded_dir(name: str, exclude_dirs: frozenset[str]) -> bool:
    return name in exclude_dirs or fnmatch.fnmatch(name, _EGG_INFO_GLOB)


def _confirm_readable_text(path: Path) -> None:
    with path.open("rb") as handle:
        prefix = handle.read(_READ_PROBE_BYTES)
    prefix.decode("utf-8")


def scan(root: Path, exclude_dirs: frozenset[str] = DEFAULT_EXCLUDES) -> ScanResult:
    paths: list[str] = []
    warnings: list[str] = []

    def _on_walk_error(err: OSError) -> None:
        warnings.append(f"Could not list directory {err.filename}: {err.strerror}")

    for dirpath, dirnames, filenames in os.walk(root, onerror=_on_walk_error):
        dirnames[:] = [d for d in dirnames if not _is_excluded_dir(d, exclude_dirs)]
        dir_path = Path(dirpath)

        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            file_path = dir_path / filename
            rel = file_path.relative_to(root).as_posix()

            if file_path.is_symlink():
                warnings.append(f"Skipped symlinked file (not dereferenced): {rel}")
                continue

            try:
                _confirm_readable_text(file_path)
            except (OSError, UnicodeDecodeError) as exc:
                warnings.append(f"Could not read {rel}: {exc}")
                continue

            paths.append(rel)

    paths.sort()
    return ScanResult(paths=paths, warnings=warnings)
