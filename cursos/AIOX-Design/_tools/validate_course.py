#!/usr/bin/env python3
"""Valida estrutura, pedagogia e links do curso AIOX Design."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
COURSE_ID = "aiox-design"
SCOPE = "cursos/AIOX-Design"
EXPECTED_LESSONS = [
    "design-system-e-decisao",
    "design-system-greenfield-brownfield",
    "design-md-contrato",
    "taxonomia-atomica",
    "tokens-componentes-anti-drift",
    "stack-tailwind-shadcn-storybook",
    "storybook-variantes",
    "portao-qualidade-visual",
    "skill-vs-squad-design",
    "capstone-contrato-e-componente",
]
MODULE_OF = {
    1: "M0",
    2: "M0",
    3: "M1",
    4: "M1",
    5: "M1",
    6: "M2",
    7: "M2",
    8: "M2",
    9: "M3",
    10: "M3",
}
REQUIRED_SECTIONS = [
    "## Resultado",
    "## Mapa visual",
    "## Quando usar — e quando não usar",
    "## Prática",
    "## Pergunte ao seu agente",
    "## Evidência de conclusão",
]
REQUIRED_ROOT = [
    "README.md",
    "AGENT-GUIDE.md",
    "Assessments.md",
    "Rubrica.md",
    "Glossario.md",
    "FONTES.md",
    "Projeto-Integrador.md",
    "COURSE-BRIEF.md",
    "course-outline.md",
]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_PATH = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/])"
)
GABARITO_ANS = re.compile(r"^\d+\.\s+\*\*([ABCD])\.\*\*", re.M)

errors: list[str] = []
lesson_files = sorted((COURSE / "aulas").glob("*.md"))
module_files = sorted((COURSE / "modulos").glob("*.md"))
quiz_files = sorted((COURSE / "avaliacoes").glob("Quiz-M*.md"))

if len(lesson_files) != 10:
    errors.append(f"esperadas 10 aulas; encontradas {len(lesson_files)}")
if len(module_files) != 4:
    errors.append(f"esperados 4 módulos; encontrados {len(module_files)}")
if len(quiz_files) != 3:
    errors.append(f"esperados 3 quizzes; encontrados {len(quiz_files)}")

actual_ids: list[str] = []
for path in lesson_files:
    text = path.read_text(encoding="utf-8")
    fm: dict[str, str] = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip("'\"")
    lid = fm.get("lesson_id", "")
    actual_ids.append(lid)
    pos = int(fm.get("lesson_position") or "0")
    if fm.get("type") != "lesson" or fm.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de aula inválido")
    if fm.get("status") != "canonical" or fm.get("canonical_scope") != SCOPE:
        errors.append(f"{path.name}: status/scope incorreto")
    if MODULE_OF.get(pos) and fm.get("module") != MODULE_OF[pos]:
        errors.append(
            f"{path.name}: module={fm.get('module')!r} esperado {MODULE_OF.get(pos)}"
        )
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: falta {section}")
    if ABSOLUTE_PATH.search(text):
        errors.append(f"{path.name}: path absoluto de máquina")

if actual_ids != EXPECTED_LESSONS:
    errors.append(
        f"ordem/ids divergentes:\n  got {actual_ids}\n  exp {EXPECTED_LESSONS}"
    )

answer_pos: Counter[str] = Counter()
q_total = 0
for path in quiz_files:
    text = path.read_text(encoding="utf-8")
    fm: dict[str, str] = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip("'\"")
    if fm.get("type") != "quiz" or fm.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de quiz inválido")
    questions = re.findall(r"^### \d+\.", text, re.M)
    q_total += len(questions)
    if len(questions) != 4:
        errors.append(f"{path.name}: esperado 4 questões; {len(questions)}")
    if "<details>" not in text or "## Transferência" not in text:
        errors.append(f"{path.name}: falta gabarito ou transferência")
    for ans in GABARITO_ANS.findall(text):
        answer_pos[ans] += 1

if q_total != 12:
    errors.append(f"esperadas 12 questões; {q_total}")
if answer_pos and (max(answer_pos.values()) - min(answer_pos.values()) > 1):
    errors.append(f"gabarito desbalanceado: {dict(answer_pos)}")

for filename in REQUIRED_ROOT:
    if not (COURSE / filename).exists():
        errors.append(f"arquivo obrigatório ausente: {filename}")

for path in COURSE.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if ABSOLUTE_PATH.search(text):
        errors.append(f"{path.relative_to(COURSE)}: path absoluto")
    for raw in LINK.findall(text):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        try:
            resolved.relative_to(COURSE.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(COURSE)}: link fora do curso: {raw}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(COURSE)}: link quebrado: {raw}")

if errors:
    print("AIOX Design: FALHA")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(
    f"AIOX Design: 10 aulas, 4 módulos, 3 quizzes, {q_total} questões; "
    f"gabarito {dict(sorted(answer_pos.items()))}; erros: 0"
)
