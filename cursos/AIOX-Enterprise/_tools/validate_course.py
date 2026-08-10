#!/usr/bin/env python3
"""Validador da trilha AIOX Enterprise — Visão Operacional e Prontidão.

Além da estrutura (curriculum.yaml como fonte de verdade), aplica o contrato
anti-vazamento da trilha: descrever a experiência sem entregar comandos,
schemas, árvores internas, paths proprietários, prompts/workflows completos
ou nomes de ativos não publicados neste acervo.
"""
from __future__ import annotations

import re
import sys
import json
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
ROOT = COURSE.parents[1]
COURSE_ID = "aiox-enterprise"
SCOPE = "cursos/AIOX-Enterprise"
OFFICIAL_URL = "lp.aioxsquad.ai/enterprise"

REQUIRED_SECTIONS = [
    "## Resultado",
    "## O cenário",
    "## O que muda no Enterprise",
    "## O que não muda",
    "## Portão de diagnóstico",
    "## Navegação",
]
EXPECTED_MODULES = [
    "01-da-competencia-ao-gargalo.md",
    "02-operacao-como-sistema.md",
    "03-prontidao-e-decisao.md",
]
REQUIRED_FILES = [
    "README.md",
    "FAQ.md",
    "RECURSOS.md",
    "PROVENIENCIA.md",
    "AGENT-GUIDE.md",
    "COURSE-BRIEF.md",
    "GAP-ANALYSIS.md",
    "curriculum.yaml",
    "avaliacoes/diagnostico-de-prontidao.md",
]

# Tokens que indicariam vazamento de implementação ou de ativos não publicados.
FORBIDDEN_TOKENS = [
    "```",            # nenhum bloco de código: sem comandos, prompts ou workflows completos
    "cp -R",
    "config.yaml",
    "git clone",
    "git pull",
    "npm run",
    "npx ",
    "aiox init",
    "aiox install",
    "├",              # árvores de diretório
    "└",
    "sinkra",         # hub privado
    "aiox-ads",       # ativos apenas no upstream (catalog.json → source_only_upstream)
    "backlog-ops",
    "codex-mastery",
    "content-geo",
    "creator-economy",
    "workspace/businesses/",
    ".aiox-core/",
    ".claude/",
    ".codex/",
    "/Users/",
    "/home/",
    "C:\\",
]
# Paths de pacote reproduzíveis não pertencem à trilha (descrever ≠ entregar).
FORBIDDEN_PATTERNS = [
    (re.compile(r"squads/[a-z0-9-]+/"), "path de pacote de squad"),
    (re.compile(r"skills/[a-z0-9-]+/"), "path de pacote de skill"),
]

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def parse_curriculum(path: Path) -> list[dict[str, str]]:
    lessons: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_lessons = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("lessons:"):
            in_lessons = True
            continue
        if in_lessons and raw and not raw.startswith(" "):
            in_lessons = False
        if not in_lessons:
            continue
        stripped = raw.strip()
        if stripped.startswith("- position:"):
            current = {"position": stripped.split(":", 1)[1].strip()}
            lessons.append(current)
        elif current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    return lessons


errors: list[str] = []

curriculum_path = COURSE / "curriculum.yaml"
if not curriculum_path.exists():
    print("Erros: 1")
    print("ERROR curriculum.yaml ausente")
    sys.exit(1)
curriculum = parse_curriculum(curriculum_path)
if len(curriculum) != 7:
    errors.append(f"curriculum.yaml: esperadas 7 aulas; encontradas {len(curriculum)}")
if sum(int(item.get("reading_minutes", "0")) for item in curriculum) != 30:
    errors.append("curriculum.yaml: duração das aulas deve somar 30 minutos")
curriculum_text = curriculum_path.read_text(encoding="utf-8")
if "implementation_boundary:" not in curriculum_text or "deviations:" not in curriculum_text:
    errors.append("curriculum.yaml: fronteira de IP ou desvio curricular ausente")

lesson_files = sorted((COURSE / "aulas").glob("*.md"))
if len(lesson_files) != len(curriculum):
    errors.append(
        f"aulas/: {len(lesson_files)} arquivos para {len(curriculum)} aulas no curriculum"
    )

by_position = {entry["position"]: entry for entry in curriculum}
for path in lesson_files:
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    position = data.get("lesson_position", "")
    expected = by_position.get(position)
    if expected is None:
        errors.append(f"{path.name}: lesson_position={position!r} fora do curriculum")
    else:
        if data.get("lesson_id") != expected.get("id"):
            errors.append(
                f"{path.name}: lesson_id={data.get('lesson_id')!r}; curriculum espera {expected.get('id')!r}"
            )
        if data.get("reading_minutes") != expected.get("reading_minutes"):
            errors.append(
                f"{path.name}: reading_minutes={data.get('reading_minutes')!r}; "
                f"curriculum espera {expected.get('reading_minutes')!r}"
            )
        if not path.name.startswith(f"{int(position):02d}-"):
            errors.append(f"{path.name}: nome não começa com {int(position):02d}-")
    if data.get("type") != "lesson" or data.get("course") != COURSE_ID:
        errors.append(f"{path.name}: frontmatter de aula inválido")
    if data.get("status") != "canonical" or data.get("canonical_scope") != SCOPE:
        errors.append(f"{path.name}: status/canonical_scope incorretos")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: falta {section}")

