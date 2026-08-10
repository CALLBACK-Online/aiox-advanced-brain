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
  aiox_advanced: 12
  aiox_advanced_squads: 0
  total: 12
  counted_at: '2026-08-10'
---
# Anti-papel

Limite explícito do agente: o que ele não decide, não executa ou não pode tocar. O anti-papel evita sobreposição e torna o handoff verificável.

## Como é usado

Use **Anti-papel** ao escrever o contrato de um agente, principalmente quando outros agentes poderiam assumir a mesma tarefa. Declare as fronteiras negativas junto do papel e da autoridade concedida.

**Exemplo prático:** o agente de pesquisa pode coletar fontes e entregar um briefing, mas seu anti-papel diz que ele não edita arquivos nem aprova a arquitetura. A decisão passa ao responsável seguinte com o briefing anexado.

**Não confunda:** **Anti-papel** não é uma persona negativa nem uma lista genérica de “boas práticas”. É uma restrição operacional: deixa claro onde a responsabilidade termina e por que outro agente assume a próxima ação.

**Frequência nos cursos:** **12** menções (AIOX Advanced: 12 · AIOX Advanced Squads: 0).

## Aulas

- [[45-doze-agentes-orbitais]]

## Ver também

- [[Glossário AIOX Advanced]]
