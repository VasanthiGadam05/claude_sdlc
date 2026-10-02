"""Tests for the FileWriter module (v2 implementation)."""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from writer import FileWriter


class TestFileWriter(unittest.TestCase):
    """Test cases for FileWriter class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.writer = FileWriter()

    def test_write_markdown_creates_file(self) -> None:
        """Test that write_markdown creates a file with content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "output.md")
            content = "# Test\n\n- file1.py\n- file2.py\n"

            self.writer.write_markdown(file_path, content)

            self.assertTrue(Path(file_path).exists())
            self.assertEqual(Path(file_path).read_text(), content)

    def test_write_markdown_overwrites_existing_file(self) -> None:
        """Test that write_markdown overwrites existing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "output.md")

            # Write initial content
            Path(file_path).write_text("Old content\n")

            # Overwrite with new content
            new_content = "# New Content\n"
            self.writer.write_markdown(file_path, new_content)

            self.assertEqual(Path(file_path).read_text(), new_content)

    def test_write_markdown_with_utf8(self) -> None:
        """Test that write_markdown handles UTF-8 encoding correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "output.md")
            content = "# Python Files\n\n- 文件.py\n- файл.py\n"

            self.writer.write_markdown(file_path, content)

            self.assertEqual(Path(file_path).read_text(encoding="utf-8"), content)

    def test_write_markdown_invalid_path(self) -> None:
        """Test that write_markdown raises IOError for invalid paths."""
        invalid_path = "/invalid/nonexistent/directory/file.md"

        with self.assertRaises(IOError):
            self.writer.write_markdown(invalid_path, "content")


if __name__ == "__main__":
    unittest.main()
