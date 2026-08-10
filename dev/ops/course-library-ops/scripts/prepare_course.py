#!/usr/bin/env python3
"""Prepara bastidor draft sem tocar a superfície do aluno."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from course_common import find_root, lesson_inventory, normalize_creation_mode, safe_relative
from scaffold_course import KEBAB, PROFILES, read_template, replace_tokens  # noqa: E402


def lesson_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def existing_modules(course: Path) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for item in lesson_inventory(course):
        module = item["module"] if re.fullmatch(r"M(?:\d+|C)", item["module"]) else "M0"
        path = course / item["path"]
        grouped.setdefault(module, []).append(
            {"id": item["id"], "title": lesson_title(path), "reading_minutes": 10}
        )
    return [
        {"id": module, "title": f"_DRAFT_ {module}", "evidence": "_DRAFT_", "quiz": False, "lessons": lessons}
        for module, lessons in sorted(grouped.items())
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepara brief, outline e spec no bastidor")
    parser.add_argument("--course-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument(
        "--mode",
        default="create",
        help="create|upgrade (aliases greenfield→create, brownfield→upgrade)",
    )
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    mode = normalize_creation_mode(args.mode)
    if not KEBAB.fullmatch(args.course_id):
        raise SystemExit("course-id deve ser kebab-case")
    relative = safe_relative(args.path, label="path")
    if len(relative.parts) != 2 or relative.parts[0] != "cursos":
        raise SystemExit("path deve apontar para uma pasta direta em cursos/")

    course = root / relative
    harness = root / "dev" / "courses" / args.course_id
    bastidor = root / "docs" / "producao-cursos" / args.course_id
    if bastidor.exists():
        raise SystemExit(f"bastidor já existe; preservar e editar: {bastidor}")
    if mode == "create" and (course.exists() or harness.exists()):
        raise SystemExit("create exige curso e harness ausentes; use --mode upgrade")
    if mode == "upgrade" and not course.is_dir():
        raise SystemExit("upgrade exige curso existente")

    bastidor.mkdir(parents=True)
    mapping = {
        "slug": args.course_id,
        "Título": args.title,
        "Nome-Do-Curso": relative.name,
        "creation-mode": mode,
    }
    brief = replace_tokens(read_template("course-brief.md"), mapping)
    outline = replace_tokens(read_template("course-outline.md"), mapping)
    modules = existing_modules(course) if mode == "upgrade" else [
        {
            "id": "M0",
            "title": "_DRAFT_",
            "evidence": "_DRAFT_",
            "quiz": False,
            "lessons": [{"id": "primeira-aula", "title": "_DRAFT_", "reading_minutes": 10}],
        }
    ]
    spec = {
        "course_id": args.course_id,
        "title": args.title,
        "path": relative.as_posix(),
        "profile": args.profile,
        "creation_mode": mode,
        "capstone": False,
        "optional_artifacts": [],
        "approval_artifacts": {
            "brief": f"docs/producao-cursos/{args.course_id}/COURSE-BRIEF.md",
            "outline": f"docs/producao-cursos/{args.course_id}/course-outline.md",
        },
        "modules": modules,
    }
    (bastidor / "COURSE-BRIEF.md").write_text(brief.rstrip() + "\n", encoding="utf-8")
    (bastidor / "course-outline.md").write_text(outline.rstrip() + "\n", encoding="utf-8")
    (bastidor / "course-spec.json").write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"bastidor draft → {bastidor.relative_to(root)}")
    print("preencher brief/outline/spec; aprovação humana é obrigatória antes do scaffold ou edição")
    return 0


if __name__ == "__main__":
    sys.exit(main())
