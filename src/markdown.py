"""Markdown generation module for hierarchical file listing."""

from typing import Dict, List


class MarkdownGenerator:
    """Generates hierarchical Markdown from a list of Python file paths."""

    def generate_markdown(self, file_list: List[str]) -> str:
        """
        Generate Markdown content from a list of file paths.

        Args:
            file_list: List of relative file paths (POSIX-style).

        Returns:
            Formatted Markdown string with hierarchical structure.
        """
        if not file_list:
            return "# Python Files\n\nNo Python files found.\n"

        hierarchy = self.build_hierarchy(file_list)
        return self._render_hierarchy(hierarchy)

    @staticmethod
    def build_hierarchy(files: List[str]) -> Dict:
        """
        Build a nested dictionary structure from file paths.

        Args:
            files: List of relative file paths.

        Returns:
            Nested dictionary representing the directory tree.
        """
        hierarchy: Dict = {}

        for file_path in files:
            parts = file_path.split("/")
            current = hierarchy

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            if "_files" not in current:
                current["_files"] = []
            current["_files"].append(parts[-1])

        return hierarchy

    def _render_hierarchy(
        self, hierarchy: Dict, depth: int = 1
    ) -> str:
        """
        Render the hierarchy dictionary as Markdown.

        Args:
            hierarchy: The nested directory structure.
            depth: Current header depth (starts at 1).

        Returns:
            Markdown formatted string.
        """
        lines = []
        header_prefix = "#" * depth

        # Files at this level are listed first so they are not visually
        # attributed to a following sub-directory heading.
        for file_name in sorted(hierarchy.get("_files", [])):
            lines.append(f"- {file_name}")

        for key in sorted(k for k in hierarchy if k != "_files"):
            lines.append(f"\n{header_prefix} {key}\n")
            sub_content = self._render_hierarchy(hierarchy[key], depth + 1)
            lines.append(sub_content)

        return "\n".join(lines).strip() + "\n"
