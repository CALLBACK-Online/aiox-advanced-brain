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
# OCC

Optimistic Concurrency Control: estratégia que detecta conflito de escrita concorrente por versão ou revisão, rejeitando uma atualização que partiu de um estado já alterado.

## Como é usado

Use **OCC** quando várias requisições ou agentes puderem editar a mesma entidade e uma sobrescrita silenciosa for inaceitável; compare a versão lida com a versão vigente antes de salvar.

**Exemplo prático:** nas aulas [[24-entidade-como-unidade-de-processo]] e [[70-supabase-via-data-engineer]], dois workers leem um pedido na versão 7; o primeiro salva a versão 8 e o segundo, ainda esperando a 7, recebe conflito e precisa reler antes de decidir.

**Não confunda:** **OCC** não é lock pessimista nem resolução automática do conflito; ele detecta a colisão e exige uma política explícita para reprocessar, mesclar ou recusar.

**Frequência nos cursos:** **2** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 0).

## Aulas

- [[24-entidade-como-unidade-de-processo]]
- [[70-supabase-via-data-engineer]]

## Ver também

- [[Entidade]]
- [[Migration]]
- [[Supabase]]
- [[Glossário AIOX Advanced]]
