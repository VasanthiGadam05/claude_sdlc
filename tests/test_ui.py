"""Tests for the UserInterface module."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui import UserInterface


class TestUserInterface(unittest.TestCase):
    """Test cases for UserInterface class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.ui = UserInterface()

    def test_get_directory_path_valid_directory(self) -> None:
        """Test getting a valid directory path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", return_value=tmpdir):
                result = self.ui.get_directory_path()
                self.assertEqual(result, str(Path(tmpdir).resolve()))

    def test_get_directory_path_nonexistent_directory(self) -> None:
        """Test with a nonexistent directory path."""
        with patch(
            "builtins.input",
            side_effect=["/nonexistent/path", "/another/missing"]
        ):
            with self.assertRaises(EOFError):
                self.ui.get_directory_path()

    def test_get_directory_path_file_not_directory(self) -> None:
        """Test with a file path instead of directory."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            with patch(
                "builtins.input",
                side_effect=[tmpfile.name, "/nonexistent"]
            ):
                with self.assertRaises(EOFError):
                    self.ui.get_directory_path()

    def test_display_error_format(self, capsys=None) -> None:
        """Test error message formatting."""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.ui.display_error("Test error")
        output = f.getvalue()
        self.assertIn("Error:", output)
        self.assertIn("Test error", output)

    def test_display_success_format(self) -> None:
        """Test success message formatting."""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.ui.display_success("Test success")
        output = f.getvalue()
        self.assertIn("✓", output)
        self.assertIn("Test success", output)


if __name__ == "__main__":
    unittest.main()
