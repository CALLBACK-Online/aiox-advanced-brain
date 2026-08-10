#!/usr/bin/env python3

import json
import re
from pathlib import Path


import sys
_DEV = Path(__file__).resolve().parents[1]
if str(_DEV) not in sys.path:
    sys.path.insert(0, str(_DEV))
from lib.paths import find_root
ROOT = find_root(Path(__file__))
CATALOG_PATH = ROOT / "catalog.json"
EXPECTED_CORE = [
    ("obsidian-ia", "cursos/Obsidian-IA", "estudar o acervo"),
    (
        "introducao-arquitetura-sistemas",
        "cursos/Introducao-a-Arquitetura-de-Sistemas",
        "entender sistemas",
    ),
    ("aiox-fundamentals", "cursos/AIOX-Fundamentals", "instalar e operar o aiox-core"),
    ("aiox-advanced", "cursos/AIOX Advanced", "aplicar o método"),
]
EXPECTED_APPLICATION_ROUTES = {
    "published-specialists": (
        "aiox-advanced-squads",
        "cursos/AIOX-Advanced-Squads",
        "operar especialistas publicados",
    ),
    "agentic-capability": (
        "aiox-agent-engineering",
        "cursos/AIOX-Agent-Engineering",
        "construir e operar capacidades agentic",
    ),
    "visual-system": (
        "aiox-design",
        "cursos/AIOX-Design",
        "estabelecer contrato e qualidade visual",
    ),
    "market": (
        "aiox-productizacao",
        "cursos/AIOX-Productizacao",
        "transformar capacidade comprovada em oferta e experimento de mercado",
    ),
}
EXPECTED_CROSS_ROUTE_PAIRS = [
    ("aiox-agent-engineering", "aiox-productizacao"),
    ("aiox-agent-engineering", "aiox-advanced-squads"),
    ("aiox-design", "aiox-advanced-squads"),
    ("aiox-productizacao", "aiox-advanced-squads"),
]
EXPECTED_CONTINUITY_PREVIEW = (
    "aiox-enterprise",
    "cursos/AIOX-Enterprise",
    "diagnosticar prontidão para operação mantida",
)
INLINE_COURSE_PATH = re.compile(r"`(cursos/[^`\n]+?\.md)`")


