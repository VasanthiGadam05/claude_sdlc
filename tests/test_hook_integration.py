from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run(args, cwd):
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def _init_throwaway_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "throwaway"
    repo.mkdir()
    _run(["git", "init", "-q"], cwd=repo)
    _run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    _run(["git", "config", "user.name", "Test"], cwd=repo)

    shutil.copytree(REPO_ROOT / "docsync", repo / "docsync")
    shutil.copytree(REPO_ROOT / ".githooks", repo / ".githooks")
    (repo / "scripts").mkdir()
    shutil.copy2(
        REPO_ROOT / "scripts" / "install_git_hooks.py",
        repo / "scripts" / "install_git_hooks.py",
    )
    return repo


def _require_working_hook_interpreter():
    for candidate in ("python3", "python"):
        found = shutil.which(candidate)
        if found is None:
            continue
        probe = subprocess.run([found, "-c", ""], capture_output=True)
        if probe.returncode == 0:
            return
    pytest.skip("no working python3/python interpreter on PATH for the hook to invoke")


def test_install_hooks_backs_up_existing_hook(tmp_path):
    repo = _init_throwaway_repo(tmp_path)
    hooks_dir = repo / ".git" / "hooks"
    existing = hooks_dir / "pre-commit"
    existing.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")

    result = _run([sys.executable, str(repo / "scripts" / "install_git_hooks.py")], cwd=repo)

    assert result.returncode == 0
    backup = hooks_dir / "pre-commit.bak"
    assert backup.exists()
    assert backup.read_text(encoding="utf-8") == "#!/usr/bin/env sh\nexit 0\n"
    assert (hooks_dir / "pre-commit").read_text(encoding="utf-8") != backup.read_text(
        encoding="utf-8"
    )


def test_hook_generates_and_stages_source_files_md_on_commit(tmp_path):
    _require_working_hook_interpreter()
    repo = _init_throwaway_repo(tmp_path)

    install_result = _run(
        [sys.executable, str(repo / "scripts" / "install_git_hooks.py")], cwd=repo
    )
    assert install_result.returncode == 0

    (repo / "pkg").mkdir()
    (repo / "pkg" / "thing.py").write_text("print('hi')\n", encoding="utf-8")

    _run(["git", "add", "docsync", "scripts", ".githooks", "pkg"], cwd=repo)
    commit_result = _run(["git", "commit", "-q", "-m", "add thing"], cwd=repo)

    assert commit_result.returncode == 0, commit_result.stderr

    source_files = repo / "SOURCE_FILES.md"
    assert source_files.exists()
    assert "pkg/thing.py" in source_files.read_text(encoding="utf-8")

    show_result = _run(["git", "show", "--stat", "HEAD"], cwd=repo)
    assert "SOURCE_FILES.md" in show_result.stdout
