"""Resolução robusta da raiz do repositório (sem parents[N] frágil)."""
from __future__ import annotations

from pathlib import Path

_MARKERS = ("catalog.json", "package.json")


def find_root(start: Path | None = None) -> Path:
    """Sobe a partir de *start* até achar catalog.json + package.json."""
    cur = (start or Path.cwd()).resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in (cur, *cur.parents):
        if all((candidate / marker).is_file() for marker in _MARKERS):
            return candidate
    raise RuntimeError(
        "raiz do acervo não encontrada (catalog.json + package.json ausentes)"
    )
