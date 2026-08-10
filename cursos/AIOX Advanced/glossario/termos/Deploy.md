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
  aiox_advanced: 238
  aiox_advanced_squads: 26
  total: 264
  counted_at: '2026-08-10'
---
# Deploy

Publicar o artefato no ambiente-alvo (staging/production) e verificar health, caminho crítico e evidência. Vem após o Quality Gate; pode preceder Done quando o valor precisa estar no ar.

## Como é usado

Use **Deploy** quando a mudança precisa sair do ambiente de desenvolvimento; publique, verifique o serviço e registre a prova do resultado real.

**Exemplo prático:** após o Quality Gate, publique em staging, abra a URL, rode o fluxo de login e o smoke test, registre o health e só promova para production se o gate permitir.

**Não confunda:** deploy não é merge, build local ou upload de arquivos; é colocar a versão no ambiente-alvo e provar que ela funciona ali.

**Frequência nos cursos:** **264** menções (AIOX Advanced: 238 · AIOX Advanced Squads: 26).

## Aulas

- [[71-vercel-deploy]]
- [[72-cicd-pipeline-completa]]
- [[73-prontidao-de-producao]]
- [[47-ciclo-de-vida-do-story]]

## Ver também

- [[CI-CD]]
- [[Vercel]]
- [[Smoke test]]
- [[Local Staging Production]]
- [[Done]]
- [[Glossário AIOX Advanced]]