def validate_bridge(
    item: dict[str, object], courses: dict[str, dict[str, object]], errors: list[str]
) -> None:
    bridge = str(item.get("bridge", ""))
    target_id = str(item.get("to", ""))
    target_path = str(courses.get(target_id, {}).get("path", ""))
    bridge_path = ROOT / bridge
    if not bridge_path.is_file():
        errors.append(f"ponte ausente: {bridge}")
        return
    if target_path and target_path not in bridge_path.read_text(encoding="utf-8"):
        errors.append(f"ponte {bridge} não aponta para {target_path}")


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    journey = catalog.get("learning_journey", {})
    courses = catalog.get("courses", {})
    errors: list[str] = []

    if journey.get("model") != "common-core-plus-application-routes-and-continuity-preview":
        errors.append("catalog.learning_journey.model divergente")

    expected_core_ids = [course_id for course_id, _, _ in EXPECTED_CORE]
    if journey.get("common_core") != expected_core_ids:
        errors.append("catalog.learning_journey.common_core diverge do núcleo comum")

    responsibilities = journey.get("responsibilities", {})
    expected_responsibilities: dict[str, str] = {}
    for course_id, course_path, responsibility in EXPECTED_CORE:
        expected_responsibilities[course_id] = responsibility
        course = courses.get(course_id)
        if course is None:
            errors.append(f"curso ausente do catálogo: {course_id}")
            continue
        if course.get("path") != course_path:
            errors.append(f"path divergente para {course_id}: {course.get('path')!r}")
        if not (ROOT / course_path / "README.md").is_file():
            errors.append(f"README ausente: {course_path}/README.md")

    application_routes = journey.get("application_routes", {})
    if set(application_routes) != set(EXPECTED_APPLICATION_ROUTES):
        errors.append("rotas de aplicação ausentes ou divergentes")

    for route_id, (course_id, course_path, responsibility) in EXPECTED_APPLICATION_ROUTES.items():
        expected_responsibilities[course_id] = responsibility
        course = courses.get(course_id)
        if course is None:
            errors.append(f"curso de aplicação ausente do catálogo: {course_id}")
            continue
        if course.get("path") != course_path:
            errors.append(f"path divergente para curso de aplicação {course_id}")
        if not (ROOT / course_path / "README.md").is_file():
            errors.append(f"README de aplicação ausente: {course_path}/README.md")

        route = application_routes.get(route_id, {})
        if route.get("entry_from") != "aiox-advanced":
            errors.append(f"rota {route_id}: entrada deve partir do Advanced")
        if route.get("courses") != [course_id]:
            errors.append(f"rota {route_id}: curso divergente")
        validate_bridge(
            {"to": course_id, "bridge": route.get("bridge", "")}, courses, errors
        )

    preview_id, preview_path, preview_responsibility = EXPECTED_CONTINUITY_PREVIEW
    expected_responsibilities[preview_id] = preview_responsibility
    preview_course = courses.get(preview_id)
    if preview_course is None:
        errors.append(f"vitrine de continuidade ausente do catálogo: {preview_id}")
    else:
        if preview_course.get("path") != preview_path:
            errors.append(f"path divergente para vitrine {preview_id}")
        if preview_course.get("kind") != "preview":
            errors.append(f"{preview_id}: kind deve ser preview")
        if not (ROOT / preview_path / "README.md").is_file():
            errors.append(f"README de vitrine ausente: {preview_path}/README.md")

    continuity_preview = journey.get("continuity_preview", {})
    if continuity_preview.get("course") != preview_id:
        errors.append("vitrine de continuidade divergente")
    if continuity_preview.get("kind") != "preview":
        errors.append("vitrine de continuidade deve declarar kind=preview")
    if continuity_preview.get("entry_from") != "aiox-advanced":
        errors.append("vitrine de continuidade deve partir do Advanced com gate real")
    validate_bridge(
        {
            "to": preview_id,
            "bridge": continuity_preview.get("bridge", ""),
        },
        courses,
        errors,
    )

    if responsibilities != expected_responsibilities:
        errors.append("responsabilidades não cobrem os oito cursos formativos e o preview")

    if "canonical_order" in journey or "specializations" in journey or "transitions" in journey:
        errors.append("schema legado de jornada linear ainda presente")

    core_transitions = journey.get("core_transitions", [])
    expected_core_pairs = list(zip(expected_core_ids, expected_core_ids[1:]))
    actual_core_pairs = [(item.get("from"), item.get("to")) for item in core_transitions]
    if actual_core_pairs != expected_core_pairs:
        errors.append("transições não cobrem todos os pares do núcleo comum")
    for item in core_transitions:
        validate_bridge(item, courses, errors)

    cross_route_transitions = journey.get("cross_route_transitions", [])
    actual_cross_pairs = [
        (item.get("from"), item.get("to")) for item in cross_route_transitions
    ]
    if actual_cross_pairs != EXPECTED_CROSS_ROUTE_PAIRS:
        errors.append("conexões entre rotas de aplicação ausentes ou divergentes")
    for item in cross_route_transitions:
        validate_bridge(item, courses, errors)

    if "consolidation_loop" in journey:
        errors.append("loop de consolidação obrigatório não pertence à jornada")
    if any("consolidates_into" in course for course in courses.values()):
        errors.append("curso de aplicação não pode consolidar obrigatoriamente em etapa anterior")

    active_files = [
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        ROOT / "JORNADA-AIOX.md",
        ROOT / "00-HOME.md",
        ROOT / "cursos" / "README.md",
        ROOT / "cursos" / "COMO-ESTUDAR.md",
        ROOT / "cursos" / "MOC-Acervo-AIOX.md",
        ROOT / "skills" / "aiox-brain" / "SKILL.md",
        ROOT / "skills" / "aiox-brain" / "references" / "brain-map.md",
        ROOT / "skills" / "obsidian-course-vault" / "SKILL.md",
        ROOT / "skills" / "course-moc" / "SKILL.md",
        ROOT / "cursos" / "AIOX-Enterprise" / "README.md",
    ]
    old_path = "cursos/AIOX-Fundamentos-de-Arquitetura"
    stale_journey_terms = [
        "cinco etapas",
        "especializações laterais",
        "especialização lateral",
        "quinto degrau",
        "quinta etapa",
    ]
    for path in active_files:
        content = path.read_text(encoding="utf-8")
        if old_path in content:
            errors.append(f"path legado ativo em {path.relative_to(ROOT)}")
        for term in stale_journey_terms:
            if term in content.lower():
                errors.append(
                    f"modelo linear legado ({term}) em {path.relative_to(ROOT)}"
                )

    checked_inline_paths = 0
    for path in (ROOT / "cursos").rglob("*.md"):
        if "archive" in path.relative_to(ROOT).parts:
            continue
        for raw in INLINE_COURSE_PATH.findall(path.read_text(encoding="utf-8")):
            if "…" in raw or "{" in raw or "<" in raw:
                continue
            checked_inline_paths += 1
            if not (ROOT / raw).is_file():
                errors.append(
                    f"path de curso não resolve em {path.relative_to(ROOT)}: {raw}"
                )

    print(
        "Jornada AIOX: "
        f"8 cursos formativos + 1 preview ({len(EXPECTED_CORE)} no núcleo comum, "
        f"{len(core_transitions)}/{len(expected_core_pairs)} transições do núcleo, "
        f"{len(application_routes)}/{len(EXPECTED_APPLICATION_ROUTES)} rotas de aplicação, "
        f"{len(cross_route_transitions)}/{len(EXPECTED_CROSS_ROUTE_PAIRS)} conexões entre rotas, "
        f"1 vitrine de continuidade), {checked_inline_paths} paths verificados"
    )
    if errors:
        for error in errors:
            print(f"ERRO: {error}")
        print(f"Erros: {len(errors)}")
        return 1

    print("Erros: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
