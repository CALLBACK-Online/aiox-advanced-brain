#!/usr/bin/env python3
"""Cria scaffold de curso e harness a partir de outline JSON aprovado."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from course_common import normalize_creation_mode, validate_approval_artifacts

PACK = Path(__file__).resolve().parents[1]
TEMPLATES = PACK / "assets" / "course-templates"
KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MODULE_ID = re.compile(r"M(?:\d+|C)")

PROFILES = {
    "fundacional": (
        "lesson-decision-map.md",
        ["## Resultado", "## Mapa visual", "## Prática", "## Evidência de conclusão", "## Navegação"],
    ),
    "tecnico-operacional": (
        "lesson-fundamentals.md",
        [
            "## Objetivo",
            "## Contexto",
            "## Erro comum",
            "## Prática",
            "## Recuperação sem IA",
            "## Evidência",
            "## Fontes no snapshot",
            "## Navegação",
        ],
    ),
    "decisorio-aplicado": (
        "lesson-decision-map.md",
        ["## Resultado", "## Mapa visual", "## Prática", "## Evidência de conclusão", "## Navegação"],
    ),
    "catalogo-roteamento": (
        "lesson-operational.md",
        [
            "## Resultado",
            "## Quando usar — e quando não usar",
            "## Prepare a entrada",
            "## Como ativar",
            "## Briefing copiável",
            "## Evidência de conclusão",
            "## Limites neste acervo",
            "## Navegação",
        ],
    ),
    "preview-protegido": (
        "lesson-preview.md",
        [
            "## Resultado",
            "## O cenário",
            "## O que muda",
            "## O que não muda",
            "## Portão de diagnóstico",
            "## Navegação",
        ],
    ),
    "migracao-profunda": (
        "lesson-migration.md",
        [
            "## O que você consegue no fim desta aula",
            "## Mapa desta aula",
            "## Portão da aula",
            "## Origem curricular",
            "## Navegação",
        ],
    ),
}

OPTIONAL_ARTIFACTS = {
    "AGENT-GUIDE.md",
    "Glossario.md",
    "Mapa-de-decisao.md",
    "Mapa-de-termos.md",
}


def find_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "catalog.json").is_file() and (candidate / "package.json").is_file():
            return candidate
    raise SystemExit("raiz do acervo não encontrada (catalog.json + package.json)")


def read_template(name: str) -> str:
    path = TEMPLATES / name
    if not path.is_file():
        raise SystemExit(f"template ausente: {path}")
    return path.read_text(encoding="utf-8")


def slugify(value: str) -> str:
    normalized = value.lower()
    for source, target in {
        "á": "a",
        "à": "a",
        "â": "a",
        "ã": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c",
    }.items():
        normalized = normalized.replace(source, target)
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", normalized))


def validate_spec(spec: dict) -> tuple[Path, list[dict]]:
    required = (
        "course_id",
        "title",
        "path",
        "profile",
        "creation_mode",
        "modules",
        "approval_artifacts",
    )
    missing = [field for field in required if not spec.get(field)]
    if missing:
        raise SystemExit(f"spec sem campos obrigatórios: {missing}")
    if not KEBAB.fullmatch(spec["course_id"]):
        raise SystemExit("course_id deve ser kebab-case")
    if spec["profile"] not in PROFILES:
        raise SystemExit(f"profile inválido; use um de {sorted(PROFILES)}")
    spec["creation_mode"] = normalize_creation_mode(str(spec["creation_mode"]))

    relative = Path(spec["path"])
    if relative.is_absolute() or not relative.parts or relative.parts[0] != "cursos" or ".." in relative.parts:
        raise SystemExit("path deve ser relativo e começar com cursos/")
    if len(relative.parts) != 2:
        raise SystemExit("path deve apontar para uma pasta direta em cursos/")

    unknown_artifacts = set(spec.get("optional_artifacts") or []) - OPTIONAL_ARTIFACTS
    if unknown_artifacts:
        raise SystemExit(f"optional_artifacts desconhecidos: {sorted(unknown_artifacts)}")

    lessons: list[dict] = []
    seen_modules: set[str] = set()
    seen_lessons: set[str] = set()
    for module in spec["modules"]:
        module_id = module.get("id", "")
        if not MODULE_ID.fullmatch(module_id) or module_id in seen_modules:
            raise SystemExit(f"id de módulo inválido ou duplicado: {module_id!r}")
        seen_modules.add(module_id)
        if not module.get("title") or not module.get("lessons"):
            raise SystemExit(f"{module_id}: title e lessons são obrigatórios")
        for lesson in module["lessons"]:
            lesson_id = lesson.get("id", "")
            if not KEBAB.fullmatch(lesson_id) or lesson_id in seen_lessons:
                raise SystemExit(f"id de aula inválido ou duplicado: {lesson_id!r}")
            if not lesson.get("title"):
                raise SystemExit(f"{lesson_id}: title obrigatório")
            if spec["profile"] == "migracao-profunda":
                source_fields = ("source_lesson_id", "source_path", "source_version")
                if any(not lesson.get(field) for field in source_fields):
                    raise SystemExit(f"{lesson_id}: migração exige {source_fields}")
            lessons.append({**lesson, "module": module_id})
            seen_lessons.add(lesson_id)
    return relative, lessons


def replace_tokens(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(f"<{key}>", value)
    return text


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"write {path}")


def supporting_file(course_id: str, scope: str, filename: str) -> str:
    types = {
        "Assessments.md": "assessments",
        "Projeto-Integrador.md": "project",
        "Rubrica.md": "rubric",
        "FONTES.md": "sources",
        "PROVENIENCIA.md": "provenance",
        "Glossario.md": "glossary",
        "Mapa-de-decisao.md": "decision-map",
        "Mapa-de-termos.md": "term-map",
    }
    title = filename.removesuffix(".md").replace("-", " ")
    return f"""---
