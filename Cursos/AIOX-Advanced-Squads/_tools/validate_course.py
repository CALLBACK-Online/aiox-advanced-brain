from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


COURSE = Path(__file__).resolve().parents[1]
EXPECTED_SQUADS = [
    "advisory-board",
    "research",
    "code-anatomist",
    "domain-decoder",
    "agent-autonomy",
    "claude-code-mastery",
    "aiox-sop",
    "etl-ops",
    "runner-ops",
    "data",
    "db-sage",
    "clickup-ops-squad",
    "brand",
    "design-system",
    "design-ops",
    "storytelling",
    "slides-creator",
    "conteudo",
    "copy",
    "sales",
    "hormozi",
    "skill-creator-ops",
    "squad-creator",
    "squad-creator-pro",
]
REQUIRED_SECTIONS = [
    "## Resultado",
    "## Quando usar — e quando não usar",
    "## Prepare a entrada",
    "## Como ativar",
    "## Execução guiada",
    "## Briefing copiável",
    "## Evidência de conclusão",
    "## Limites neste acervo",
    "## Prática",
]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


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
quiz_files = sorted((COURSE / "avaliacoes").glob("Quiz-*.md"))

intro_files = [p for p in lesson_files if p.name.startswith("00-")]
squad_lesson_files = [p for p in lesson_files if not p.name.startswith("00-")]

if len(squad_lesson_files) != 24:
    errors.append(f"esperadas 24 aulas de squad; encontradas {len(squad_lesson_files)}")
if len(intro_files) < 1:
    errors.append("esperada ao menos 1 aula intro (00-*)")
if len(module_files) != 6:
    errors.append(f"esperados 6 módulos; encontrados {len(module_files)}")
if len(quiz_files) != 6:
    errors.append(f"esperados 6 quizzes; encontrados {len(quiz_files)}")

actual_squads: list[str] = []
lesson_metadata: list[dict[str, str]] = []

for path in intro_files:
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    if data.get("type") != "lesson" or data.get("course") != "aiox-advanced-squads":
        errors.append(f"{path.name}: frontmatter de intro inválido")
    if data.get("lesson_kind") != "intro":
        errors.append(f"{path.name}: lesson_kind deve ser intro")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: seção ausente {section}")

for position, path in enumerate(squad_lesson_files, 1):
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    lesson_metadata.append(data)
    actual_squads.append(data.get("squad", ""))
    required = {
        "type": "lesson",
        "course": "aiox-advanced-squads",
        "lesson_position": str(position),
        "status": "canonical",
        "canonical_scope": "Cursos/AIOX-Advanced-Squads",
    }
    for key, expected in required.items():
        if data.get(key) != expected:
            errors.append(f"{path.name}: {key}={data.get(key)!r}; esperado {expected!r}")
    if data.get("maturity") not in {"partial", "study"}:
        errors.append(f"{path.name}: maturity inválida")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: seção ausente {section}")
    if "## Pré-requisito no AIOX Advanced" not in text:
        errors.append(f"{path.name}: falta bloco Pré-requisito no AIOX Advanced")

if actual_squads != EXPECTED_SQUADS:
    errors.append(f"ordem/cobertura de squads divergente: {actual_squads}")

catalog_path = COURSE.parents[1] / "catalog.json"
if catalog_path.exists():
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if sorted(catalog.get("squads", [])) != sorted(EXPECTED_SQUADS):
        errors.append("catálogo e currículo divergem na cobertura dos squads")
    squad_meta = catalog.get("squad_meta", {})
    for data in lesson_metadata:
        name = data.get("squad", "")
        expected = squad_meta.get(name, {})
        for field in ("maturity", "agents", "tasks", "workflows"):
            if str(expected.get(field, "")) != data.get(field):
                errors.append(
                    f"{name}: {field}={data.get(field)!r}; catálogo={expected.get(field)!r}"
                )

for path in COURSE.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(COURSE):
            errors.append(f"{path.relative_to(COURSE)}: link sai do curso -> {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(COURSE)}: link não resolve -> {target}")

for path in quiz_files:
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    questions = re.findall(r"(?m)^### \d+\. ", text)
    answers = re.findall(r"(?m)^\*\*\d+\. [A-D]\*\*", text)
    if data.get("question_count") != "4" or len(questions) != 4 or len(answers) != 4:
        errors.append(f"{path.name}: quiz deve ter 4 questões e 4 respostas")

print(
    f"AIOX Advanced Squads: {len(lesson_files)} aulas "
    f"({len(intro_files)} intro + {len(squad_lesson_files)} squads), "
    f"{len(module_files)} módulos, {len(quiz_files)} quizzes"
)
print(f"Squads cobertos: {len([name for name in actual_squads if name])}/24")
print(f"Erros: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")

if errors:
    sys.exit(1)
