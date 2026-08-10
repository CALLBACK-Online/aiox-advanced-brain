#!/usr/bin/env python3
"""Bootstrap de um acervo educacional no molde aiox-advanced-brain.

Copia/gera skeleton mínimo operável com harness de validação e surface check.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
SKELETON = PACK / "assets" / "library-skeleton"


def write(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        print(f"skip exists: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"write {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap course library repo")
    parser.add_argument("--dest", type=Path, required=True, help="Directory for the new library")
    parser.add_argument("--title", default="AIOX Course Library")
    parser.add_argument("--slug", default="course-library", help="Library id for catalog")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    dest: Path = args.dest.expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    if any(dest.iterdir()) and not args.force:
        non_git = [p for p in dest.iterdir() if p.name != ".git"]
        if non_git:
            print(f"destino não vazio: {dest} (use --force para sobrescrever arquivos do skeleton)", file=sys.stderr)
            return 2

    # Prefer packing skeleton tree if present
    if SKELETON.is_dir():
        for path in SKELETON.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(SKELETON)
            target = dest / rel
            if target.exists() and not args.force:
                print(f"skip exists: {target}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix in {".py", ".md", ".json", ".yaml", ".yml", ".txt"} or path.name in {
                ".gitignore",
            }:
                text = path.read_text(encoding="utf-8")
                text = text.replace("{{LIBRARY_TITLE}}", args.title)
                text = text.replace("{{LIBRARY_SLUG}}", args.slug)
                target.write_text(text, encoding="utf-8")
            else:
                shutil.copy2(path, target)
            print(f"write {target}")
    else:
        print("skeleton ausente; gerando mínimo embutido", file=sys.stderr)

    # Ensure critical files exist even if skeleton incomplete
    ensure_minimum(dest, args.title, args.slug, force=args.force)

    # Copy ops pack into dev/ops for SoT inside new library
    ops_dest = dest / "dev" / "ops" / "course-library-ops"
    if not ops_dest.exists() or args.force:
        if ops_dest.exists():
            shutil.rmtree(ops_dest)
        shutil.copytree(
            PACK,
            ops_dest,
            ignore=shutil.ignore_patterns("dist", "__pycache__", "*.pyc", ".DS_Store"),
        )
        print(f"write {ops_dest} (ops SoT)")

    print(
        f"\nBootstrap OK: {dest}\n"
        f"  cd {dest}\n"
        f"  python3 dev/validate.py\n"
        f"  bash dev/ops/course-library-ops/scripts/install.sh --target both\n"
        f"  # then create-course via course-library-ops\n"
    )
    return 0


def ensure_minimum(dest: Path, title: str, slug: str, *, force: bool) -> None:
    catalog = {
        "schema_version": 1,
        "library_version": "0.1.0",
        "library": {"id": slug, "title": title},
        "courses": {},
        "learning_journey": {
            "model": "common-core-plus-application-routes-and-continuity-preview",
            "common_core": [],
            "responsibilities": {},
            "core_transitions": [],
            "application_routes": {},
            "cross_route_transitions": [],
        },
    }
    if not (dest / "catalog.json").exists() or force:
        write(dest / "catalog.json", json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", force=True)

    pkg = {
        "name": slug,
        "version": "0.1.0",
        "private": True,
        "description": title,
        "files": [
            "cursos/",
            "AGENTS.md",
            "CLAUDE.md",
            "catalog.json",
            "README.md",
            "notas/",
        ],
        "scripts": {
            "validate": "python3 dev/validate.py",
            "validate:courses": "python3 dev/validate.py --only-courses",
        },
    }
    if not (dest / "package.json").exists() or force:
        write(dest / "package.json", json.dumps(pkg, indent=2) + "\n", force=True)


if __name__ == "__main__":
    sys.exit(main())