module_files = sorted((COURSE / "modulos").glob("*.md"))
if [path.name for path in module_files] != EXPECTED_MODULES:
    errors.append(
        "modulos/: ordem ou cobertura divergente: "
        f"{[path.name for path in module_files]}"
    )
for position, path in enumerate(module_files, 1):
    data = frontmatter(path.read_text(encoding="utf-8"))
    for key, expected_value in {
        "type": "module",
        "course": COURSE_ID,
        "module_position": str(position),
        "status": "canonical",
        "canonical_scope": SCOPE,
    }.items():
        if data.get(key) != expected_value:
            errors.append(f"{path.name}: {key} divergente")

for relative in REQUIRED_FILES:
    if not (COURSE / relative).exists():
        errors.append(f"arquivo obrigatório ausente: {relative}")

readme_text = (COURSE / "README.md").read_text(encoding="utf-8") if (COURSE / "README.md").exists() else ""
if OFFICIAL_URL not in readme_text:
    errors.append("README.md: falta link da página oficial (fonte canônica de condições)")
readme_frontmatter = frontmatter(readme_text)
for key, expected_value in {
    "course": COURSE_ID,
    "title": "AIOX Enterprise — Visão Operacional e Prontidão",
    "kind": "preview",
    "status": "canonical",
    "lessons": "7",
    "modules": "3",
    "duration_minutes": "30",
}.items():
    if readme_frontmatter.get(key) != expected_value:
        errors.append(f"README.md: {key} divergente")
final_lesson = COURSE / "aulas" / "06-o-primeiro-passo-se-houver-fit.md"
if final_lesson.exists() and OFFICIAL_URL not in final_lesson.read_text(encoding="utf-8"):
    errors.append(f"{final_lesson.name}: falta link da página oficial no primeiro passo")

public_files = sorted(COURSE.rglob("*.md"))
for path in public_files:
    text = path.read_text(encoding="utf-8")
    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"{path.relative_to(COURSE)}: vazamento — contém {token!r}")
    for pattern, label in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.relative_to(COURSE)}: vazamento — {label}")

for path in COURSE.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith("mailto:"):
            continue
        if target.startswith(("http://", "https://")):
            if OFFICIAL_URL not in target:
                errors.append(f"{path.relative_to(COURSE)}: link externo não permitido -> {target}")
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(COURSE.resolve()):
            errors.append(f"{path.relative_to(COURSE)}: link sai do curso -> {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(COURSE)}: link não resolve -> {target}")

catalog_path = ROOT / "catalog.json"
package_path = ROOT / "package.json"
if catalog_path.exists() and package_path.exists():
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    course = catalog.get("courses", {}).get(COURSE_ID, {})
    for key, expected_value in {
        "path": SCOPE,
        "kind": "preview",
        "lessons": 7,
        "modules": 3,
        "duration_minutes": 30,
        "hub": "cursos/README.md",
        "agent_guide": f"{SCOPE}/AGENT-GUIDE.md",
        "assessment": f"{SCOPE}/avaliacoes/diagnostico-de-prontidao.md",
    }.items():
        if course.get(key) != expected_value:
            errors.append(f"catalog.json: courses.{COURSE_ID}.{key} divergente")
    supplemental = next(
        (
            item
            for item in catalog.get("supplemental_courses", [])
            if item.get("path") == SCOPE
        ),
        {},
    )
    for key, expected_value in {
        "markdown_files": 18,
        "lessons": 7,
        "modules": 3,
        "kind": "preview",
        "title": "AIOX Enterprise — Visão Operacional e Prontidão",
        "agent_guide": f"{SCOPE}/AGENT-GUIDE.md",
    }.items():
        if supplemental.get(key) != expected_value:
            errors.append(f"catalog.json: supplemental Enterprise {key} divergente")
    validate_script = json.loads(package_path.read_text(encoding="utf-8")).get("scripts", {}).get("validate", "")
    if f"{SCOPE}/_tools/validate_course.py" not in validate_script:
        errors.append("package.json: validador Enterprise ausente de npm run validate")

for bootstrap_name in ["AGENTS.md", "CLAUDE.md"]:
    bootstrap = ROOT / bootstrap_name
    if not bootstrap.exists() or f"{SCOPE}/AGENT-GUIDE.md" not in bootstrap.read_text(encoding="utf-8"):
        errors.append(f"{bootstrap_name}: descoberta automática da trilha ausente")

for navigation_path in [
    ROOT / "README.md",
    ROOT / "JORNADA-AIOX.md",
    ROOT / "cursos" / "README.md",
    ROOT / "cursos" / "MOC-Acervo-AIOX.md",
]:
    if not navigation_path.exists() or f"{SCOPE}/README.md" not in navigation_path.read_text(encoding="utf-8"):
        errors.append(f"{navigation_path.relative_to(ROOT)}: rota da trilha ausente")

print(
    f"AIOX Enterprise (preview): {len(module_files)} módulos, "
    f"{len(lesson_files)} aulas, contrato anti-vazamento ativo"
)
print(f"Erros: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")
if errors:
    sys.exit(1)
