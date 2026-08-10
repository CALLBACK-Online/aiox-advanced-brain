"""Checagens específicas — AIOX Agent Engineering.

Carregado por dev/validate.py. Preferir lib.* para utilitários novos.
"""
from __future__ import annotations

from lib.context import Context


def run(ctx: Context) -> str | None:
    """Mutates ctx.errors; optional return detail string for the report line."""
    import json
    import re
    import sys
    from collections import Counter, defaultdict
    from pathlib import Path
    from urllib.parse import unquote

    try:
        import yaml
    except ImportError:
        yaml = None  # type: ignore

    ROOT = ctx.root
    COURSE = ctx.course
    VAULT = ctx.root
    COURSE_ID = ctx.course_id
    SCOPE = ctx.scope
    errors = ctx.errors

    import json
    import re
    import sys
    from collections import Counter
    from pathlib import Path
    from urllib.parse import unquote


    COURSE_ID = "aiox-agent-engineering"
    SCOPE = "cursos/AIOX-Agent-Engineering"
    PROMISE = (
        "Projetar, construir, orquestrar, escalar e colocar em produção uma "
        "capacidade agentic verificável."
    )
    CAPSTONE_CHAIN = (
        "Research → PRD → capacidade → orquestração → harness/API → deploy → evidências"
    )
    EXPECTED_SEEDS = [
        ("01-pipeline-etl-com-agentes.md", 22, "M0"),
        ("02-taxonomia-da-capacidade.md", 28, "M0"),
        ("03-subagents-vs-swarm.md", 29, "M0"),
        ("04-runner-deterministico.md", 30, "M0"),
        ("05-entidade-e-ciclo-de-vida.md", 51, "M0"),
        ("06-workflow-vs-comando.md", 52, "M0"),
        ("07-mesa-redonda-e-advisory-board.md", 35, "M1"),
        ("08-tech-research.md", 36, "M1"),
        ("09-spy-bench.md", 37, "M1"),
        ("10-code-anatomy-e-domain-decoder.md", 38, "M1"),
        ("11-pasta-os.md", 39, "M1"),
        ("12-research-ao-prd.md", 40, "M1"),
        ("13-reuse-adapt-create.md", 54, "M2"),
        ("14-triagem-de-squad.md", 55, "M2"),
        ("15-anatomia-de-squad.md", 33, "M2"),
        ("16-squad-creator.md", 34, "M2"),
        ("17-ralph.md", 58, "M3"),
        ("18-paralelo-vs-sequencial.md", 59, "M3"),
        ("19-routing-de-modelos.md", 60, "M3"),
        ("20-wave-execute.md", 61, "M3"),
        ("21-harness.md", 67, "M4"),
        ("22-squad-fora-da-ide.md", 68, "M4"),
        ("23-escada-progressiva.md", 69, "M4"),
        ("24-supabase-via-data-engineer.md", 70, "M5"),
        ("25-vercel-deploy.md", 71, "M5"),
        ("26-cicd.md", 72, "M5"),
        ("27-prontidao-de-producao.md", 73, "M5"),
    ]
    CAPSTONE = "28-capstone-capacidade-em-producao.md"
    EXPECTED_LESSONS = [seed[0] for seed in EXPECTED_SEEDS] + [CAPSTONE]
    EXPECTED_MODULES = {
        "M0-arquitetura-da-capacidade.md": ("M0", "arquitetura operacional da capacidade"),
        "M1-discovery-e-research.md": ("M1", "dossiê de pesquisa que termina em PRD executável"),
        "M2-construcao-de-capacidade.md": ("M2", "squad mínimo capaz de executar uma unidade real de processo"),
        "M3-orquestracao-e-escala.md": ("M3", "dependências, routing e wall-clock observáveis"),
        "M4-runtime-fora-da-ide.md": ("M4", "runner, API ou harness reproduzível"),
        "M5-producao.md": ("M5", "URL funcional, pipeline e checklist de prontidão"),
        "MC-capstone.md": ("MC", CAPSTONE_CHAIN),
    }
    EXPECTED_QUIZZES = {
        "Quiz-M0-arquitetura-da-capacidade.md": "M0",
        "Quiz-M1-discovery-e-research.md": "M1",
        "Quiz-M2-construcao-de-capacidade.md": "M2",
        "Quiz-M3-orquestracao-e-escala.md": "M3",
        "Quiz-M4-runtime-fora-da-ide.md": "M4",
        "Quiz-M5-producao.md": "M5",
    }
    PRODUCT_SOURCE_IDS = {62, 63, 64, 65, 66}
    MODULE_OF = {
        **{position: "M0" for position in range(1, 7)},
        **{position: "M1" for position in range(7, 13)},
        **{position: "M2" for position in range(13, 17)},
        **{position: "M3" for position in range(17, 21)},
        **{position: "M4" for position in range(21, 24)},
        **{position: "M5" for position in range(24, 28)},
        28: "MC",
    }
    REQUIRED_ROOT = [
        "README.md",
        "AGENT-GUIDE.md",
        "Assessments.md",
        "Rubrica.md",
        "FONTES.md",
        "PROVENIENCIA.md",
        "Projeto-Integrador.md",
    ]
    LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    ABSOLUTE_PATH = re.compile(
        r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:[\\/]Users[\\/])"
    )
    ANSWER = re.compile(r"^\d+\.\s+\*\*([ABCD])\.\*\*", re.M)


    def frontmatter(text: str) -> dict[str, str]:
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        data: dict[str, str] = {}
        if match:
            for line in match.group(1).splitlines():
                if ":" in line and not line.startswith((" ", "-")):
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip().strip("'\"")
        return data


    errors = ctx.errors  # shared list
    lessons = sorted((COURSE / "aulas").glob("*.md"))
    modules = sorted((COURSE / "modulos").glob("*.md"))
    quizzes = sorted((COURSE / "avaliacoes").glob("Quiz-M*.md"))

    for found, expected, label in [
        (len(lessons), 28, "aulas"),
        (len(modules), 7, "módulos"),
        (len(quizzes), 6, "quizzes"),
    ]:
        if found != expected:
            errors.append(f"esperados {expected} {label}; encontrados {found}")

    if [path.name for path in lessons] != EXPECTED_LESSONS:
        errors.append("ordem ou nomes de aulas divergentes da rota canônica")

    if [path.name for path in modules] != sorted(EXPECTED_MODULES):
        errors.append("nomes de módulos divergentes de M0–M5 + MC")

    if [path.name for path in quizzes] != sorted(EXPECTED_QUIZZES):
        errors.append("nomes de quizzes divergentes de M0–M5")

    for path in lessons:
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        position = int(fm.get("lesson_position") or "0")
        if fm.get("type") != "lesson" or fm.get("course") != COURSE_ID:
            errors.append(f"{path.name}: frontmatter de aula inválido")
        if fm.get("status") != "canonical" or fm.get("canonical_scope") != SCOPE:
            errors.append(f"{path.name}: status/scope incorreto")
        if fm.get("module") != MODULE_OF.get(position):
            errors.append(
                f"{path.name}: módulo {fm.get('module')!r}; esperado {MODULE_OF.get(position)!r}"
            )
        if "## Navegação" not in text:
            errors.append(f"{path.name}: seção Navegação ausente")
        if path.name == CAPSTONE:
            if fm.get("source") != "synthesis":
                errors.append(f"{path.name}: capstone deve declarar source: synthesis")
            if CAPSTONE_CHAIN not in text:
                errors.append(f"{path.name}: cadeia canônica ausente")
            continue

        seed = EXPECTED_SEEDS[position - 1] if 1 <= position <= len(EXPECTED_SEEDS) else None
        if not seed or path.name != seed[0]:
            errors.append(f"{path.name}: lesson_position não corresponde à rota canônica")
            continue
        _, expected_source_id, expected_module = seed
        if fm.get("module") != expected_module:
            errors.append(f"{path.name}: módulo divergente da fonte {expected_source_id}")
        source_path = fm.get("source_path")
        if not source_path:
            errors.append(f"{path.name}: source_path ausente")
        elif not (ROOT / source_path).is_file():
            errors.append(f"{path.name}: source_path não resolve: {source_path}")
        else:
            source_match = re.match(r"(\d+)-", Path(source_path).name)
            source_id = int(source_match.group(1)) if source_match else None
            if source_id != expected_source_id:
                errors.append(
                    f"{path.name}: fonte {source_id}; esperada {expected_source_id}"
                )
            if source_id in PRODUCT_SOURCE_IDS:
                errors.append(f"{path.name}: fonte {source_id} pertence à Productização")
        for section in ["## Mapa desta aula", "## Origem curricular", "## Navegação"]:
            if section not in text:
                errors.append(f"{path.name}: seção pedagógica ausente: {section}")

    for path in modules:
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        expected_module, evidence = EXPECTED_MODULES[path.name]
        if fm.get("type") != "module" or fm.get("course") != COURSE_ID:
            errors.append(f"{path.name}: frontmatter de módulo inválido")
        if fm.get("module") != expected_module:
            errors.append(f"{path.name}: id de módulo divergente")
        if fm.get("status") != "canonical" or fm.get("canonical_scope") != SCOPE:
            errors.append(f"{path.name}: status/scope incorreto")
        if evidence not in text:
            errors.append(f"{path.name}: evidência curricular ausente: {evidence}")

    answers: Counter[str] = Counter()
    question_total = 0
    for path in quizzes:
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm.get("type") != "quiz" or fm.get("course") != COURSE_ID:
            errors.append(f"{path.name}: frontmatter de quiz inválido")
        if fm.get("module") != EXPECTED_QUIZZES[path.name]:
            errors.append(f"{path.name}: módulo de quiz divergente")
        if fm.get("status") != "canonical" or fm.get("canonical_scope") != SCOPE:
            errors.append(f"{path.name}: status/scope incorreto")
        questions = re.findall(r"^### \d+\.", text, re.M)
        question_total += len(questions)
        if len(questions) != 4:
            errors.append(f"{path.name}: esperado 4 questões; {len(questions)}")
        if "<details>" not in text or "## Transferência" not in text:
            errors.append(f"{path.name}: falta gabarito ou transferência")
        answers.update(ANSWER.findall(text))

    if question_total != 24:
        errors.append(f"esperadas 24 questões; {question_total}")
    if answers and max(answers.values()) - min(answers.values()) > 1:
        errors.append(f"gabarito desbalanceado: {dict(answers)}")

    for filename in REQUIRED_ROOT:
        if not (COURSE / filename).is_file():
            errors.append(f"arquivo obrigatório ausente: {filename}")

    for path in COURSE.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if ABSOLUTE_PATH.search(text):
            errors.append(f"{path.relative_to(COURSE)}: path absoluto")
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            try:
                resolved.relative_to(COURSE.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(COURSE)}: link fora do curso: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(COURSE)}: link quebrado: {raw}")

    readme = (COURSE / "README.md").read_text(encoding="utf-8")
    project = (COURSE / "Projeto-Integrador.md").read_text(encoding="utf-8")
    if PROMISE not in readme:
        errors.append("README.md: promessa canônica ausente")
    for path, text in [
        (COURSE / "README.md", readme),
        (COURSE / "Projeto-Integrador.md", project),
    ]:
        if CAPSTONE_CHAIN not in text:
            errors.append(f"{path.name}: cadeia canônica do capstone ausente")
    for filename in EXPECTED_LESSONS:
        if f"aulas/{filename}" not in readme:
            errors.append(f"README.md: aula ausente da sequência: {filename}")

    product_source_ids: set[int] = set()
    for path in (ROOT / "cursos/AIOX-Productizacao/aulas").glob("*.md"):
        source_path = frontmatter(path.read_text(encoding="utf-8")).get("source_path")
        if not source_path:
            continue
        source_match = re.match(r"(\d+)-", Path(source_path).name)
        if source_match:
            product_source_ids.add(int(source_match.group(1)))
    if product_source_ids != PRODUCT_SOURCE_IDS:
        errors.append(
            "AIOX Productização: fontes esperadas 62–66; "
            f"encontradas {sorted(product_source_ids)}"
        )

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    course = catalog.get("courses", {}).get(COURSE_ID, {})
    expected_catalog = {
        "path": SCOPE,
        "lessons": 28,
        "modules": 7,
        "quizzes": 6,
        "questions": 24,
        "agent_guide": f"{SCOPE}/AGENT-GUIDE.md",
    }
    for key, value in expected_catalog.items():
        if course.get(key) != value:
            errors.append(f"catalog.json: courses.{COURSE_ID}.{key} divergente")

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if f'dev/validate.py' not in package.get("scripts", {}).get(
        "validate", ""
    ):
        errors.append("package.json: validador do curso ausente de npm run validate")

    # Detail line if checks set local counters commonly named
    detail_parts = []
    for name in ("lesson_files", "lessons", "module_files", "modules", "quiz_files", "quizzes"):
        pass
    return None
