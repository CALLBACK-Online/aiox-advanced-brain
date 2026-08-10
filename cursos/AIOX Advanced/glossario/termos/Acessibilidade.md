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
  aiox_advanced: 44
  aiox_advanced_squads: 0
  total: 44
  counted_at: '2026-08-10'
---
# Acessibilidade

Condição de uma interface poder ser percebida, operada e compreendida por pessoas com diferentes capacidades e tecnologias assistivas; no AIOX, inclui teclado, foco, nome acessível, estados, contraste e responsividade.

## Como é usado

Use **Acessibilidade** como critério de componente e de fluxo, não como uma revisão visual no fim. Comece por HTML semântico, garanta nome e foco acessíveis, permita operação por teclado e use ARIA apenas para completar semântica que o HTML não expressa.

**Exemplo prático:** na aula [[57-storybook-para-variantes]], uma modal que parece perfeita no default precisa ter foco inicial, ordem de tabulação, fechamento previsível e retorno do foco; a [[Variant matrix]] registra esses cenários e o [[Storybook]] os torna revisáveis.

**Não confunda:** **a11y** é a abreviação de acessibilidade; não é sinônimo de ARIA nem de contraste. **ARIA** comunica papel, estado e propriedade para tecnologia assistiva, mas não corrige sozinho foco ausente, interação impossível por teclado ou HTML semântico mal escolhido. Primeiro semântica e comportamento; depois ARIA quando necessário.

**Frequência nos cursos:** **44** menções (AIOX Advanced: 44 · AIOX Advanced Squads: 0).

## Aulas

- [[57-storybook-para-variantes]]
- [[56-tailwind-shadcn-storybook]]
- [[48-quality-gate-completo]]

## Ver também

- [[Variant matrix]]
- [[Storybook]]
- [[Chromatic]]
- [[Design Ops]]
- [[Quality Gate]]
- [[Glossário AIOX Advanced]]
