---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: do-estudo-a-execucao
lesson_position: 7
title: "Context Brief: do estudo à execução"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 18
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Context Brief: do estudo à execução

[← MOCs e hubs](06-mocs-e-hubs.md) · [⌂ Curso](../README.md) · [→ Estudo → execução → memória](08-pratica-integrada.md)

## Resultado

Ao final desta aula você consegue **preencher um Context Brief** a partir de 1–3 fontes do vault, para a próxima etapa de estudo ou — com base operacional — para um projeto AIOX.

## Quando usar — e quando não usar

**Use** quando a missão já tem transformação observável.

**Não** copie 24 squads “por precaução”.  
**Não** transfira `notas/`, secrets ou o vault inteiro.

## Arquitetura da integração

```text
Segundo cérebro ── Context Brief de estudo ──→ próxima trilha
        │
        └──── Context Brief + asset ─────────→ projeto AIOX
        ←──── resultado + decisão + evidência ┘
        └──── nota de retorno
```

O projeto não precisa acessar todo o vault, e o vault não precisa virar parte do projeto. A ponte é o **menor contexto suficiente** para a missão.

## Dois modos de Brief

| | **Estudo (modo A)** | **Operação (modo B)** |
|--|---------------------|------------------------|
| Missão | Compreender / decidir com base em aula | Transformação no projeto |
| Mecanismo | Curso/aula | Skill ou squad |
| Maturidade | “não se aplica” ou n/a | Obrigatória (`catalog.json`) |
| Handoff | Síntese + próxima trilha | Brief + menor asset |
| Aceite | Explicar / diagrama / exercício | Artefato validado |
| Retorno | Nota de estudo | `notas/retornos/` com evidência |

Mesmo template; campos mudam de peso. Na primeira passagem, complete o modo estudo. Depois de Fundamentals/Advanced + projeto seguro, complete o modo operação (aula 08).

## Menor mecanismo suficiente

```text
Dúvida sobre sistemas → Introdução à Arquitetura de Sistemas
Dúvida sobre o Core   → AIOX Fundamentals
Dúvida sobre método   → AIOX Advanced
Organizar estudo      → aiox-brain / course-moc / study-capture
Tarefa estreita       → skills/<nome>
Missão multi-agente   → squads/<nome> + curso Squads + agent-router
```

Na **primeira passagem**, escolha curso/aula como mecanismo e use o briefing para estudar. No **retorno operacional**, escolha skill/squad e faça handoff ao projeto. Exigir um asset executável antes de Fundamentals inverteria os pré-requisitos da jornada.

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

Use o [template canônico](../templates/context-brief.md) e copie somente o bloco marcado como **Template copiável** para sua nota pessoal. Ele deve responder:

```text
Missão: qual transformação observável precisa acontecer?
Fontes: quais aulas/notas sustentam a decisão e por quê?
Restrições: o que deve ser preservado ou evitado?
Mecanismo: qual curso/aula ou skill/squad, maturidade e fronteira?
Handoff: o que vai para a próxima etapa ou projeto e o que fica no vault?
Aceite: como saber que a missão terminou?
Evidência: qual artefato ou validação provará a execução?
Retorno: o que será registrado no segundo cérebro depois?
```

O briefing é copiável para qualquer runtime. Paths do vault servem como proveniência; o conteúdo necessário deve estar **resumido no próprio briefing**, porque o agent do projeto pode não enxergar este repositório.

## Handoff seguro à próxima etapa

1. Se a missão é de **estudo**, confirme o curso/aula, leve a síntese e defina como demonstrará compreensão.
2. Se a missão é **operacional**, confirme que o asset existe e leia sua maturidade.
3. Descubra no projeto de destino onde o runtime carrega skills ou squads; não invente o diretório.
4. Copie somente `skills/<nome>/` ou `squads/<id>/` quando necessário.
5. Entregue o Context Brief ao agent da próxima etapa ou do projeto.
6. Exija artefato + validação; uma conversa concluída não é evidência.
7. Não transfira `notas/`, secrets, logs brutos nem o vault inteiro.

## Falhas comuns de handoff

| Falha | Sintoma | Correção |
|-------|---------|----------|
| Brief vazio de fontes | Agent do projeto improvisa | 1–3 paths + síntese no Brief |
| Asset errado / inexistente | “Skill not found” | Confirmar path neste repo + maturidade |
| Vault inteiro no zip | Ruído + risco de notas privadas | Só Brief + pasta do asset |
| Maturidade `study` tratada como pronto | Expectativa de run autônomo | Declarar limite; estudar anatomia |
| Sem aceite | “Acho que terminou” | Critério verificável antes de executar |
| Sem plano de retorno | Aprendizado some | Campo retorno no Brief + nota depois |

## Runtime honesto

Só use `$skill`, `@agent`, `*comando`, `/comando` se existirem no ambiente de destino. Caso contrário, entregue o Context Brief e aponte para os arquivos copiados do asset, sem fingir ativação.

## Prática

Pegue uma missão real da sua captura ou MOC e preencha o bloco copiável do template em uma nota pessoal:

```text
Missão: …
Fontes recuperadas: …
Decisões e restrições: …
Curso/aula ou skill/squad: …
Maturidade: … (use “não se aplica” para rota de estudo)
Por que não o vizinho: …
O que levo para a próxima etapa ou projeto: …
Critérios de aceite: …
Evidência que vou exigir: …
Retorno que vou capturar: …
```

Marque no topo da nota: **modo estudo** ou **modo operação**.

## Evidência de conclusão

Context Brief preenchido com pelo menos uma fonte real, um destino existente, aceite verificável e retorno planejado. Na rota operacional, inclua também asset e maturidade confirmados.

## Navegação
[← Anterior](06-mocs-e-hubs.md) · [↑ Curso](../README.md) · [Próxima →](08-pratica-integrada.md)
