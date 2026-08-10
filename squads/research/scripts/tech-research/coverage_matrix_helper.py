#!/usr/bin/env python3
"""Coverage matrix helper for tech-research and research-bench pipelines.

Worker atom: STORY-RA-F.2 (status code 4-níveis + symbol mapping + matrix validation).

This module is the SINGLE CANONICAL source for the 4-level status enum used in
any coverage / feature / dimension matrix emitted by either skill. It exposes:

    normalize_status(raw) -> Literal["confirmed", "partial", "uncertain", "not_present"]
    status_to_score(status) -> float    # confirmed=2.0, partial=1.0, uncertain=0.5, not_present=0.0
    status_to_symbol(status) -> str     # ✅, ◐, ?, —  (or ASCII fallback when RESEARCH_OUTPUT_ASCII=true)
    validate_matrix(matrix) -> ValidationResult

Per STORY-RA-F.2 §Conditions Item 1, this helper lives at
`squads/research/scripts/tech-research/coverage_matrix_helper.py` and is imported
by BOTH skills (tech-research + research-bench) via absolute path. Do NOT duplicate
it under research-bench/.

Per STORY-RA-F.2 R2 (Risk register row 2), Unicode symbols degrade gracefully when
the environment variable `RESEARCH_OUTPUT_ASCII=true` is set (e.g. ASCII-only
terminals).

Anti-patterns ENFORCED here:
    - 5+ levels (only 4 are accepted)
    - Creative emojis (✅/◐/?/— only — no 🟢/🟡/🔴)
    - `uncertain` as fallback for "not evaluated" (caller must mark as gap explicitly)

Story §AC-1: status code 4-níveis padronizado
Story §AC-2: helper utility exposed functions
"""

from __future__ import annotations

import os
import sys
from typing import Any, Iterable, Literal, NamedTuple

# ─────────────────────────────────────────────────────────────────────────────
# Canonical enum + maps
# ─────────────────────────────────────────────────────────────────────────────

Status = Literal["confirmed", "partial", "uncertain", "not_present"]

# Canonical 4-level enum order: strongest → weakest evidence.
STATUS_ENUM: tuple[Status, ...] = ("confirmed", "partial", "uncertain", "not_present")

# PT-BR aliases accepted on input (case-insensitive; mapped on normalize).
# Story §AC-1: aliases em PT-BR aceitos: sim/parcial/incerto/não.
PT_BR_ALIASES: dict[str, Status] = {
    "sim": "confirmed",
    "parcial": "partial",
    "incerto": "uncertain",
    "nao": "not_present",
    "não": "not_present",
}

# Legacy binary strings accepted as input (non-breaking migration per Story §Non-Goals).
LEGACY_ALIASES: dict[str, Status] = {
    "tem": "confirmed",
    "yes": "confirmed",
    "true": "confirmed",
    "presente": "confirmed",
    "nao tem": "not_present",
    "não tem": "not_present",
    "no": "not_present",
    "false": "not_present",
    "ausente": "not_present",
    "missing": "not_present",
}

# Numeric scores per Story §AC-1.
SCORE_MAP: dict[Status, float] = {
    "confirmed": 2.0,
    "partial": 1.0,
    "uncertain": 0.5,
    "not_present": 0.0,
}

# Visual symbols per Story §AC-1 (anti-pattern: no creative emojis).
SYMBOL_MAP_UNICODE: dict[Status, str] = {
    "confirmed": "✅",
    "partial": "◐",
    "uncertain": "?",
    "not_present": "—",
}

# ASCII fallback per Story §R2 (RESEARCH_OUTPUT_ASCII=true).
SYMBOL_MAP_ASCII: dict[Status, str] = {
    "confirmed": "[X]",
    "partial": "[~]",
    "uncertain": "[?]",
    "not_present": "[ ]",
}


class StatusValueError(ValueError):
    """Raised when normalize_status cannot resolve a value to the 4-level enum.

    Important: this is RAISED only when caller passes a value that is neither a
    canonical status, a PT-BR alias, nor a known legacy alias. Empty/None values
    raise too — callers must mark unmeasured cells as gaps explicitly, NEVER
    fall back to `uncertain` (Story §Anti-patterns).
    """


