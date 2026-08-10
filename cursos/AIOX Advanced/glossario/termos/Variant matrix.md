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
  aiox_advanced: 0
  aiox_advanced_squads: 0
  total: 0
  counted_at: '2026-08-10'
---
# Variant matrix

Mapa que cruza um componente com seus eixos relevantes — variante, tamanho, estado, tema, viewport e conteúdo — para escolher cenários que precisam ser renderizados e verificados.

## Como é usado

Use **Variant matrix** para tornar explícita a cobertura de um componente antes de criar Stories: liste os eixos que mudam o comportamento, selecione combinações com significado de produto e marque quais exigem teste visual, teclado, responsivo ou de tema.

**Exemplo prático:** na aula [[57-storybook-para-variantes]], monte uma matriz para `Button` com `default`, `loading`, `disabled`, dark mode e viewport móvel; na aula [[56-tailwind-shadcn-storybook]], use as Stories como catálogo vivo das combinações escolhidas.

**Não confunda:** **Variant matrix** não é o produto cartesiano cego de todas as props nem uma coleção de screenshots. Ela é um critério de seleção: cobre estados que importam, evita o “default eterno” e controla a explosão combinatória. A [[Acessibilidade]] entra como eixo de verificação, não como decoração posterior.

**Frequência nos cursos:** **0** menções (AIOX Advanced: 0 · AIOX Advanced Squads: 0).

## Aulas

- [[57-storybook-para-variantes]]
- [[56-tailwind-shadcn-storybook]]
- [[42-design-atomico-brad-frost]]

## Ver também

- [[Storybook]]
- [[Chromatic]]
- [[Acessibilidade]]
- [[Render-contract]]
- [[Design System]]
- [[Glossário AIOX Advanced]]
