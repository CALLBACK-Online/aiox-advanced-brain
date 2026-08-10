# Anatomia de um acervo educacional (library)

Alvo do modo **bootstrap**: um repositório no molde do aiox-advanced-brain.

## Árvore mínima operável

```text
<acervo>/
├── AGENTS.md                 # constituição: papéis, superfície, validação
├── CLAUDE.md                 # bootstrap Claude Code → aponta AGENTS.md
├── README.md                 # hub humano
├── catalog.json              # manifesto: courses, journey, counts
├── package.json              # files do aluno + script validate
├── .gitignore                # /docs/, .claude/, .agents/, notas/**
├── cursos/
│   └── README.md             # hub de trilhas
├── dev/
│   ├── README.md
│   ├── validate.py           # harness
│   ├── lib/                  # context, generic, links, frontmatter, …
│   └── courses/
│       └── check_course_surface.py
├── docs/                     # bastidor (gitignored no root template)
│   └── producao-cursos/README.md
├── notas/
│   └── README.md
└── .obsidian/                # vault mínimo (opcional mas útil)
```

Opcionais no mesmo acervo (se também distribuir assets):

- `skills/` — skills de **estudo/operação no projeto do aluno** (não ops de maintainer)
- `squads/` — pacotes multi-agente

## Modelo de jornada

`catalog.json` → `learning_journey`:

- `model`: tipicamente `common-core-plus-application-routes-and-continuity-preview`
- `common_core`: lista de course ids
- `application_routes`: rotas após o núcleo
- `core_transitions` / `cross_route_transitions`: `bridge` = path de arquivo real
- `continuity_preview`: trilha “preview” (ex. Enterprise), não formação completa

Ver `journey-model.md`.

## Validação

```bash
npm run validate
# = python3 dev/validate.py
# ordem típica: surface → cada curso → journey → routing (se houver)
```

Novo curso no acervo: pasta em `cursos/` + `dev/courses/<slug>/` + entrada no
`catalog.json` + (se trilha oficial) journey + hub.

## Fronteiras

| Pedido | Não fazer no bootstrap |
|--------|------------------------|
| Copiar monorepo AIOX Core inteiro | Só contratos educacionais |
| Incluir course-library-ops no pack aluno | Ops fica em `dev/ops/` ou pack de time |
| Paths `/Users/...` | Placeholders portáteis |
