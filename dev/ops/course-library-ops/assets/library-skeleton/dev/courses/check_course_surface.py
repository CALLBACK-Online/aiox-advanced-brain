#!/usr/bin/env python3
"""Protege a separação entre o pacote do aluno e o bastidor de produção."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_DEV = Path(__file__).resolve().parents[1]
if str(_DEV) not in sys.path:
    sys.path.insert(0, str(_DEV))

from lib.paths import find_root  # noqa: E402

ROOT = find_root(Path(__file__))
COURSES = ROOT / "cursos"
FORBIDDEN_DIRECTORIES = {"_tools", "tests", "__tests__", "scripts"}
FORBIDDEN_SUFFIXES = {".js", ".mjs", ".py", ".pyc", ".sh", ".ts"}
PRODUCTION_FILES = {
    "course-brief-original.md",
    "course-brief.md",
    "course-outline.md",
    "course-spec.json",
    "curriculum-expansion.md",
    "curriculum-gap.md",
    "deviations.json",
    "deviations.md",
    "deviations.yaml",
    "deviations.yml",
    "gap-analysis.md",
    "didactic-audit.md",
    "reformed-brief-validation-report.md",
    "upgrade-ledger.md",
    "upgrade-plan.json",
}


def main() -> int:
    errors: list[str] = []
    if not COURSES.is_dir():
        print("cursos/ ausente")
        return 1
    course_files = [path for path in COURSES.rglob("*") if path.is_file()]
    for path in course_files:
        relative = path.relative_to(ROOT)
        relative_parts = set(relative.parts)
        filename = path.name.lower()
        if relative_parts & FORBIDDEN_DIRECTORIES:
            errors.append(f"tooling dentro da superfície do aluno: {relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"arquivo executável dentro da superfície do aluno: {relative}")
        if filename in PRODUCTION_FILES or "validation-report" in filename:
            errors.append(f"documento de produção dentro da superfície do aluno: {relative}")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    for entry in package.get("files", []):
        normalized = entry.strip("./")
        if normalized == "dev" or normalized.startswith("dev/"):
            errors.append(f"package.json inclui tooling de maintainer: {entry}")
        if normalized == "docs" or normalized.startswith("docs/"):
            errors.append(f"package.json inclui documentação de produção: {entry}")

    if errors:
        print("❌ Separação cursos/dev/docs inválida:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"✅ Superfície dos cursos limpa ({len(course_files)} arquivos verificados)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
