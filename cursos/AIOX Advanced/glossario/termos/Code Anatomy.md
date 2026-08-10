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
  aiox_advanced: 52
  aiox_advanced_squads: 0
  total: 52
  counted_at: '2026-08-10'
---
# Code Anatomy

Engenharia reversa estruturada de um codebase em nove fases: extrai arquitetura, domínio, dados, API, dependências e infraestrutura e formaliza a regra de negócio escondida no código.

## Como é usado

Use **Code Anatomy** antes de mudar um sistema que você ainda não entende. Siga as fases para localizar dependências, consumidores e regras de domínio; use o mapa produzido para delimitar a mudança.

**Exemplo prático:** na aula [[38-code-anatomy-domain-decoder]], antes de alterar a prioridade de tickets, trace controller/API, schema, cache e job de SLA e registre a regra extraída; só depois escolha os arquivos do enhancement.

**Não confunda:** **Code Anatomy** não é ler o README ou a tela e supor o comportamento, nem é começar a codar enquanto descobre. A saída é um mapa verificável da estrutura e da regra de negócio.

**Frequência nos cursos:** **52** menções (AIOX Advanced: 52 · AIOX Advanced Squads: 0).

## Aulas

- [[38-code-anatomy-domain-decoder]]
- [[31-brownfield-discovery]]

## Ver também

- [[Domain Decoder]]
- [[9 fases]]
- [[-code-anatomist]]
- [[Brownfield Discovery]]
- [[Glossário AIOX Advanced]]
