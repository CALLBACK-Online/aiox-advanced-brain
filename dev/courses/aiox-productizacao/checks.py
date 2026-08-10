"""Checagens específicas — AIOX Productização (lib.frontmatter/links/quizzes)."""
from __future__ import annotations

import json
from collections import Counter

from lib.context import Context
from lib.frontmatter import parse_frontmatter
from lib.links import scan_course_markdown
from lib.quizzes import balance_ok, collect_answers, count_questions

EXPECTED = [
    "service-as-software",
    "dor-e-roi",
    "distribuicao-vs-produto",
    "caminhos-de-produto",
    "estagios-de-monetizacao",
    "capstone-decisao-de-productizacao",
]
MODULE_OF = {1: "M1", 2: "M1", 3: "M2", 4: "M2", 5: "M2", 6: "MC"}
REQUIRED_ROOT = [
    "README.md",
    "AGENT-GUIDE.md",
    "Assessments.md",
    "Rubrica.md",
    "FONTES.md",
    "PROVENIENCIA.md",
    "Projeto-Integrador.md",
    "Mapa-de-decisao.md",
    "Glossario.md",
]
REQUIRED_TEMPLATES = [
    "README.md",
    "wedge-card.md",
    "oferta-uma-pagina.md",
    "experimento-distribuicao.md",
    "decision-pack.md",
]
REQUIRED_BRIDGES = ["agent-engineering.md", "squads-comerciais.md"]
REQUIRED_LESSON_SECTIONS = [
    "## Pergunte ao seu agente",
    "## Evidência de conclusão",
    "## Navegação",
]
README_ROUTES = [
    "aulas/01-service-as-software.md",
    "aulas/02-dor-e-roi.md",
    "aulas/03-distribuicao-vs-produto.md",
    "aulas/04-caminhos-de-produto.md",
    "aulas/05-estagios-de-monetizacao.md",
    "aulas/06-capstone-decisao-de-productizacao.md",
    "Projeto-Integrador.md",
    "AGENT-GUIDE.md",
    "Mapa-de-decisao.md",
]


def run(ctx: Context) -> str:
    root = ctx.root
    course = ctx.course
    course_id = ctx.course_id
    scope = ctx.scope
    errors = ctx.errors

    lessons = sorted((course / "aulas").glob("*.md"))
    modules = sorted((course / "modulos").glob("*.md"))
    quizzes = sorted((course / "avaliacoes").glob("Quiz-M*.md"))

    for found, expected, label in [
        (len(lessons), 6, "aulas"),
        (len(modules), 3, "módulos"),
        (len(quizzes), 2, "quizzes"),
    ]:
        if found != expected:
            errors.append(f"esperados {expected} {label}; encontrados {found}")

    actual: list[str] = []
    for path in lessons:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        position = int(fm.get("lesson_position") or "0")
        actual.append(path.stem.split("-", 1)[1])
        if fm.get("type") != "lesson" or fm.get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de aula inválido")
        if fm.get("status") != "canonical" or fm.get("canonical_scope") != scope:
            errors.append(f"{path.name}: status/scope incorreto")
        if fm.get("module") != MODULE_OF.get(position):
            errors.append(
                f"{path.name}: módulo {fm.get('module')!r}; esperado {MODULE_OF.get(position)!r}"
            )
        if not fm.get("lesson_id") or fm.get("lesson_id") != path.stem.split("-", 1)[1]:
            errors.append(f"{path.name}: lesson_id ausente ou divergente")
        if not fm.get("reading_minutes") or not fm.get("curriculum_role"):
            errors.append(f"{path.name}: reading_minutes/curriculum_role ausente")
        for section in REQUIRED_LESSON_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: seção obrigatória ausente: {section}")
        source_path = fm.get("source_path")
        if source_path and not (root / source_path).is_file():
            errors.append(f"{path.name}: source_path não resolve: {source_path}")

    if actual != EXPECTED:
        errors.append(f"ordem/ids divergentes:\n  got {actual}\n  exp {EXPECTED}")

    answers: Counter[str] = Counter()
    question_total = 0
    for path in quizzes:
        text = path.read_text(encoding="utf-8")
        if parse_frontmatter(text).get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de quiz inválido")
        n = count_questions(text)
        question_total += n
        if n != 4:
            errors.append(f"{path.name}: esperado 4 questões; {n}")
        if "<details>" not in text or "## Transferência" not in text:
            errors.append(f"{path.name}: falta gabarito ou transferência")
        answers.update(collect_answers(text))

    if question_total != 8:
        errors.append(f"esperadas 8 questões; {question_total}")
    if answers and not balance_ok(answers):
        errors.append(f"gabarito desbalanceado: {dict(answers)}")

    ctx.require_files(REQUIRED_ROOT)
    for filename in REQUIRED_TEMPLATES:
        if not (course / "templates" / filename).exists():
            errors.append(f"template obrigatório ausente: {filename}")
    for filename in REQUIRED_BRIDGES:
        if not (course / "ponte" / filename).exists():
            errors.append(f"ponte obrigatória ausente: {filename}")

    scan_course_markdown(course, errors=errors)

    readme = (course / "README.md").read_text(encoding="utf-8")
    for expected_path in README_ROUTES:
        if expected_path not in readme:
            errors.append(f"README.md: rota obrigatória ausente: {expected_path}")

    catalog_path = root / "catalog.json"
    package_path = root / "package.json"
    if catalog_path.is_file() and package_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        entry = catalog.get("courses", {}).get(course_id, {})
        for key, value in {
            "path": scope,
            "lessons": 6,
            "modules": 3,
            "quizzes": 2,
            "questions": 8,
            "agent_guide": f"{scope}/AGENT-GUIDE.md",
        }.items():
            if entry.get(key) != value:
                errors.append(f"catalog.json: courses.{course_id}.{key} divergente")

        validate_script = json.loads(package_path.read_text(encoding="utf-8")).get(
            "scripts", {}
        ).get("validate", "")
        if "dev/validate.py" not in validate_script:
            errors.append("package.json: validate não referencia dev/validate.py")

        guide_path = f"{scope}/AGENT-GUIDE.md"
        for bootstrap_name in ["AGENTS.md", "CLAUDE.md"]:
            bootstrap = root / bootstrap_name
            if not bootstrap.is_file() or guide_path not in bootstrap.read_text(
                encoding="utf-8"
            ):
                errors.append(f"{bootstrap_name}: descoberta automática do curso ausente")

    return (
        f"{len(lessons)} aulas, {len(modules)} módulos, {len(quizzes)} quizzes, "
        f"{question_total} questões; gabarito {dict(sorted(answers.items()))}"
    )
