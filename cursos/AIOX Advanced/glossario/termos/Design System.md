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
  aiox_advanced: 140
  aiox_advanced_squads: 25
  total: 165
  counted_at: '2026-08-10'
---
# Design System

Conjunto versionado de decisões reutilizáveis de interface — tokens, componentes, variantes e contratos de uso. A IA consulta o `DESIGN.md` antes de gerar ou alterar uma tela.

## Como é usado

Use **Design System** sempre que duas ou mais telas precisarem compartilhar comportamento visual ou quando uma nova decisão de UI tiver de ser repetida e revisada.

**Exemplo prático:** se dashboard e detalhe usam o mesmo botão de confirmação, reutilize o componente, tokens e variante documentados; se o estado “carregando” faltar, adicione essa variante ao **Design System** antes de copiá-la nas duas telas.

**Não confunda:** **Design System** não é galeria de telas nem só biblioteca de componentes; ele também registra decisões, restrições e a forma correta de combinar as peças.

**Frequência nos cursos:** **165** menções (AIOX Advanced: 140 · AIOX Advanced Squads: 25).

## Aulas

- [[41-design-system-e-decisao]]
- [[42-design-atomico-brad-frost]]
- [[43-design-md-novo-contrato]]

## Ver também

- [[DESIGN md]]
- [[Atomo]]
- [[atomic-design-taxonomy]]
- [[Glossário AIOX Advanced]]
