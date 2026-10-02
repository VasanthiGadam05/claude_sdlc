"""User interface module for directory input and messaging."""

from pathlib import Path


class UserInterface:
    """Handles all user interactions (prompts, error/success messages)."""

    def get_directory_path(self) -> str:
        """
        Prompt user for directory path and validate it.

        Returns:
            Absolute path to the directory as a string.

        Raises:
            ValueError: If the path is invalid or not a directory.
        """
        while True:
            user_input = input("Enter the directory path to scan: ").strip()

            if not user_input:
                self.display_error("Directory path cannot be empty.")
                continue

            try:
                path = Path(user_input).resolve()
                if not path.exists():
                    self.display_error(
                        f"Directory does not exist: {user_input}"
                    )
                    continue
                if not path.is_dir():
                    self.display_error(
                        f"Path is not a directory: {user_input}"
                    )
                    continue
                return str(path)
            except (OSError, ValueError) as e:
                self.display_error(f"Invalid path: {e}")
                continue

    def display_error(self, message: str) -> None:
        """
        Display an error message to the user.

        Args:
            message: The error message to display.
        """
        print(f"Error: {message}")

    def display_success(self, message: str) -> None:
        """
        Display a success message to the user.

        Args:
            message: The success message to display.
        """
        print(f"✓ {message}")
