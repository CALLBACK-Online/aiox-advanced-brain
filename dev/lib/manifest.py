"""Loader de manifest de validação (YAML opcional; fallback sem PyYAML)."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value or value.startswith("#"):
        return ""
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in {"null", "~"}:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _load_simple(text: str) -> dict[str, Any]:
    """Suporta escalares top-level, listas `- item` e um nível de mapa aninhado."""
    data: dict[str, Any] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            i += 1
            continue
        if ":" not in raw:
            i += 1
            continue
        key, rest = raw.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if rest and not rest.startswith("#"):
            data[key] = _parse_scalar(rest.split(" #", 1)[0])
            i += 1
            continue
        # bloco indentado
        i += 1
        items: list[Any] = []
        nested: dict[str, Any] = {}
        mode: str | None = None
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.lstrip().startswith("#"):
                i += 1
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent == 0:
                break
            body = line.strip()
            if body.startswith("- "):
                mode = "list"
                items.append(_parse_scalar(body[2:].split(" #", 1)[0]))
                i += 1
                continue
            if ":" in body and indent >= 2:
                mode = "map"
                nk, nv = body.split(":", 1)
                nk = nk.strip()
                nv = nv.strip()
                if nv and not nv.startswith("#"):
                    nested[nk] = _parse_scalar(nv.split(" #", 1)[0])
                    i += 1
                    continue
                # mapa de segundo nível (ex.: catalog.expect)
                i += 1
                sub: dict[str, Any] = {}
                while i < len(lines):
                    sub_line = lines[i]
                    if not sub_line.strip() or sub_line.lstrip().startswith("#"):
                        i += 1
                        continue
                    sub_indent = len(sub_line) - len(sub_line.lstrip(" "))
                    if sub_indent <= indent:
                        break
                    if ":" not in sub_line:
                        i += 1
                        continue
                    sk, sv = sub_line.strip().split(":", 1)
                    sub[sk.strip()] = _parse_scalar(sv.split(" #", 1)[0])
                    i += 1
                nested[nk] = sub
                continue
            i += 1
        if mode == "list":
            data[key] = items
        elif mode == "map":
            data[key] = nested
        else:
            data[key] = None
    return data


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
        return _load_simple(text)
