"""Checagens genéricas dirigidas pelo manifest.yaml."""
from __future__ import annotations

import json
from typing import Any

from .context import Context
from .links import scan_course_markdown


def run_generic(ctx: Context) -> None:
    """Aplica regras declarativas do manifesto (quando presentes)."""
    m = ctx.manifest

    required_root = m.get("required_root") or []
    if required_root:
        ctx.require_files(list(required_root))

    for rel in m.get("required_files") or []:
        if not (ctx.course / rel).exists():
            ctx.errors.append(f"arquivo obrigatório ausente: {rel}")

    counts = m.get("counts") or {}
    mapping = {
        "lessons": ("aulas", m.get("lessons_glob", "aulas/**/*.md")),
        "modules": ("módulos", m.get("modules_glob", "modulos/**/*.md")),
        "quizzes": ("quizzes", m.get("quizzes_glob", "avaliacoes/**/*")),
    }
    for key, (label, default_glob) in mapping.items():
        if key not in counts:
            continue
        glob_pat = m.get(f"{key}_glob", default_glob)
        # Prefer explicit globs from manifest
        found = len(list(ctx.course.glob(glob_pat)))
        # Fallback for nested aulas/**/*.md
        if found == 0 and "**" in glob_pat:
            found = len(list(ctx.course.glob(glob_pat)))
        expected = int(counts[key])
        if found != expected:
            ctx.errors.append(f"esperados {expected} {label}; encontrados {found}")

    if m.get("scan_links", True):
        suffixes = set(m.get("scan_suffixes") or [".md"])
        scan_course_markdown(
            ctx.course,
            errors=ctx.errors,
            require_in_course=bool(m.get("links_must_stay_in_course", True)),
            suffixes=suffixes,
        )

    catalog_expect = m.get("catalog") or {}
    if catalog_expect:
        catalog_path = ctx.root / "catalog.json"
        if not catalog_path.is_file():
            ctx.errors.append("catalog.json ausente na raiz")
            return
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        bucket = catalog_expect.get("bucket", "courses")
        key = catalog_expect.get("key", ctx.course_id)
        if bucket == "courses":
            entry: dict[str, Any] = catalog.get("courses", {}).get(key, {})
            prefix = f"catalog.json: courses.{key}"
        elif bucket == "supplemental":
            path = catalog_expect.get("path", ctx.scope)
            entry = next(
                (
                    item
                    for item in catalog.get("supplemental_courses", [])
                    if item.get("path") == path
                ),
                {},
            )
            prefix = f"catalog.json: supplemental {path}"
        else:
            entry = {}
            prefix = "catalog.json"
        for field, expected in (catalog_expect.get("expect") or {}).items():
            if entry.get(field) != expected:
                ctx.errors.append(f"{prefix}.{field} divergente (got {entry.get(field)!r})")

    # package.json must reference the harness (not per-course scripts)
    if m.get("require_in_validate_script"):
        package_path = ctx.root / "package.json"
        if package_path.is_file():
            import json as _json

            script = (
                _json.loads(package_path.read_text(encoding="utf-8"))
                .get("scripts", {})
                .get("validate", "")
            )
            needle = m["require_in_validate_script"]
            if needle not in script:
                ctx.errors.append(f"package.json: validate não referencia {needle}")
