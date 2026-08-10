#!/usr/bin/env python3
"""Valida estrutura, pedagogia e links do curso AIOX Design (v2 — 20 aulas)."""
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
    "CURRICULUM-EXPANSION.md",
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

if len(lesson_files) != 20:
    errors.append(f"esperadas 20 aulas; encontradas {len(lesson_files)}")
if len(module_files) != 6:
    errors.append(f"esperados 6 módulos; encontrados {len(module_files)}")
if len(quiz_files) != 5:
    errors.append(f"esperados 5 quizzes; encontrados {len(quiz_files)}")

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

if q_total != 20:
    errors.append(f"esperadas 20 questões; {q_total}")
if answer_pos and (max(answer_pos.values()) - min(answer_pos.values()) > 1):
    errors.append(f"gabarito desbalanceado: {dict(answer_pos)}")

for filename in REQUIRED_ROOT:
    if not (COURSE / filename).exists():
        errors.append(f"arquivo obrigatório ausente: {filename}")

cap = COURSE / "aulas" / "20-capstone-ds-storybook-executavel.md"
if cap.exists():
    ct = cap.read_text(encoding="utf-8")
    if not re.search(r"Storybook.*obrigat", ct, re.I):
        errors.append("capstone: Storybook deve ser obrigatório")

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
    f"AIOX Design: 20 aulas, 6 módulos, 5 quizzes, {q_total} questões; "
    f"gabarito {dict(sorted(answer_pos.items()))}; erros: 0"
)
