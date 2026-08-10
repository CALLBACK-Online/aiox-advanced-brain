"""Contexto de validação por curso."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Context:
    root: Path
    course: Path
    course_id: str
    scope: str
    title: str
    slug: str
    manifest: dict[str, Any]
    tools_dir: Path
    errors: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    def require_files(self, relative_paths: list[str], *, label: str = "arquivo") -> None:
        for rel in relative_paths:
            if not (self.course / rel).exists():
                self.errors.append(f"{label} obrigatório ausente: {rel}")

    def count_glob(self, pattern: str) -> int:
        return len(list(self.course.glob(pattern)))
