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
  aiox_advanced: 2
  aiox_advanced_squads: 0
  total: 2
  counted_at: '2026-08-10'
---
# Reality-First

Princípio de validar o valor no ambiente em que a solução será usada, com smoke test, health check e comportamento observável — não apenas com “build passou”.

## Como é usado

Use **Reality-First** no gate final ou de prontidão para exigir evidência do fluxo funcionando no ambiente-alvo, com dados representativos e sinais que outra pessoa consiga conferir.

**Exemplo prático:** depois de o build passar, publique em staging, abra a aplicação, complete o fluxo principal com dados representativos, confira health e logs e registre o resultado antes de declarar a Story pronta.

**Não confunda:** **Reality-First** não significa testar somente em produção, mas também não aceita build verde ou “funciona localmente” como prova suficiente do uso real.

**Frequência nos cursos:** **2** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 0).

## Aulas

- [[73-prontidao-de-producao]]
- [[71-vercel-deploy]]
- [[74-caso-integrado-end-to-end]]

## Ver também

- [[Smoke test]]
- [[Evidência]]
- [[Deploy]]
- [[Done]]
- [[Glossário AIOX Advanced]]
