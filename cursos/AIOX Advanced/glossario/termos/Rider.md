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
  aiox_advanced: 104
  aiox_advanced_squads: 0
  total: 104
  counted_at: '2026-08-10'
---
# Rider

Contrato de condução de uma execução longa: reúne contexto, fontes de verdade, skills, restrições, critérios, gates, riscos e pontos de elicitação para manter o agente no trilho.

## Como é usado

Use **Rider** quando a missão tiver várias etapas, autonomia prolongada ou decisões em que o julgamento humano muda a rota. O operador acompanha os gates de ouro e deixa passos determinísticos e reversíveis seguirem sem aprovação a cada movimento.

**Exemplo prático:** na aula [[50-rider-modo-elicitacao]], o rider interrompe o loop antes de um `drop` para confirmar ambiente, impacto e rollback, mas não pede aprovação para formatar arquivos ou repetir um teste. O piloto entra no precipício, não em cada pedra.

**Não confunda:** **Rider** é o contrato que governa a condução e os pontos de intervenção; **loop** é o ciclo de executar, validar e corrigir; **autonomia** é o grau de trabalho que o agente realiza sem intervenção contínua.

**Frequência nos cursos:** **104** menções (AIOX Advanced: 104 · AIOX Advanced Squads: 0).

## Aulas

- [[11-goal-vs-loop]]
- [[50-rider-modo-elicitacao]]
- [[21-deterministico-primeiro-llm-onde-gera-ouro]]

## Ver também

- [[Anti-drift]]
- [[Definition of Done]]
- [[Stop rule]]
- [[Goal vs Loop]]
- [[Glossário AIOX Advanced]]
