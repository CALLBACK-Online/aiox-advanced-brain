"""Checagens de paths absolutos e links Markdown relativos."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ABSOLUTE_PATH = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\/]Users[\/])"
)
MD_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def scan_course_markdown(
    course: Path,
    *,
    errors: list[str],
    require_in_course: bool = True,
    suffixes: set[str] | None = None,
) -> None:
    suffixes = suffixes or {".md"}
    course_resolved = course.resolve()
    for path in course.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(course)
        if ABSOLUTE_PATH.search(text):
            errors.append(f"{relative}: path absoluto de máquina")
        if path.suffix != ".md":
            continue
        for raw in MD_LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if require_in_course:
                try:
                    resolved.relative_to(course_resolved)
                except ValueError:
                    errors.append(f"{relative}: link fora do curso: {raw}")
                    continue
            if not resolved.exists():
                errors.append(f"{relative}: link quebrado: {raw}")
