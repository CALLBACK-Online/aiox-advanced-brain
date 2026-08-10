"""Checagens específicas — Introdução à Arquitetura (lib.frontmatter/links/quizzes)."""
from __future__ import annotations

import json
import re

from lib.context import Context
from lib.frontmatter import parse_frontmatter
from lib.links import scan_course_markdown
from lib.quizzes import count_questions

EXPECTED_LESSONS = [
    "sistema-componentes-fronteiras",
    "cliente-servidor-frontend-backend",
    "http-request-response-api",
    "estado-entidade-ciclo-de-vida",
    "banco-schema-indice-transacao",
    "cache-arquivos-object-storage",
    "json-yaml-markdown-contratos",
    "sincrono-assincrono",
    "webhook-fila-evento-pubsub",
    "processo-task-job-worker-runner",
    "workflow-pipeline-batch-stream",
    "concorrencia-paralelismo-fanout-fanin",
    "escala-load-balancing",
    "timeout-retry-backoff-rate-limit",
    "idempotencia-deduplicacao-circuit-breaker",
    "logs-metricas-traces-health-checks",
    "runtime-harness-ambiente-container",
    "cicd-deploy-rollback",
    "autenticacao-autorizacao-secrets",
    "multitenancy-isolamento-rls",
    "monolito-modulos-microsservicos",
    "modelo-contexto-memoria-tool-skill",
    "orquestrador-squad-human-in-loop",
    "capstone-arquitetura-agentic",
]
REQUIRED_SECTIONS = [
    "## Resultado",
    "## Mapa visual",
    "## Quando usar — e quando não usar",
    "## Prática",
    "## Pergunte ao seu agente",
    "## Evidência de conclusão",
]
REQUIRED_ROOT_FILES = [
    "README.md",
    "AGENT-GUIDE.md",
    "Mapa-de-termos.md",
    "Glossario.md",
    "FONTES.md",
    "PROVENIENCIA.md",
    "Assessments.md",
    "Projeto-Integrador.md",
    "Rubrica.md",
]


def run(ctx: Context) -> str:
    root = ctx.root
    course = ctx.course
    course_id = ctx.course_id
    scope = ctx.scope
    errors = ctx.errors

    lesson_files = sorted((course / "aulas").glob("*.md"))
    module_files = sorted((course / "modulos").glob("*.md"))
    quiz_files = sorted((course / "avaliacoes").glob("*.md"))

    if len(lesson_files) != 24:
        errors.append(f"esperadas 24 aulas; encontradas {len(lesson_files)}")
    if len(module_files) != 8:
        errors.append(f"esperados 8 módulos; encontrados {len(module_files)}")
    if len(quiz_files) != 8:
        errors.append(f"esperados 8 quizzes; encontrados {len(quiz_files)}")

    actual_ids: list[str] = []
    for position, path in enumerate(lesson_files, start=1):
        text = path.read_text(encoding="utf-8")
        data = parse_frontmatter(text)
        lesson_id = data.get("lesson_id", "")
        actual_ids.append(lesson_id)
        expected_module = f"M{((position - 1) // 3) + 1}"
        if data.get("type") != "lesson" or data.get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de aula inválido")
        if data.get("status") != "canonical" or data.get("canonical_scope") != scope:
            errors.append(f"{path.name}: status/scope incorreto")
        if data.get("lesson_position") != str(position):
            errors.append(f"{path.name}: lesson_position={data.get('lesson_position')!r}")
        if data.get("module") != expected_module:
            errors.append(
                f"{path.name}: module={data.get('module')!r}; esperado {expected_module}"
            )
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: falta {section}")
        adapted_from = data.get("adapted_from", "")
        for source_path in adapted_from.split(" + ") if adapted_from else []:
            if not (root / source_path).is_file():
                errors.append(f"{path.name}: adapted_from não resolve: {source_path}")

    if actual_ids != EXPECTED_LESSONS:
        errors.append(f"ordem/ids divergentes: {actual_ids}")

    question_count = 0
    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        data = parse_frontmatter(text)
        if data.get("type") != "quiz" or data.get("course") != course_id:
            errors.append(f"{path.name}: frontmatter de quiz inválido")
        n = count_questions(text)
        question_count += n
        if n != 4:
            errors.append(f"{path.name}: esperado 4 questões; encontradas {n}")
        if "<details>" not in text or "## Transferência" not in text:
            errors.append(f"{path.name}: falta gabarito ou transferência")

    if question_count != 32:
        errors.append(f"esperadas 32 questões; encontradas {question_count}")

    ctx.require_files(REQUIRED_ROOT_FILES)

    term_map = (course / "Mapa-de-termos.md").read_text(encoding="utf-8")
    mapped_lessons = set(re.findall(r"\(aulas/([^)#]+\.md)(?:#[^)]+)?\)", term_map))
    expected_lesson_files = {path.name for path in lesson_files}
    if mapped_lessons != expected_lesson_files:
        missing = sorted(expected_lesson_files - mapped_lessons)
        extra = sorted(mapped_lessons - expected_lesson_files)
        errors.append(
            f"mapa de termos sem cobertura 1:1; ausentes={missing}; extras={extra}"
        )

    agent_guide = (course / "AGENT-GUIDE.md").read_text(encoding="utf-8")
    for section in [
        "## Algoritmo obrigatório",
        "## Formato mínimo",
        "## Roteamento por intenção",
        "## Falhas seguras",
    ]:
        if section not in agent_guide:
            errors.append(f"AGENT-GUIDE.md: falta {section}")

    if (root / "package.json").exists():
        guide_path = f"{scope}/AGENT-GUIDE.md"
        for bootstrap_name in ["AGENTS.md", "CLAUDE.md"]:
            bootstrap = root / bootstrap_name
            if not bootstrap.exists() or guide_path not in bootstrap.read_text(
                encoding="utf-8"
            ):
                errors.append(f"bootstrap sem rota para o curso: {bootstrap_name}")

        catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
        course_entry = catalog.get("courses", {}).get(course_id, {})
        if course_entry.get("path") != scope or course_entry.get("agent_guide") != guide_path:
            errors.append("catalog.json: curso ou agent_guide não registrados")

        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
        if "dev/validate.py" not in package.get("scripts", {}).get("validate", ""):
            errors.append("package.json: validador do curso fora de npm run validate")

    scan_course_markdown(course, errors=errors)

    return (
        f"{len(lesson_files)} aulas, {len(module_files)} módulos, "
        f"{len(quiz_files)} quizzes, {question_count} questões"
    )
