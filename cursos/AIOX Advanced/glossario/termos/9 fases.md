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
  aiox_advanced: 32
  aiox_advanced_squads: 0
  total: 32
  counted_at: '2026-08-10'
---
# 9 fases

O pipeline completo do /code-anatomist, que cobre arquitetura, domínio, dados, API, dependências e infra em fases ordenadas.

## Como é usado

Use as **9 fases** quando precisar extrair a anatomia de um sistema existente antes de mexer nele: o /code-anatomist percorre o pipeline em ordem — do spy inicial do código até a formalização da regra de negócio — e extrai as 6 camadas da anatomia (arquitetura, domínio, dados, API, dependências e infra), em vez de devolver uma impressão geral do código.

**Exemplo prático:** na aula [[38-code-anatomy-domain-decoder]], antes de reescrever um sistema legado, o /code-anatomist roda as **9 fases** sobre o repositório: investiga o código, extrai cada uma das 6 camadas e entrega o Decoder — o mapa acionável com a regra de negócio formalizada — que o squad usa como fonte de verdade, não como suposição.

**Não confunda:** **9 fases** não é sinônimo das 6 camadas: as fases são as etapas ordenadas do pipeline; as camadas são o que ele extrai. Também não é leitura de README nem resumo gerado de uma vez — pular fases devolve um mapa com buracos que contamina as decisões seguintes.

**Frequência nos cursos:** **32** menções (AIOX Advanced: 32 · AIOX Advanced Squads: 0).

## Aulas

- [[38-code-anatomy-domain-decoder]]

## Ver também

- [[Glossário AIOX Advanced]]
