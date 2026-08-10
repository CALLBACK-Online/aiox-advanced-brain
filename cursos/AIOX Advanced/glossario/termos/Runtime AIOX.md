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
  aiox_advanced: 5
  aiox_advanced_squads: 25
  total: 30
  counted_at: '2026-08-10'
---
# Runtime AIOX

Label de maturidade que indica dependência do ambiente AIOX completo, como `.aiox-core` e SYNAPSE. No acervo educacional, uma skill Runtime não é automaticamente executável.

## Como é usado

Use **Runtime AIOX** como label de maturidade ao classificar uma skill no catálogo: significa que ela exige o ambiente AIOX completo (.aiox-core, SYNAPSE etc.) e não funciona sozinha em um harness qualquer.

**Exemplo prático:** na aula [[67-harness-ambiente-execucao]], confira a maturidade no `catalog.json` antes de copiar uma skill: Runtime exige dependências do ambiente; Portable pode ser transferida com o `cp`.

**Não confunda:** **Runtime AIOX** não é defeito nem versão inferior: é uma declaração honesta de dependência — o erro é copiar uma skill runtime para fora do ambiente e esperar que funcione.

**Frequência nos cursos:** **30** menções (AIOX Advanced: 5 · AIOX Advanced Squads: 25).

## Aulas

- [[67-harness-ambiente-execucao]]
- [[02-aiox-nao-e-ferramenta]]
- [[68-squad-fora-do-claude-code]]

## Ver também

- [[Maturidade]]
- [[Portable]]
- [[Harness]]
- [[Software House no Computador]]
- [[Glossário AIOX Advanced]]
