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
  aiox_advanced: 57
  aiox_advanced_squads: 0
  total: 57
  counted_at: '2026-08-10'
---
# Render-contract

Regra executável que especifica como tokens, componentes, props e contextos viram uma interface renderizada; reduz a margem para a IA improvisar tela a tela.

## Como é usado

Use **Render-contract** depois de registrar a decisão visual: descreva como um token se aplica em tema, viewport, estado e componente, e use o contrato para verificar se a renderização respeita essa regra.

**Exemplo prático:** na aula [[43-design-md-novo-contrato]], o `render-contract` delimita como os tokens extraídos pela skill `/design-md` viram tela; na aula [[41-design-system-e-decisao]], ele fecha a passagem de decisão registrada para geração coerente.

**Não confunda:** **DESIGN.md** é o contrato visual amplo e o ponto de entrada que a IA lê antes de gerar: decisões, tokens, componentes e regras. **Render-contract** é uma parte especializada desse contrato: diz como renderizar os valores em contextos concretos. DESIGN.md define o que vale; render-contract define como isso aparece na tela.

**Frequência nos cursos:** **57** menções (AIOX Advanced: 57 · AIOX Advanced Squads: 0).

## Aulas

- [[43-design-md-novo-contrato]]
- [[41-design-system-e-decisao]]
- [[56-tailwind-shadcn-storybook]]

## Ver também

- [[DESIGN md]]
- [[-design-md]]
- [[Design token]]
- [[Variant matrix]]
- [[Storybook]]
- [[Design System]]
- [[Glossário AIOX Advanced]]
