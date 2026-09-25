from __future__ import annotations

import shutil
import stat
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def install() -> int:
    root = _repo_root()
    source = root / ".githooks" / "pre-commit"
    dest = root / ".git" / "hooks" / "pre-commit"

    if not source.is_file():
        print(f"install_git_hooks: source hook not found: {source}", file=sys.stderr)
        return 1

    if dest.exists():
        backup = dest.with_name("pre-commit.bak")
        shutil.copy2(dest, backup)
        print(f"install_git_hooks: existing hook backed up to {backup}")

    shutil.copy2(source, dest)
    dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"install_git_hooks: installed {source} -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(install())
