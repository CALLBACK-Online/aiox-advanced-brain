# {{LIBRARY_TITLE}}

Acervo educacional (cursos Markdown + harness de validação).

## Para estudar

1. Abra esta pasta no Obsidian ou no editor.
2. Comece por `cursos/README.md`.
3. Siga a jornada em `catalog.json` → `learning_journey`.

## Para o time (maintainer)

```bash
npm run validate
bash dev/ops/course-library-ops/scripts/install.sh --target both
python3 dev/ops/course-library-ops/scripts/doctor.py
```

Ops de criação/gestão de cursos: skill **course-library-ops** (não é skill de aluno).

## Superfícies

| Path | Quem |
|------|------|
| `cursos/` | Aluno |
| `dev/` | Prova do acervo / maintainer |
| `docs/producao-cursos/` | Bastidor editorial (local) |
