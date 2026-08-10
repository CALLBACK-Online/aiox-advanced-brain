"""Checagens genéricas do manifest."""
from __future__ import annotations

from .context import Context


def run_generic(ctx: Context) -> None:
    m = ctx.manifest
    for rel in m.get("required_root") or []:
        if not (ctx.course / rel).exists():
            ctx.errors.append(f"arquivo obrigatório ausente: {rel}")
    counts = m.get("counts") or {}
    if "lessons" in counts:
        found = len(list(ctx.course.glob(m.get("lessons_glob", "aulas/**/*.md"))))
        expected = int(counts["lessons"])
        if found != expected:
            ctx.errors.append(f"esperados {expected} aulas; encontrados {found}")
