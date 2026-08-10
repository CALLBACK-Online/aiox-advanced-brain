"""Helpers de quizzes Markdown."""
from __future__ import annotations

import re

QUESTION_HEADING = re.compile(r"^### \d+\.", re.MULTILINE)
GABARITO_ANS = re.compile(r"^\d+\.\s+\*\*([ABCD])\.\*\*", re.MULTILINE)


def count_questions(text: str) -> int:
    return len(QUESTION_HEADING.findall(text))


def collect_answers(text: str) -> list[str]:
    return GABARITO_ANS.findall(text)


def balance_ok(answers: dict[str, int], *, max_spread: int = 1) -> bool:
    if not answers:
        return True
    values = list(answers.values())
    return max(values) - min(values) <= max_spread
