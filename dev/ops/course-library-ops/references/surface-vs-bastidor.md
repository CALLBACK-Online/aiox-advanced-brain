# Superfície do aluno vs bastidor vs prova

Contrato KISS herdado do acervo aiox-advanced-brain.

| Camada | Path | Versionar? | No npm pack aluno? | Quem usa |
|--------|------|------------|--------------------|----------|
| **Aluno** | `cursos/`, `skills/`, `squads/`, pack root | Sim | Sim | Estudante / cópia de estudo |
| **Prova** | `dev/` | Sim | **Não** | Maintainer / CI |
| **Bastidor** | `docs/producao-cursos/` | Local (muitas vezes gitignored em `/docs/`) | **Não** | Autor editorial |
| **Runtime IDE** | `.claude/`, `.agents/` | Não (gitignore) | **Não** | Time com ops instalado |

## O que nunca vai em `cursos/`

- `COURSE-BRIEF`, `course-outline`, `course-spec`, `gap-analysis`, `deviations.*`, `*validation-report*`
- `didactic-audit`, `upgrade-plan`, `upgrade-ledger`, `retrospective`
- `CURRICULUM-GAP`, `CURRICULUM-EXPANSION`
- `_tools/`, `tests/`, `scripts/`
- sufixos `.py`, `.sh`, `.js`, `.ts`, `.mjs`

Gate: `dev/courses/check_course_surface.py`.

## O que vai em `docs/producao-cursos/<id>/`

- COURSE-BRIEF.md
- course-outline.md
- course-spec.json
- gap-analysis.md
- didactic-audit.md
- upgrade-plan.json / upgrade-ledger.md
- retrospective.md
- deviations.yaml
- validation-report.md
- expansões / drafts editoriais

## O que vai em `dev/courses/<slug>/`

- `manifest.yaml` — id, path, title, regras genéricas opcionais
- `checks.py` — `def run(ctx)` específico do curso

O harness **não** pode exigir arquivos de `docs/` (clone limpo = EXIT 0).
