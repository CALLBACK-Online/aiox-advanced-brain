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
  aiox_advanced: 16
  aiox_advanced_squads: 0
  total: 16
  counted_at: '2026-08-10'
---
# /swarm-execute

Comando que lança batches de agentes em paralelo no Swarm OS, mantendo **send_message** ativo para que eles troquem hipóteses e convirjam em uma rota.

## Como é usado

Use **/swarm-execute** quando os agentes precisarem conversar para descobrir ou negociar a solução. Antes de despachar, defina a pergunta, os limites do debate e o critério de convergência.

**Exemplo prático:** para escolher a arquitetura de uma integração ainda incerta, lance batches com hipóteses diferentes, acompanhe as mensagens entre os agentes e feche a execução quando houver uma rota justificada e registrada.

**Não confunda:** **/swarm-execute** não é apenas fan-out de tarefas independentes. Para pedaços que não precisam trocar informação, use sessões isoladas de sub-agents; o swarm paga seu custo quando o debate muda a resposta.

**Frequência nos cursos:** **16** menções (AIOX Advanced: 16 · AIOX Advanced Squads: 0).

## Aulas

- [[29-sub-agents-vs-swarm-agents]]

## Ver também

- [[Glossário AIOX Advanced]]
