from __future__ import annotations

import argparse
import logging
from pathlib import Path

from docsync import render, scanner

logger = logging.getLogger("docsync")

_OUTPUT_FILENAME = "SOURCE_FILES.md"


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="docsync")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory to scan for .py files (defaults to the current directory).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    args = _parse_args(argv)
    root = Path(args.root)

    if not root.is_dir():
        logger.error("Root path is not a directory: %s", root)
        return 1

    result = scanner.scan(root)
    for warning in result.warnings:
        logger.warning(warning)

    markdown = render.render_markdown(root, result.paths)

    try:
        (root / _OUTPUT_FILENAME).write_text(markdown, encoding="utf-8")
    except OSError as exc:
        logger.error("Could not write %s: %s", _OUTPUT_FILENAME, exc)
        return 1

    logger.info(
        "Wrote %s: %d files listed, %d skipped",
        _OUTPUT_FILENAME,
        len(result.paths),
        len(result.warnings),
    )
    return 0
