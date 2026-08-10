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
  aiox_advanced: 2
  aiox_advanced_squads: 0
  total: 2
  counted_at: '2026-08-10'
---
# Agent Teams

Times de agentes com papéis coordenados (não um monólogo). Exige ownership, handoff e gates — não 'mais prompts'.

## Como é usado

Use **Agent Teams** quando a missão exigir papéis coordenados: cada agente do time recebe ownership de uma parte (o que pode tocar), um handoff definido (o que entrega e para quem) e gates que validam cada passagem — em vez de um único agente fazendo tudo em monólogo.

**Exemplo prático:** um time com dev, QA e DevOps divide uma Story: o dev implementa e entrega o diff, o QA revisa contra o critério de aceite e o DevOps é o único autorizado a fazer push — cada handoff passa por um gate antes de o trabalho seguir. No AIOX, a skill /roundtable usa **Agent Teams** na prática: lentes de especialista (@architect, @cso, @qa) atacam a mesma proposta cada uma pelo seu domínio, com fallback quando um agente falha.

**Não confunda:** **Agent Teams** não é vários prompts simultâneos nem um swarm de clones paralelos: sem ownership (fronteira do que cada um toca), handoff definido e gate validando cada passagem, o que existe é ruído coordenado, não um time.

**Frequência nos cursos:** **2** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]
- [[45-doze-agentes-orbitais]]
- [[04-agentes-orbitais-aiox]]

## Ver também

- [[Agentes Orbitais]]
- [[Sub-agent]]
- [[Swarm]]
- [[Squad]]
- [[Glossário AIOX Advanced]]
