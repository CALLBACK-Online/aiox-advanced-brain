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
  aiox_advanced: 14
  aiox_advanced_squads: 0
  total: 14
  counted_at: '2026-08-10'
---
# YAML Markdown JSON

Trio de formatos com papéis diferentes no contexto de agents: YAML para configuração legível por humanos, Markdown para prosa e instrução, e JSON para troca estrita entre máquinas.

## Como é usado

Use **YAML Markdown JSON** perguntando primeiro qual é o trabalho do artefato e quem o edita e consome. Escolha YAML para configuração e metadados que humanos revisam, Markdown para explicação e contrato que pessoas e LLMs leem, e JSON para integração com schema rígido.

**Exemplo prático:** na aula [[18-yaml-markdown-json-sweet-spot]], mantenha o frontmatter da nota em YAML, a aula e as instruções em Markdown e um payload de API ou registro de tokens em JSON; não force a configuração editada na mão a carregar aspas e vírgulas de JSON.

**Não confunda:** os três formatos podem representar dados, mas não têm o mesmo sweet spot. YAML favorece edição humana e comentários; Markdown favorece leitura e estrutura leve; JSON favorece parsing e intercâmbio previsível. Usar Markdown como banco de dados ou JSON como texto editorial gera ruído, manutenção difícil ou parsing quebrado.

**Frequência nos cursos:** **14** menções (AIOX Advanced: 14 · AIOX Advanced Squads: 0).

## Aulas

- [[18-yaml-markdown-json-sweet-spot]]
- [[17-engenharia-de-contexto]]
- [[13-pensamento-estruturado-antes-do-terminal]]

## Ver também

- [[Frontmatter]]
- [[Wikilink]]
- [[Obsidian]]
- [[Engenharia de Contexto]]
- [[DESIGN md]]
- [[Glossário AIOX Advanced]]
