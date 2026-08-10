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
# Brownfield Enhancement

Adicionar valor a um sistema existente depois do Discovery: escolher a menor superfície, respeitar o domínio e provar não-regressão antes do merge.

## Como é usado

Use **Brownfield Enhancement** depois de mapear o repositório. Nomeie módulos e consumidores, classifique o risco como local, núcleo ou transversal e escolha uma fatia vertical com o kit de prova correspondente.

**Exemplo prático:** na aula [[53-brownfield-enhancement]], ao adicionar prioridade a um ticket, mapeie form, endpoint, cache Redis e job de SLA; use testes do módulo e smoke se o toque for local, ou ADR, flag, QG reforçado e rollback se atingir schema compartilhado.

**Não confunda:** **Brownfield Enhancement** não é Brownfield Discovery, que decifra o sistema antes da feature, nem refatoração cosmética ou rewrite total. Enhancement entrega uma fatia com prova de não-regressão.

**Frequência nos cursos:** **11** menções (AIOX Advanced: 11 · AIOX Advanced Squads: 0).

## Aulas

- [[53-brownfield-enhancement]]
- [[31-brownfield-discovery]]

## Ver também

- [[Brownfield Discovery]]
- [[Greenfield]]
- [[Entidade]]
- [[Glossário AIOX Advanced]]
