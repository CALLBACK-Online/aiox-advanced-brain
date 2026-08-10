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
  aiox_advanced: 41
  aiox_advanced_squads: 2
  total: 43
  counted_at: '2026-08-10'
---
# Rollback

Retorno controlado de um serviço, artefato ou configuração para uma versão conhecida como boa quando a mudança atual causa falha ou risco inaceitável. É um caminho planejado, não uma reação improvisada.

## Como é usado

Use **Rollback** quando um critério de abortar for atingido: pare a promoção, selecione a versão anterior ou desative a mudança, execute o caminho documentado e repita health check e smoke test para provar a recuperação.

**Exemplo prático:** a versão `v1.8.1` aumenta os erros no login depois do deploy. O operador interrompe a promoção, faz redeploy de `v1.8.0`, verifica o health check, percorre o login no smoke test e registra horário, versão e evidência do retorno.

**Não confunda:** **Rollback** desfaz uma mudança de aplicação ou configuração; **Release** identifica uma entrega versionada e **Deploy** publica um artefato em um ambiente. Se dados foram corrompidos, rollback do código pode não bastar: pode ser necessário [[Backup restore]].

**Frequência nos cursos:** **43** menções (AIOX Advanced: 41 · AIOX Advanced Squads: 2).

## Aulas

- [[71-vercel-deploy]]
- [[72-cicd-pipeline-completa]]
- [[73-prontidao-de-producao]]
- [[05-ambientes-local-staging-production]]

## Ver também

- [[Deploy]]
- [[Release]]
- [[Backup restore]]
- [[Smoke test]]
- [[Health check]]
- [[Glossário AIOX Advanced]]
