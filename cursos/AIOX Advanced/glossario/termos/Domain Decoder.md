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
  aiox_advanced: 9
  aiox_advanced_squads: 16
  total: 25
  counted_at: '2026-08-10'
---
# Domain Decoder

Extrair regras de negócio, taxonomias e decisões escondidas no código — domínio primeiro, não só pastas.

## Como é usado

Use **Domain Decoder** quando um sistema brownfield precisa ser entendido pelo domínio antes de qualquer mudança: o decoder roda as 9 fases do code-anatomist e extrai as camadas do sistema — arquitetura, domínio, dados, API, dependências e infra — formalizando as regras de negócio escondidas no código.

**Exemplo prático:** na aula [[38-code-anatomy-domain-decoder]], um sistema legado sem documentação que será reescrito ou integrado passa pelo decoder completo e sai como "o laudo do engenheiro": a anatomia mapeada e a regra de negócio formalizada, não uma impressão da fachada. Neste acervo, o domínio vive na skill/squad `code-anatomist`; para regras de domínio brownfield, `decoder-chief` → squad `domain-decoder`.

**Não confunda:** decoder não é leitura rápida de código: um script trivial de 20 linhas não pede as 9 fases; um legado que trava decisão cara de reverter, sim. E o decoder responde pelo domínio — a regra que move o código — não pela estrutura de pastas.

**Frequência nos cursos:** **25** menções (AIOX Advanced: 9 · AIOX Advanced Squads: 16).

## Aulas

- [[38-code-anatomy-domain-decoder]]
- [[31-brownfield-discovery]]
- [[53-brownfield-enhancement]]

## Ver também

- [[Code Anatomy]]
- [[Entidade]]
- [[Brownfield Discovery]]
- [[Glossário AIOX Advanced]]
