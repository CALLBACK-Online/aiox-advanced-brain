"""Loader de manifest.yaml simples (sem PyYAML obrigatório)."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"manifest ausente: {path}")
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict):
            raise ValueError(f"manifest inválido: {path}")
        return data
    except ImportError:
        data: dict[str, Any] = {}
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
                continue
            if line.startswith((" ", "\t")):
                continue
            key, rest = line.split(":", 1)
            data[key.strip()] = _parse_scalar(rest.split(" #", 1)[0])
        return data
