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
  aiox_advanced: 42
  aiox_advanced_squads: 31
  total: 73
  counted_at: '2026-08-10'
---
# Design Ops

Operação e governança contínuas do design system: decisões, tokens, ciclo de vida, acessibilidade e regressão visual. Vai além de criar componentes.

## Como é usado

Use **Design Ops** quando uma escolha visual se repete entre telas. Registre-a como token e regra no `DESIGN.md`, faça os componentes consumirem o contrato e verifique acessibilidade e regressão antes de propagar a mudança.

**Exemplo prático:** na aula [[41-design-system-e-decisao]], altere o raio do botão primário no token, renderize suas variantes no Storybook, rode a verificação visual do Chromatic e confira o critério de acessibilidade antes de aceitar a alteração.

**Não confunda:** **Design Ops** não é escolher a aparência de uma tela isolada nem manter uma galeria de componentes bonitos. É governar a decisão visual ao longo do ciclo de vida, com contrato e verificação.

**Frequência nos cursos:** **73** menções (AIOX Advanced: 42 · AIOX Advanced Squads: 31).

## Aulas

- [[41-design-system-e-decisao]]
- [[56-tailwind-shadcn-storybook]]
- [[43-design-md-novo-contrato]]

## Ver também

- [[Design System]]
- [[Storybook]]
- [[Chromatic]]
- [[DESIGN md]]
- [[Glossário AIOX Advanced]]
