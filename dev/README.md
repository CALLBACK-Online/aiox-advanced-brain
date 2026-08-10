# `dev/` — maintainer only

Fora do npm pack. Contrato: `AGENTS.md` § Superfície do aluno vs maintainer.

```bash
npm run validate                              # surface → cursos → journey → routing
npm run validate:courses                      # só os 9 cursos
python3 dev/validate.py --course aiox-design  # um curso
python3 dev/validate.py --list
# um curso via npm:
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
```

Novo curso: `manifest.yaml` + `checks.py` → `python3 dev/validate.py --course <slug>`.

Não colocar aqui: aulas (`cursos/`), briefs editoriais (`docs/producao-cursos/`).
