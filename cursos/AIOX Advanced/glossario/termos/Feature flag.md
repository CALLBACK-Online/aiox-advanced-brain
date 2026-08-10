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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# Feature flag

Chave de configuração que liga ou desliga uma capacidade em tempo de execução, separando a publicação do código da exposição da funcionalidade para usuários ou grupos.

## Como é usado

Use **Feature flag** para fazer dark launch, limitar acesso por allowlist, liberar uma mudança por etapas ou manter um kill switch. Defina dono, valor padrão seguro, público-alvo, métricas e data de remoção da flag.

**Exemplo prático:** o código do novo checkout é deployado em production com a flag `checkout_v2` desligada. O time a liga para usuários internos, observa erros e conversão, depois amplia para 10%, 50% e 100%; se o gate falhar, desliga a flag e registra a decisão.

**Não confunda:** **Feature flag** é o mecanismo de controle da funcionalidade; **Canary release** é a estratégia de expor uma versão a uma pequena parcela de tráfego, usuários ou instâncias. Uma flag pode implementar um canary, mas nem todo canary usa flag. Flag desligada também não substitui rollback quando há efeitos persistentes ou mudança incompatível.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[53-brownfield-enhancement]]
- [[48-quality-gate-completo]]
- [[61-wave-execute]]

## Ver também

- [[Canary release]]
- [[Rollback]]
- [[Deploy]]
- [[Quality Gate]]
- [[Production readiness]]
- [[Glossário AIOX Advanced]]
