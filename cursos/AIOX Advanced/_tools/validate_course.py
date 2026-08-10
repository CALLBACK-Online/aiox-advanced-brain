#!/usr/bin/env python3
"""Valida a edição 2.0 do AIOX Advanced e sua migração curricular."""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parents[1]
VAULT = COURSE.parents[1]
COURSE_ID = "aiox-advanced"
SCOPE = "cursos/AIOX Advanced"
EXPECTED_SEQUENCE = [
    "01-token-economy-mindset", "08-principio-processo-certo",
    "12-repertorio-vs-tecnica", "13-pensamento-estruturado-antes-do-terminal",
    "26-nao-delegar-pensar", "03-claude-md-leis-da-fisica",
    "05-ambientes-local-staging-production", "15-quatro-executores",
    "16-janela-de-contexto", "17-engenharia-de-contexto",
    "18-yaml-markdown-json-sweet-spot", "25-core-config-leis-sociais",
    "27-otimizacao-claude-md", "06-code-rabbit-boost", "19-ciclo-do-repositorio",
    "46-etapas-de-desenvolvimento", "48-quality-gate-completo",
    "49-apply-qa-fixes-loop", "11-goal-vs-loop", "20-determinismo-progressivo",
    "21-deterministico-primeiro-llm-onde-gera-ouro", "50-rider-modo-elicitacao",
    "23-o-que-e-um-squad", "24-entidade-como-unidade-de-processo",
    "31-brownfield-discovery", "53-brownfield-enhancement", "44-metodo-s2s",
    "74-caso-integrado-end-to-end",
]
EXPECTED_MODULE_COUNTS = {"M0": 5, "M1": 8, "M2": 5, "M3": 4, "M4": 4, "MC": 2}
EXPECTED_MODULE_FILES = {
    "Módulo 0 - Mindset e Princípios", "Módulo 1 - Sistema e Contexto",
    "Módulo 2 - SDC e Qualidade", "Módulo 3 - Determinismo e Comando",
    "Módulo 4 - Método e Brownfield", "Módulo C - Capstone",
}
WIKILINK = re.compile(r"!?\[\[([^\]]+)\]\]")
ABSOLUTE_PATH = re.compile(r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/])")


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (yaml.safe_load(match.group(1)) or {}, text) if match else ({}, text)


errors: list[str] = []
lessons = list((COURSE / "lessons").glob("*.md"))
lesson_records: list[tuple[int, str]] = []
module_counts: Counter[str] = Counter()

if len(lessons) != 28:
    errors.append(f"esperadas 28 aulas ativas; encontradas {len(lessons)}")

for path in lessons:
    data, text = frontmatter(path)
    for field in ("module", "sequence", "track", "status", "canonical_scope"):
        if data.get(field) is None:
            errors.append(f"{path.name}: falta {field}")
    if data.get("course") != COURSE_ID or data.get("track") != "core":
        errors.append(f"{path.name}: course/track inválido")
    if data.get("status") != "canonical" or data.get("canonical_scope") != SCOPE:
        errors.append(f"{path.name}: status/scope inválido")
    if data.get("manual") is not True:
        errors.append(f"{path.name}: manual=true ausente")
    if "⌂ [[cursos/AIOX Advanced/README|Curso]]" not in text:
        errors.append(f"{path.name}: navegação editorial ausente")
    sequence = int(data.get("sequence") or 0)
    lesson_records.append((sequence, path.stem))
    module_counts[data.get("module")] += 1

actual_sequence = [stem for _, stem in sorted(lesson_records)]
if actual_sequence != EXPECTED_SEQUENCE:
    errors.append(f"sequência ativa divergente: {actual_sequence}")
if dict(module_counts) != EXPECTED_MODULE_COUNTS:
    errors.append(f"distribuição por módulo divergente: {dict(module_counts)}")

module_files = list((COURSE / "modulos").glob("*.md"))
if {path.stem for path in module_files} != EXPECTED_MODULE_FILES:
    errors.append(f"MOCs ativos divergentes: {[path.stem for path in module_files]}")
