"""File writing module for Markdown output."""

from pathlib import Path


class FileWriter:
    """Handles safe writing of Markdown content to disk."""

    @staticmethod
    def write_markdown(file_path: str, content: str) -> None:
        """
        Write Markdown content to a file.

        Args:
            file_path: Absolute path where the file should be written.
            content: The Markdown content to write.

        Raises:
            IOError: If the write operation fails.
        """
        try:
            path = Path(file_path)
            path.write_text(content, encoding="utf-8")
        except (OSError, PermissionError) as e:
            raise IOError(
                f"Failed to write Markdown file: {e}"
            ) from e
