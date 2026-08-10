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
  aiox_advanced: 45
  aiox_advanced_squads: 0
  total: 45
  counted_at: '2026-08-10'
---
# Sub-agent

Agente filho em sessão isolada (um por chamada, sem cross-talk livre). Diferente de swarm com mensagens entre agentes.

## Como é usado

Use **Sub-agent** para delegar uma tarefa fechada a uma sessão isolada: o agente pai dispara o filho com briefing e escopo, o filho trabalha com contexto próprio e devolve um resultado único — sem conversar com outros sub-agents pelo caminho.

**Exemplo prático:** na aula [[29-sub-agents-vs-swarm-agents]], um orquestrador dispara três sub-agents de pesquisa, cada um lendo uma parte diferente do repositório; cada filho devolve seu resumo ao pai, que consolida — nenhum deles vê o trabalho dos outros.

**Não confunda:** **Sub-agent** não é swarm: no swarm os agentes trocam mensagens entre si; o sub-agent só fala com quem o disparou — uma chamada, um resultado, sessão descartada.

**Frequência nos cursos:** **45** menções (AIOX Advanced: 45 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]
- [[14-anatomia-do-agente]]
- [[15-quatro-executores]]

## Ver também

- [[Agent tool]]
- [[Swarm]]
- [[Agent Teams]]
- [[Agente]]
- [[Glossário AIOX Advanced]]
