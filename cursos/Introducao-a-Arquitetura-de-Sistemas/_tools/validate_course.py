#!/usr/bin/env python3
"""Valida estrutura, pedagogia e links do curso de Introdução à Arquitetura de Sistemas."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
ROOT = COURSE.parents[1]
COURSE_ID = "introducao-arquitetura-sistemas"
SCOPE = "cursos/Introducao-a-Arquitetura-de-Sistemas"
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
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_PATH = re.compile(r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+[\\/])")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("'\"")
    return result


errors: list[str] = []
lesson_files = sorted((COURSE / "aulas").glob("*.md"))
module_files = sorted((COURSE / "modulos").glob("*.md"))
quiz_files = sorted((COURSE / "avaliacoes").glob("*.md"))

if len(lesson_files) != 24:
    errors.append(f"esperadas 24 aulas; encontradas {len(lesson_files)}")
if len(module_files) != 8:
    errors.append(f"esperados 8 módulos; encontrados {len(module_files)}")
if len(quiz_files) != 8:
    errors.append(f"esperados 8 quizzes; encontrados {len(quiz_files)}")

actual_ids: list[str] = []
for position, path in enumerate(lesson_files, start=1):
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    lesson_id = data.get("lesson_id", "")
    actual_ids.append(lesson_id)
    expected_module = f"M{((position - 1) // 3) + 1}"
    if data.get("type") != "lesson" or data.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de aula inválido")
    if data.get("status") != "canonical" or data.get("canonical_scope") != SCOPE:
        errors.append(f"{path.name}: status/scope incorreto")
    if data.get("lesson_position") != str(position):
        errors.append(f"{path.name}: lesson_position={data.get('lesson_position')!r}")
    if data.get("module") != expected_module:
        errors.append(f"{path.name}: module={data.get('module')!r}; esperado {expected_module}")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: falta {section}")
    adapted_from = data.get("adapted_from", "")
    for source_path in adapted_from.split(" + ") if adapted_from else []:
        if not (ROOT / source_path).is_file():
            errors.append(f"{path.name}: adapted_from não resolve: {source_path}")

if actual_ids != EXPECTED_LESSONS:
    errors.append(f"ordem/ids divergentes: {actual_ids}")

question_count = 0
for path in quiz_files:
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    if data.get("type") != "quiz" or data.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de quiz inválido")
    questions = re.findall(r"^### \d+\.", text, re.MULTILINE)
    question_count += len(questions)
    if len(questions) != 4:
        errors.append(f"{path.name}: esperado 4 questões; encontradas {len(questions)}")
    if "<details>" not in text or "## Transferência" not in text:
        errors.append(f"{path.name}: falta gabarito ou transferência")

if question_count != 32:
    errors.append(f"esperadas 32 questões; encontradas {question_count}")

for filename in REQUIRED_ROOT_FILES:
    if not (COURSE / filename).exists():
        errors.append(f"arquivo obrigatório ausente: {filename}")

term_map = (COURSE / "Mapa-de-termos.md").read_text(encoding="utf-8")
mapped_lessons = set(re.findall(r"\(aulas/([^)#]+\.md)(?:#[^)]+)?\)", term_map))
expected_lesson_files = {path.name for path in lesson_files}
if mapped_lessons != expected_lesson_files:
    missing = sorted(expected_lesson_files - mapped_lessons)
    extra = sorted(mapped_lessons - expected_lesson_files)
    errors.append(f"mapa de termos sem cobertura 1:1; ausentes={missing}; extras={extra}")

agent_guide = (COURSE / "AGENT-GUIDE.md").read_text(encoding="utf-8")
for section in ["## Algoritmo obrigatório", "## Formato mínimo", "## Roteamento por intenção", "## Falhas seguras"]:
    if section not in agent_guide:
        errors.append(f"AGENT-GUIDE.md: falta {section}")

if (ROOT / "package.json").exists():
    guide_path = f"{SCOPE}/AGENT-GUIDE.md"
    for bootstrap_name in ["AGENTS.md", "CLAUDE.md"]:
        bootstrap = ROOT / bootstrap_name
        if not bootstrap.exists() or guide_path not in bootstrap.read_text(encoding="utf-8"):
            errors.append(f"bootstrap sem rota para o curso: {bootstrap_name}")

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    course_entry = catalog.get("courses", {}).get(COURSE_ID, {})
    if course_entry.get("path") != SCOPE or course_entry.get("agent_guide") != guide_path:
        errors.append("catalog.json: curso ou agent_guide não registrados")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if f'{SCOPE}/_tools/validate_course.py' not in package.get("scripts", {}).get("validate", ""):
        errors.append("package.json: validador do curso fora de npm run validate")

for path in COURSE.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".py"}:
        continue
    text = path.read_text(encoding="utf-8")
    if ABSOLUTE_PATH.search(text):
        errors.append(f"{path.relative_to(COURSE)}: path absoluto específico de máquina")
    if path.suffix != ".md":
        continue
    for raw_target in LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(COURSE.resolve()):
            errors.append(f"{path.relative_to(COURSE)}: link sai do curso -> {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(COURSE)}: link não resolve -> {target}")

print(
    f"Introdução à Arquitetura de Sistemas: {len(lesson_files)} aulas, "
    f"{len(module_files)} módulos, {len(quiz_files)} quizzes, {question_count} questões"
)
print(f"Erros: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")
if errors:
    sys.exit(1)
