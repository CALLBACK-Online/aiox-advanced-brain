#!/usr/bin/env python3
"""Gera e verifica ledger didático baseado na rubrica canônica de seis dimensões."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from course_common import find_root, resolve_course

DIMENSIONS = (
    "objetivo-verificavel",
    "ancoragem-no-acervo",
    "exercicio-checkpoint",
    "navegacao",
    "ponte-metodo-operacao",
    "terminologia-consistente",
)
OBJECTIVE = re.compile(r"(?im)(^#{2,3}\s+(?:objetivo|resultado|o que você consegue)|ao final.{0,80}(?:consegue|será capaz))")
EXERCISE = re.compile(r"(?im)^#{2,3}\s+(?:exercício|prática|checkpoint|autoavaliação|portão|evidência)")
ANCHOR = re.compile(r"(?:skills/|squads/|aulas/|modulos/|ponte/|\]\((?!https?://|#)[^)]+\.md(?:#[^)]+)?\))")


def navigation_region(text: str) -> str:
    """Aceita seção ## Navegação ou breadcrumb compacto (README / ← / →)."""
    if "## Navegação" in text:
        return text.split("## Navegação", 1)[1]
    # primeiras linhas pós-título costumam carregar o breadcrumb
    lines = text.splitlines()
    chunk: list[str] = []
    for line in lines[:50]:
        if "README.md" in line or "←" in line or "→" in line or re.search(r"(?i)curso|anterior|próxim", line):
            chunk.append(line)
    return "\n".join(chunk)


