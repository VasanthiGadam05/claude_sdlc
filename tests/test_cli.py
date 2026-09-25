from __future__ import annotations

from pathlib import Path

import pytest

from docsync import cli


def test_invalid_root_returns_nonzero_and_logs_error(tmp_path, caplog):
    missing_root = tmp_path / "does-not-exist"

    exit_code = cli.main([str(missing_root)])

    assert exit_code != 0
    assert "does-not-exist" in caplog.text


def test_normal_run_writes_source_files_md(tmp_path):
    (tmp_path / "a.py").write_text("print(1)\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "b.py").write_text("print(2)\n", encoding="utf-8")

    exit_code = cli.main([str(tmp_path)])

    assert exit_code == 0
    output_file = tmp_path / "SOURCE_FILES.md"
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "a.py" in content
    assert "pkg/b.py" in content


def test_write_failure_returns_nonzero(tmp_path, monkeypatch):
    (tmp_path / "a.py").write_text("print(1)\n", encoding="utf-8")

    def _boom(self, *args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(Path, "write_text", _boom)

    exit_code = cli.main([str(tmp_path)])

    assert exit_code != 0
