"""Saída padronizada dos validadores."""
from __future__ import annotations

from typing import Any


def format_ok(title: str, detail: str) -> str:
    return f"{title}: {detail}; erros: 0"


def format_fail(title: str, errors: list[str]) -> str:
    lines = [f"{title}: FALHA"]
    for err in errors:
        lines.append(f"  - {err}")
    return "\n".join(lines)


def print_course_result(
    title: str,
    errors: list[str],
    *,
    detail: str = "",
    stats: dict[str, Any] | None = None,
) -> int:
    """Imprime resultado; retorna exit code (0/1)."""
    if errors:
        print(format_fail(title, errors), flush=True)
        return 1
    extra = detail
    if stats and not extra:
        parts = [f"{k}={v}" for k, v in stats.items()]
        extra = ", ".join(parts)
    print(format_ok(title, extra or "ok"), flush=True)
    return 0