type: {types[filename]}
course: {course_id}
status: draft
canonical_scope: {scope}
---

# {title}

_DRAFT_
"""


def render_readme(spec: dict, scope: str, lessons: list[dict], module_files: dict[str, str], quizzes: int) -> str:
    links = []
    position = 1
    for module in spec["modules"]:
        links.append(f"## {module['id']} — {module['title']}")
        links.append("")
        links.append(f"[Módulo]({module_files[module['id']]})")
        links.append("")
        for lesson in module["lessons"]:
            links.append(f"- [{lesson['title']}](aulas/{position:02d}-{lesson['id']}.md)")
            position += 1
        links.append("")
    return f"""---
type: course
course: {spec['course_id']}
title: "{spec['title']}"
status: draft
canonical_scope: {scope}
sharing_boundary: cursos
lessons: {len(lessons)}
curriculum_modules: {len(spec['modules'])}
quizzes: {quizzes}
questions: {quizzes * 4}
---

# {spec['title']}

_DRAFT: promessa e anti-escopo._

## Entrada

_DRAFT: pré-requisito observável._

## Resultado

_DRAFT: performance terminal e artefato._

{chr(10).join(links)}
"""


def render_agent_guide(spec: dict, scope: str, lessons: list[dict]) -> str:
    routes = "\n".join(f"| {lesson['title']} | `aulas/{position:02d}-{lesson['id']}.md` |" for position, lesson in enumerate(lessons, 1))
    return f"""---
type: agent-guide
course: {spec['course_id']}
status: draft
canonical_scope: {scope}
---

# AGENT-GUIDE — {spec['title']}

## Roteamento

| Intenção | Aula |
|---|---|
{routes}

## Contrato pedagógico

_DRAFT_

## Algoritmo obrigatório

1. Abrir a aula antes de responder.
2. Exigir a evidência definida pela aula.
3. Não inventar fonte, asset ou runtime.

## Fronteira

_DRAFT: anti-sinais e curso vizinho._
"""


def render_module(spec: dict, module: dict, scope: str, lesson_positions: dict[str, int], filename: str) -> str:
    lesson_links = "\n".join(
        f"- [{lesson['title']}](../aulas/{lesson_positions[lesson['id']]:02d}-{lesson['id']}.md)"
        for lesson in module["lessons"]
    )
    checkpoint = f"[Quiz](../avaliacoes/Quiz-{module['id']}.md)" if module.get("quiz") else "Prática integrada do módulo"
    return f"""---
type: course-module
course: {spec['course_id']}
module: {module['id']}
status: draft
canonical_scope: {scope}
---

# {module['id']} — {module['title']}

## Resultado

_DRAFT_

## Aulas

{lesson_links}

## Checkpoint

{checkpoint}

## Evidência de conclusão

{module.get('evidence') or '_DRAFT_'}

