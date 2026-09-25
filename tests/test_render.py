from __future__ import annotations

from pathlib import Path

from docsync.render import render_markdown


def test_render_lists_all_paths_in_given_order():
    output = render_markdown(Path("/some/root"), ["a.py", "pkg/b.py"])

    assert "a.py" in output
    assert "pkg/b.py" in output
    assert output.index("a.py") < output.index("pkg/b.py")


def test_render_empty_paths_states_no_files_found():
    output = render_markdown(Path("/some/root"), [])

    assert "No Python source files were found" in output
    assert ".py" not in output.replace("No Python source files were found.", "")


def test_render_is_byte_identical_across_calls():
    first = render_markdown(Path("/some/root"), ["a.py", "b.py"])
    second = render_markdown(Path("/some/root"), ["a.py", "b.py"])

    assert first == second


def test_render_does_not_touch_filesystem(tmp_path):
    nonexistent_root = tmp_path / "does-not-exist"

    output = render_markdown(nonexistent_root, ["x.py"])

    assert "x.py" in output
    assert not nonexistent_root.exists()
