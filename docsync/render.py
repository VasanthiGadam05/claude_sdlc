from __future__ import annotations

from pathlib import Path

_EMPTY_BODY = "No Python source files were found.\n"


def render_markdown(root: Path, paths: list[str]) -> str:
    del root  # kept for interface symmetry with scanner.scan; content is paths-only (FR3)
    lines = ["# Source Files", ""]

    if not paths:
        lines.append(_EMPTY_BODY.rstrip("\n"))
    else:
        lines.extend(f"- {path}" for path in paths)

    return "\n".join(lines) + "\n"
