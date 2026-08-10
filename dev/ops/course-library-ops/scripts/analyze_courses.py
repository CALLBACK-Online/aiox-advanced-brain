#!/usr/bin/env python3
"""Extrai o DNA estrutural e pedagógico de cursos Markdown sem alterar arquivos."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
WORD = re.compile(r"\b\w+\b", re.UNICODE)
MD_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")

PROFILE_SIGNATURES = {
    "fundacional": {
        "mapa visual",
        "modelo mental",
        "caso rápido",
        "quando usar — e quando não usar",
    },
    "técnico-operacional": {
        "objetivo",
        "contexto",
        "erro comum",
        "recuperação sem ia",
        "fontes no snapshot",
    },
    "decisório-aplicado": {
        "mapa desta aula",
        "mapa da decisão",
        "portão da aula",
        "pergunte ao seu agente",
        "evidência de conclusão",
    },
    "catálogo-roteamento": {
        "prepare a entrada",
        "como ativar",
        "briefing copiável",
        "execução guiada",
        "limites neste acervo",
    },
    "preview-protegido": {
        "o cenário",
        "o que muda no enterprise",
        "o que não muda",
        "portão de diagnóstico",
    },
    "migração-profunda": {
        "origem curricular",
        "mapa desta aula",
        "navegação",
    },
}


def find_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "catalog.json").is_file() and (candidate / "cursos").is_dir():
            return candidate
    raise SystemExit("raiz do acervo não encontrada (catalog.json + cursos/)")


def normalize_heading(value: str) -> str:
    value = re.sub(r"[`*_#]", "", value).strip().lower()
    return re.sub(r"\s+", " ", value)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or line.startswith(("-", "#")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("'\"")
    return result


def course_files(course: Path, part: str, suffixes: set[str], include_archive: bool) -> list[Path]:
    files: list[Path] = []
    for path in course.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        relative = path.relative_to(course)
        if part not in relative.parts:
            continue
        if not include_archive and "archive" in relative.parts:
            continue
        files.append(path)
    return sorted(files)


def infer_profile(section_presence: Counter[str], metadata_presence: Counter[str]) -> tuple[str, dict[str, int]]:
    scores = {
        profile: sum(section_presence.get(section, 0) for section in signature)
        for profile, signature in PROFILE_SIGNATURES.items()
    }
    scores["migração-profunda"] += metadata_presence.get("source_path", 0)
    scores["migração-profunda"] += metadata_presence.get("source_lesson_id", 0)
    scores["catálogo-roteamento"] += metadata_presence.get("maturity", 0)
    scores["catálogo-roteamento"] += metadata_presence.get("squad", 0)
    profile = max(scores, key=scores.get) if scores and max(scores.values()) else "não-classificado"
    return profile, scores


def analyze(course: Path, root: Path, include_archive: bool) -> dict:
    lessons = course_files(course, "aulas", {".md"}, include_archive)
    modules = course_files(course, "modulos", {".md"}, include_archive)
    assessment_files = course_files(course, "avaliacoes", {".md", ".yaml", ".yml"}, include_archive)
    quizzes = [path for path in assessment_files if "quiz" in path.name.lower()]
    section_occurrences: Counter[str] = Counter()
    section_presence: Counter[str] = Counter()
    metadata_presence: Counter[str] = Counter()
    word_counts: list[int] = []
    markdown_links = 0
    external_links = 0
    wikilinks = 0

    for path in lessons:
        text = path.read_text(encoding="utf-8", errors="replace")
        word_counts.append(len(WORD.findall(text)))
        metadata_presence.update(parse_frontmatter(text).keys())
        headings = [normalize_heading(value) for value in HEADING.findall(text)]
        section_occurrences.update(headings)
        section_presence.update(set(headings))
        targets = MD_LINK.findall(text)
        markdown_links += len(targets)
        external_links += sum(target.startswith(("http://", "https://")) for target in targets)
        wikilinks += len(WIKILINK.findall(text))

    profile, profile_scores = infer_profile(section_presence, metadata_presence)
    root_files = sorted(path.name for path in course.iterdir() if path.is_file())
    relative = course.relative_to(root).as_posix()
    return {
        "course": course.name,
        "path": relative,
        "profile_suggestion": profile,
        "profile_scores": profile_scores,
        "counts": {
            "lessons": len(lessons),
            "modules": len(modules),
            "quizzes": len(quizzes),
            "assessment_files": len(assessment_files),
            "root_files": len(root_files),
        },
        "lesson_words": {
            "min": min(word_counts) if word_counts else 0,
            "average": round(sum(word_counts) / len(word_counts)) if word_counts else 0,
            "max": max(word_counts) if word_counts else 0,
        },
        "root_file_names": root_files,
        "frontmatter_coverage": dict(metadata_presence.most_common()),
        "dominant_sections": dict(section_presence.most_common(20)),
        "section_occurrences": dict(section_occurrences.most_common(20)),
        "links": {
            "markdown": markdown_links,
            "external": external_links,
            "wikilinks": wikilinks,
        },
    }


def render_markdown(results: list[dict]) -> str:
    lines = ["# Course DNA", ""]
    for item in results:
        counts = item["counts"]
        words = item["lesson_words"]
        lines.extend(
            [
                f"## {item['course']}",
                "",
                f"- path: `{item['path']}`",
                f"- profile: `{item['profile_suggestion']}`",
                f"- lessons/modules/quizzes: {counts['lessons']}/{counts['modules']}/{counts['quizzes']}",
                f"- lesson words min/avg/max: {words['min']}/{words['average']}/{words['max']}",
                f"- root files: {', '.join(item['root_file_names']) or '—'}",
                "- dominant sections: "
                + "; ".join(f"{name} ({count})" for name, count in item["dominant_sections"].items()),
                "- source fields: "
                + ", ".join(
                    f"{name} ({item['frontmatter_coverage'].get(name, 0)})"
                    for name in ("source_refs", "source_commit", "source_path", "source_lesson_id", "adapted_from")
                    if item["frontmatter_coverage"].get(name)
                )
                if any(
                    item["frontmatter_coverage"].get(name)
                    for name in ("source_refs", "source_commit", "source_path", "source_lesson_id", "adapted_from")
                )
                else "- source fields: —",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analisa o DNA dos cursos sem alterar o acervo")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--course", action="append", type=Path, dest="courses")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--include-archive", action="store_true")
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    if args.courses:
        courses = [(path if path.is_absolute() else root / path).resolve() for path in args.courses]
    else:
        courses = sorted(
            path for path in (root / "cursos").iterdir() if path.is_dir() and (path / "aulas").is_dir()
        )

    for course in courses:
        if not course.is_dir() or not (course / "aulas").is_dir():
            raise SystemExit(f"curso inválido: {course}")
        try:
            course.relative_to(root / "cursos")
        except ValueError as exc:
            raise SystemExit(f"curso fora de cursos/: {course}") from exc

    results = [analyze(course, root, args.include_archive) for course in courses]
    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
