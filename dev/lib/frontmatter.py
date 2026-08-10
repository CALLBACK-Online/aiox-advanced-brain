"""Parser leve de frontmatter YAML/flat (sem depender de PyYAML)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_FM = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Retorna mapa plano string→string (linhas `key: value` no bloco)."""
    match = _FM.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-", "#")):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def parse_frontmatter_yaml(path: Path) -> tuple[dict[str, Any], str]:
    """Frontmatter via PyYAML quando disponível; fallback para parse plano."""
    text = path.read_text(encoding="utf-8")
    match = _FM.match(text)
    if not match:
        return {}, text
    block = match.group(1)
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(block) or {}
        if isinstance(loaded, dict):
            return loaded, text
    except Exception:
        pass
    return parse_frontmatter(text), text
