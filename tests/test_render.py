"""Tests for the MarkdownGenerator module (v2 implementation)."""

import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markdown import MarkdownGenerator


class TestMarkdownGenerator(unittest.TestCase):
    """Test cases for MarkdownGenerator class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.generator = MarkdownGenerator()

    def test_generate_markdown_empty_list(self) -> None:
        """Test generating markdown from empty file list."""
        result = self.generator.generate_markdown([])
        self.assertIn("No Python files found", result)
        self.assertIn("# Python Files", result)

    def test_generate_markdown_single_file(self) -> None:
        """Test generating markdown from single file."""
        result = self.generator.generate_markdown(["file.py"])
        self.assertIn("file.py", result)
        self.assertIn("- file.py", result)

    def test_generate_markdown_flat_structure(self) -> None:
        """Test generating markdown with files in root."""
        files = ["file1.py", "file2.py", "file3.py"]
        result = self.generator.generate_markdown(files)
        for file_name in files:
            self.assertIn(f"- {file_name}", result)

    def test_generate_markdown_nested_structure(self) -> None:
        """Test generating markdown with nested directories."""
        files = ["src/main.py", "src/utils/helper.py", "tests/test_main.py"]
        result = self.generator.generate_markdown(files)
        self.assertIn("src", result)
        self.assertIn("utils", result)
        self.assertIn("tests", result)
        self.assertIn("main.py", result)
        self.assertIn("helper.py", result)
        self.assertIn("test_main.py", result)

    def test_generate_markdown_headers_format(self) -> None:
        """Test that markdown uses proper header formatting."""
        files = ["src/utils/helper.py"]
        result = self.generator.generate_markdown(files)
        self.assertIn("# src", result)
        self.assertIn("## utils", result)
        self.assertIn("- helper.py", result)

    def test_generate_markdown_deterministic(self) -> None:
        """Test that output is deterministic (same input = same output)."""
        files = ["z_file.py", "a_file.py", "m_file.py"]
        result1 = self.generator.generate_markdown(files)
        result2 = self.generator.generate_markdown(files)
        self.assertEqual(result1, result2)

    def test_build_hierarchy(self) -> None:
        """Test building intermediate hierarchy structure."""
        files = ["src/main.py", "src/utils/helper.py", "tests/test.py"]
        hierarchy = self.generator.build_hierarchy(files)
        self.assertIn("src", hierarchy)
        self.assertIn("tests", hierarchy)
        self.assertIn("utils", hierarchy["src"])
        self.assertIn("_files", hierarchy["src"])
        self.assertIn("main.py", hierarchy["src"]["_files"])


if __name__ == "__main__":
    unittest.main()
