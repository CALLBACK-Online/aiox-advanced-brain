# Changelog — deep-strategic-planning

> Histórico fora do SKILL.md por diretiva do founder (2026-07-06): "changelog ou
> referências não devem ir em lugares onde a LLM carrega — só gasta tokens".
> Body = contrato de runtime; história = este arquivo (AN_KE_173).

| Versão | Data | Mudança |
|--------|------|---------|
| 1.3.0 | 2026-07-06 | Codifica follow-up pós-QG: mini-debate adversarial para divergência ≥8 pontos, rollup por alternativa com dominância robusta, vereditos legítimos SPLIT/ESCALATED, predictions com `source` e `confidence` (calibração Brier na Phase 6), metodologia de scoring com agregação única + tie-break Σ bruto pré-cap (precedente da run de maio, "mesmo erro 2×") + pesos com ponto de aplicação definido, gate mecânico `scripts/validate-run.mjs` (fim do auto-atestado), e higiene: api_reference.md reescrito (squad fantasma `multi-lens-framework` removido), placeholder de assets deletado, skill registrada no skill-registry.yaml (estava em produção sem registro). Changelog extraído do SKILL.md para este arquivo. |
| 1.2.0 | 2026-07-06 | Heurísticas embutidas como MECANISMO (diretiva do founder: "aplicar, não catalogar"): Robustness Check com veto na seleção de O Um (position-over-prediction, P4), tabela card→mecanismo mapeando os 4 policy cards às estruturas do skill. |
| 1.1.0 | 2026-07-06 | Pós-mortem da run policy_runtime_future_proofing: Phase 0 (prior-art + learning log), Red Team de alternativas na Phase 1, modo --multi-vendor na Phase 3, pesos por tipo de decisão + honestidade de scores na Phase 4, Posição Antifrágil + predictions.yaml na Phase 5, Phase 6 (re-bench diferido), tiers quick/deep, modo --inline oficial, Protocolo de Resiliência (executor-agnóstico), paths {SKILL_DIR}, harness atual (sem TeamCreate/TeamDelete), frontmatter purity (agent removido). |
| 1.0.0 | — | Versão original (5 fases, 12 lentes, Teams). |
