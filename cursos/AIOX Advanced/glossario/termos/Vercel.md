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
  aiox_advanced: 39
  aiox_advanced_squads: 0
  total: 39
  counted_at: '2026-08-10'
---
# Vercel

Plataforma de hospedagem e deploy para aplicações web, com integração ao repositório, previews por mudança e ambiente de production. No curso, é o degrau verificável entre localhost e o acesso público.

## Como é usado

Use **Vercel** para publicar uma versão revisável da aplicação: conecte o repositório, gere uma preview para cada PR e promova para production apenas a versão que passou pelos checks e pelo smoke test.

**Exemplo prático:** um PR gera uma URL de preview na Vercel; o revisor confere o fluxo de login nessa URL, registra o smoke test e, após **PASS**, promove o commit aprovado para production.

**Não confunda:** **Vercel** hospeda e promove o artefato; não substitui banco, backend, CI/CD ou quality gate. Uma URL publicada prova deploy, não prova que a aplicação atende ao aceite.

**Frequência nos cursos:** **39** menções (AIOX Advanced: 39 · AIOX Advanced Squads: 0).

## Aulas

- [[71-vercel-deploy]]
- [[72-cicd-pipeline-completa]]
- [[73-prontidao-de-producao]]

## Ver também

- [[Deploy]]
- [[CI-CD]]
- [[Local Staging Production]]
- [[Glossário AIOX Advanced]]
