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
  aiox_advanced: 20
  aiox_advanced_squads: 0
  total: 20
  counted_at: '2026-08-10'
---
# Agent tool

Mecanismo que dispara um sub-agent em sessão isolada. Cada chamada cria um filho sem conversa lateral com outros agentes.

## Como é usado

Use **Agent tool** para delegar uma tarefa fechada: o filho recebe briefing, limites e formato de saída, trabalha na própria sessão e devolve o resultado ao agente pai.

**Exemplo prático:** na aula [[29-sub-agents-vs-swarm-agents]], peça a um sub-agent para auditar a acessibilidade de uma Story e devolver findings; o pai confere e integra o relatório depois.

**Não confunda:** **Agent tool** cria filhos isolados; swarm agents coordenam-se entre si. Sem briefing, limites e formato de saída, o sub-agent devolve ruído.

**Frequência nos cursos:** **20** menções (AIOX Advanced: 20 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]

## Ver também

- [[Glossário AIOX Advanced]]