def signals(course_id: str, course: Path, path: Path, index: int, total: int) -> dict[str, tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    body = text.split("## Navegação", 1)[0]
    navigation = navigation_region(text)
    has_course = "README.md" in navigation
    has_module = not (course / "modulos").is_dir() or bool(
        re.search(r"\]\(\.\./modulos/[^)]+\.md(?:#[^)]+)?\)", navigation)
    )
    has_previous = index == 0 or bool(re.search(r"(?i)anterior|←", navigation))
    has_next = index == total - 1 or bool(re.search(r"(?i)próxim|→", navigation))
    bridge_dir = course / "ponte"
    bridge_required = course_id in {"aiox-advanced", "aiox-advanced-squads"} or bridge_dir.is_dir()
    bridge_files = list(bridge_dir.glob("*.md")) if bridge_dir.is_dir() else []
    glossary = course / "Glossario.md"
    return {
        "objetivo-verificavel": (
            "PENDING" if OBJECTIVE.search(body) else "FAIL",
            "sinal encontrado; confirmar verbo e critério" if OBJECTIVE.search(body) else "objetivo observável não encontrado",
        ),
        "ancoragem-no-acervo": (
            "PENDING" if ANCHOR.search(body) else "FAIL",
            "referência local encontrada; confirmar que o asset existe" if ANCHOR.search(body) else "nenhuma ancoragem local fora da navegação",
        ),
        "exercicio-checkpoint": (
            "PENDING" if EXERCISE.search(body) else "FAIL",
            "prática/checkpoint encontrado; revisar qualidade" if EXERCISE.search(body) else "prática ou checkpoint não encontrado",
        ),
        "navegacao": (
            "PASS" if has_course and has_module and has_previous and has_next else "FAIL",
            f"curso={has_course} módulo={has_module} anterior={has_previous} próxima={has_next}",
        ),
        "ponte-metodo-operacao": (
            "PENDING"
            if bridge_required and bridge_files
            else ("FAIL" if bridge_required else "PASS"),
            "confirmar cobertura semântica em ponte/"
            if bridge_required and bridge_files
            else ("ponte/ ausente" if bridge_required else "fora do escopo desta trilha"),
        ),
        "terminologia-consistente": (
            "PENDING",
            "Glossario.md presente; revisar deriva"
            if glossary.is_file()
            else "revisar vocabulário; glossário não obrigatório",
        ),
    }


def escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render(root: Path, course_id: str, course: Path) -> tuple[str, Counter]:
    lessons = sorted((course / "aulas").rglob("*.md"))
    rows: list[str] = []
    counts: Counter = Counter()
    for index, path in enumerate(lessons):
        relative = path.relative_to(root).as_posix()
        for dimension, (status, hint) in signals(course_id, course, path, index, len(lessons)).items():
            counts[(dimension, status)] += 1
            rows.append(
                f"| `{relative}` | {dimension} | {status} | {status} | {escape(hint)} |  |  |"
            )
    summary = [
        f"- `{dimension}`: FAIL={counts[(dimension, 'FAIL')]} PENDING={counts[(dimension, 'PENDING')]} PASS={counts[(dimension, 'PASS')]}"
        for dimension in DIMENSIONS
    ]
    text = f"""# Auditoria didática — {course_id}

Data: {date.today().isoformat()}  
Rubrica preferencial: `skills/teach/SKILL.md`; fallback: `checklists/didactic-rubric.md`.
Lessons: {len(lessons)}  
Expected rows: {len(lessons) * len(DIMENSIONS)}

Status permitido: `PASS`, `FAIL`, `PENDING`. Sinais automáticos não aprovam semântica;
resolver cada `PENDING` com evidência humana. O check fecha somente com tudo `PASS`.

## Resumo inicial

{chr(10).join(summary)}

## Ledger

| Aula | Dimensão | Status inicial | Status atual | Sinal/evidência inicial | Ação corretiva | Evidência final |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""
    return text, counts


def check(path: Path) -> int:
    counts: Counter = Counter()
    keys: set[tuple[str, str]] = set()
    text = path.read_text(encoding="utf-8")
    expected_match = re.search(r"(?m)^Expected rows:\s*(\d+)\s*$", text)
    if not expected_match:
        raise SystemExit("ledger sem Expected rows")
    expected_rows = int(expected_match.group(1))
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[1] not in DIMENSIONS:
            continue
        key = (cells[0], cells[1])
        if key in keys:
            raise SystemExit(f"linha duplicada no ledger: {key}")
        keys.add(key)
        initial = cells[2].upper()
        current = cells[3].upper()
        for label, status in (("inicial", initial), ("atual", current)):
            if status not in {"PASS", "FAIL", "PENDING"}:
                raise SystemExit(f"status {label} inválido em ledger: {status}")
        if current == "PASS" and initial != "PASS" and (not cells[5] or not cells[6]):
            raise SystemExit(f"PASS corrigido exige ação e evidência final: {key}")
        counts[(cells[1], current)] += 1
    rows = len(keys)
    if not rows:
        raise SystemExit("ledger sem linhas reconhecíveis")
    if rows != expected_rows:
        raise SystemExit(f"ledger incompleto: rows={rows} expected={expected_rows}")
    lessons: dict[str, set[str]] = {}
    for lesson, dimension in keys:
        lessons.setdefault(lesson, set()).add(dimension)
    for lesson, dimensions in lessons.items():
        missing = set(DIMENSIONS) - dimensions
        if missing:
            raise SystemExit(f"ledger incompleto para {lesson}: faltam {sorted(missing)}")
    for dimension in DIMENSIONS:
        print(f"{dimension}: FAIL={counts[(dimension, 'FAIL')]} PENDING={counts[(dimension, 'PENDING')]} PASS={counts[(dimension, 'PASS')]}")
    blocking = sum(value for (dimension, status), value in counts.items() if status != "PASS")
    print(f"rows={rows} blocking={blocking}")
    return 1 if blocking else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita didática sem score numérico não calibrado")
    parser.add_argument("--course")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    root = find_root(args.repo_root or Path.cwd())
    if args.check:
        path = args.check if args.check.is_absolute() else root / args.check
        return check(path)
    if not args.course:
        parser.error("--course é obrigatório sem --check")
    course_id, course = resolve_course(root, args.course)
    report, _ = render(root, course_id, course)
    if not args.write:
        print(report)
        return 0
    target = root / "docs" / "producao-cursos" / course_id / "didactic-audit.md"
    if target.exists() and not args.refresh:
        raise SystemExit(f"auditoria já existe; preservar decisões ou usar --refresh conscientemente: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report, encoding="utf-8")
    print(f"ledger → {target.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
