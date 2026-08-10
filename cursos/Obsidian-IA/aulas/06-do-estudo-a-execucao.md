---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: do-estudo-a-execucao
lesson_position: 6
title: "Context Brief: do estudo à execução"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 18
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Context Brief: do estudo à execução

> [[00-HOME]] · [[cursos/Obsidian-IA/README|Obsidian-IA]] · [[cursos/entradas/README|entradas]] · [[notas/README|notas]]

[← MOCs e hubs](05-mocs-e-hubs.md) · [⌂ Curso](../README.md) · [→ Estudo → execução → memória](07-pratica-integrada.md)

## Resultado

Transformar conhecimento recuperado no vault em um **Context Brief**, levar somente o contexto e o asset necessários ao projeto AIOX e preparar o retorno ao segundo cérebro.

## Quando usar — e quando não usar

**Use** quando a missão já tem transformação observável.

**Não** copie 24 squads “por precaução”.

## Arquitetura da integração

```text
Segundo cérebro                    Projeto AIOX
cursos + notas + MOCs              código + runtime + validação
        │                                     │
        └──── Context Brief + asset ─────────→│
        │←── resultado + decisão + evidência ─┘
        └──── nota de retorno
```

O projeto não precisa acessar todo o vault, e o vault não precisa virar parte do projeto. A ponte é o **menor contexto suficiente** para a missão.

## Menor mecanismo suficiente

```text
Dúvida conceitual     → aula (Advanced)
Organizar estudo      → aiox-brain / course-moc / study-capture
Tarefa estreita       → skills/<nome>
Missão multi-agente   → squads/<nome> + curso Squads + agent-router
```

## Loop operacional

1. Estudo no Obsidian (canônico).
2. Recuperação de 1–3 fontes realmente úteis.
3. Captura pessoal ou MOC que explica por que essas fontes importam.
4. Context Brief com missão, restrições, mecanismo e aceite.
5. Escolha de skill ou squad com maturidade confirmada em `catalog.json`.
6. Cópia somente do asset necessário para o destino confirmado pelo projeto.
7. Execução no projeto com o briefing como contexto de entrada.
8. Validação do artefato produzido.
9. Nota de retorno com resultado, decisão e aprendizado reutilizável.

Para squads em linguagem natural: curso `cursos/AIOX-Advanced-Squads/` + `AGENT-GUIDE.md` + `agent-router.json` (paths no repo).

## Context Brief

Use o [template canônico](../templates/context-brief.md). Ele deve responder:

```text
Missão: qual transformação observável precisa acontecer?
Fontes: quais aulas/notas sustentam a decisão e por quê?
Restrições: o que deve ser preservado ou evitado?
Mecanismo: qual skill/squad, maturidade e fronteira?
Handoff: o que vai para o projeto e o que fica no vault?
Aceite: como saber que a missão terminou?
Evidência: qual artefato ou validação provará a execução?
Retorno: o que será registrado no segundo cérebro depois?
```

O briefing é copiável para qualquer runtime. Paths do vault servem como proveniência; o conteúdo necessário deve estar resumido no próprio briefing, porque o agent do projeto pode não enxergar este repositório.

## Handoff seguro ao projeto

1. Confirme que o asset citado existe e leia sua maturidade.
2. Descubra no projeto de destino onde aquele runtime carrega skills ou squads; não invente o diretório.
3. Copie somente `skills/<nome>/` ou `squads/<id>/` quando necessário.
4. Entregue o Context Brief ao agent do projeto.
5. Exija artefato + validação; uma conversa concluída não é evidência.
6. Não transfira `notas/`, secrets, logs brutos nem o vault inteiro.

## Runtime honesto

Só use `$skill`, `@agent`, `*comando`, `/comando` se existirem no ambiente de destino. Caso contrário, entregue o Context Brief e aponte para os arquivos copiados do asset, sem fingir ativação.

## Prática

Pegue uma missão real da sua captura ou MOC e preencha uma cópia do template:

```text
Missão: …
Fontes recuperadas: …
Decisões e restrições: …
Skill ou squad: …
Maturidade: …
Por que não o vizinho: …
O que copio para o projeto: …
Critérios de aceite: …
Evidência que vou exigir: …
Retorno que vou capturar: …
```

## Evidência de conclusão

Context Brief preenchido com pelo menos uma fonte real, um asset existente com maturidade confirmada, aceite verificável e retorno planejado.
