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
  aiox_advanced: 20
  aiox_advanced_squads: 0
  total: 20
  counted_at: '2026-08-10'
---
# Atomizar

Extrair de uma UI existente os primitivos que se repetem — tokens, estados e componentes atômicos — para torná-los reutilizáveis sem apagar o comportamento original.

## Como é usado

Use **Atomizar** ao analisar uma tela ou fluxo já existente: identifique padrões repetidos, nomeie seus tokens e componentes e só depois componha novas telas com essas peças.

**Exemplo prático:** uma área de conta repete três estilos de botão e dois campos de formulário; extraia cor, espaçamento e estados para tokens e componentes, documente as variantes no Storybook e confira se a tela continua igual.

**Não confunda:** **Atomizar** não é quebrar um arquivo em dezenas de componentes sem reuso nem é refazer a interface por preferência visual. A extração deve nascer de padrões observados e preservar o contrato da UI.

**Frequência nos cursos:** **20** menções (AIOX Advanced: 20 · AIOX Advanced Squads: 0).

## Aulas

- [[32-design-system-greenfield-brownfield]]

## Ver também

- [[Glossário AIOX Advanced]]
