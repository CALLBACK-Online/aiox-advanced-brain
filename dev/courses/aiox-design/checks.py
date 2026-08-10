"""Checagens específicas — AIOX Design (piloto: consome dev/lib de fato).

Política de sequência/seções fica aqui. Contagens canônicas vêm de catalog.json
(não duplicar no manifest). required_root + scan_links: generic via manifest.
"""
from __future__ import annotations

import json
import re
from collections import Counter

from lib.context import Context
from lib.frontmatter import parse_frontmatter
from lib.links import scan_course_markdown
from lib.quizzes import balance_ok, collect_answers, count_questions

# Sequência canônica das aulas (política de validação — não está no catalog).
EXPECTED_LESSONS = [
    "design-system-e-decisao",
    "design-system-greenfield-brownfield",
    "repertorio-e-referencias",
    "tema-visual-vs-design-system",
    "top-down-vs-bottom-up",
    "brand-book-para-tokens",
    "anti-ai-look-e-exploracao",
    "design-md-contrato",
    "tokens-componentes-anti-drift",
    "taxonomia-atomica",
    "storybook-fonte-da-verdade",
    "stack-tailwind-shadcn-storybook",
    "storybook-install-e-stories",
    "storybook-variantes",
    "governanca-e-permissoes",
    "ds-multi-produto",
    "ciclo-screenshot-correcao",
    "portao-qualidade-visual",
    "skill-vs-squad-design",
    "capstone-ds-storybook-executavel",
]
MODULE_OF = {
    1: "M0",
    2: "M0",
    3: "M0",
    4: "M1",
    5: "M1",
    6: "M1",
    7: "M2",
    8: "M2",
    9: "M2",
    10: "M2",
    11: "M3",
    12: "M3",
    13: "M3",
    14: "M3",
    15: "M4",
    16: "M4",
    17: "M4",
    18: "M4",
    19: "M5",
    20: "M5",
}
REQUIRED_SECTIONS = [
    "## Resultado",
    "## Mapa visual",
    "## Quando usar — e quando não usar",
    "## Prática",
    "## Pergunte ao seu agente",
    "## Evidência de conclusão",
]
CAPSTONE = "20-capstone-ds-storybook-executavel.md"


def run(ctx: Context) -> str:
    course = ctx.course
    course_id = ctx.course_id
    scope = ctx.scope
    errors = ctx.errors

    lesson_files = sorted((course / "aulas").glob("*.md"))
    module_files = sorted((course / "modulos").glob("*.md"))
    quiz_files = sorted((course / "avaliacoes").glob("Quiz-M*.md"))

    # Contagens: fonte de verdade = catalog.json (quando presente)
    catalog_path = ctx.root / "catalog.json"
    catalog_course: dict = {}
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog_course = catalog.get("courses", {}).get(course_id, {})

    expected_lessons = int(catalog_course.get("lessons") or len(EXPECTED_LESSONS))
    expected_modules = int(catalog_course.get("modules") or 6)
    expected_quizzes = int(catalog_course.get("quizzes") or 5)
    expected_questions = int(catalog_course.get("questions") or 20)

    if len(lesson_files) != expected_lessons:
        errors.append(
            f"esperadas {expected_lessons} aulas; encontradas {len(lesson_files)}"
        )
    if len(module_files) != expected_modules:
        errors.append(
            f"esperados {expected_modules} módulos; encontrados {len(module_files)}"
        )
    if len(quiz_files) != expected_quizzes:
        errors.append(
            f"esperados {expected_quizzes} quizzes; encontrados {len(quiz_files)}"
        )

    actual_ids: list[str] = []
    for path in lesson_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        lid = fm.get("lesson_id", "")
        actual_ids.append(lid)
        pos = int(fm.get("lesson_position") or "0")
        if fm.get("type") != "lesson" or fm.get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de aula inválido")
        if fm.get("status") != "canonical" or fm.get("canonical_scope") != scope:
            errors.append(f"{path.name}: status/scope incorreto")
        if MODULE_OF.get(pos) and fm.get("module") != MODULE_OF[pos]:
            errors.append(
                f"{path.name}: module={fm.get('module')!r} esperado {MODULE_OF.get(pos)}"
            )
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: falta {section}")

    if actual_ids != EXPECTED_LESSONS:
        errors.append(
            f"ordem/ids divergentes:\n  got {actual_ids}\n  exp {EXPECTED_LESSONS}"
        )

    answers: Counter[str] = Counter()
    q_total = 0
    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm.get("type") != "quiz" or fm.get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de quiz inválido")
        n = count_questions(text)
        q_total += n
        if n != 4:
            errors.append(f"{path.name}: esperado 4 questões; {n}")
        if "<details>" not in text or "## Transferência" not in text:
            errors.append(f"{path.name}: falta gabarito ou transferência")
        answers.update(collect_answers(text))

    if q_total != expected_questions:
        errors.append(f"esperadas {expected_questions} questões; {q_total}")
    if answers and not balance_ok(answers):
        errors.append(f"gabarito desbalanceado: {dict(answers)}")

    # catalog ↔ filesystem (catalog é a fonte; não re-hardcodar contagens)
    if catalog_course:
        pairs = {
            "lessons": len(lesson_files),
            "modules": len(module_files),
            "quizzes": len(quiz_files),
            "questions": q_total,
        }
        for key, actual in pairs.items():
            if key in catalog_course and catalog_course.get(key) != actual:
                errors.append(
                    f"catalog.json: courses.{course_id}.{key}="
                    f"{catalog_course.get(key)!r} ≠ filesystem {actual}"
                )

    cap = course / "aulas" / CAPSTONE
    if not cap.is_file():
        errors.append(f"capstone ausente: {CAPSTONE}")
    else:
        if not re.search(r"Storybook.*obrigat", cap.read_text(encoding="utf-8"), re.I):
            errors.append("capstone: Storybook deve ser obrigatório")

    # Links + absolutos (lib) — manifest marca scan_links:false para não duplicar no generic
    scan_course_markdown(course, errors=errors, require_in_course=True)

    return (
        f"{len(lesson_files)} aulas, {len(module_files)} módulos, "
        f"{len(quiz_files)} quizzes, {q_total} questões; "
        f"gabarito {dict(sorted(answers.items()))}"
    )
