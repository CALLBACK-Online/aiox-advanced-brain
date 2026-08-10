---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 23
  aiox_advanced_squads: 51
  total: 74
  counted_at: '2026-08-10'
---
# Orquestrador

Papel de entrada que entende a missão, escolhe a rota, coordena especialistas, tasks, workflows, gates e handoffs. No AIOX, costuma aparecer como **chief** ou `orchestrator`.

## Como é usado

Use o **Orquestrador** na fronteira de entrada do squad: ele lê o briefing, confirma o fit com a rota, delega ao agente especialista correto e cobra a evidência final. A [[cursos/AIOX-Advanced-Squads/AGENT-GUIDE]] determina que o chief deve rotear sem pular o diagnóstico e exigir `briefing`, `decision-log`, `deliverable` e `validation`.

**Exemplo prático:** na aula [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad]], uma missão para materializar um processo já validado começa no `clickup-chief`. Ele confirma o anti-escopo, encaminha a execução para `materializer` ou `auditor` e preserva o gate; não grava no ClickUp sem autoridade confirmada. Na aula [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]], o `squad-chief` recebe a especificação e coordena o scaffolding e a validação do novo squad.

**Não confunda:** **Orquestrador** não é um agente especialista que faz todo o trabalho. O chief coordena a rota e as fronteiras; o especialista decide dentro do domínio e a task transforma estado. Também não é o dono automático de merge ou push: a aula [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]] deixa o handoff para a autoridade correspondente.

**Frequência nos cursos:** **74** menções (AIOX Advanced: 23 · AIOX Advanced Squads: 51).

## Aulas

- [[cursos/AIOX-Advanced-Squads/aulas/00-como-usar-este-curso]]
- [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]]
- [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad]]
- [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]]
- [[cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro]]

## Ver também

- [[Agent]]
- [[Squad]]
- [[Roteamento de squad]]
- [[cursos/AIOX-Advanced-Squads/Guia-de-execucao]]
- [[Glossário AIOX Advanced]]
