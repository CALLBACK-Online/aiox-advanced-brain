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
  aiox_advanced: 40
  aiox_advanced_squads: 0
  total: 40
  counted_at: '2026-08-10'
---
# Apply QA Fixes

Loop de remediação que devolve findings ao Dev na mesma Story/PR, preserva aceite, branch e evidência e repete o gate até PASS ou até uma decisão explícita de parar.

## Como é usado

Depois de um FAIL, classifique o finding como block, major, nit ou outra Story. Para o que cabe na Story atual, aplique o patch no mesmo PR, registre o delta e rode o Quality Gate novamente.

**Exemplo prático:** um teste do fallback de onboarding falha; QA marca o blocker, o Dev corrige o mesmo PR, atualiza o log ou screenshot da evidência e o gate é reexecutado antes do merge.

**Não confunda:** **Apply QA Fixes** não é abrir um ticket solto nem autoaprovar a própria correção. Se o finding não cabe no aceite, faça split ou crie outra Story e registre essa decisão.

**Frequência nos cursos:** **40** menções (AIOX Advanced: 40 · AIOX Advanced Squads: 0).

## Aulas

- [[48-quality-gate-completo]]
- [[49-apply-qa-fixes-loop]]

## Ver também

- [[Glossário AIOX Advanced]]
