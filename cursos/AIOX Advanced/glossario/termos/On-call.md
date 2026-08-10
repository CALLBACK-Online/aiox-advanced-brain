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
  aiox_advanced: 9
  aiox_advanced_squads: 0
  total: 9
  counted_at: '2026-08-10'
---
# On-call

Escala ou designação de quem responde a alertas e incidentes em uma janela definida, com canal de contato, prioridade, runbook, tempo de resposta e escalonamento conhecidos. Mesmo em um time de uma pessoa, o plantão precisa ser explícito.

## Como é usado

Use **On-call** antes de uma release em production: nomeie responsável primário e substituto, informe a janela, teste o canal de alerta e deixe instruções para diagnóstico, comunicação, rollback e escalonamento.

**Exemplo prático:** para uma release na sexta-feira, o engenheiro primário fica on-call das 18h às 22h, o substituto recebe os alertas, o canal e o runbook estão registrados, e o procedimento manda verificar health check, smoke test e rollback antes de ampliar a exposição.

**Não confunda:** **On-call** é responsabilidade de responder a incidentes em uma janela; não é autoridade geral, senioridade ou permissão para tocar qualquer domínio. A pessoa on-call só executa ações dentro da autoridade definida, como [[Autoridade]] e [[Autoridade exclusiva]], e escala o que estiver fora do seu escopo.

**Frequência nos cursos:** **9** menções (AIOX Advanced: 9 · AIOX Advanced Squads: 0).

## Aulas

- [[73-prontidao-de-producao]]
- [[14-anatomia-do-agente]]
- [[25-core-config-leis-sociais]]

## Ver também

- [[Production readiness]]
- [[Rollback]]
- [[Health check]]
- [[Smoke test]]
- [[Autoridade]]
- [[Autoridade exclusiva]]
- [[Glossário AIOX Advanced]]
