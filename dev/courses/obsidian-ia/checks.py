"""Checagens específicas — Obsidian + IA.

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

    ROOT = ctx.root
    COURSE = ctx.course
    VAULT = ctx.root
    COURSE_ID = ctx.course_id
    SCOPE = ctx.scope
    errors = ctx.errors

    import json
    import re
    import sys
    from pathlib import Path
    from urllib.parse import unquote

    EXPECTED = [
        "por-que-obsidian-ia",
        "abrir-o-vault",
        "wikilinks-e-grafo",
        "agent-como-professor",
        "captura-sem-poluir",
        "mocs-e-hubs",
        "do-estudo-a-execucao",
        "pratica-integrada",
    ]
    REQUIRED_SECTIONS = [
        "## Resultado",
        "## Quando usar — e quando não usar",
        "## Prática",
        "## Evidência de conclusão",
    ]
    REQUIRED_CAPSTONE_SECTIONS = [
        "## Context Brief",
        "## Execução no projeto AIOX",
        "## Retorno ao segundo cérebro",
        "## Definition of Done",
    ]
    REQUIRED_TEMPLATE_SECTIONS = [
        "## Missão",
        "## Contexto recuperado",
        "## Decisões e restrições",
        "## Mecanismo escolhido",
        "## Handoff à próxima etapa",
        "## Critérios de aceite",
        "## Evidência esperada",
        "## Retorno ao segundo cérebro",
    ]
    REQUIRED_TEMPLATE_FIELDS = [
        "Não o copie inteiro",
        "## Template copiável",
        "status: draft",
        "**Transformação observável:**",
        "**Destino:**",
        "- Fonte:",
        "- Decisão já tomada:",
        "- Maturidade:",
        "- Contexto transferido:",
        "- [ ] {resultado observável 1}",
        "- Artefato:",
        "- Validação:",
        "- Decisão final:",
        "- Aprendizado reutilizável:",
    ]
    REQUIRED_CAPSTONE_STEPS = [
        "1. **Missão**",
        "2. **Vault**",
        "3. **Captura ou MOC**",
        "4. **Context Brief**",
        "5. **Roteamento**",
        "6. **Handoff**",
        "7. **Execução no projeto**",
        "8. **Validação**",
        "9. **Retorno**",
    ]
    REQUIRED_OPERATIONAL_LOOP = [
        "1. Estudo no Obsidian",
        "2. Recuperação de 1–3 fontes",
        "3. Captura pessoal ou MOC",
        "4. Context Brief",
        "5. Escolha de skill ou squad",
        "6. Cópia somente do asset necessário",
        "7. Execução no projeto",
        "8. Validação do artefato",
        "9. Nota de retorno",
    ]
    LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


    def frontmatter(text: str) -> dict[str, str]:
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            return {}
        result: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line or line.startswith((" ", "-")):
                continue
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
        return result


    def require_tokens(text: str, tokens: list[str], label: str, errors: list[str]) -> None:
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: falta contrato {token}")


    def require_in_order(text: str, tokens: list[str], label: str, errors: list[str]) -> None:
        positions = [text.find(token) for token in tokens]
        for token, position in zip(tokens, positions):
            if position < 0:
                errors.append(f"{label}: falta etapa {token}")
        existing = [position for position in positions if position >= 0]
        if len(existing) == len(tokens) and existing != sorted(existing):
            errors.append(f"{label}: etapas fora de ordem")


    errors = ctx.errors  # shared list
    lesson_files = sorted((COURSE / "aulas").glob("*.md"))
    quiz_files = sorted((COURSE / "avaliacoes").glob("Quiz-*.md"))
    question_count = 0

    if len(lesson_files) != 8:
        errors.append(f"esperadas 8 aulas; encontradas {len(lesson_files)}")

    actual_ids: list[str] = []
    for position, path in enumerate(lesson_files):
        text = path.read_text(encoding="utf-8")
        data = frontmatter(text)
        lid = data.get("lesson_id", "")
        actual_ids.append(lid)
        if data.get("type") != "lesson" or data.get("course") != "obsidian-ia":
            errors.append(f"{path.name}: frontmatter inválido")
        if data.get("status") != "canonical":
            errors.append(f"{path.name}: status deve ser canonical")
        if data.get("canonical_scope") != "cursos/Obsidian-IA":
            errors.append(f"{path.name}: canonical_scope incorreto")
        if data.get("lesson_position") != str(position):
            errors.append(f"{path.name}: lesson_position={data.get('lesson_position')!r}")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.name}: falta {section}")

    if actual_ids != EXPECTED:
        errors.append(f"ordem/ids divergentes: {actual_ids}")

    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        data = frontmatter(text)
        questions = len(re.findall(r"^### \d+\.", text, re.MULTILINE))
        question_count += questions
        if data.get("type") != "course-quiz" or data.get("course") != "obsidian-ia":
            errors.append(f"{path.relative_to(COURSE)}: frontmatter inválido")
        if data.get("status") != "canonical":
            errors.append(f"{path.relative_to(COURSE)}: status deve ser canonical")
        if data.get("question_count") != str(questions):
            errors.append(
                f"{path.relative_to(COURSE)}: question_count={data.get('question_count')!r}; "
                f"encontradas {questions}"
            )

    capstone = COURSE / "aulas" / "07-pratica-integrada.md"
    if capstone.exists():
        capstone_body = capstone.read_text(encoding="utf-8")
        require_tokens(capstone_body, REQUIRED_CAPSTONE_SECTIONS, capstone.name, errors)
        require_in_order(capstone_body, REQUIRED_CAPSTONE_STEPS, capstone.name, errors)
        require_tokens(
            capstone_body,
            [
                "O modo A é apenas o gate preparatório",
                "A conclusão do mini-curso exige todos os itens abaixo",
                "Menor asset necessário disponível no projeto real",
                "Artefato produzido no projeto real",
                "Conclusão do mini-curso:",
                "artefato validado no projeto",
                "nota de retorno",
            ],
            capstone.name,
            errors,
        )

    operation_lesson = COURSE / "aulas" / "06-do-estudo-a-execucao.md"
    if operation_lesson.exists():
        operation_body = operation_lesson.read_text(encoding="utf-8")
        require_in_order(operation_body, REQUIRED_OPERATIONAL_LOOP, operation_lesson.name, errors)

    onboarding_lesson = COURSE / "aulas" / "01-abrir-o-vault.md"
    if onboarding_lesson.exists():
        onboarding_body = onboarding_lesson.read_text(encoding="utf-8")
        require_tokens(
            onboarding_body,
            ["Abra a **raiz do repositório**", "notas/inbox/", "notas/retornos/"],
            onboarding_lesson.name,
            errors,
        )

    context_brief = COURSE / "templates" / "context-brief.md"
    if not context_brief.exists():
        errors.append("template Context Brief ausente")
    else:
        template_body = context_brief.read_text(encoding="utf-8")
        require_tokens(
            template_body,
            REQUIRED_TEMPLATE_SECTIONS + REQUIRED_TEMPLATE_FIELDS,
            "templates/context-brief.md",
            errors,
        )

    external_contracts = {
        ROOT / "00-HOME.md": ["Context Brief", "notas/retornos/"],
        ROOT / "AGENTS.md": ["Context Brief", "nota de retorno"],
        ROOT / "CLAUDE.md": [
            "encerre em estudo/captura",
            "Integrar segundo cérebro",
            "Context Brief",
            "study-capture",
        ],
        ROOT / "README.md": ["Context Brief", "execução validada no projeto", "retorno ao vault"],
        ROOT / "cursos/MOC-Acervo-AIOX.md": ["Context Brief", "execução", "retorno"],
        ROOT / "notas/README.md": [
            "## Primeiro uso",
            "mkdir -p notas/inbox",
            "notas/retornos/",
        ],
        ROOT / "skills/aiox-brain/SKILL.md": ["Context Brief", "Depois da execução"],
        ROOT / "skills/course-moc/SKILL.md": ["Context Brief", "aiox-brain"],
        ROOT / "skills/obsidian-course-vault/SKILL.md": ["Context Brief", "aiox-brain"],
        ROOT / "skills/study-capture/SKILL.md": [
            "Context Brief:",
            "Operação sugerida:",
            "Retorno planejado:",
        ],
    }
    for path, tokens in external_contracts.items():
        if not path.exists():
            errors.append(f"contrato externo ausente: {path.relative_to(ROOT)}")
            continue
        external_body = path.read_text(encoding="utf-8")
        require_tokens(external_body, tokens, str(path.relative_to(ROOT)), errors)
        if path.name == "SKILL.md" and path.parent.name == "study-capture":
            require_in_order(external_body, tokens, str(path.relative_to(ROOT)), errors)

    catalog_path = ROOT / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    course_records = [
        item
        for item in catalog.get("supplemental_courses", [])
        if item.get("path") == "cursos/Obsidian-IA"
    ]
    if len(course_records) != 1:
        errors.append(f"catalog.json: esperado 1 registro Obsidian-IA; encontrados {len(course_records)}")
    else:
        course_record = course_records[0]
        markdown_count = len(list(COURSE.rglob("*.md")))
        if course_record.get("markdown_files") != markdown_count:
            errors.append(
                "catalog.json: markdown_files Obsidian-IA="
                f"{course_record.get('markdown_files')}; encontrados {markdown_count}"
            )
        if course_record.get("lessons") != len(lesson_files):
            errors.append(
                f"catalog.json: lessons Obsidian-IA={course_record.get('lessons')}; "
                f"encontradas {len(lesson_files)}"
            )
        if course_record.get("quizzes") != len(quiz_files):
            errors.append(
                f"catalog.json: quizzes Obsidian-IA={course_record.get('quizzes')}; "
                f"encontrados {len(quiz_files)}"
            )
        if course_record.get("questions") != question_count:
            errors.append(
                f"catalog.json: questions Obsidian-IA={course_record.get('questions')}; "
                f"encontradas {question_count}"
            )

    readme = COURSE / "README.md"
    if not readme.exists():
        errors.append("README.md ausente")
    else:
        body = readme.read_text(encoding="utf-8")
        if "Obsidian + IA" not in body:
            errors.append("README.md sem título esperado")
        for promise in ("Context Brief", "projeto AIOX", "nota de retorno"):
            if promise not in body:
                errors.append(f"README.md sem promessa operacional: {promise}")
        require_tokens(body, ["**ou** 1 MOC", "source_version: 1.3.0"], "README.md", errors)

    for path in COURSE.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(COURSE.resolve()):
                errors.append(f"{path.relative_to(COURSE)}: link sai do curso -> {target}")
            elif not resolved.exists():
                errors.append(f"{path.relative_to(COURSE)}: link não resolve -> {target}")
        for raw_target in WIKILINK.findall(text):
            target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
            if target.startswith(("00-HOME", "cursos/", "notas/", "skills/", "squads/")):
                errors.append(f"{path.relative_to(COURSE)}: wikilink sai do curso -> {target}")

    # Detail line if checks set local counters commonly named
    detail_parts = []
    for name in ("lesson_files", "lessons", "module_files", "modules", "quiz_files", "quizzes"):
        pass
    return None
