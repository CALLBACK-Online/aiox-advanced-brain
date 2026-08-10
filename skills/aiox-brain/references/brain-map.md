# Mapa do segundo cérebro AIOX

## Camadas

```text
┌─────────────────────────────────────────────────────────┐
│  AGENTS.md / CLAUDE.md — professor-especialista         │
├─────────────────────────────────────────────────────────┤
│  cursos/          material canônico (wikilinks)         │
│  skills/          procedimentos (incl. brain + AIOX)    │
│  squads/          pacotes multi-agente                  │
│  catalog.json     inventário + maturidade               │
├─────────────────────────────────────────────────────────┤
│  notas/                 captura e retorno do aluno       │
│  vault pessoal (opcional)  PARA/LYT da pessoa           │
└─────────────────────────────────────────────────────────┘
                          │
             Context Brief + asset mínimo
                          ▼
┌─────────────────────────────────────────────────────────┐
│  projeto AIOX      código + runtime + validação         │
└─────────────────────────────────────────────────────────┘
                          │
             resultado + decisão + evidência
                          └──────────────→ notas/retornos/
```

## Trilhas canônicas

| Trilha | Entrada |
|--------|---------|
| Hub | `cursos/README.md` |
| Obsidian + IA (mini) | `cursos/Obsidian-IA/README.md` |
| Método | `cursos/AIOX Advanced/README.md` |
| Squads | `cursos/AIOX-Advanced-Squads/README.md` |
| Router agents | `cursos/AIOX-Advanced-Squads/agent-router.json` |

## Skills de vault (Camada 1)

| Skill | Transformação |
|-------|----------------|
| `aiox-brain` | Orientar o uso do repo como segundo cérebro |
| `obsidian-course-vault` | Operar `cursos/` no Obsidian |
| `course-moc` | Mapas de conteúdo / hubs de estudo |
| `study-capture` | Notas de aprendizado ligadas às aulas |

## Fluxo ideal

1. Onboard vault (`obsidian-course-vault` ou README) — root do repo para Graph colorido.
2. Abrir `00-HOME.md` e o Graph (cores em `.obsidian/graph.json`).
3. Partir de uma missão e recuperar 1–3 aulas/notas relevantes.
4. Capturar (`study-capture`) sem editar canônico.
5. Consolidar hubs (`course-moc` + `cursos/MOC-*.md`) quando houver pelo menos 5 conexões úteis.
6. Montar o Context Brief com fontes sintetizadas, restrições, mecanismo, aceite e evidência.
7. Confirmar maturidade e copiar somente o asset necessário ao projeto.
8. Executar e validar no runtime real do projeto.
9. Devolver resultado, decisão e aprendizado a `notas/retornos/` ou ao vault pessoal indicado.

## Artefato-ponte

O Context Brief evita acoplar vault e projeto. O template canônico fica em `cursos/Obsidian-IA/templates/context-brief.md` e transporta:

- transformação observável;
- fontes e síntese relevante;
- decisões, restrições e fora de escopo;
- asset e maturidade;
- critérios de aceite e evidência;
- retorno que fechará o loop.

## Graph (cores)

| Pasta | Cor |
|-------|-----|
| `cursos/AIOX Advanced` | azul |
| `cursos/AIOX-Advanced-Squads` | roxo |
| `cursos/Obsidian-IA` | ciano |
| `skills/` | verde |
| `squads/` | laranja |
| `notas/` | âmbar |
| `#hub` | rosa |
