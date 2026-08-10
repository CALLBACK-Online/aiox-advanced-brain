#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
COURSE_ID = "aiox-fundamentals"
SCOPE = "cursos/AIOX-Fundamentals"
SOURCE_COMMIT = "a68bd88f45e560f606e9bdc8a0f663570bdcef88"

EXPECTED_LESSONS = [
    ("lessons/01-fundamentos/1.1-o-que-e-aiox.md", "M1", "o-que-e-aiox"),
    ("lessons/01-fundamentos/1.2-cli-first-e-duas-fases.md", "M1", "cli-first-e-duas-fases"),
    ("lessons/01-fundamentos/1.3-anatomia-do-framework.md", "M1", "anatomia-do-framework"),
    ("lessons/01-fundamentos/1.4-instalacao-e-primeiro-valor.md", "M1", "instalacao-e-primeiro-valor"),
    ("lessons/02-sinais-e-contexto/2.1-ler-o-contexto-antes-de-agir.md", "M2", "ler-o-contexto-antes-de-agir"),
    ("lessons/02-sinais-e-contexto/2.2-escolher-o-agente-certo.md", "M2", "escolher-o-agente-certo"),
    ("lessons/02-sinais-e-contexto/2.3-task-skill-workflow-ou-squad.md", "M2", "task-skill-workflow-ou-squad"),
    ("lessons/02-sinais-e-contexto/2.4-greenfield-brownfield-e-story.md", "M2", "greenfield-brownfield-e-story"),
    ("lessons/03-validacao-basica/3.1-qualidade-em-tres-camadas.md", "M3", "qualidade-em-tres-camadas"),
    ("lessons/03-validacao-basica/3.2-autoridade-e-permissoes.md", "M3", "autoridade-e-permissoes"),
    ("lessons/03-validacao-basica/3.3-ciclo-da-story-na-pratica.md", "M3", "ciclo-da-story-na-pratica"),
    ("lessons/03-validacao-basica/3.4-evidencia-doctor-e-handoff.md", "M3", "evidencia-doctor-e-handoff"),
]
REQUIRED_SECTIONS = [
    "## Objetivo",
    "## Contexto",
    "## Erro comum",
    "## Prática",
    "## Recuperação sem IA",
    "## Evidência",
    "## Fontes no snapshot",
]
REQUIRED_ROOT_FILES = [
    ".metadata.json",
    "README.md",
    "AGENT-GUIDE.md",
    "COURSE-BRIEF.md",
    "course-outline.md",
    "curriculum.yaml",
    "deviations.yaml",
    "gap-analysis.md",
    "reformed-brief-validation-report.md",
    "FONTES.md",
    "PROVENIENCIA.md",
    "sources/SOURCE-MANIFEST.yaml",
    "assessments/final-project.md",
    "assessments/final-project-rubric.md",
]
EXPECTED_AGENTS = [
    "@aiox-master",
    "@analyst",
    "@architect",
    "@data-engineer",
    "@dev",
    "@devops",
    "@pm",
    "@po",
    "@qa",
    "@sm",
    "@squad-creator",
    "@ux-design-expert",
]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_PATH = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+[\\/])"
)


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


errors: list[str] = []
curriculum = (COURSE / "curriculum.yaml").read_text(encoding="utf-8")

for filename in REQUIRED_ROOT_FILES:
    if not (COURSE / filename).exists():
        errors.append(f"arquivo obrigatório ausente: {filename}")

metadata = json.loads((COURSE / ".metadata.json").read_text(encoding="utf-8"))
if metadata.get("source", {}).get("commit") != SOURCE_COMMIT:
    errors.append(".metadata.json: commit de origem divergente")
if metadata.get("curriculum", {}).get("lessons") != 12:
    errors.append(".metadata.json: contagem de aulas divergente")

lesson_files = sorted(path.relative_to(COURSE).as_posix() for path in (COURSE / "lessons").rglob("*.md"))
expected_paths = [item[0] for item in EXPECTED_LESSONS]
if lesson_files != expected_paths:
    errors.append(f"paths de aula divergentes: {lesson_files}")

for position, (relative, module, lesson_id) in enumerate(EXPECTED_LESSONS, start=1):
    path = COURSE / relative
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    expected = {
        "type": "lesson",
        "course": COURSE_ID,
        "module": module,
        "lesson_position": str(position),
        "lesson_id": lesson_id,
        "status": "canonical",
        "canonical_scope": SCOPE,
        "source_commit": SOURCE_COMMIT,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{relative}: {key}={data.get(key)!r}; esperado {value!r}")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{relative}: falta {section}")
    if relative not in curriculum:
        errors.append(f"curriculum.yaml: path ausente {relative}")

agent_lesson = (COURSE / EXPECTED_LESSONS[5][0]).read_text(encoding="utf-8")
for agent in EXPECTED_AGENTS:
    if agent not in agent_lesson:
        errors.append(f"aula de agents: falta {agent}")

quiz_files = sorted((COURSE / "assessments").glob("quiz-module-*.yaml"))
if len(quiz_files) != 3:
    errors.append(f"esperados 3 quizzes; encontrados {len(quiz_files)}")
question_count = 0
for path in quiz_files:
    text = path.read_text(encoding="utf-8")
    questions = re.findall(r"^  - question_id:", text, re.MULTILINE)
    question_count += len(questions)
    if len(questions) != 5:
        errors.append(f"{path.name}: esperadas 5 questões; encontradas {len(questions)}")
    if text.count("    correct:") != 5 or text.count("    rationale:") != 5:
        errors.append(f"{path.name}: gabarito/rationale incompleto")
    relative = path.relative_to(COURSE).as_posix()
    if relative not in curriculum:
        errors.append(f"curriculum.yaml: assessment ausente {relative}")
if question_count != 15:
    errors.append(f"esperadas 15 questões; encontradas {question_count}")

manifest = (COURSE / "sources/SOURCE-MANIFEST.yaml").read_text(encoding="utf-8")
if f'commit: "{SOURCE_COMMIT}"' not in manifest:
    errors.append("SOURCE-MANIFEST.yaml: commit divergente")
if len(re.findall(r"^  - path:", manifest, re.MULTILINE)) != 32:
    errors.append("SOURCE-MANIFEST.yaml: esperadas 32 fontes com hash")
if len(re.findall(r'^    sha256: "[0-9a-f]{64}"$', manifest, re.MULTILINE)) != 32:
    errors.append("SOURCE-MANIFEST.yaml: hashes ausentes ou inválidos")

for path in COURSE.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".yaml", ".json", ".py"}:
        continue
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(COURSE)
    if ABSOLUTE_PATH.search(text):
        errors.append(f"{relative}: path absoluto específico de máquina")
    if path.suffix != ".md":
        continue
    for raw_target in LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(COURSE.resolve()):
            errors.append(f"{relative}: link sai do curso -> {target}")
        elif not resolved.exists():
            errors.append(f"{relative}: link não resolve -> {target}")

print(
    f"AIOX Fundamentals: {len(lesson_files)} aulas, 3 módulos, "
    f"{len(quiz_files)} quizzes, {question_count} questões"
)
print(f"Fontes com hash: {len(re.findall(r'^  - path:', manifest, re.MULTILINE))}")
print(f"Erros: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")
if errors:
    sys.exit(1)
