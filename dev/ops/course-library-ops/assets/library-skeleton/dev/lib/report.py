"""Saída padronizada."""
from __future__ import annotations

from typing import Any


def print_course_result(
    title: str,
    errors: list[str],
    *,
    detail: str = "",
    stats: dict[str, Any] | None = None,
) -> int:
    if errors:
        print(f"{title}: FALHA", flush=True)
        for err in errors:
            print(f"  - {err}", flush=True)
        return 1
    extra = detail or (stats and ", ".join(f"{k}={v}" for k, v in stats.items())) or "ok"
    print(f"{title}: {extra}; erros: 0", flush=True)
    return 0
