# `dev/` — maintainer only

Fora do npm pack do aluno.

```bash
npm run validate
python3 dev/validate.py --list
python3 dev/validate.py --course <slug>
```

Novo curso: `dev/courses/<slug>/{manifest.yaml,checks.py}` + superfície em `cursos/`.

Ops de time: `dev/ops/course-library-ops/`.
