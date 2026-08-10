# `dev/` — maintainer only

Fora do npm pack. Contrato: `AGENTS.md` § Superfície do aluno vs maintainer.

```bash
npm run validate                              # surface → cursos → journey → routing
npm run validate:courses                      # só os cursos
npm run selftest                              # suite + contrato no-yaml
python3 dev/validate.py --course aiox-design  # um curso
python3 dev/validate.py --list
npm run validate -- --course aiox-design
```

```text
dev/validate.py              entrypoint
dev/lib/                     utilitários compartilhados
dev/courses/<slug>/
  manifest.yaml              id, path, title (+ regras opcionais)
  checks.py                  def run(ctx) — só o específico do curso
dev/courses/check_course_surface.py
dev/courses/validate_learning_journey.py
dev/ops/course-library-ops/  OPS de time (7 modos) — ver SKILL.md
```

## course-library-ops (time)

Skill **operacional** (não vai no catálogo do aluno). SoT: `dev/ops/course-library-ops/`.

| Modo | Comando principal |
|------|-------------------|
| reverse-engineer | `python3 …/scripts/analyze_courses.py` |
| bootstrap | `python3 …/scripts/bootstrap_library.py --dest <path>` |
| create-course | `prepare_course.py` → `check_approvals.py` → `scaffold_course.py --spec …` |
| upgrade-course | `plan_upgrade.py --write` + `apply_upgrade.py --add/--archive` (nunca scaffold em destino existente) |
| improve-course | `audit_didactics.py --course <id> --write` + rubrica `skills/teach` |
| manage / doctor | `doctor.py` · `doctor.py --course <id>` (estado **derivado**) |
| pack-install | `bash …/scripts/install.sh --target both` · `package.sh` · `selftest.py` |

Projeções gitignored: `.claude/skills/course-library-ops/` e `.agents/skills/…`.  
Só editar o SoT; depois `install.sh --target both`. Backups vão em `skills-backups/`, **nunca** em `skills/`.

Contrato: `dev/ops/course-library-ops/SKILL.md`.

Não colocar aqui: aulas (`cursos/`), briefs editoriais (`docs/producao-cursos/`).
