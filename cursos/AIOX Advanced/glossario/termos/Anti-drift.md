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
  aiox_advanced: 7
  aiox_advanced_squads: 0
  total: 7
  counted_at: '2026-08-10'
---
# Anti-drift

Contrato que evita o loop sair do goal.

## Como é usado

Use **Anti-drift** ao desenhar autonomia longa: o rider/spec carrega escopo, fontes, skills, stop rules e gates para que o loop continue apontado para o goal em vez de derivar para tarefas paralelas.

**Exemplo prático:** na aula [[50-rider-modo-elicitacao]], o rider roda com `elicit: true` nos momentos críticos: o loop segue autônomo, mas para e pergunta ao operador nos pontos de decisão — autonomia com freio, não microgestão. É o contrato anti-drift em ação.

**Não confunda:** anti-drift não é supervisionar cada passo do agente: é amarrar goal, limites e stop rules **antes** de o loop começar, justamente para não precisar vigiá-lo o tempo todo.

**Frequência nos cursos:** **7** menções (AIOX Advanced: 7 · AIOX Advanced Squads: 0).

## Aulas

- [[50-rider-modo-elicitacao]]

## Ver também

- [[Glossário AIOX Advanced]]
