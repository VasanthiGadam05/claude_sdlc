"""Tests for the DirectoryScanner module (v2 implementation)."""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner import DirectoryScanner


class TestDirectoryScanner(unittest.TestCase):
    """Test cases for DirectoryScanner class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.scanner = DirectoryScanner()

    def test_scan_directory_empty(self) -> None:
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(result, [])

    def test_scan_directory_with_python_files(self) -> None:
        """Test scanning a directory with Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            Path(tmpdir, "file2.py").touch()
            Path(tmpdir, "file.txt").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(len(result), 2)
            self.assertIn("file1.py", result)
            self.assertIn("file2.py", result)
            self.assertNotIn("file.txt", result)

    def test_scan_directory_recursive(self) -> None:
        """Test recursive scanning with subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            Path(tmpdir, "subdir").mkdir()
            Path(tmpdir, "subdir", "file2.py").touch()
            Path(tmpdir, "subdir", "subdir2").mkdir()
            Path(tmpdir, "subdir", "subdir2", "file3.py").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(len(result), 3)
            self.assertIn("file1.py", result)
            self.assertIn("subdir/file2.py", result)
            self.assertIn("subdir/subdir2/file3.py", result)

    def test_scan_directory_excludes_hidden_directories(self) -> None:
        """Test that hidden directories are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            Path(tmpdir, ".hidden").mkdir()
            Path(tmpdir, ".hidden", "file2.py").touch()
            Path(tmpdir, ".git").mkdir()
            Path(tmpdir, ".git", "file3.py").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(len(result), 1)
            self.assertIn("file1.py", result)
            self.assertNotIn(".hidden/file2.py", result)
            self.assertNotIn(".git/file3.py", result)

    def test_scan_directory_excludes_pycache(self) -> None:
        """Test that __pycache__ directories are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            Path(tmpdir, "__pycache__").mkdir()
            Path(tmpdir, "__pycache__", "file2.py").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(len(result), 1)
            self.assertIn("file1.py", result)
            self.assertNotIn("__pycache__/file2.py", result)

    def test_scan_directory_nonexistent(self) -> None:
        """Test scanning a nonexistent directory."""
        with self.assertRaises(FileNotFoundError):
            self.scanner.scan_directory("/nonexistent/path")

    def test_scan_directory_file_not_directory(self) -> None:
        """Test with a file path instead of directory."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            with self.assertRaises(NotADirectoryError):
                self.scanner.scan_directory(tmpfile.name)

    def test_scan_directory_returns_sorted(self) -> None:
        """Test that results are sorted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "z_file.py").touch()
            Path(tmpdir, "a_file.py").touch()
            Path(tmpdir, "m_file.py").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(result, sorted(result))

    def test_scan_directory_posix_paths(self) -> None:
        """Test that paths use forward slashes (POSIX style)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "subdir").mkdir()
            Path(tmpdir, "subdir", "file.py").touch()

            result = self.scanner.scan_directory(tmpdir)
            self.assertEqual(result[0], "subdir/file.py")
            self.assertNotIn("\\", result[0])

    def test_is_hidden_directory(self) -> None:
        """Test the is_hidden_directory method."""
        self.assertTrue(self.scanner.is_hidden_directory(".git"))
        self.assertTrue(self.scanner.is_hidden_directory(".github"))
        self.assertTrue(self.scanner.is_hidden_directory(".hidden"))
        self.assertTrue(self.scanner.is_hidden_directory("__pycache__"))
        self.assertFalse(self.scanner.is_hidden_directory("src"))
        self.assertFalse(self.scanner.is_hidden_directory("tests"))
        self.assertFalse(self.scanner.is_hidden_directory("normal_dir"))

    def test_scan_directory_skips_symlinked_files(self) -> None:
        """Test that symlinked files are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            # Create symlink target
            Path(tmpdir, "target.py").touch()
            # Create symlink (may fail on some systems, skip if not supported)
            try:
                link = Path(tmpdir, "link.py")
                link.symlink_to(Path(tmpdir, "target.py"))
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks not supported on this system")

            result = self.scanner.scan_directory(tmpdir)
            # Should include actual file and target, but not symlink
            self.assertIn("file1.py", result)
            self.assertIn("target.py", result)
            self.assertNotIn("link.py", result)


if __name__ == "__main__":
    unittest.main()
