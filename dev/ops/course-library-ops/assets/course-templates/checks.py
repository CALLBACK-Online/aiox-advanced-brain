"""Checagens específicas — <Título do curso>."""
from __future__ import annotations

import json
import re

from lib.context import Context
from lib.frontmatter import parse_frontmatter
from lib.links import scan_course_markdown
from lib.quizzes import balance_ok, collect_answers, count_questions

COURSE_ID = "<slug>"
SCOPE = "<scope>"
EXPECTED = <expected>
REQUIRED_ROOT = <required_root>
REQUIRED_LESSON_SECTIONS = <required_sections>
PLACEHOLDER = re.compile(
    r"(?:\bTODO\b|_DRAFT_|<(?:slug|scope|lesson-id|Título|Nome-Do-Curso|tema|source-[^>]+)>)"
)


def run(ctx: Context) -> str:
    errors = ctx.errors
    course = ctx.course
    ctx.require_files(REQUIRED_ROOT)

    lessons = sorted((course / "aulas").glob("*.md"))
    actual: list[str] = []
    for position, path in enumerate(lessons, start=1):
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        actual.append(frontmatter.get("lesson_id", ""))
        if frontmatter.get("type") != "lesson" or frontmatter.get("course") != COURSE_ID:
            errors.append(f"{path.name}: frontmatter de aula inválido")
        if frontmatter.get("canonical_scope") != SCOPE:
            errors.append(f"{path.name}: canonical_scope divergente")
        if frontmatter.get("lesson_position") != str(position):
            errors.append(f"{path.name}: lesson_position divergente")
        for section in REQUIRED_LESSON_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: seção obrigatória ausente: {section}")

    if actual != EXPECTED:
        errors.append(f"ordem/ids divergentes: got={actual!r} expected={EXPECTED!r}")

    quiz_files = sorted((course / "avaliacoes").glob("Quiz-*.md"))
    answers = []
    question_total = 0
    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        question_total += count_questions(text)
        answers.extend(collect_answers(text))
        if "<details>" not in text or "## Transferência" not in text:
            errors.append(f"{path.name}: falta gabarito ou transferência")
    if answers and not balance_ok(dict((letter, answers.count(letter)) for letter in "ABCD")):
        errors.append(f"gabarito desbalanceado: {dict((letter, answers.count(letter)) for letter in 'ABCD')}")

    for path in course.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json"}:
            if PLACEHOLDER.search(path.read_text(encoding="utf-8", errors="replace")):
                errors.append(f"placeholder editorial: {path.relative_to(course)}")

    scan_course_markdown(course, errors=errors, require_in_course=True)
    catalog_path = ctx.root / "catalog.json"
    if catalog_path.is_file():
        entry = json.loads(catalog_path.read_text(encoding="utf-8")).get("courses", {}).get(COURSE_ID)
        if not entry:
            errors.append(f"catalog.json: courses.{COURSE_ID} ausente")
        elif entry.get("lessons") != len(lessons):
            errors.append(f"catalog.json: courses.{COURSE_ID}.lessons divergente")

    return f"{len(lessons)} aulas, {len(quiz_files)} quizzes, {question_total} questões"
