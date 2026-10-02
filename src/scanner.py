"""Directory scanning module for discovering Python files."""

import os
from pathlib import Path
from typing import List


class DirectoryScanner:
    """Recursively scans directories for Python files with filtering."""

    def scan_directory(self, root_path: str) -> List[str]:
        """
        Recursively scan directory for Python files.

        Args:
            root_path: Absolute path to the root directory to scan.

        Returns:
            Sorted list of relative file paths (POSIX-style, forward slashes).

        Raises:
            FileNotFoundError: If root_path doesn't exist.
            NotADirectoryError: If root_path is not a directory.
        """
        root = Path(root_path).resolve()

        if not root.exists():
            raise FileNotFoundError(f"Directory not found: {root_path}")

        if not root.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {root_path}")

        python_files = []

        try:
            for dirpath, dirnames, filenames in os.walk(
                root, followlinks=False
            ):
                # Filter out hidden directories
                dirnames[:] = [
                    d for d in dirnames
                    if not self.is_hidden_directory(d)
                ]

                current_path = Path(dirpath)

                for filename in filenames:
                    if filename.endswith(".py"):
                        file_path = current_path / filename
                        relative_path = file_path.relative_to(root)
                        python_files.append(relative_path.as_posix())

        except PermissionError as e:
            print(f"Warning: Permission denied while scanning. {e}")

        return sorted(python_files)

    @staticmethod
    def is_hidden_directory(directory_name: str) -> bool:
        """
        Check if a directory name is hidden.

        Args:
            directory_name: The directory name to check.

        Returns:
            True if the directory is hidden (starts with . or is __pycache__).
        """
        return (
            directory_name.startswith(".")
            or directory_name == "__pycache__"
        )
