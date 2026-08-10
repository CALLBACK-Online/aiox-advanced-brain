from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


COURSE = Path(__file__).resolve().parents[1]
VAULT = COURSE.parents[1]
COURSES = VAULT / "cursos"
WIKILINK = re.compile(r"!?(?:\[\[)([^\]]+)(?:\]\])")


def normalized_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
    return target.lstrip("/")


course_files = [path for path in COURSES.rglob("*") if path.is_file()]
by_stem: dict[str, list[Path]] = defaultdict(list)
by_suffix: dict[str, list[Path]] = defaultdict(list)
by_exact: dict[str, list[Path]] = defaultdict(list)

for path in course_files:
    relative = path.relative_to(VAULT)
    exact_parts = relative.as_posix().split("/")
    by_exact[path.name].append(path)
    for index in range(len(exact_parts)):
        by_exact["/".join(exact_parts[index:])].append(path)
    if path.suffix == ".md":
        by_stem[path.stem].append(path)
        no_suffix_parts = relative.with_suffix("").as_posix().split("/")
        for index in range(len(no_suffix_parts)):
            by_suffix["/".join(no_suffix_parts[index:])].append(path)

unresolved = []
ambiguous = []
outside_course = []
wikilinks = 0

for source in sorted(COURSE.rglob("*.md")):
    text = source.read_text(encoding="utf-8")
    for line_number, raw in enumerate(text.splitlines(), 1):
        for match in WIKILINK.finditer(raw):
            wikilinks += 1
            target = normalized_target(match.group(1))
            if not target:
                continue
            if Path(target).suffix:
                candidates = by_exact.get(target, [])
                if not candidates:
                    candidates = by_stem.get(target, [])
            elif "/" in target:
                candidates = by_suffix.get(target, [])
            else:
                candidates = by_stem.get(target, [])
            unique = sorted(set(candidates))
            if not unique:
                unresolved.append((source, line_number, target))
            elif len(unique) > 1:
                exact_course = [path for path in unique if path.is_relative_to(COURSE)]
                if len(exact_course) != 1:
                    ambiguous.append((source, line_number, target, unique))
            resolved = [path for path in unique if path.is_relative_to(COURSE)]
            if unique and not resolved:
                outside_course.append((source, line_number, target, unique[0]))

lesson_files = sorted((COURSE / "lessons").glob("*.md"))
metadata_errors = []
lesson_tracks = Counter()
lesson_modules = Counter()
for path in lesson_files:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    data = yaml.safe_load(match.group(1)) if match else {}
    for field in ("module", "sequence", "track", "status", "canonical_scope"):
        if not data.get(field):
            metadata_errors.append((path, field))
    if data.get("manual") is not True:
        metadata_errors.append((path, "manual=true"))
    if "⌂ [[cursos/AIOX Advanced/README|Curso]]" not in text:
        metadata_errors.append((path, "navegação editorial"))
    lesson_tracks[data.get("track")] += 1
    lesson_modules[data.get("module")] += 1

expected_tracks = {"essential": 32, "complete": 38, "legacy": 4, "support": 1}
if dict(lesson_tracks) != expected_tracks:
    metadata_errors.append((COURSE / "README.md", f"trilhas={dict(lesson_tracks)}"))

expected_curriculum_modules = {f"M{index}" for index in range(13)} | {"MC"}
expected_lesson_modules = expected_curriculum_modules | {"SUP"}
if set(lesson_modules) != expected_lesson_modules:
    metadata_errors.append(
        (COURSE / "README.md", f"módulos de aula={sorted(lesson_modules)}")
    )

module_files = sorted((COURSE / "modulos").glob("*.md"))
module_ids = set()
for path in module_files:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    data = yaml.safe_load(match.group(1)) if match else {}
    module_ids.add(data.get("module"))
    for field in ("module", "sequence", "status", "canonical_scope", "source_version"):
        if data.get(field) is None:
            metadata_errors.append((path, field))
    if "## Rota Essencial" not in text or "## Evidência de conclusão" not in text:
        metadata_errors.append((path, "estrutura pedagógica"))
    if "## Checkpoint" not in text or "## Navegação" not in text:
        metadata_errors.append((path, "checkpoint/navegação"))

if module_ids != expected_curriculum_modules:
    metadata_errors.append((COURSE / "README.md", f"MOCs={sorted(module_ids)}"))

quiz_files = sorted((COURSE / "avaliacoes").glob("Quiz *.md"))
quiz_modules = set()
question_texts = []
answer_positions = Counter()
question_total = 0
for path in quiz_files:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    data = yaml.safe_load(match.group(1)) if match else {}
    quiz_modules.add(data.get("module"))
    questions = re.findall(r"(?m)^### \d+\. (.+)$", text)
    answers = re.findall(r"(?m)^\*\*\d+\. ([A-D])\*\*", text)
    question_total += len(questions)
    question_texts.extend(re.sub(r"\s+", " ", item.lower()).strip() for item in questions)
    answer_positions.update(answers)
    if data.get("question_count") != len(questions) or len(answers) != len(questions):
        metadata_errors.append((path, "contagem de questões/gabarito"))
    if data.get("passing_score") != 80:
        metadata_errors.append((path, "passing_score=80"))
    if "Em uma situação real do seu projeto, o próximo passo correto" in text:
        metadata_errors.append((path, "pergunta genérica residual"))

duplicate_questions = [
    question for question, count in Counter(question_texts).items() if count > 1
]
if quiz_modules != expected_curriculum_modules:
    metadata_errors.append((COURSE / "Assessments.md", f"quizzes={sorted(quiz_modules)}"))
if duplicate_questions:
    metadata_errors.append((COURSE / "Assessments.md", "questões duplicadas"))
if answer_positions and max(answer_positions.values()) - min(answer_positions.values()) > 1:
    metadata_errors.append(
        (COURSE / "Assessments.md", f"gabarito desbalanceado={dict(answer_positions)}")
    )

print(f"arquivos Markdown no curso: {len(list(COURSE.rglob('*.md')))}")
print(f"aulas: {len(lesson_files)}")
print(f"módulos curriculares: {len(module_files)}")
print(f"quizzes: {len(quiz_files)}")
print(f"questões curadas: {question_total}")
print(f"gabarito por posição: {dict(sorted(answer_positions.items()))}")
print(f"trilhas: {dict(sorted(lesson_tracks.items()))}")
print(f"wikilinks verificados: {wikilinks}")
print(f"links não resolvidos dentro de /cursos: {len(unresolved)}")
print(f"links ambíguos dentro de /cursos: {len(ambiguous)}")
print(f"links fora da pasta do curso: {len(outside_course)}")
print(f"erros de metadados/navegação: {len(metadata_errors)}")

for source, line_number, target in unresolved:
    print(f"UNRESOLVED {source.relative_to(VAULT)}:{line_number} -> {target}")
for source, line_number, target, candidates in ambiguous:
    paths = ", ".join(str(path.relative_to(VAULT)) for path in candidates)
    print(f"AMBIGUOUS {source.relative_to(VAULT)}:{line_number} -> {target}: {paths}")
for source, line_number, target, resolved in outside_course:
    print(
        f"OUTSIDE_COURSE {source.relative_to(VAULT)}:{line_number} -> "
        f"{target}: {resolved.relative_to(VAULT)}"
    )
for path, field in metadata_errors:
    print(f"METADATA {path.relative_to(VAULT)} -> {field}")

if (
    unresolved
    or ambiguous
    or outside_course
    or metadata_errors
    or len(lesson_files) != 75
    or len(module_files) != 14
    or len(quiz_files) != 14
    or question_total != 62
):
    sys.exit(1)
