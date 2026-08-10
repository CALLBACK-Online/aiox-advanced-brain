#!/usr/bin/env python3
"""Planeja upgrade brownfield sem editar, mover ou apagar o curso."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from course_common import (
    find_root,
    lesson_inventory,
    normalize_creation_mode,
    resolve_course,
    validate_approval_artifacts,
)
from scaffold_course import validate_spec


def target_lessons(spec: dict) -> list[dict]:
    lessons: list[dict] = []
    position = 1
    for module in spec["modules"]:
        for lesson in module["lessons"]:
            lessons.append({**lesson, "module": module["id"], "position": position})
            position += 1
    return lessons


def build_plan(root: Path, course_id: str, course: Path, spec: dict, approved: bool) -> dict:
    existing = lesson_inventory(course)
    existing_by_id = {lesson["id"]: lesson for lesson in existing}
    target = target_lessons(spec)
    target_ids = {lesson["id"] for lesson in target}
    changes: list[dict] = []
    for lesson in target:
        current = existing_by_id.get(lesson["id"])
        changes.append(
            {
                "lesson_id": lesson["id"],
                "module": lesson["module"],
                "action": "review-preserve-path" if current else "add",
                "current_path": current["path"] if current else None,
                "target_position": lesson["position"],
                "status": "pending",
            }
        )
    for lesson in existing:
        if lesson["id"] not in target_ids:
            changes.append(
                {
                    "lesson_id": lesson["id"],
                    "module": lesson["module"],
                    "action": "archive-candidate",
                    "current_path": lesson["path"],
                    "target_position": None,
                    "status": "pending",
                }
            )
    return {
        "schema_version": 1,
        "course_id": course_id,
        "course_path": course.relative_to(root).as_posix(),
        "generated_date": date.today().isoformat(),
        "approvals_verified": approved,
        "rules": [
            "preservar paths e lesson_id válidos",
            "archive-candidate exige decisão humana; este script não move nem apaga",
            "editar em lote pequeno e validar entre lotes",
        ],
        "changes": changes,
        "validation_command": f"python3 dev/validate.py --course {course_id}",
    }


def render_ledger(plan: dict) -> str:
    rows = []
    for change in plan["changes"]:
        rows.append(
            "| {module} | `{lesson}` | {path} | {action} | PENDING |  |  |".format(
                module=change["module"],
                lesson=change["lesson_id"],
                path=f"`{change['current_path']}`" if change["current_path"] else "—",
                action=change["action"],
            )
        )
    return f"""# Ledger de upgrade — {plan['course_id']}

Aprovações verificadas: `{str(plan['approvals_verified']).lower()}`  
Nenhuma linha autoriza apagar. `archive-candidate` exige decisão humana e destino recuperável.

| Módulo | Aula | Path atual | Ação planejada | Status | Gate/evidência | Ação corretiva |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventário + gap brownfield sem mutação do curso")
    parser.add_argument("--course", required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    root = find_root(args.repo_root or Path.cwd())
    course_id, course = resolve_course(root, args.course)
    spec_path = args.spec if args.spec.is_absolute() else root / args.spec
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if "creation_mode" in spec:
        spec["creation_mode"] = normalize_creation_mode(str(spec["creation_mode"]))
    else:
        spec["creation_mode"] = "upgrade"
    validate_spec(spec)
    if spec["creation_mode"] != "upgrade":
        raise SystemExit("plan_upgrade exige creation_mode=upgrade (alias brownfield ok)")
    if spec["course_id"] != course_id or spec["path"] != course.relative_to(root).as_posix():
        raise SystemExit("spec deve apontar para o mesmo course_id e path do curso existente")
    approved = False
    if args.require_approved:
        validate_approval_artifacts(root, spec)
        approved = True
    plan = build_plan(root, course_id, course, spec, approved)
    counts = Counter(change["action"] for change in plan["changes"])
    print(json.dumps({"course_id": course_id, "approved": approved, "actions": counts}, ensure_ascii=False, default=dict))
    if not args.write:
        return 0
    bastidor = root / "docs" / "producao-cursos" / course_id
    targets = (bastidor / "upgrade-plan.json", bastidor / "upgrade-ledger.md")
    if any(path.exists() for path in targets) and not args.refresh:
        raise SystemExit("plano/ledger já existe; preservar decisões ou usar --refresh conscientemente")
    bastidor.mkdir(parents=True, exist_ok=True)
    targets[0].write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    targets[1].write_text(render_ledger(plan), encoding="utf-8")
    print(f"plan → {targets[0].relative_to(root)}")
    print(f"ledger → {targets[1].relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
