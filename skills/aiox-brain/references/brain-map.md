# Mapa do segundo cérebro AIOX

## Camadas

```text
┌─────────────────────────────────────────────────────────┐
│  AGENTS.md / CLAUDE.md — professor-especialista         │
├─────────────────────────────────────────────────────────┤
│  Cursos/          material canônico (wikilinks)         │
│  skills/          procedimentos (incl. brain + AIOX)    │
│  squads/          pacotes multi-agente                  │
│  catalog.json     inventário + maturidade               │
├─────────────────────────────────────────────────────────┤
│  Cursos/_notas-pessoais/   captura do aluno (local)     │
│  vault pessoal (opcional)  PARA/LYT da pessoa           │
└─────────────────────────────────────────────────────────┘
```

## Trilhas canônicas

| Trilha | Entrada |
|--------|---------|
| Hub | `Cursos/README.md` |
| Obsidian + IA (mini) | `Cursos/Obsidian-IA/README.md` |
| Método | `Cursos/AIOX Advanced/README.md` |
| Squads | `Cursos/AIOX-Advanced-Squads/README.md` |
| Router agents | `Cursos/AIOX-Advanced-Squads/agent-router.json` |

## Skills de vault (Camada 1)

| Skill | Transformação |
|-------|----------------|
| `aiox-brain` | Orientar o uso do repo como segundo cérebro |
| `obsidian-course-vault` | Operar `Cursos/` no Obsidian |
| `course-moc` | Mapas de conteúdo / hubs de estudo |
| `study-capture` | Notas de aprendizado ligadas às aulas |

## Fluxo ideal

1. Onboard vault (`obsidian-course-vault` ou README) — root do repo para Graph colorido.
2. Abrir `00-HOME.md` e o Graph (cores em `.obsidian/graph.json`).
3. Rota Essencial ou missão → aulas.
4. Capturar (`study-capture`) sem editar canônico.
5. Consolidar hubs (`course-moc` + `Cursos/MOC-*.md`).
6. Quando for **fazer**: skill/squad + cópia ao projeto.

## Graph (cores)

| Pasta | Cor |
|-------|-----|
| `Cursos/AIOX Advanced` | azul |
| `Cursos/AIOX-Advanced-Squads` | roxo |
| `Cursos/Obsidian-IA` | ciano |
| `skills/` | verde |
| `squads/` | laranja |
| `_notas-pessoais/` | âmbar |
| `#hub` | rosa |
