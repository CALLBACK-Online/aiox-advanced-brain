#!/usr/bin/env python3
"""Valida estrutura, metadados e links do curso AIOX Productização."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
ROOT = COURSE.parents[1]
COURSE_ID = "aiox-productizacao"
SCOPE = "cursos/AIOX-Productizacao"
EXPECTED = [
    "service-as-software", "dor-e-roi", "distribuicao-vs-produto",
    "caminhos-de-produto", "estagios-de-monetizacao",
    "capstone-decisao-de-productizacao",
]
MODULE_OF = {1: "M1", 2: "M1", 3: "M2", 4: "M2", 5: "M2", 6: "MC"}
REQUIRED_ROOT = [
    "README.md", "AGENT-GUIDE.md", "Assessments.md", "Rubrica.md", "FONTES.md",
    "PROVENIENCIA.md", "Projeto-Integrador.md", "COURSE-BRIEF.md",
    "Mapa-de-decisao.md", "Glossario.md",
]
REQUIRED_TEMPLATES = [
    "README.md", "wedge-card.md", "oferta-uma-pagina.md",
    "experimento-distribuicao.md", "decision-pack.md",
]
REQUIRED_BRIDGES = ["agent-engineering.md", "squads-comerciais.md"]
REQUIRED_LESSON_SECTIONS = [
    "## Pergunte ao seu agente", "## Evidência de conclusão", "## Navegação",
]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_PATH = re.compile(r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/])")
ANSWER = re.compile(r"^\d+\.\s+\*\*([ABCD])\.\*\*", re.M)


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    data: dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip().strip("'\"")
    return data


errors: list[str] = []
lessons = sorted((COURSE / "aulas").glob("*.md"))
modules = sorted((COURSE / "modulos").glob("*.md"))
quizzes = sorted((COURSE / "avaliacoes").glob("Quiz-M*.md"))

for found, expected, label in [(len(lessons), 6, "aulas"), (len(modules), 3, "módulos"), (len(quizzes), 2, "quizzes")]:
    if found != expected:
        errors.append(f"esperados {expected} {label}; encontrados {found}")

actual: list[str] = []
for path in lessons:
    text = path.read_text(encoding="utf-8")
    fm = frontmatter(text)
    position = int(fm.get("lesson_position") or "0")
    actual.append(path.stem.split("-", 1)[1])
    if fm.get("type") != "lesson" or fm.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de aula inválido")
    if fm.get("status") != "canonical" or fm.get("canonical_scope") != SCOPE:
        errors.append(f"{path.name}: status/scope incorreto")
    if fm.get("module") != MODULE_OF.get(position):
        errors.append(f"{path.name}: módulo {fm.get('module')!r}; esperado {MODULE_OF.get(position)!r}")
    if not fm.get("lesson_id") or fm.get("lesson_id") != path.stem.split("-", 1)[1]:
        errors.append(f"{path.name}: lesson_id ausente ou divergente")
    if not fm.get("reading_minutes") or not fm.get("curriculum_role"):
        errors.append(f"{path.name}: reading_minutes/curriculum_role ausente")
    for section in REQUIRED_LESSON_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: seção obrigatória ausente: {section}")
    source_path = fm.get("source_path")
    if source_path and not (ROOT / source_path).is_file():
        errors.append(f"{path.name}: source_path não resolve: {source_path}")

if actual != EXPECTED:
    errors.append(f"ordem/ids divergentes:\n  got {actual}\n  exp {EXPECTED}")

answers: Counter[str] = Counter()
question_total = 0
for path in quizzes:
    text = path.read_text(encoding="utf-8")
    if frontmatter(text).get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de quiz inválido")
    questions = re.findall(r"^### \d+\.", text, re.M)
    question_total += len(questions)
    if len(questions) != 4:
        errors.append(f"{path.name}: esperado 4 questões; {len(questions)}")
    if "<details>" not in text or "## Transferência" not in text:
        errors.append(f"{path.name}: falta gabarito ou transferência")
    answers.update(ANSWER.findall(text))

if question_total != 8:
    errors.append(f"esperadas 8 questões; {question_total}")
if answers and max(answers.values()) - min(answers.values()) > 1:
    errors.append(f"gabarito desbalanceado: {dict(answers)}")

for filename in REQUIRED_ROOT:
    if not (COURSE / filename).exists():
        errors.append(f"arquivo obrigatório ausente: {filename}")

for filename in REQUIRED_TEMPLATES:
    if not (COURSE / "templates" / filename).exists():
        errors.append(f"template obrigatório ausente: {filename}")

for filename in REQUIRED_BRIDGES:
    if not (COURSE / "ponte" / filename).exists():
        errors.append(f"ponte obrigatória ausente: {filename}")

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

readme = (COURSE / "README.md").read_text(encoding="utf-8")
for expected_path in [
    "aulas/01-service-as-software.md", "aulas/02-dor-e-roi.md",
    "aulas/03-distribuicao-vs-produto.md", "aulas/04-caminhos-de-produto.md",
    "aulas/05-estagios-de-monetizacao.md", "aulas/06-capstone-decisao-de-productizacao.md",
    "Projeto-Integrador.md", "AGENT-GUIDE.md", "Mapa-de-decisao.md",
]:
    if expected_path not in readme:
        errors.append(f"README.md: rota obrigatória ausente: {expected_path}")

catalog_path = ROOT / "catalog.json"
package_path = ROOT / "package.json"
if catalog_path.is_file() and package_path.is_file():
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    course = catalog.get("courses", {}).get(COURSE_ID, {})
    expected_catalog = {
        "path": SCOPE,
        "lessons": 6,
        "modules": 3,
        "quizzes": 2,
        "questions": 8,
        "agent_guide": f"{SCOPE}/AGENT-GUIDE.md",
    }
    for key, value in expected_catalog.items():
        if course.get(key) != value:
            errors.append(f"catalog.json: courses.{COURSE_ID}.{key} divergente")

    package = json.loads(package_path.read_text(encoding="utf-8"))
    validate_script = package.get("scripts", {}).get("validate", "")
    if f'{SCOPE}/_tools/validate_course.py' not in validate_script:
        errors.append("package.json: validador do curso ausente de npm run validate")

    guide_path = f"{SCOPE}/AGENT-GUIDE.md"
    for bootstrap_name in ["AGENTS.md", "CLAUDE.md"]:
        bootstrap = ROOT / bootstrap_name
        if not bootstrap.is_file() or guide_path not in bootstrap.read_text(encoding="utf-8"):
            errors.append(f"{bootstrap_name}: descoberta automática do curso ausente")

if errors:
    print("AIOX Productização: FALHA")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    f"AIOX Productização: 6 aulas, 3 módulos, 2 quizzes, {question_total} questões; "
    f"gabarito {dict(sorted(answers.items()))}; erros: 0"
)