class ValidationResult(NamedTuple):
    valid: bool
    errors: list[str]
    warnings: list[str]
    cell_count: int
    invalid_cells: list[dict[str, Any]]


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def normalize_status(raw: Any) -> Status:
    """Normalize a raw status value to the canonical 4-level enum.

    Accepts (case-insensitive):
      - canonical enum: confirmed | partial | uncertain | not_present
      - PT-BR aliases: sim | parcial | incerto | não/nao
      - legacy binary: tem | não tem | yes | no | true | false | presente | ausente

    Raises StatusValueError for anything else (including empty / None).

    Per Story §Anti-patterns: NEVER silently fall back to `uncertain` when value
    is missing — callers must distinguish "evidence searched, not confirmed"
    (uncertain) from "not evaluated" (must be exposed as gap, not status).
    """
    if raw is None:
        raise StatusValueError(
            "status value is None; mark as gap explicitly, do not fall back to `uncertain`"
        )
    if not isinstance(raw, str):
        raise StatusValueError(
            f"status must be a string; got {type(raw).__name__}: {raw!r}"
        )
    candidate = raw.strip().lower()
    if not candidate:
        raise StatusValueError(
            "status value is empty; mark as gap explicitly, do not fall back to `uncertain`"
        )
    if candidate in STATUS_ENUM:
        return candidate  # type: ignore[return-value]
    if candidate in PT_BR_ALIASES:
        return PT_BR_ALIASES[candidate]
    if candidate in LEGACY_ALIASES:
        return LEGACY_ALIASES[candidate]
    raise StatusValueError(
        f"status {raw!r} not in canonical enum {STATUS_ENUM} or known aliases; "
        "update coverage_matrix_helper.py if a new alias is legitimate"
    )


def status_to_score(status: Any) -> float:
    """Return numeric score for a status (confirmed=2.0 ... not_present=0.0).

    Accepts raw or canonical inputs — runs through normalize_status first.
    """
    canonical = normalize_status(status)
    return SCORE_MAP[canonical]


def status_to_symbol(status: Any) -> str:
    """Return visual symbol for a status.

    Default: Unicode (✅/◐/?/—). When env var RESEARCH_OUTPUT_ASCII=true is set,
    returns ASCII fallback ([X]/[~]/[?]/[ ]) per Story §R2.

    Accepts raw or canonical inputs — runs through normalize_status first.
    """
    canonical = normalize_status(status)
    if os.environ.get("RESEARCH_OUTPUT_ASCII", "").lower() == "true":
        return SYMBOL_MAP_ASCII[canonical]
    return SYMBOL_MAP_UNICODE[canonical]


