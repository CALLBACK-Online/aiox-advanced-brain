"""Helpers de quizzes markdown (padrão ### N. + gabarito A/B/C/D)."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

QUESTION_HEADING = re.compile(r"^### \d+\.", re.M)
GABARITO_ANS = re.compile(r"^\d+\.\s+\*\*([ABCD])\.\*\*", re.M)


def count_questions(text: str) -> int:
    return len(QUESTION_HEADING.findall(text))


def collect_answers(text: str) -> list[str]:
    return GABARITO_ANS.findall(text)


def balance_ok(answers: Counter[str] | dict[str, int], *, max_spread: int = 1) -> bool:
    if not answers:
        return True
    values = list(answers.values()) if isinstance(answers, dict) else list(answers.values())
    return max(values) - min(values) <= max_spread


def scan_md_quizzes(
    quiz_files: list[Path],
    *,
    errors: list[str],
    per_quiz: int | None = 4,
    require_details: bool = True,
    require_transfer: bool = True,
    course_id: str | None = None,
    frontmatter_fn=None,
) -> tuple[int, Counter[str]]:
    """Valida quizzes .md; retorna (total_questões, contagem A/B/C/D)."""
    from .frontmatter import parse_frontmatter

    fm_fn = frontmatter_fn or parse_frontmatter
    total = 0
    answers: Counter[str] = Counter()
    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        if course_id is not None:
            fm = fm_fn(text)
            if fm.get("type") == "quiz" or "type" in fm:
                if fm.get("course") and fm.get("course") != course_id:
                    errors.append(f"{path.name}: frontmatter de quiz inválido (course)")
                if fm.get("type") and fm.get("type") != "quiz":
                    errors.append(f"{path.name}: frontmatter de quiz inválido (type)")
        n = count_questions(text)
        total += n
        if per_quiz is not None and n != per_quiz:
            errors.append(f"{path.name}: esperado {per_quiz} questões; {n}")
        if require_details and "<details>" not in text:
            errors.append(f"{path.name}: falta gabarito (<details>)")
        if require_transfer and "## Transferência" not in text:
            errors.append(f"{path.name}: falta ## Transferência")
        answers.update(collect_answers(text))
    if answers and not balance_ok(answers):
        errors.append(f"gabarito desbalanceado: {dict(answers)}")
    return total, answers
