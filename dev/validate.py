#!/usr/bin/env python3
"""Harness único de validação do acervo.

Uso:
  python3 dev/validate.py
  python3 dev/validate.py --course aiox-design
  python3 dev/validate.py --only-courses
  python3 dev/validate.py --list
"""
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

COURSE_ORDER = [
    "aiox-advanced",
    "introducao-arquitetura",
    "aiox-fundamentals",
    "aiox-agent-engineering",
    "aiox-design",
    "aiox-productizacao",
    "aiox-advanced-squads",
    "obsidian-ia",
    "aiox-enterprise",
]


def load_checks(course_dir: Path):
    checks_path = course_dir / "checks.py"
    if not checks_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        f"course_checks_{course_dir.name}", checks_path
    )
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
            try:
                result = module.run(ctx)
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 1
                ctx.errors.append(
                    f"checks.py chamou sys.exit({code}) — use ctx.errors, não exit"
                )
                result = None
            except Exception as exc:  # noqa: BLE001 — agrega falha, não aborta suite
                ctx.errors.append(f"checks.py exceção: {type(exc).__name__}: {exc}")
                result = None
            if isinstance(result, tuple):
                extra_errors, detail = result[0], result[1] if len(result) > 1 else ""
                if extra_errors:
                    ctx.errors.extend(extra_errors)
                if detail:
                    ctx.stats["detail"] = detail
            elif isinstance(result, list):
                ctx.errors.extend(result)
            elif isinstance(result, str):
                ctx.stats["detail"] = result
        detail = str(ctx.stats.get("detail") or "")
        return print_course_result(ctx.title, ctx.errors, detail=detail, stats=ctx.stats)
    except Exception as exc:  # noqa: BLE001
        print(f"{slug}: FALHA\n  - harness: {type(exc).__name__}: {exc}", flush=True)
        return 1


def run_subprocess(root: Path, script: Path, *, node: bool = False) -> int:
    if not script.is_file():
        print(f"suite: script ausente: {script}")
        return 1
    cmd = ["node", str(script)] if node else [sys.executable, str(script)]
    return subprocess.run(cmd, cwd=str(root), check=False).returncode


def run_surface(root: Path) -> int:
    return run_subprocess(root, DEV / "courses" / "check_course_surface.py")


def run_journey(root: Path) -> int:
    return run_subprocess(root, DEV / "courses" / "validate_learning_journey.py")


def run_routing(root: Path) -> int:
    return run_subprocess(
        root,
        DEV / "courses" / "aiox-advanced-squads" / "validate-agent-routing.mjs",
        node=True,
    )


def discover_slugs() -> list[str]:
    found = []
    for path in sorted((DEV / "courses").iterdir()):
        if path.is_dir() and (path / "manifest.yaml").is_file():
            found.append(path.name)
    ordered = [s for s in COURSE_ORDER if s in found]
    ordered.extend(s for s in found if s not in ordered)
    return ordered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida cursos do aiox-advanced-brain")
    parser.add_argument(
        "--course",
        action="append",
        dest="courses",
        metavar="SLUG",
        help="Slug do curso (repetível). Default: todos.",
    )
    parser.add_argument("--list", action="store_true", help="Lista cursos com manifesto")
    parser.add_argument("--skip-journey", action="store_true")
    parser.add_argument("--skip-routing", action="store_true")
    parser.add_argument(
        "--only-courses",
        action="store_true",
        help="Só validadores de curso (sem surface/journey/routing)",
    )
    parser.add_argument("--skip-surface", action="store_true")
    args = parser.parse_args(argv)

    root = find_root(DEV)
    slugs = discover_slugs()

    if args.list:
        for slug in slugs:
            manifest = load_manifest(DEV / "courses" / slug / "manifest.yaml")
            print(f"{slug:28} {manifest.get('path', '')}")
        return 0

    selected = args.courses or slugs
    unknown = [s for s in selected if s not in slugs]
    if unknown:
        print(f"cursos desconhecidos (sem manifest.yaml): {unknown}", file=sys.stderr)
        return 2

    failed = 0
    if not args.only_courses and not args.skip_surface and not args.courses:
        if run_surface(root) != 0:
            failed += 1

    for slug in selected:
        if run_course(root, slug) != 0:
            failed += 1

    if not args.only_courses and not args.skip_journey and not args.courses:
        if run_journey(root) != 0:
            failed += 1

    if not args.only_courses and not args.skip_routing and not args.courses:
        if run_routing(root) != 0:
            failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
