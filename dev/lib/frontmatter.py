"""Parser leve de frontmatter YAML/flat (sem depender de PyYAML)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_FM = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def _coerce(value: str) -> Any:
    raw = value.strip().strip("'\"")
    low = raw.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in {"null", "~", ""}:
        return None if low in {"null", "~"} else raw
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def parse_frontmatter(text: str) -> dict[str, str]:
    """Mapa plano string→string (linhas `key: value` no bloco)."""
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


def parse_frontmatter_typed(text: str) -> dict[str, Any]:
    """Como parse_frontmatter, com bool/int/float coeridos (fallback sem PyYAML)."""
    return {k: _coerce(v) for k, v in parse_frontmatter(text).items()}


def parse_frontmatter_yaml(path: Path) -> tuple[dict[str, Any], str]:
    """Frontmatter via PyYAML quando disponível; senão parse tipado plano."""
    text = path.read_text(encoding="utf-8")
    match = _FM.match(text)
    if not match:
        return {}, text
    block = match.group(1)
    try:
        import yaml  # type: ignore
    except ImportError:
        return parse_frontmatter_typed(text), text
    try:
        loaded = yaml.safe_load(block) or {}
        if isinstance(loaded, dict):
            return loaded, text
    except Exception:
        pass
    return parse_frontmatter_typed(text), text
