#!/usr/bin/env python3
"""Doctor: inventário e divergências de um acervo educacional.

Roda no root do acervo (catalog.json + package.json). Exit 0 se sem erros
estruturais graves; 1 se houver divergências.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ABSOLUTE = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/])"
)
PRODUCTION_FILES = {
    "course-brief.md",
    "course-outline.md",
    "gap-analysis.md",
    "didactic-audit.md",
    "upgrade-ledger.md",
    "upgrade-plan.json",
    "course-spec.json",
    "retrospective.md",
    "deviations.yaml",
    "deviations.yml",
}


PACK_EXCLUDE = {"dist", "__pycache__", ".DS_Store", ".git"}


def pack_files(base: Path) -> dict[str, bytes]:
    """Conteúdo por path relativo, ignorando artefatos de build."""
    files: dict[str, bytes] = {}
    if not base.is_dir():
        return files
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if PACK_EXCLUDE & set(rel.parts):
            continue
        files[rel.as_posix()] = path.read_bytes()
    return files


def compare_trees(sot: dict[str, bytes], installed: dict[str, bytes]) -> list[str]:
    drift: list[str] = []
    for rel in sorted(sot.keys() | installed.keys()):
        if rel not in installed:
            drift.append(f"faltando no instalado: {rel}")
        elif rel not in sot:
            drift.append(f"extra no instalado: {rel}")
        elif sot[rel] != installed[rel]:
            drift.append(f"conteúdo difere: {rel}")
    return drift


def find_root(start: Path) -> Path:
    cur = start.resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / "catalog.json").is_file() and (candidate / "package.json").is_file():
            return candidate
    raise SystemExit("raiz do acervo não encontrada (catalog.json + package.json)")


def journey_course_ids(journey: dict) -> set[str]:
    ids = set(journey.get("common_core") or [])
    for route in (journey.get("application_routes") or {}).values():
        ids.update(route.get("courses") or [])
        if route.get("entry_from"):
            ids.add(route["entry_from"])
    for transition in (journey.get("core_transitions") or []) + (
        journey.get("cross_route_transitions") or []
    ):
        ids.update(value for value in (transition.get("from"), transition.get("to")) if value)
    preview = journey.get("continuity_preview") or {}
    ids.update(value for value in (preview.get("course"), preview.get("entry_from")) if value)
    return ids


def journey_bridges(journey: dict) -> list[str]:
    bridges: list[str] = []
    for transition in (journey.get("core_transitions") or []) + (
        journey.get("cross_route_transitions") or []
    ):
        if transition.get("bridge"):
            bridges.append(transition["bridge"])
    for route in (journey.get("application_routes") or {}).values():
        if route.get("bridge"):
            bridges.append(route["bridge"])
    preview = journey.get("continuity_preview") or {}
    if preview.get("bridge"):
        bridges.append(preview["bridge"])
    return bridges


def report_course_state(root: Path, query: str) -> int:
    """Estado derivado de um curso (sem course-state.json)."""
    # Import local: doctor pode rodar sem scripts no path se invocado de outro cwd.
    scripts = Path(__file__).resolve().parent
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from course_common import infer_course_state, resolve_course  # noqa: WPS433

    course_id, course = resolve_course(root, query)
    state = infer_course_state(root, course_id, course)
    print(f"# course state (derived)\nroot: {root}\n")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    # Diagnóstico: sempre 0. Use validate.py para falhar builds.
    return 0


def report_all_states(root: Path) -> int:
    scripts = Path(__file__).resolve().parent
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from course_common import infer_course_state, resolve_course  # noqa: WPS433

    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    courses = catalog.get("courses") or {}
    print(f"# course states (derived)\nroot: {root}\n")
    print("| id | state | lessons | placeholders | harness | catalog | validate |")
    print("|---|---|---:|---:|---|---|---|")
    for cid in sorted(courses):
        try:
            course_id, course = resolve_course(root, cid)
            st = infer_course_state(root, course_id, course)
            print(
                f"| `{cid}` | {st.get('state')} | {st.get('lessons')} | "
                f"{st.get('placeholders')} | {st.get('harness')} | "
                f"{st.get('in_catalog')} | {st.get('validate_exit', '—')} |"
            )
        except SystemExit as exc:
            print(f"| `{cid}` | error | — | — | — | — | {exc} |")
    print("\nNota: estado derivado do filesystem; aprovações só no frontmatter.")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Doctor do acervo ou estado derivado de um curso")
    parser.add_argument("--course", help="infere estado de um curso (derived, sem JSON de estado)")
    parser.add_argument(
        "--states",
        action="store_true",
        help="tabela de estado derivado de todos os courses no catalog",
    )
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    if args.course and args.states:
        raise SystemExit("use --course ou --states, não ambos")
    if args.course:
        return report_course_state(root, args.course)
    if args.states:
        return report_all_states(root)

    errors: list[str] = []
    warnings: list[str] = []

    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    courses = catalog.get("courses") or {}
    supplemental = catalog.get("supplemental_courses") or []
    journey = catalog.get("learning_journey") or {}
    pkg = json.loads((root / "package.json").read_text(encoding="utf-8"))

    print(f"# course-library-ops doctor\nroot: {root}\n")
    # package surface
    files = pkg.get("files") or []
    for bad in ("dev", "dev/", "docs", "docs/"):
        if any(str(f).strip("./") == bad.rstrip("/") or str(f).startswith(bad) for f in files):
            errors.append(f"package.json files inclui maintainer path: {bad}")

    # surface pollution
    cursos = root / "cursos"
    if cursos.is_dir():
        for path in cursos.rglob("*"):
            if not path.is_file():
                continue
            name = path.name.lower()
            if name in PRODUCTION_FILES or "validation-report" in name:
                errors.append(f"bastidor em superfície: {path.relative_to(root)}")
            if path.suffix.lower() in {".py", ".sh", ".js", ".ts", ".mjs"}:
                errors.append(f"executável em cursos/: {path.relative_to(root)}")
            if path.suffix == ".md":
                text = path.read_text(encoding="utf-8", errors="replace")
                if ABSOLUTE.search(text):
                    errors.append(f"path absoluto: {path.relative_to(root)}")

    # index harness manifests by course path
    harness_by_path: dict[str, str] = {}
    harness_root = root / "dev" / "courses"
    if harness_root.is_dir():
        for child in harness_root.iterdir():
            man = child / "manifest.yaml"
            if not man.is_file():
                continue
            text = man.read_text(encoding="utf-8")
            for line in text.splitlines():
                if line.startswith("path:"):
                    raw = line.split(":", 1)[1].strip().strip("'\"")
                    harness_by_path[raw] = child.name
                    break

    # catalog courses vs disk
    print("## courses")
    for cid, meta in sorted(courses.items()):
        path = meta.get("path")
        if not path:
            errors.append(f"courses.{cid}: path ausente")
            continue
        full = root / path
        exists = full.is_dir()
        aulas_dir = full / "aulas"
        if exists and aulas_dir.is_dir():
            lessons_disk = len(list(aulas_dir.rglob("*.md")))
        else:
            lessons_disk = 0
        lessons_cat = meta.get("lessons")
        mark = "OK" if exists else "MISSING"
        line = f"- {cid}: {path} [{mark}] aulas_disk={lessons_disk}"
        if lessons_cat is not None and exists and lessons_cat != lessons_disk:
            line += f" catalog.lessons={lessons_cat} DIVERGE"
            errors.append(f"{cid}: lessons catalog={lessons_cat} disk={lessons_disk}")
        print(line)
        harness_slug = harness_by_path.get(path) or cid
        harness = root / "dev" / "courses" / harness_slug
        if exists and not (harness / "manifest.yaml").is_file():
            warnings.append(f"{cid}: sem harness (esperado dev/courses/{harness_slug}/)")

    catalog_paths = {meta.get("path") for meta in courses.values() if meta.get("path")}
    catalog_paths.update(item.get("path") for item in supplemental if item.get("path"))
    for path in sorted(cursos.iterdir()):
        if path.is_dir() and (path / "aulas").is_dir():
            relative = path.relative_to(root).as_posix()
            if relative not in catalog_paths:
                warnings.append(f"curso no disco sem catálogo: {relative}")

    # journey ids
    print("\n## learning_journey")
    if not journey:
        warnings.append("learning_journey ausente no catalog")
    else:
        print(f"- model: {journey.get('model')}")
        print(f"- common_core: {journey.get('common_core') or []}")
        known_ids = set(courses)
        known_ids.update(item.get("id") for item in supplemental if item.get("id"))
        for cid in sorted(journey_course_ids(journey)):
            if cid not in known_ids:
                warnings.append(f"journey referencia id sem courses/supplemental: {cid}")
        for bridge in journey_bridges(journey):
            if not (root / bridge).is_file():
                errors.append(f"bridge ausente: {bridge}")

    # harness presence
    print("\n## harness")
    validate = root / "dev" / "validate.py"
    print(f"- validate.py: {'yes' if validate.is_file() else 'NO'}")
    if not validate.is_file():
        errors.append("dev/validate.py ausente")

    # ops install state + drift SoT <-> projeções
    print("\n## runtime ops")
    sot = root / "dev" / "ops" / "course-library-ops"
    sot_files = pack_files(sot)
    # Skills fantasma: qualquer dir extra com SKILL.md dentro de skills/ é
    # carregado pelo runtime (backups antigos do install poluem o namespace).
    for runtime_dir in (root / ".claude" / "skills", root / ".agents" / "skills"):
        if not runtime_dir.is_dir():
            continue
        for child in sorted(runtime_dir.iterdir()):
            if child.is_dir() and ".backup." in child.name and (child / "SKILL.md").is_file():
                errors.append(
                    f"skill fantasma no runtime: {child.relative_to(root)} — "
                    "mova backups para fora de skills/ (install.sh atual já faz isso)"
                )
    for rel in (".claude/skills/course-library-ops", ".agents/skills/course-library-ops"):
        installed = root / rel
        if not (installed / "SKILL.md").is_file():
            print(f"- {rel}: não instalado (scripts/install.sh)")
            continue
        if not sot_files:
            print(f"- {rel}: instalado (SoT ausente; sem comparação)")
            continue
        drift = compare_trees(sot_files, pack_files(installed))
        if drift:
            print(f"- {rel}: instalado, DERIVA ({len(drift)} arquivo(s))")
            for item in drift[:6]:
                print(f"    · {item}")
            errors.append(
                f"{rel} divergente do SoT — rode bash dev/ops/course-library-ops/scripts/install.sh --target both"
            )
        else:
            print(f"- {rel}: instalado, em paridade com o SoT")

    print("\n## summary")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERR:  {e}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