for path in module_files:
    data, text = frontmatter(path)
    if data.get("course") != COURSE_ID or data.get("module") not in EXPECTED_MODULE_COUNTS:
        errors.append(f"{path.name}: frontmatter de módulo inválido")
    for section in ("## Resultado", "## Evidência de conclusão", "## Checkpoint", "## Navegação"):
        if section not in text:
            errors.append(f"{path.name}: falta {section}")

quiz_files = list((COURSE / "avaliacoes").glob("Quiz *.md"))
question_total = 0
answer_positions: Counter[str] = Counter()
quiz_modules: set[str] = set()
for path in quiz_files:
    data, text = frontmatter(path)
    quiz_modules.add(data.get("module"))
    questions = re.findall(r"^### \d+\.", text, re.M)
    answers = re.findall(r"\*\*\d+\. ([A-D])\*\*", text)
    question_total += len(questions)
    answer_positions.update(answers)
    if data.get("type") != "quiz" or data.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de quiz inválido")
    if data.get("question_count") != 8 or len(questions) != 8 or len(answers) != 8:
        errors.append(f"{path.name}: contagem de questões/gabarito inválida")
    if data.get("passing_score") != 80 or "## Transferência" not in text:
        errors.append(f"{path.name}: gate pedagógico inválido")

if len(quiz_files) != 6 or quiz_modules != set(EXPECTED_MODULE_COUNTS):
    errors.append(f"quizzes ativos divergentes: {len(quiz_files)} / {sorted(quiz_modules)}")
if question_total != 48:
    errors.append(f"esperadas 48 questões; encontradas {question_total}")
if answer_positions and max(answer_positions.values()) - min(answer_positions.values()) > 1:
    errors.append(f"gabarito desbalanceado: {dict(answer_positions)}")

migrated = list((COURSE / "archive/migrated/lessons").glob("*.md"))
legacy = list((COURSE / "archive/legacy/lessons").glob("*.md"))
if len(migrated) != 42:
    errors.append(f"esperadas 42 aulas migradas; encontradas {len(migrated)}")
if len(legacy) != 4:
    errors.append(f"esperadas 4 aulas legacy; encontradas {len(legacy)}")
if not (COURSE / "support/75-faq-cohort-campo.md").exists():
    errors.append("FAQ de campo ausente em support/")

all_markdown = list(COURSE.rglob("*.md"))
by_stem: dict[str, list[Path]] = defaultdict(list)
for path in all_markdown:
    by_stem[path.stem].append(path)

for source in all_markdown:
    text = source.read_text(encoding="utf-8")
    if ABSOLUTE_PATH.search(text):
        errors.append(f"{source.relative_to(COURSE)}: path absoluto")
    for raw in WIKILINK.findall(text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip().lstrip("/")
        if not target:
            continue
        if target.startswith("cursos/") and source.is_relative_to(COURSE / "glossario/termos"):
            external = VAULT / (target if target.endswith(".md") else f"{target}.md")
            if external.exists():
                continue
        course_prefix = "cursos/AIOX Advanced/"
        local_target = target[len(course_prefix):] if target.startswith(course_prefix) else target
        direct = COURSE / (local_target if local_target.endswith(".md") else f"{local_target}.md")
        if direct.exists():
            continue
        candidates = by_stem.get(Path(target).stem, [])
        active = [path for path in candidates if "archive" not in path.parts]
        if len(active) == 1 or (not active and len(candidates) == 1):
            continue
        if not candidates:
            errors.append(f"{source.relative_to(COURSE)}: wikilink não resolvido: {target}")
        else:
            errors.append(f"{source.relative_to(COURSE)}: wikilink ambíguo: {target}")

if errors:
    print("AIOX Advanced: FALHA")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    "AIOX Advanced: 28 aulas ativas, 6 módulos, 6 quizzes, "
    f"{question_total} questões; arquivo 42+4+1; gabarito {dict(sorted(answer_positions.items()))}; erros: 0"
)
