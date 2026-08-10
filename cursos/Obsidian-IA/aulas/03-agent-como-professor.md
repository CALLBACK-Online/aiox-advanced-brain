---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: agent-como-professor
lesson_position: 3
title: "O agent como professor-especialista"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 14
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# O agent como professor-especialista

[← Wikilinks e grafo](02-wikilinks-e-grafo.md) · [⌂ Curso](../README.md) · [→ Captura sem poluir](04-captura-sem-poluir.md)

## Resultado

Ao final desta aula você consegue **formular um pedido** ao agent como condutor do segundo cérebro (path + próximo passo + evidência), não como autocomplete de opinião.

## Quando usar — e quando não usar

**Use** quando o repo estiver aberto no Claude Code, Codex ou similar com `AGENTS.md` / `CLAUDE.md`.

**Não use** o agent para inventar comandos de runtime que não existem no seu projeto.  
**Não use** plugin de IA *dentro* do Obsidian como substituto deste contrato — são papéis diferentes.

## Agent no repo × plugin de IA no Obsidian

| | **Agent (Claude Code / Codex / …)** | **Plugin de IA no Obsidian** |
|--|-------------------------------------|-----------------------------|
| Onde roda | Terminal / IDE com o repo | Dentro do app Obsidian |
| Contrato | `AGENTS.md`, skills, `catalog.json` | Depende do plugin (fora deste acervo) |
| Força | Ler aulas, rotear squad, montar Brief, capturar | Resumir nota aberta, chat local |
| Risco | Inventar runtime se você não cobrar path | Poluir vault, vazar nota, sem maturidade AIOX |

Neste mini, **a superfície de IA é o agent no repositório** (e depois no projeto). Plugin no Obsidian é opcional de produto, não pré-requisito e não está no caminho crítico 00→07.

## Contrato

Neste repositório o agent deve:

1. Localizar material em `cursos/`, `skills/`, `squads/`.
2. Ensinar com profundidade calibrada.
3. Rotear squads via manifesto quando a missão for operacional.
4. Exigir evidência.
5. Não inventar paths de máquina nem credenciais.

Arquivos de bootstrap (na raiz do repo): `AGENTS.md`, `CLAUDE.md`.

## Skills de vault (menor mecanismo)

| Pedido | Skill (path no repo) |
|--------|----------------------|
| “Como uso o segundo cérebro?” | `skills/aiox-brain/SKILL.md` |
| Abrir vault, achar aula, Graph | `skills/obsidian-course-vault/SKILL.md` |
| MOC / hub | `skills/course-moc/SKILL.md` |
| Capturar insight ou retorno | `skills/study-capture/SKILL.md` |
| Qual squad? | `skills/aiox-squads/SKILL.md` + curso Squads |

Peça a skill **pelo nome ou path** se o runtime não tiver `$skill` registrado. Menor skill basta; não invoque squad para “só capturar uma nota”.

## Prompts que funcionam

```text
Estou no aiox-advanced-brain. Descubra se estou no núcleo comum ou em uma rota de aplicação e me
ensine o próximo passo com 1 aula e 1 exercício — sem despejar o catálogo.
```

```text
Use as skills de vault (aiox-brain / obsidian-course-vault).
Quero estudar design system: monte um caminho de 3 aulas e diga se preciso de squad.
```

```text
Consulte o agent-router dos squads e diga qual squad serve para:
"meu agente entra em loop e depende de mim".
```

```text
Recupere de 1 a 3 fontes reais deste vault para a missão abaixo e monte um
Context Brief. Não execute aqui: prepare o handoff mínimo para o projeto.
Missão: {transformação observável}
```

```text
Calibre para iniciante: 1 ideia + 1 próximo passo + 1 path. Não liste o catálogo inteiro.
```

## Anti-prompts (o que evitar)

| Pedido fraco | Por quê | Em vez disso |
|--------------|---------|--------------|
| “Me explica o AIOX” | Catálogo infinito | Etapa + 1 aula |
| “Reescreve todas as aulas do meu jeito” | Polui canônico | Captura em `notas/` |
| “Roda o squad aqui no vault” | Vault ≠ projeto | Context Brief + handoff |
| “Inventa o comando `/xyz`” | Runtime desconhecido | Path + `generic_prompt` |
| “Cola o vault no meu app” | Contexto sem fronteira | Brief + asset mínimo |

## Superfícies (lembrete)

| Runtime | Bootstrap | Cuidado |
|---------|-----------|--------|
| Claude Code | `CLAUDE.md` → `AGENTS.md` | `$skill` / `@agent` só se existirem |
| Codex | `AGENTS.md` | Não assumir `*` / `/` |
| Genérico | paths + `generic_prompt` | Colar briefing da aula |

## Calibrar profundidade

| Você… | Peça |
|-------|------|
| Iniciante / perdido | 1 aula + 1 exercício + 1 path |
| Intermediário | Mapa curto (2–3 aulas) + prática |
| Operação | Briefing, maturidade, ativação, evidência |

Se a resposta vier sem path relativo válido, peça de novo: *“cite o arquivo do acervo”*.

## Prática

Faça **uma** pergunta real ao agent sobre uma dúvida sua do AIOX. Exija na resposta: path de arquivo + próximo passo. Se a resposta for genérica, reenvie com o anti-prompt corrigido.

## Evidência de conclusão

Cole (na sua nota pessoal) a resposta do agent com pelo menos um path relativo válido **e** um próximo passo verificável.

## Navegação
[← Anterior](02-wikilinks-e-grafo.md) · [↑ Curso](../README.md) · [Próxima →](04-captura-sem-poluir.md)
