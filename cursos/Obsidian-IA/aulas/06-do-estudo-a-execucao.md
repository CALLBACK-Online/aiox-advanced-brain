---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: do-estudo-a-execucao
lesson_position: 6
title: "Do estudo à execução"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 12
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Do estudo à execução

[← MOCs e hubs](05-mocs-e-hubs.md) · [⌂ Curso](../README.md) · [→ Prática integrada](07-pratica-integrada.md)

## Resultado

Saber **quando parar de estudar** e copiar um asset para o projeto real.

## Quando usar — e quando não usar

**Use** quando a missão já tem transformação observável.

**Não** copie 24 squads “por precaução”.

## Menor mecanismo suficiente

```text
Dúvida conceitual     → aula (Advanced)
Organizar estudo      → aiox-brain / course-moc / study-capture
Tarefa estreita       → skills/<nome>
Missão multi-agente   → squads/<nome> + curso Squads + agent-router
```

## Loop

1. Estudo no Obsidian (canônico).
2. Captura pessoal.
3. Escolha skill ou squad (maturidade em `catalog.json`).
4. `cp -R` para o **seu** projeto.
5. Briefing + evidência (não “rodei o chat”).

Para squads em linguagem natural: curso `cursos/AIOX-Advanced-Squads/` + `AGENT-GUIDE.md` + `agent-router.json` (paths no repo).

## Runtime honesto

Só use `$skill`, `@agent`, `*comando`, `/comando` se existirem no ambiente de destino. Caso contrário, prompt genérico + paths de arquivo.

## Prática

Pegue a missão da sua captura ou MOC e escreva:

```text
Missão: …
Skill ou squad: …
Por que não o vizinho: …
O que copio para o projeto: …
Evidência que vou exigir: …
```

## Evidência de conclusão

Bloco acima preenchido sem inventar nome de asset fora do catálogo.
