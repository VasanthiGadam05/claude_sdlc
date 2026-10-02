"""Integration tests for the main CLI (v2 implementation)."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import main as main_module


class TestMainIntegration(unittest.TestCase):
    """Integration tests for the main orchestrator."""

    def test_main_with_valid_directory(self) -> None:
        """Test main with a valid directory containing Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.py").touch()
            Path(tmpdir, "file2.py").touch()

            with patch("builtins.input", return_value=tmpdir):
                exit_code = main_module.main()

            self.assertEqual(exit_code, 0)
            output_file = Path(tmpdir, "generated_files.md")
            self.assertTrue(output_file.exists())
            content = output_file.read_text()
            self.assertIn("file1.py", content)
            self.assertIn("file2.py", content)

    def test_main_with_nonexistent_directory(self) -> None:
        """Test main with a nonexistent directory."""
        with patch("builtins.input", return_value="/nonexistent/path"):
            exit_code = main_module.main()

        self.assertEqual(exit_code, 1)

    def test_main_with_empty_directory(self) -> None:
        """Test main with an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", return_value=tmpdir):
                exit_code = main_module.main()

            self.assertEqual(exit_code, 0)
            output_file = Path(tmpdir, "generated_files.md")
            self.assertTrue(output_file.exists())
            content = output_file.read_text()
            self.assertIn("No Python files found", content)


if __name__ == "__main__":
    unittest.main()
