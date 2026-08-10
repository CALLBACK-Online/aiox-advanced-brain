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
  aiox_advanced: 373
  aiox_advanced_squads: 67
  total: 440
  counted_at: '2026-08-10'
---
# Agent

IA com persona genérica, para raciocínio aberto e linguagem.

## Como é usado

Use **Agent** para raciocínio aberto, síntese e linguagem quando ainda existe ambiguidade que não cabe em uma regra fixa. Na aula [[15-quatro-executores]], é um dos quatro executores (humano, agent, clone, worker): a task é a unidade; o agent é o executor escolhido quando ela exige julgamento contextual.

**Exemplo prático:** "resumir 40 entrevistas e extrair padrões" vai para um Agent; "renomear 200 arquivos por regex" vai para um worker. Quando o julgamento do Agent se torna repetível, ele desce a taxonomia e vira Task, Skill, Workflow ou Runner.

**Não confunda:** o Agent produz julgamento contextual; um Worker ou Runner executa passos mecânicos, baratos e confiáveis. Jogar toda task num agent por reflexo — "IA pra tudo" — é a dor que a aula nomeia.

**Frequência nos cursos:** **440** menções (AIOX Advanced: 373 · AIOX Advanced Squads: 67).

## Aulas

- [[15-quatro-executores]]

## Ver também

- [[Glossário AIOX Advanced]]