[Curso](../README.md)
"""


def render_lesson(
    template: str,
    spec: dict,
    scope: str,
    lesson: dict,
    position: int,
    previous_path: str | None,
    next_path: str | None,
) -> str:
    mapping = {
        "slug": spec["course_id"],
        "lesson-id": lesson["id"],
        "Título": lesson["title"],
        "scope": scope,
        "Nome-Do-Curso": Path(spec["path"]).name,
        "source-lesson-id": str(lesson.get("source_lesson_id", "DRAFT")),
        "source-path": str(lesson.get("source_path", "DRAFT")),
        "source-version": str(lesson.get("source_version", "DRAFT")),
    }
    text = replace_tokens(template, mapping)
    text = text.replace(f"cursos/{Path(spec['path']).name}", scope)
    text = re.sub(r"(?m)^lesson_position:\s*\d+", f"lesson_position: {position}", text)
    text = re.sub(r"(?m)^module:\s*M(?:\d+|C)", f"module: {lesson['module']}", text)
    if "reading_minutes:" in text:
        text = re.sub(
            r"(?m)^reading_minutes:\s*\d+",
            f"reading_minutes: {int(lesson.get('reading_minutes', 10))}",
            text,
        )
    navigation = []
    if previous_path:
        navigation.append(f"[← Anterior]({previous_path})")
    navigation.append("[↑ Curso](../README.md)")
    if next_path:
        navigation.append(f"[Próxima →]({next_path})")
    navigation_block = "## Navegação\n\n" + " · ".join(navigation)
    if "## Navegação" in text:
        text = re.sub(r"## Navegação\n[\s\S]*$", navigation_block, text)
    else:
        text = re.sub(r"(?m)^Próxima: \[próxima aula\]\(02-stub\.md\)\.\s*$", "", text)
        text = text.rstrip() + "\n\n" + navigation_block + "\n"
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold seguro de curso a partir de course-spec JSON")
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    spec_path = args.spec if args.spec.is_absolute() else root / args.spec
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    relative, lessons = validate_spec(spec)
    if spec["creation_mode"] != "create":
        raise SystemExit("scaffold_course aceita somente creation_mode=create; use plan_upgrade no brownfield")
    scope = relative.as_posix()
    course = root / relative
    harness = root / "dev" / "courses" / spec["course_id"]
    bastidor = root / "docs" / "producao-cursos" / spec["course_id"]
    validate_approval_artifacts(root, spec)

    existing = [path for path in (course, harness) if path.exists()]
    if existing:
        raise SystemExit(f"destino já existe; scaffold não sobrescreve: {[str(path) for path in existing]}")
    canonical_spec = bastidor / "course-spec.json"
    if canonical_spec.exists() and canonical_spec.resolve() != spec_path.resolve():
        raise SystemExit(f"spec canônica já existe; use-a sem sobrescrever: {canonical_spec}")

    if args.dry_run:
        print(json.dumps({"course": str(course), "harness": str(harness), "bastidor": str(bastidor), "lessons": len(lessons)}, indent=2, ensure_ascii=False))
        return 0

    lesson_positions = {lesson["id"]: position for position, lesson in enumerate(lessons, 1)}
    module_files = {
        module["id"]: f"modulos/{module['id']}-{slugify(module['title'])}.md"
        for module in spec["modules"]
    }
    quiz_modules = [module for module in spec["modules"] if module.get("quiz")]
    required_root = ["README.md", "FONTES.md", "PROVENIENCIA.md"]
    optional_artifacts = list(spec.get("optional_artifacts") or [])
    required_root.extend(optional_artifacts)
    if quiz_modules or spec.get("capstone"):
        required_root.append("Assessments.md")
    if spec.get("capstone"):
        required_root.extend(["Projeto-Integrador.md", "Rubrica.md"])

    write(course / "README.md", render_readme(spec, scope, lessons, module_files, len(quiz_modules)))
    for filename in [name for name in required_root if name != "README.md"]:
        if filename == "AGENT-GUIDE.md":
            write(course / filename, render_agent_guide(spec, scope, lessons))
        else:
            write(course / filename, supporting_file(spec["course_id"], scope, filename))

    template_name, required_sections = PROFILES[spec["profile"]]
    lesson_template = read_template(template_name)
    for position, lesson in enumerate(lessons, 1):
        previous_path = f"{position - 1:02d}-{lessons[position - 2]['id']}.md" if position > 1 else None
        next_path = f"{position + 1:02d}-{lessons[position]['id']}.md" if position < len(lessons) else None
        write(
            course / "aulas" / f"{position:02d}-{lesson['id']}.md",
            render_lesson(lesson_template, spec, scope, lesson, position, previous_path, next_path),
        )

    for module in spec["modules"]:
        filename = module_files[module["id"]].removeprefix("modulos/")
        write(course / "modulos" / filename, render_module(spec, module, scope, lesson_positions, filename))

    quiz_template = read_template("quiz.md")
    for module in quiz_modules:
        quiz = replace_tokens(
            quiz_template,
            {"slug": spec["course_id"], "scope": scope, "Nome-Do-Curso": relative.name},
        )
        quiz = re.sub(r"(?m)^module:\s*M(?:\d+|C)", f"module: {module['id']}", quiz)
        quiz = quiz.replace("# Quiz M1 — <tema>", f"# Quiz {module['id']} — {module['title']}")
        write(course / "avaliacoes" / f"Quiz-{module['id']}.md", quiz)

    if not canonical_spec.exists():
        write(canonical_spec, json.dumps(spec, indent=2, ensure_ascii=False))

    manifest = replace_tokens(
        read_template("manifest.yaml"),
        {"slug": spec["course_id"], "Título": spec["title"], "Nome-Do-Curso": relative.name},
    ).replace(f'path: "cursos/{relative.name}"', f'path: "{scope}"')
    write(harness / "manifest.yaml", manifest)
    checks = replace_tokens(
        read_template("checks.py"),
        {
            "Título do curso": spec["title"],
            "slug": spec["course_id"],
            "scope": scope,
            "expected": repr([lesson["id"] for lesson in lessons]),
            "required_root": repr(required_root),
            "required_sections": repr(required_sections),
        },
    )
    write(harness / "checks.py", checks)

    print(
        f"\nScaffold criado em estado draft: {scope}\n"
        f"1. Aprovações preservadas em {bastidor.relative_to(root)}\n"
        f"2. Substituir _DRAFT_ em lotes e integrar catalog.json/journey\n"
        f"3. python3 dev/validate.py --course {spec['course_id']}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
