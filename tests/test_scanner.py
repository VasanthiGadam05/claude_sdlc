from __future__ import annotations

import os
import sys

import pytest

from docsync.scanner import DEFAULT_EXCLUDES, scan


def _touch(path, content="print('hi')\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_recursive_discovery(tmp_path):
    _touch(tmp_path / "a.py")
    _touch(tmp_path / "pkg" / "b.py")
    _touch(tmp_path / "pkg" / "sub" / "c.py")
    _touch(tmp_path / "notes.txt", "not python\n")

    result = scan(tmp_path)

    assert result.paths == ["a.py", "pkg/b.py", "pkg/sub/c.py"]
    assert result.warnings == []


@pytest.mark.parametrize(
    "excluded_dir",
    sorted(d for d in DEFAULT_EXCLUDES),
)
def test_default_excluded_dir_names(tmp_path, excluded_dir):
    _touch(tmp_path / "keep.py")
    _touch(tmp_path / excluded_dir / "skip.py")

    result = scan(tmp_path)

    assert result.paths == ["keep.py"]


def test_egg_info_glob_excluded(tmp_path):
    _touch(tmp_path / "keep.py")
    _touch(tmp_path / "mypkg.egg-info" / "skip.py")

    result = scan(tmp_path)

    assert result.paths == ["keep.py"]


def test_zero_files_found(tmp_path):
    (tmp_path / "readme.md").write_text("hello\n", encoding="utf-8")

    result = scan(tmp_path)

    assert result.paths == []
    assert result.warnings == []


def test_unreadable_file_yields_warning_but_other_files_still_returned(tmp_path):
    _touch(tmp_path / "good.py")
    bad = tmp_path / "bad.py"
    _touch(bad)

    if sys.platform == "win32":
        pytest.skip("chmod-based unreadable-file simulation is not reliable on Windows")

    os.chmod(bad, 0o000)
    try:
        result = scan(tmp_path)
    finally:
        os.chmod(bad, 0o644)

    assert result.paths == ["good.py"]
    assert any("bad.py" in w for w in result.warnings)


def test_unlistable_subdirectory_yields_warning_but_other_dirs_still_scanned(tmp_path):
    _touch(tmp_path / "good.py")
    blocked = tmp_path / "blocked"
    blocked.mkdir()
    _touch(blocked / "hidden.py")

    if sys.platform == "win32":
        pytest.skip("chmod-based unlistable-directory simulation is not reliable on Windows")

    os.chmod(blocked, 0o000)
    try:
        result = scan(tmp_path)
    finally:
        os.chmod(blocked, 0o755)

    assert result.paths == ["good.py"]
    assert any("blocked" in w for w in result.warnings)


def test_symlinked_file_is_skipped_without_being_dereferenced(tmp_path):
    target_dir = tmp_path / "outside"
    target_dir.mkdir()
    target = target_dir / "secret.py"
    target.write_text("SHOULD_NOT_BE_READ = True\n", encoding="utf-8")

    root = tmp_path / "root"
    root.mkdir()
    _touch(root / "kept.py")
    link = root / "linked.py"

    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation not permitted in this environment")

    result = scan(root)

    assert result.paths == ["kept.py"]
    assert any("linked.py" in w for w in result.warnings)


def test_output_is_sorted_and_posix_style(tmp_path):
    _touch(tmp_path / "z_dir" / "z.py")
    _touch(tmp_path / "a_dir" / "a.py")
    _touch(tmp_path / "m.py")

    result = scan(tmp_path)

    assert result.paths == sorted(result.paths)
    assert all("\\" not in p for p in result.paths)
