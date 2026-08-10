#!/usr/bin/env python3

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "catalog.json"
EXPECTED = [
    ("obsidian-ia", "cursos/Obsidian-IA", "estudar o acervo"),
    (
        "introducao-arquitetura-sistemas",
        "cursos/Introducao-a-Arquitetura-de-Sistemas",
        "entender sistemas",
    ),
    ("aiox-fundamentals", "cursos/AIOX-Fundamentals", "instalar e operar o aiox-core"),
    ("aiox-advanced", "cursos/AIOX Advanced", "aplicar o método"),
    (
        "aiox-advanced-squads",
        "cursos/AIOX-Advanced-Squads",
        "operar os especialistas",
    ),
]
EXPECTED_SPECIALIZATIONS = {
    "aiox-agent-engineering": (
        "cursos/AIOX-Agent-Engineering",
        "construir e operar capacidades agentic",
    ),
    "aiox-design": (
        "cursos/AIOX-Design",
        "estabelecer contrato e qualidade visual",
    ),
    "aiox-productizacao": (
        "cursos/AIOX-Productizacao",
        "transformar capacidade comprovada em oferta e experimento de mercado",
    ),
}
INLINE_COURSE_PATH = re.compile(r"`(cursos/[^`\n]+?\.md)`")


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    journey = catalog.get("learning_journey", {})
    courses = catalog.get("courses", {})
    errors: list[str] = []

    expected_order = [course_id for course_id, _, _ in EXPECTED]
    if journey.get("canonical_order") != expected_order:
        errors.append("catalog.learning_journey.canonical_order diverge da jornada canônica")

    responsibilities = journey.get("responsibilities", {})
    for course_id, course_path, responsibility in EXPECTED:
        course = courses.get(course_id)
        if course is None:
            errors.append(f"curso ausente do catálogo: {course_id}")
            continue
        if course.get("path") != course_path:
            errors.append(f"path divergente para {course_id}: {course.get('path')!r}")
        if not (ROOT / course_path / "README.md").is_file():
            errors.append(f"README ausente: {course_path}/README.md")
        if responsibilities.get(course_id) != responsibility:
            errors.append(f"responsabilidade divergente para {course_id}")

    specializations = journey.get("specializations", {})
    expected_specializations = {
        course_id: responsibility
        for course_id, (_, responsibility) in EXPECTED_SPECIALIZATIONS.items()
    }
    if specializations != expected_specializations:
        errors.append("especializações laterais ausentes ou divergentes")
    for course_id, (course_path, _) in EXPECTED_SPECIALIZATIONS.items():
        if course_id in expected_order:
            errors.append(f"especialização inserida na jornada canônica: {course_id}")
        if courses.get(course_id, {}).get("path") != course_path:
            errors.append(f"path divergente para especialização {course_id}")
        if not (ROOT / course_path / "README.md").is_file():
            errors.append(f"README de especialização ausente: {course_path}/README.md")

    if "consolidation_loop" in journey:
        errors.append("loop Squads → Advanced não pertence à jornada linear")
    if any("consolidates_into" in course for course in courses.values()):
        errors.append("curso terminal não pode consolidar de volta em etapa anterior")

    transitions = journey.get("transitions", [])
    expected_pairs = list(zip(expected_order, expected_order[1:]))
    actual_pairs = [(item.get("from"), item.get("to")) for item in transitions]
    if actual_pairs != expected_pairs:
        errors.append("transições não cobrem todos os pares consecutivos na ordem canônica")

    for item in transitions:
        bridge = item.get("bridge", "")
        target_id = item.get("to", "")
        target_path = courses.get(target_id, {}).get("path", "")
        bridge_path = ROOT / bridge
        if not bridge_path.is_file():
            errors.append(f"ponte ausente: {bridge}")
            continue
        if target_path and target_path not in bridge_path.read_text(encoding="utf-8"):
            errors.append(f"ponte {bridge} não aponta para {target_path}")

    terminal_files = [
        ROOT / "cursos" / "AIOX-Advanced-Squads" / "README.md",
        ROOT / "cursos" / "AIOX-Advanced-Squads" / "Projeto-Integrador.md",
    ]
    reverse_target = "cursos/AIOX Advanced/Projeto Integrador.md"
    for path in terminal_files:
        if reverse_target in path.read_text(encoding="utf-8"):
            errors.append(f"retorno obrigatório Squads → Advanced em {path.relative_to(ROOT)}")

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
    ]
    old_path = "cursos/AIOX-Fundamentos-de-Arquitetura"
    for path in active_files:
        content = path.read_text(encoding="utf-8")
        if old_path in content:
            errors.append(f"path legado ativo em {path.relative_to(ROOT)}")

    checked_inline_paths = 0
    for path in (ROOT / "cursos").rglob("*.md"):
        if "archive" in path.relative_to(ROOT).parts:
            continue
        for raw in INLINE_COURSE_PATH.findall(path.read_text(encoding="utf-8")):
            if "…" in raw or "{" in raw:
                continue
            checked_inline_paths += 1
            if not (ROOT / raw).is_file():
                errors.append(
                    f"path de curso não resolve em {path.relative_to(ROOT)}: {raw}"
                )

    print(
        f"Jornada AIOX: {len(EXPECTED)} etapas, {len(transitions)}/{len(expected_pairs)} transições, {len(specializations)} especializações laterais, {checked_inline_paths} paths verificados"
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
