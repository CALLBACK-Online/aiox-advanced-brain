#!/usr/bin/env python3
"""Smoke funcional dos fluxos bootstrap, create, improve e upgrade."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
SCRIPTS = PACK / "scripts"


def run(*args: str, cwd: Path | None = None, expected: int = 0) -> None:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != expected:
        raise SystemExit(
            f"selftest falhou ({result.returncode} != {expected}): {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def approve(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    replacements = {
        "status: draft": "status: approved",
        'approved_by: ""': 'approved_by: "selftest-human"',
        'approval_date: ""': 'approval_date: "2026-08-10"',
        'approval_scope: ""': 'approval_scope: "brief ou outline do selftest"',
    }
    for before, after in replacements.items():
        if before not in text:
            raise SystemExit(f"selftest: campo ausente em {path}: {before}")
        text = text.replace(before, after, 1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="course-library-ops-") as temp:
        root = Path(temp)
        run(
            sys.executable,
            str(SCRIPTS / "bootstrap_library.py"),
            "--dest",
            str(root),
            "--title",
            "Selftest Library",
            "--slug",
            "selftest-library",
        )
        run(sys.executable, "dev/validate.py", cwd=root)
        run(
            sys.executable,
            str(SCRIPTS / "prepare_course.py"),
            "--course-id",
            "aiox-exemplo",
            "--title",
            "AIOX Exemplo",
            "--path",
            "cursos/AIOX-Exemplo",
            "--profile",
            "decisorio-aplicado",
            "--repo-root",
            str(root),
        )
        bastidor = root / "docs" / "producao-cursos" / "aiox-exemplo"
        spec_path = bastidor / "course-spec.json"
        run(
            sys.executable,
            str(SCRIPTS / "check_approvals.py"),
            "--spec",
            str(spec_path),
            "--repo-root",
            str(root),
            expected=1,
        )
        approve(bastidor / "COURSE-BRIEF.md")
        approve(bastidor / "course-outline.md")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["modules"] = [
            {
                "id": "M0",
                "title": "Decisão inicial",
                "evidence": "Artefato verificável",
                "quiz": False,
                "lessons": [{"id": "primeira-decisao", "title": "Primeira decisão", "reading_minutes": 10}],
            }
        ]
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        brief = bastidor / "COURSE-BRIEF.md"
        outline = bastidor / "course-outline.md"
        brief.write_text(
            brief.read_text(encoding="utf-8").replace(
                'approved_artifact: ""',
                'approved_artifact: "docs/producao-cursos/aiox-exemplo/COURSE-BRIEF.md"',
            ),
            encoding="utf-8",
        )
        outline.write_text(
            outline.read_text(encoding="utf-8").replace(
                'approved_artifact: ""',
                'approved_artifact: "docs/producao-cursos/aiox-exemplo/course-outline.md"',
            ),
            encoding="utf-8",
        )
        run(sys.executable, str(SCRIPTS / "check_approvals.py"), "--spec", str(spec_path), "--repo-root", str(root))
        run(sys.executable, str(SCRIPTS / "scaffold_course.py"), "--spec", str(spec_path), "--repo-root", str(root))
        run(sys.executable, "dev/validate.py", "--course", "aiox-exemplo", cwd=root, expected=1)
        run(
            sys.executable,
            str(SCRIPTS / "audit_didactics.py"),
            "--course",
            "aiox-exemplo",
            "--write",
            "--repo-root",
            str(root),
        )
        run(
            sys.executable,
            str(SCRIPTS / "audit_didactics.py"),
            "--check",
            str(bastidor / "didactic-audit.md"),
            "--repo-root",
            str(root),
            expected=1,
        )
        audit_path = bastidor / "didactic-audit.md"
        closed_rows: list[str] = []
        for line in audit_path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| `"):
                closed_rows.append(line)
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            cells[3] = "PASS"
            if cells[2] != "PASS":
                cells[5] = "corrigido no selftest"
                cells[6] = "evidência selftest"
            closed_rows.append("| " + " | ".join(cells) + " |")
        audit_path.write_text("\n".join(closed_rows) + "\n", encoding="utf-8")
        run(
            sys.executable,
            str(SCRIPTS / "audit_didactics.py"),
            "--check",
            str(audit_path),
            "--repo-root",
            str(root),
        )
        run(
            sys.executable,
            str(SCRIPTS / "plan_upgrade.py"),
            "--course",
            "aiox-exemplo",
            "--spec",
            str(spec_path),
            "--require-approved",
            "--write",
            "--repo-root",
            str(root),
            expected=1,
        )
        spec["creation_mode"] = "upgrade"
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        run(
            sys.executable,
            str(SCRIPTS / "plan_upgrade.py"),
            "--course",
            "aiox-exemplo",
            "--spec",
            str(spec_path),
            "--require-approved",
            "--write",
            "--repo-root",
            str(root),
        )
        # expand plan with a second lesson and apply --add
        spec["modules"][0]["lessons"].append(
            {"id": "segunda-decisao", "title": "Segunda decisão", "reading_minutes": 10}
        )
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        run(
            sys.executable,
            str(SCRIPTS / "plan_upgrade.py"),
            "--course",
            "aiox-exemplo",
            "--spec",
            str(spec_path),
            "--require-approved",
            "--write",
            "--refresh",
            "--repo-root",
            str(root),
        )
        run(
            sys.executable,
            str(SCRIPTS / "apply_upgrade.py"),
            "--course",
            "aiox-exemplo",
            "--add",
            "segunda-decisao",
            "--repo-root",
            str(root),
        )
        run(
            sys.executable,
            str(SCRIPTS / "doctor.py"),
            "--course",
            "aiox-exemplo",
            "--repo-root",
            str(root),
        )
    print("course-library-ops selftest: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
