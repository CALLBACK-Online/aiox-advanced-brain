#!/usr/bin/env python3
"""Validador leve do mini-curso Obsidian + IA (autocontido na pasta do curso)."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
EXPECTED = [
    "por-que-obsidian-ia",
    "abrir-o-vault",
    "wikilinks-e-grafo",
    "agent-como-professor",
    "captura-sem-poluir",
    "mocs-e-hubs",
    "do-estudo-a-execucao",
    "pratica-integrada",
]
REQUIRED_SECTIONS = [
    "## Resultado",
    "## Quando usar — e quando não usar",
    "## Prática",
    "## Evidência de conclusão",
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

if len(lesson_files) != 8:
    errors.append(f"esperadas 8 aulas; encontradas {len(lesson_files)}")

actual_ids: list[str] = []
for position, path in enumerate(lesson_files):
    text = path.read_text(encoding="utf-8")
    data = frontmatter(text)
    lid = data.get("lesson_id", "")
    actual_ids.append(lid)
    if data.get("type") != "lesson" or data.get("course") != "obsidian-ia":
        errors.append(f"{path.name}: frontmatter inválido")
    if data.get("status") != "canonical":
        errors.append(f"{path.name}: status deve ser canonical")
    if data.get("canonical_scope") != "Cursos/Obsidian-IA":
        errors.append(f"{path.name}: canonical_scope incorreto")
    if data.get("lesson_position") != str(position):
        errors.append(f"{path.name}: lesson_position={data.get('lesson_position')!r}")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: falta {section}")

if actual_ids != EXPECTED:
    errors.append(f"ordem/ids divergentes: {actual_ids}")

readme = COURSE / "README.md"
if not readme.exists():
    errors.append("README.md ausente")
else:
    body = readme.read_text(encoding="utf-8")
    if "Obsidian + IA" not in body:
        errors.append("README.md sem título esperado")

for path in COURSE.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(COURSE.resolve()):
            errors.append(f"{path.relative_to(COURSE)}: link sai do curso -> {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(COURSE)}: link não resolve -> {target}")

print(f"Obsidian + IA: {len(lesson_files)} aulas")
print(f"Erros: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")
if errors:
    sys.exit(1)
