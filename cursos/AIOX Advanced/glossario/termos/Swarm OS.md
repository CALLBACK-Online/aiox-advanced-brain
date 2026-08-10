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
  aiox_advanced: 11
  aiox_advanced_squads: 0
  total: 11
  counted_at: '2026-08-10'
---
# Swarm OS

Sistema de orquestração de batches paralelos de agentes que trocam `send_message`; no curso, é acionado por `/swarm-execute` para descobrir e convergir caminhos.

## Como é usado

Use **Swarm OS** quando agentes precisarem conversar para explorar rotas ou negociar consenso; defina ownership, mensagens e gate de convergência antes do dispatch.

**Exemplo prático:** na aula [[29-sub-agents-vs-swarm-agents]], `/swarm-execute` compara arquiteturas; os agentes debatem via `send_message` e o fan-in fecha uma rota acordada.

**Não confunda:** Swarm OS não é sub-agent em maior quantidade: sub-agents fazem fan-out isolado e respondem só ao chamador; no swarm os agentes se comunicam entre si — e sem ownership claro e fan-in, o paralelismo vira ruído.

**Frequência nos cursos:** **11** menções (AIOX Advanced: 11 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]
- [[58-ralph-paralelizacao]]

## Ver também

- [[Swarm]]
- [[Sub-agent]]
- [[-swarm-execute]]
- [[Glossário AIOX Advanced]]
