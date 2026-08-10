#!/usr/bin/env python3
"""Aplica ações do plano de upgrade de forma assistida e explícita.

Nunca apaga. `archive` move para archive/ com path recuperável.
`add` cria stub de aula ausente a partir do template do perfil.
`review-preserve-path` é no-op (só registra).
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
from scaffold_course import PROFILES, read_template, render_lesson, validate_spec


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


def archive_lesson(course: Path, bastidor: Path, change: dict) -> Path:
    if change.get("action") != "archive-candidate":
        raise SystemExit(f"{change['lesson_id']}: action não é archive-candidate")
    rel = change.get("current_path")
    if not rel:
        raise SystemExit(f"{change['lesson_id']}: current_path ausente")
    source = (course / rel).resolve()
    if not source.is_relative_to(course.resolve()):
        raise SystemExit(f"path de archive fora do curso: {rel}")
    if not source.is_file():
        raise SystemExit(f"arquivo ausente: {source}")
    dest_dir = bastidor / "archive" / "upgraded" / date.today().isoformat()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if dest.exists():
        raise SystemExit(f"archive já existe; preservar e resolver manualmente: {dest}")
    shutil.move(str(source), str(dest))
    return dest


def add_lesson_stub(course: Path, spec: dict, change: dict) -> Path:
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
    position_conflicts = list((course / "aulas").glob(f"{position:02d}-*.md"))
    if position_conflicts:
        raise SystemExit(
            f"posição {position} já ocupada; preserve paths e resolva ordem manualmente: "
            f"{position_conflicts[0].relative_to(course)}"
        )
    target = next(
        (
            lesson
            for module_spec in spec["modules"]
            for lesson in module_spec["lessons"]
            if lesson["id"] == lesson_id
        ),
        None,
    )
    if target is None:
        raise SystemExit(f"{lesson_id}: ausente no course-spec.json")
    template_name, _ = PROFILES[spec["profile"]]
    scope = spec["path"]
    positioned = []
    for path in sorted((course / "aulas").glob("*.md")):
        prefix, separator, _ = path.name.partition("-")
        if separator and prefix.isdigit():
            positioned.append((int(prefix), path.name))
    previous_path = next((name for pos, name in reversed(positioned) if pos < position), None)
    next_path = next((name for pos, name in positioned if pos > position), None)
    text = render_lesson(
        read_template(template_name),
        spec,
        scope,
        {**target, "module": module},
        position,
        previous_path,
        next_path,
    )
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
    if not plan.get("approvals_verified"):
        raise SystemExit("plano sem aprovações verificadas; regenere com plan_upgrade --require-approved")
    if plan.get("course_id") != course_id or plan.get("course_path") != course.relative_to(root).as_posix():
        raise SystemExit("plano não corresponde ao curso solicitado")

    bastidor = root / "docs" / "producao-cursos" / course_id
    spec_path = bastidor / "course-spec.json"
    if not spec_path.is_file():
        raise SystemExit(f"course-spec.json ausente: {spec_path}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    mode = normalize_creation_mode(str(spec.get("creation_mode", "upgrade")))
    if mode != "upgrade":
        raise SystemExit("apply_upgrade exige creation_mode=upgrade no course-spec.json")
    spec["creation_mode"] = mode
    validate_spec(spec)
    if hashlib.sha256(spec_path.read_bytes()).hexdigest() != plan.get("spec_sha256"):
        raise SystemExit("course-spec mudou após o plano; regenere e re-aprove o plano")

    approvals = validate_approval_artifacts(root, spec)
    approval_sha256 = {
        gate: hashlib.sha256(path.read_bytes()).hexdigest()
        for gate, path in approvals.items()
    }
    if approval_sha256 != plan.get("approval_sha256"):
        raise SystemExit("artefatos aprovados mudaram após o plano; reaprovação obrigatória")

    if not args.archive and not args.add:
        raise SystemExit("informe ao menos --archive LESSON_ID e/ou --add LESSON_ID")

    actions_log: list[str] = []
    for lesson_id in args.archive:
        change = find_change(plan, lesson_id)
        if change.get("status") != "approved":
            raise SystemExit(f"{lesson_id}: ação exige status=approved marcado pelo humano no plano")
        if args.dry_run:
            actions_log.append(f"DRY archive {lesson_id} ← {change.get('current_path')}")
            continue
        dest = archive_lesson(course, bastidor, change)
        actions_log.append(f"archived {lesson_id} → {dest.relative_to(root)}")

    for lesson_id in args.add:
        change = find_change(plan, lesson_id)
        if change.get("status") != "approved":
            raise SystemExit(f"{lesson_id}: ação exige status=approved marcado pelo humano no plano")
        if args.dry_run:
            actions_log.append(f"DRY add stub {lesson_id} @ pos {change.get('target_position')}")
            continue
        dest = add_lesson_stub(course, spec, change)
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
