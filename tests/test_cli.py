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

    def test_main_reprompts_on_nonexistent_then_succeeds(self) -> None:
        """A nonexistent path is rejected by the UI, which re-prompts until valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", side_effect=["/nonexistent/path", tmpdir]) as mock_in:
                exit_code = main_module.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_in.call_count, 2)

    def test_main_returns_1_when_input_closed(self) -> None:
        """EOF on stdin (after an invalid path) must exit 1 rather than loop forever."""
        with patch("builtins.input", side_effect=["/nonexistent/path", EOFError]):
            exit_code = main_module.main()

        self.assertEqual(exit_code, 1)

    def test_main_returns_1_when_scanner_raises(self) -> None:
        """A FileNotFoundError from the scanner maps to exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", return_value=tmpdir), patch.object(
                main_module.DirectoryScanner,
                "scan_directory",
                side_effect=FileNotFoundError("gone"),
            ):
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