def validate_matrix(matrix: Any) -> ValidationResult:
    """Validate a coverage matrix against the 4-level enum.

    Accepts the following shapes (auto-detected):

    1. Pandas DataFrame (if pandas available) — every non-header cell must
       normalize to a canonical status.

    2. List of dicts where each dict is a row with `cells` (dict of player → cell).
       Each cell may be either `{"status": "..."}` or a bare string status.

    3. Dict with `rows: [{dimension, cells: {player: status_or_dict}}]`.

    4. Plain list/tuple of statuses (flat shape — most permissive).

    Returns ValidationResult with `valid: bool`, errors[], warnings[],
    cell_count, and invalid_cells[] (each entry includes `path` for traceability).

    Story §AC-2: `validate_matrix` rejects matrix with values outside the 4-level
    enum.
    """
    errors: list[str] = []
    warnings: list[str] = []
    invalid_cells: list[dict[str, Any]] = []
    cell_count = 0

    def _check_cell(value: Any, path: str) -> None:
        nonlocal cell_count
        cell_count += 1
        # Skip empty rows in DataFrame headers etc.
        if value is None or (isinstance(value, str) and not value.strip()):
            invalid_cells.append({"path": path, "value": value, "reason": "empty/null"})
            errors.append(f"{path}: empty/null status — mark as gap explicitly")
            return
        try:
            normalize_status(value)
        except StatusValueError as exc:
            invalid_cells.append({"path": path, "value": value, "reason": str(exc)})
            errors.append(f"{path}: {exc}")

    # Shape 1: pandas DataFrame
    try:
        import pandas as pd  # type: ignore[import-not-found]

        if isinstance(matrix, pd.DataFrame):
            for col in matrix.columns:
                for idx, value in matrix[col].items():
                    # Skip first column (dimension label) — caller marks it via
                    # convention; we walk only the cells. Heuristic: only check
                    # string-or-status-like values.
                    if col == matrix.columns[0]:
                        continue
                    _check_cell(value, f"DataFrame[{idx}, {col}]")
            return ValidationResult(
                valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                cell_count=cell_count,
                invalid_cells=invalid_cells,
            )
    except ImportError:
        pass  # pandas not available — fall through to other shapes

    # Shape 2/3: dict with rows[]
    if isinstance(matrix, dict) and isinstance(matrix.get("rows"), list):
        for r_idx, row in enumerate(matrix["rows"]):
            if not isinstance(row, dict):
                errors.append(f"rows[{r_idx}]: expected dict, got {type(row).__name__}")
                continue
            cells = row.get("cells", {})
            if isinstance(cells, dict):
                for player, cell in cells.items():
                    path = f"rows[{r_idx}].cells.{player}"
                    if isinstance(cell, dict) and "status" in cell:
                        _check_cell(cell["status"], f"{path}.status")
                    elif isinstance(cell, str):
                        _check_cell(cell, path)
                    elif cell is None:
                        _check_cell(None, path)
                    else:
                        # Cell with no status field (legacy score-only cell) —
                        # treat as warning, not error, to keep F.1 fixtures
                        # backwards-compatible.
                        warnings.append(
                            f"{path}: cell has no `status` field "
                            f"(found keys: {list(cell.keys()) if isinstance(cell, dict) else type(cell).__name__}). "
                            "Story RA-F.2 AC-1 expects status in each cell going forward."
                        )
            elif isinstance(cells, list):
                for c_idx, cell in enumerate(cells):
                    path = f"rows[{r_idx}].cells[{c_idx}]"
                    if isinstance(cell, dict) and "status" in cell:
                        _check_cell(cell["status"], f"{path}.status")
                    elif isinstance(cell, str):
                        _check_cell(cell, path)
            else:
                errors.append(
                    f"rows[{r_idx}].cells: expected dict or list, got {type(cells).__name__}"
                )
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cell_count=cell_count,
            invalid_cells=invalid_cells,
        )

    # Shape 4: list of dicts (row-per-entry) OR flat list of statuses
    if isinstance(matrix, (list, tuple)):
        for r_idx, item in enumerate(matrix):
            if isinstance(item, dict) and "cells" in item:
                cells = item["cells"]
                if isinstance(cells, dict):
                    for player, cell in cells.items():
                        path = f"[{r_idx}].cells.{player}"
                        if isinstance(cell, dict) and "status" in cell:
                            _check_cell(cell["status"], f"{path}.status")
                        elif isinstance(cell, str):
                            _check_cell(cell, path)
            elif isinstance(item, str):
                _check_cell(item, f"[{r_idx}]")
            elif item is None:
                _check_cell(None, f"[{r_idx}]")
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cell_count=cell_count,
            invalid_cells=invalid_cells,
        )

    errors.append(
        f"unrecognized matrix shape: {type(matrix).__name__}; "
        "expected DataFrame, list[dict], or dict with rows[]"
    )
    return ValidationResult(
        valid=False,
        errors=errors,
        warnings=warnings,
        cell_count=cell_count,
        invalid_cells=invalid_cells,
    )


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point — quick validation from shell
# ─────────────────────────────────────────────────────────────────────────────


