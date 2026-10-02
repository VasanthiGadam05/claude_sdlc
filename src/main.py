"""Main orchestrator for the Python source file scanner."""

import os
import sys
from pathlib import Path

from markdown import MarkdownGenerator
from scanner import DirectoryScanner
from ui import UserInterface
from writer import FileWriter


def main() -> int:
    """
    Main orchestrator coordinating the scan, generate, and write workflow.

    Returns:
        0 on success, 1 on error.
    """
    ui = UserInterface()
    scanner = DirectoryScanner()
    generator = MarkdownGenerator()
    writer = FileWriter()

    try:
        root_path = ui.get_directory_path()
        files = scanner.scan_directory(root_path)
        markdown_content = generator.generate_markdown(files)
        output_path = os.path.join(root_path, "generated_files.md")
        writer.write_markdown(output_path, markdown_content)
        ui.display_success(
            f"Generated: {output_path} ({len(files)} Python files found)"
        )
        return 0

    except ValueError as e:
        ui.display_error(f"Invalid input. {str(e)}")
        return 1
    except (FileNotFoundError, NotADirectoryError) as e:
        ui.display_error(str(e))
        return 1
    except IOError as e:
        ui.display_error(str(e))
        return 1
    except Exception as e:
        ui.display_error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
