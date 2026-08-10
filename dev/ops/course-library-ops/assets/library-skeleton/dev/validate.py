#!/usr/bin/env python3
"""Harness mínimo de validação do acervo."""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

DEV = Path(__file__).resolve().parent
if str(DEV) not in sys.path:
    sys.path.insert(0, str(DEV))

from lib.context import Context  # noqa: E402
from lib.generic import run_generic  # noqa: E402
from lib.manifest import load_manifest  # noqa: E402
from lib.paths import find_root  # noqa: E402
from lib.report import print_course_result  # noqa: E402


def discover_course_slugs() -> list[str]:
    courses_dir = DEV / "courses"
    slugs: list[str] = []
    if not courses_dir.is_dir():
        return slugs
    for child in sorted(courses_dir.iterdir()):
        if child.is_dir() and (child / "manifest.yaml").is_file():
            slugs.append(child.name)
    return slugs


def load_checks(course_dir: Path):
    checks_path = course_dir / "checks.py"
    if not checks_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"course_checks_{course_dir.name}", checks_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não carregou checks: {checks_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "run"):
        raise RuntimeError(f"{checks_path}: falta def run(ctx)")
    return module


def build_context(root: Path, slug: str) -> Context:
    course_dir = DEV / "courses" / slug
    manifest = load_manifest(course_dir / "manifest.yaml")
    course_id = str(manifest.get("id") or slug)
    scope = str(manifest.get("path") or f"cursos/{slug}")
    title = str(manifest.get("title") or slug)
    course_path = root / scope
    if not course_path.is_dir():
        raise FileNotFoundError(f"pasta do curso ausente: {course_path}")
    return Context(
        root=root,
        course=course_path,
        course_id=course_id,
        scope=scope,
        title=title,
        slug=slug,
        manifest=manifest,
        tools_dir=course_dir,
    )


def run_course(root: Path, slug: str) -> int:
    try:
        ctx = build_context(root, slug)
        run_generic(ctx)
        module = load_checks(ctx.tools_dir)
        if module is not None:
            result = module.run(ctx)
            if isinstance(result, str):
                ctx.stats["detail"] = result
        detail = str(ctx.stats.get("detail") or "")
        return print_course_result(ctx.title, ctx.errors, detail=detail, stats=ctx.stats)
    except Exception as exc:  # noqa: BLE001
        print(f"{slug}: FALHA\n  - harness: {type(exc).__name__}: {exc}", flush=True)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", help="slug único")
    parser.add_argument("--only-courses", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    root = find_root(Path(__file__))
    slugs = discover_course_slugs()

    if args.list:
        print("courses:", ", ".join(slugs) or "(none)")
        return 0

    code = 0
    if not args.only_courses and not args.course:
        surface = DEV / "courses" / "check_course_surface.py"
        if surface.is_file():
            code |= subprocess.run([sys.executable, str(surface)], cwd=str(root)).returncode

    targets = [args.course] if args.course else slugs
    for slug in targets:
        if not slug:
            continue
        code |= run_course(root, slug)

    if not targets and not args.course:
        print("nenhum curso com manifest em dev/courses/ (ok em acervo vazio)")
    return code


if __name__ == "__main__":
    sys.exit(main())
