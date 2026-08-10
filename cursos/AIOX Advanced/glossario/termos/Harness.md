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
  aiox_advanced: 68
  aiox_advanced_squads: 2
  total: 70
  counted_at: '2026-08-10'
---
# Harness

Ambiente que hospeda um agent ou squad fora do chat interativo, com runtime, autenticação, tools, filas, segredos, observabilidade e políticas de custo/falha.

## Como é usado

Use **Harness** quando o valor precisar rodar sem a IDE aberta — por exemplo, para cliente, SLA, execução contínua, dados sensíveis ou limite de custo por job.

**Exemplo prático:** na aula [[67-harness-ambiente-execucao]], desenhe um bot de tickets com worker em runtime, fila, auth, tools remotas, logs redacted e budget cap por job; teste uma execução fora da IDE.

**Não confunda:** **Harness** não é prompt, proxy de LLM ou a IDE; é a camada operacional que dá execução persistente, políticas e prova ao agent.

**Frequência nos cursos:** **70** menções (AIOX Advanced: 68 · AIOX Advanced Squads: 2).

## Aulas

- [[67-harness-ambiente-execucao]]
- [[68-squad-fora-do-claude-code]]

## Ver também

- [[Runner]]
- [[Squad]]
- [[CLAUDE md]]
- [[Glossário AIOX Advanced]]
