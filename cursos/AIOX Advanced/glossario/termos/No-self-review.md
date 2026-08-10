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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# No-self-review

Regra de separação: quem implementou não pode ser a única perspectiva que declara o resultado aprovado. O gate precisa de validação independente proporcional ao risco.

## Como é usado

Use **No-self-review** ao fechar um gate: defina um revisor ou motor independente, o critério de aceitação e a evidência que ele precisa conferir.

**Exemplo prático:** quem implementou a Story entrega diff e testes; um segundo motor — CodeRabbit no PR ou um revisor com outro modelo — roda o caminho crítico, compara com o aceite e devolve findings antes do PASS.

**Não confunda:** **No-self-review** não exige duas implementações nem revisão cerimonial; exige que produção e validação não dependam da mesma única leitura.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[48-quality-gate-completo]]
- [[06-code-rabbit-boost]]
- [[60-routing-modelos]]

## Ver também

- [[Quality Gate]]
- [[CodeRabbit]]
- [[Three-brain]]
- [[Self-heal]]
- [[Glossário AIOX Advanced]]
