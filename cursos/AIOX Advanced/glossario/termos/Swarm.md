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
  aiox_advanced: 82
  aiox_advanced_squads: 0
  total: 82
  counted_at: '2026-08-10'
---
# Swarm

Modo multi-agente em rede, com comunicação entre pares e debate explícito (ex.: Swarm OS / swarm-execute). Contrasta com sub-agent isolado.

## Como é usado

Use **Swarm** com um critério único: os agentes precisam conversar entre si? Se sim, swarm; se não, sub-agents isolados. Vale quando o caminho é incerto e o resultado depende de consenso ou descoberta coletiva.

**Exemplo prático:** na aula [[29-sub-agents-vs-swarm-agents]], dispare `/swarm-execute` para comparar arquiteturas: os agentes trocam mensagens via send_message, debatem hipóteses e o processo encerra no gate de convergência definido.

**Não confunda:** **Swarm** não é apenas fan-out de sub-agents; sem comunicação entre pares e critério de convergência, use sub-agents isolados.

**Frequência nos cursos:** **82** menções (AIOX Advanced: 82 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]
- [[58-ralph-paralelizacao]]
- [[61-wave-execute]]

## Ver também

- [[Sub-agent]]
- [[Swarm OS]]
- [[Paralelização]]
- [[Ralph]]
- [[Glossário AIOX Advanced]]
