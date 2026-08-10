---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: agent-como-professor
lesson_position: 3
title: "O agent como professor-especialista"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 12
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# O agent como professor-especialista

[← Wikilinks e grafo](02-wikilinks-e-grafo.md) · [⌂ Curso](../README.md) · [→ Captura sem poluir](04-captura-sem-poluir.md)

## Resultado

Usar o agent como **condutor do segundo cérebro**, não como autocomplete de opinião.

## Quando usar — e quando não usar

**Use** quando o repo estiver aberto no Claude Code, Codex ou similar com `AGENTS.md` / `CLAUDE.md`.

**Não use** o agent para inventar comandos de runtime que não existem no seu projeto.

## Contrato

Neste repositório o agent deve:

1. Localizar material em `cursos/`, `skills/`, `squads/`.
2. Ensinar com profundidade calibrada.
3. Rotear squads via manifesto quando a missão for operacional.
4. Exigir evidência.
5. Não inventar paths de máquina nem credenciais.

Arquivos de bootstrap (na raiz do repo): `AGENTS.md`, `CLAUDE.md`.

## Prompts que funcionam

```text
Estou no aiox-advanced-brain. Me ensine o próximo passo da Rota Essencial
com 1 aula e 1 exercício — sem listar as 75 aulas.
```

```text
Use as skills de vault (aiox-brain / obsidian-course-vault).
Quero estudar design system: monte um caminho de 3 aulas e diga se preciso de squad.
```

```text
Consulte o agent-router dos squads e diga qual squad serve para:
"meu agente entra em loop e depende de mim".
```

## Superfícies (lembrete)

| Runtime | Bootstrap | Cuidado |
|---------|-----------|--------|
| Claude Code | `CLAUDE.md` → `AGENTS.md` | `$skill` / `@agent` só se existirem |
| Codex | `AGENTS.md` | Não assumir `*` / `/` |
| Genérico | paths + `generic_prompt` | Colar briefing da aula |

## Prática

Faça **uma** pergunta real ao agent sobre uma dúvida sua do AIOX. Exija na resposta: path de arquivo + próximo passo.

## Evidência de conclusão

Cole (na sua nota pessoal) a resposta do agent com pelo menos um path relativo válido.
