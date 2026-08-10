#!/usr/bin/env python3
"""Aplica ações do plano de upgrade de forma assistida e explícita.

Nunca apaga. `archive` move para archive/ com path recuperável.
`add` cria stub de aula ausente a partir do template do perfil.
`review-preserve-path` é no-op (só registra).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from course_common import (
    find_root,
    normalize_creation_mode,
    resolve_course,
    validate_approval_artifacts,
)
from scaffold_course import PROFILES, read_template, replace_tokens


def load_plan(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not data.get("changes"):
        raise SystemExit("upgrade-plan.json inválido")
    return data


def find_change(plan: dict, lesson_id: str) -> dict:
    for change in plan["changes"]:
        if change.get("lesson_id") == lesson_id:
            return change
    raise SystemExit(f"lesson_id ausente no plano: {lesson_id}")


def archive_lesson(course: Path, change: dict) -> Path:
    if change.get("action") != "archive-candidate":
        raise SystemExit(f"{change['lesson_id']}: action não é archive-candidate")
    rel = change.get("current_path")
    if not rel:
        raise SystemExit(f"{change['lesson_id']}: current_path ausente")
    source = course / rel
    if not source.is_file():
        raise SystemExit(f"arquivo ausente: {source}")
    dest_dir = course / "archive" / "upgraded" / date.today().isoformat()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if dest.exists():
        dest = dest_dir / f"{source.stem}.{date.today().strftime('%H%M%S')}{source.suffix}"
    shutil.move(str(source), str(dest))
    return dest


def add_lesson_stub(course: Path, root: Path, spec: dict, change: dict) -> Path:
    if change.get("action") != "add":
        raise SystemExit(f"{change['lesson_id']}: action não é add")
    lesson_id = change["lesson_id"]
    module = change.get("module") or "M0"
    position = int(change.get("target_position") or 0)
    if position <= 0:
        raise SystemExit(f"{lesson_id}: target_position inválido")
    dest = course / "aulas" / f"{position:02d}-{lesson_id}.md"
    if dest.exists():
        raise SystemExit(f"já existe (não sobrescreve): {dest.relative_to(course)}")
    template_name, _ = PROFILES[spec["profile"]]
    text = read_template(template_name)
    scope = spec["path"]
    text = replace_tokens(
        text,
        {
            "slug": spec["course_id"],
            "lesson-id": lesson_id,
            "Título": lesson_id.replace("-", " ").title(),
            "scope": scope,
            "Nome-Do-Curso": Path(scope).name,
        },
    )
    text = re.sub(r"(?m)^lesson_position:\s*\d+", f"lesson_position: {position}", text)
    text = re.sub(r"(?m)^module:\s*M(?:\d+|C)", f"module: {module}", text)
    if "lesson_id:" in text:
        text = re.sub(r"(?m)^lesson_id:\s*.+$", f"lesson_id: {lesson_id}", text)
    text = re.sub(r"(?m)^# .+$", f"# {lesson_id.replace('-', ' ').title()}", text, count=1)
    if "_DRAFT_" not in text:
        text = text.rstrip() + "\n\n> _DRAFT_ stub de upgrade — preencher conteúdo.\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aplica uma ação do upgrade-plan de forma explícita (nunca apaga)"
    )
    parser.add_argument("--course", required=True)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument(
        "--plan",
        type=Path,
        help="default: docs/producao-cursos/<id>/upgrade-plan.json",
    )
    parser.add_argument(
        "--archive",
        action="append",
        default=[],
        metavar="LESSON_ID",
        help="move archive-candidate para archive/upgraded/<date>/",
    )
    parser.add_argument(
        "--add",
        action="append",
        default=[],
        metavar="LESSON_ID",
        help="cria stub para action=add",
    )
    parser.add_argument(
        "--allow-unapproved",
        action="store_true",
        help="só para debug; por default exige brief/outline approved",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    course_id, course = resolve_course(root, args.course)
    plan_path = args.plan or (root / "docs" / "producao-cursos" / course_id / "upgrade-plan.json")
    if not args.plan:
        plan_path = root / "docs" / "producao-cursos" / course_id / "upgrade-plan.json"
    elif not plan_path.is_absolute():
        plan_path = root / plan_path
    if not plan_path.is_file():
        raise SystemExit(f"plano ausente: {plan_path}")
    plan = load_plan(plan_path)

    bastidor = root / "docs" / "producao-cursos" / course_id
    spec_path = bastidor / "course-spec.json"
    if not spec_path.is_file():
        raise SystemExit(f"course-spec.json ausente: {spec_path}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    mode = normalize_creation_mode(str(spec.get("creation_mode", "upgrade")))
    if mode != "upgrade":
        raise SystemExit("apply_upgrade exige creation_mode=upgrade no course-spec.json")
    spec["creation_mode"] = mode

    if not args.allow_unapproved:
        validate_approval_artifacts(root, spec)

    if not args.archive and not args.add:
        raise SystemExit("informe ao menos --archive LESSON_ID e/ou --add LESSON_ID")

    actions_log: list[str] = []
    for lesson_id in args.archive:
        change = find_change(plan, lesson_id)
        if args.dry_run:
            actions_log.append(f"DRY archive {lesson_id} ← {change.get('current_path')}")
            continue
        dest = archive_lesson(course, change)
        actions_log.append(f"archived {lesson_id} → {dest.relative_to(root)}")

    for lesson_id in args.add:
        change = find_change(plan, lesson_id)
        if args.dry_run:
            actions_log.append(f"DRY add stub {lesson_id} @ pos {change.get('target_position')}")
            continue
        dest = add_lesson_stub(course, root, spec, change)
        actions_log.append(f"added stub {dest.relative_to(course)}")

    for line in actions_log:
        print(line)
    print(
        "apply_upgrade: done — rode validate e atualize contadores/catalog; "
        "review-preserve-path permanece edição humana"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
