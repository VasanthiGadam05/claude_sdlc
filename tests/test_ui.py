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

    def test_get_directory_path_nonexistent_then_valid(self) -> None:
        """Test that invalid paths are rejected and valid paths are accepted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "builtins.input",
                side_effect=["/nonexistent/path", tmpdir]
            ):
                result = self.ui.get_directory_path()
                self.assertEqual(result, str(Path(tmpdir).resolve()))

    def test_get_directory_path_file_then_valid(self) -> None:
        """Test that file paths are rejected but directory paths are accepted."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            with tempfile.TemporaryDirectory() as tmpdir:
                with patch(
                    "builtins.input",
                    side_effect=[tmpfile.name, tmpdir]
                ):
                    result = self.ui.get_directory_path()
                    self.assertEqual(result, str(Path(tmpdir).resolve()))

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

    def test_display_success_falls_back_on_unencodable_stdout(self) -> None:
        """Success output must not raise when stdout cannot encode the check mark."""
        import io
        from contextlib import redirect_stdout

        raw = io.BytesIO()
        stream = io.TextIOWrapper(raw, encoding="cp1252", errors="strict")
        with redirect_stdout(stream):
            self.ui.display_success("Test success")
        stream.flush()
        output = raw.getvalue().decode("cp1252")
        self.assertIn("[OK]", output)
        self.assertIn("Test success", output)


if __name__ == "__main__":
    unittest.main()
