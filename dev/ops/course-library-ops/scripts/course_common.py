#!/usr/bin/env python3
"""Contratos compartilhados pelos fluxos operacionais de curso."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

PLACEHOLDER = re.compile(r"(?:_DRAFT_|\bTODO\b|REPLACE|PENDING|<[^>]+>)", re.IGNORECASE)
APPROVAL_FIELDS = ("approved_by", "approval_date", "approved_artifact", "approval_scope")


def find_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "catalog.json").is_file() and (candidate / "package.json").is_file():
            return candidate
    raise SystemExit("raiz do acervo não encontrada (catalog.json + package.json)")


def safe_relative(value: str, *, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise SystemExit(f"{label} deve ser path relativo seguro")
    return path


def scalar_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def validate_approval_artifacts(root: Path, spec: dict) -> dict[str, Path]:
    records = spec.get("approval_artifacts")
    if not isinstance(records, dict):
        raise SystemExit("spec exige approval_artifacts.brief e approval_artifacts.outline")

    course_id = spec.get("course_id", "")
    expected_root = (root / "docs" / "producao-cursos" / course_id).resolve()
    resolved: dict[str, Path] = {}
    for gate in ("brief", "outline"):
        raw = records.get(gate)
        if not isinstance(raw, str) or not raw:
            raise SystemExit(f"approval_artifacts.{gate} ausente")
        relative = safe_relative(raw, label=f"approval_artifacts.{gate}")
        path = (root / relative).resolve()
        if path.parent != expected_root:
            raise SystemExit(f"approval_artifacts.{gate} deve estar em docs/producao-cursos/{course_id}/")
        if not path.is_file():
            raise SystemExit(f"artefato de aprovação ausente: {relative}")

        fields = scalar_frontmatter(path)
        if fields.get("status") != "approved":
            raise SystemExit(f"{relative}: status deve ser approved")
        for field in APPROVAL_FIELDS:
            value = fields.get(field, "")
            if not value or PLACEHOLDER.search(value):
                raise SystemExit(f"{relative}: {field} exige registro humano explícito")
        if fields["approved_artifact"] != relative.as_posix():
            raise SystemExit(
                f"{relative}: approved_artifact deve registrar exatamente {relative.as_posix()}"
            )
        try:
            date.fromisoformat(fields["approval_date"])
        except ValueError as exc:
            raise SystemExit(f"{relative}: approval_date deve ser YYYY-MM-DD") from exc
        resolved[gate] = path
    return resolved


def _manifest_path(root: Path, course_id: str) -> Path | None:
    """Resolve path from harness before catalog registration (create/selftest)."""
    man = root / "dev" / "courses" / course_id / "manifest.yaml"
    if not man.is_file():
        return None
    for line in man.read_text(encoding="utf-8").splitlines():
        if line.startswith("path:"):
            raw = line.split(":", 1)[1].strip().strip("'\"")
            candidate = root / raw
            if candidate.is_dir() and (candidate / "aulas").is_dir():
                return candidate
    return None


def resolve_course(root: Path, query: str) -> tuple[str, Path]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    courses = catalog.get("courses") or {}
    if query in courses:
        path = root / courses[query]["path"]
        if not path.is_dir():
            raise SystemExit(f"curso ausente no disco: {courses[query]['path']}")
        return query, path

    # Harness exists after scaffold even before catalog integration.
    harness_course = _manifest_path(root, query)
    if harness_course is not None:
        return query, harness_course

    relative = safe_relative(query, label="course")
    path = root / relative
    for course_id, meta in courses.items():
        if meta.get("path") == relative.as_posix():
            return course_id, path
    if path.is_dir() and (path / "aulas").is_dir():
        # Prefer harness id when query is a path.
        for child in sorted((root / "dev" / "courses").glob("*/manifest.yaml")):
            for line in child.read_text(encoding="utf-8").splitlines():
                if line.startswith("path:") and line.split(":", 1)[1].strip().strip("'\"") == relative.as_posix():
                    return child.parent.name, path
        return path.name.lower().replace(" ", "-"), path
    raise SystemExit(f"curso não encontrado no catálogo, harness ou disco: {query}")

def lesson_inventory(course: Path) -> list[dict[str, str]]:
    inventory: list[dict[str, str]] = []
    for position, path in enumerate(sorted((course / "aulas").rglob("*.md")), 1):
        fields = scalar_frontmatter(path)
        lesson_id = fields.get("lesson_id") or re.sub(r"^\d+-", "", path.stem)
        inventory.append(
            {
                "id": lesson_id,
                "module": fields.get("module", "M0"),
                "position": fields.get("lesson_position", str(position)),
                "path": path.relative_to(course).as_posix(),
            }
        )
    return inventory


# creation_mode canônico: create | upgrade. Aliases legados normalizados na entrada.
CREATION_MODE_ALIASES = {
    "create": "create",
    "greenfield": "create",
    "new": "create",
    "upgrade": "upgrade",
    "brownfield": "upgrade",
    "modernize": "upgrade",
}


def normalize_creation_mode(value: str) -> str:
    key = (value or "").strip().lower()
    if key not in CREATION_MODE_ALIASES:
        raise SystemExit(
            f"creation_mode inválido: {value!r}; use create|upgrade "
            f"(aliases: greenfield→create, brownfield→upgrade)"
        )
    return CREATION_MODE_ALIASES[key]


def bastidor_dir(root: Path, course_id: str) -> Path:
    return root / "docs" / "producao-cursos" / course_id


# Marcadores de scaffold (não confundir com "TODO" em prosa didática).
SCAFFOLD_MARKERS = re.compile(
    r"(?:_DRAFT_|REPLACE_ME|REPLACE-ME|<\s*(?:slug|Título|Nome-Do-Curso|lesson-id|creation-mode)\s*>)",
    re.IGNORECASE,
)


def count_placeholders(course: Path) -> int:
    total = 0
    if not course.is_dir():
        return 0
    for path in course.rglob("*.md"):
        total += len(SCAFFOLD_MARKERS.findall(path.read_text(encoding="utf-8", errors="replace")))
    return total


def approval_status(root: Path, course_id: str, spec: dict | None = None) -> dict[str, str]:
    """Lê status de brief/outline no bastidor (sem falhar se draft)."""
    bastidor = bastidor_dir(root, course_id)
    out: dict[str, str] = {}
    for gate, default_name in (("brief", "COURSE-BRIEF.md"), ("outline", "course-outline.md")):
        path = bastidor / default_name
        if isinstance(spec, dict):
            raw = (spec.get("approval_artifacts") or {}).get(gate)
            if isinstance(raw, str) and raw:
                path = root / safe_relative(raw, label=f"approval_artifacts.{gate}")
        if not path.is_file():
            out[gate] = "missing"
            continue
        status = scalar_frontmatter(path).get("status", "unknown")
        out[gate] = status
    return out


def harness_slug_for_course(root: Path, course_id: str, course: Path) -> str | None:
    direct = root / "dev" / "courses" / course_id / "manifest.yaml"
    if direct.is_file():
        return course_id
    relative = course.relative_to(root).as_posix()
    for manifest in sorted((root / "dev" / "courses").glob("*/manifest.yaml")):
        fields = scalar_frontmatter(manifest)
        if fields.get("path") == relative:
            return manifest.parent.name
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.startswith("path:") and line.split(":", 1)[1].strip().strip("'\"") == relative:
                return manifest.parent.name
    return None


def infer_course_state(root: Path, course_id: str, course: Path) -> dict:
    """Deriva estado operacional do filesystem — sem course-state.json.

    Estados (do mais precoce ao ready):
      absent | brief_draft | brief_approved | outline_approved |
      scaffolded | lessons_in_progress | validation_failed | ready
    """
    bastidor = bastidor_dir(root, course_id)
    harness_slug = harness_slug_for_course(root, course_id, course) if course.is_dir() else None
    spec_path = bastidor / "course-spec.json"
    spec = None
    if spec_path.is_file():
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            spec = None

    signals: dict = {
        "course_id": course_id,
        "course_path": course.relative_to(root).as_posix() if course.is_dir() else None,
        "bastidor": bastidor.relative_to(root).as_posix() if bastidor.is_dir() else None,
        "harness": harness_slug is not None,
        "harness_slug": harness_slug,
        "in_catalog": course_id in (json.loads((root / "catalog.json").read_text(encoding="utf-8")).get("courses") or {}),
        "approvals": approval_status(root, course_id, spec),
        "placeholders": count_placeholders(course) if course.is_dir() else 0,
        "lessons": len(list((course / "aulas").rglob("*.md"))) if course.is_dir() and (course / "aulas").is_dir() else 0,
        "upgrade_plan": (bastidor / "upgrade-plan.json").is_file(),
        "didactic_audit": (bastidor / "didactic-audit.md").is_file(),
    }

    if not course.is_dir() and not bastidor.is_dir():
        state = "absent"
    elif not course.is_dir():
        apps = signals["approvals"]
        if apps.get("brief") == "approved" and apps.get("outline") == "approved":
            state = "outline_approved"
        elif apps.get("brief") == "approved":
            state = "brief_approved"
        elif bastidor.is_dir():
            state = "brief_draft"
        else:
            state = "absent"
    else:
        apps = signals["approvals"]
        # validate harness if present
        validate_code: int | None = None
        if signals["harness"]:
            import subprocess
            import sys

            result = subprocess.run(
                [sys.executable, "dev/validate.py", "--course", harness_slug],
                cwd=str(root),
                capture_output=True,
                text=True,
                check=False,
            )
            validate_code = result.returncode
            signals["validate_exit"] = validate_code

        if validate_code not in (None, 0):
            state = "validation_failed"
        elif signals["placeholders"] > 0:
            state = "scaffolded" if signals["harness"] else "lessons_in_progress"
        elif signals["harness"] and signals["in_catalog"] and validate_code == 0:
            state = "ready"
        elif signals["harness"] and validate_code == 0:
            state = "lessons_in_progress"  # validate ok but not catalogued
        elif apps.get("outline") == "approved":
            state = "outline_approved"
        elif apps.get("brief") == "approved":
            state = "brief_approved"
        else:
            state = "brief_draft" if bastidor.is_dir() else "lessons_in_progress"

    signals["state"] = state
    signals["derived"] = True
    signals["note"] = "estado inferido do filesystem; aprovações humanas só no frontmatter"
    return signals