def _cli() -> int:
    """CLI smoke test:
        python coverage_matrix_helper.py self-test
        python coverage_matrix_helper.py validate <yaml-file>
    """
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    cmd = sys.argv[1]

    if cmd == "self-test":
        # AC-1 enum round-trip
        for s in STATUS_ENUM:
            assert normalize_status(s) == s, f"identity failed for {s}"
            assert status_to_score(s) == SCORE_MAP[s]
            assert status_to_symbol(s) in (SYMBOL_MAP_UNICODE[s], SYMBOL_MAP_ASCII[s])

        # PT-BR aliases
        assert normalize_status("sim") == "confirmed"
        assert normalize_status("PARCIAL") == "partial"
        assert normalize_status("Incerto") == "uncertain"
        assert normalize_status("não") == "not_present"
        assert normalize_status("nao") == "not_present"

        # Legacy aliases
        assert normalize_status("tem") == "confirmed"
        assert normalize_status("yes") == "confirmed"
        assert normalize_status("ausente") == "not_present"

        # Score map
        assert status_to_score("confirmed") == 2.0
        assert status_to_score("partial") == 1.0
        assert status_to_score("uncertain") == 0.5
        assert status_to_score("not_present") == 0.0

        # Symbol map (Unicode)
        os.environ.pop("RESEARCH_OUTPUT_ASCII", None)
        assert status_to_symbol("confirmed") == "✅"
        assert status_to_symbol("partial") == "◐"
        assert status_to_symbol("uncertain") == "?"
        assert status_to_symbol("not_present") == "—"

        # Symbol map (ASCII fallback)
        os.environ["RESEARCH_OUTPUT_ASCII"] = "true"
        assert status_to_symbol("confirmed") == "[X]"
        assert status_to_symbol("partial") == "[~]"
        assert status_to_symbol("uncertain") == "[?]"
        assert status_to_symbol("not_present") == "[ ]"
        os.environ.pop("RESEARCH_OUTPUT_ASCII", None)

        # Invalid input rejected
        try:
            normalize_status("yolo")
        except StatusValueError:
            pass
        else:
            raise AssertionError("expected StatusValueError for 'yolo'")

        try:
            normalize_status(None)
        except StatusValueError:
            pass
        else:
            raise AssertionError("expected StatusValueError for None")

        try:
            normalize_status("")
        except StatusValueError:
            pass
        else:
            raise AssertionError("expected StatusValueError for empty string")

        # validate_matrix — happy path (dict with rows)
        valid_matrix = {
            "rows": [
                {
                    "dimension": "agentic_planning",
                    "cells": {
                        "claude_code": "confirmed",
                        "aider": "partial",
                        "cline": "uncertain",
                        "openhands": "not_present",
                    },
                }
            ]
        }
        res = validate_matrix(valid_matrix)
        assert res.valid, f"expected valid; got errors: {res.errors}"
        assert res.cell_count == 4

        # validate_matrix — rejects invalid
        invalid_matrix = {
            "rows": [
                {"dimension": "x", "cells": {"a": "yolo", "b": "confirmed"}}
            ]
        }
        res = validate_matrix(invalid_matrix)
        assert not res.valid, "expected invalid"
        assert any("yolo" in e for e in res.errors)

        # validate_matrix — PT-BR aliases accepted
        pt_matrix = {
            "rows": [{"dimension": "x", "cells": {"a": "sim", "b": "parcial", "c": "incerto", "d": "não"}}]
        }
        res = validate_matrix(pt_matrix)
        assert res.valid, f"PT-BR aliases should be valid: {res.errors}"

        print("self-test PASSED")
        return 0

    if cmd == "validate":
        if len(sys.argv) < 3:
            print("usage: coverage_matrix_helper.py validate <yaml-file>", file=sys.stderr)
            return 2
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError:
            print("PyYAML required for `validate` subcommand", file=sys.stderr)
            return 3
        with open(sys.argv[2], encoding="utf-8") as f:
            data = yaml.safe_load(f)
        result = validate_matrix(data)
        if result.valid:
            print(f"VALID — {result.cell_count} cells checked")
            for w in result.warnings:
                print(f"  WARN: {w}")
            return 0
        print(f"INVALID — {result.cell_count} cells checked, {len(result.errors)} errors")
        for e in result.errors:
            print(f"  ERROR: {e}")
        return 1

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())
