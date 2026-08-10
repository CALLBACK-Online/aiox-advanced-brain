# Gap Analysis — {subject} vs. {comparison_set}

**Type:** standalone gap-analysis atomo (multi-player research)
**Date:** {DATE}
**Run:** {RESEARCH_SLUG}
**Comparison pattern:** multi_player
**Source:** 02-research-report.md §{SECTION_REF}

> Ver análise completa de pesquisa: [./02-research-report.md](./02-research-report.md)

---

## Sumário das Lacunas Estruturais

Total: {N} lacunas identificadas | Alta prioridade: {HIGH_COUNT} | Média: {MED_COUNT} | Baixa: {LOW_COUNT}

| # | Lacuna | Grau de risco | Oportunidade se corrigida | Concorrente com vantagem |
|---|--------|:-------------:|--------------------------|--------------------------|
| 1 | {GAP_TITLE_1} | {RISK_LEVEL} | {OPPORTUNITY_1} | {COMPETITOR_1} |
| 2 | {GAP_TITLE_2} | {RISK_LEVEL} | {OPPORTUNITY_2} | {COMPETITOR_2} |
| N | {GAP_TITLE_N} | {RISK_LEVEL} | {OPPORTUNITY_N} | {COMPETITOR_N} |

*Grau de risco: HIGH / MED / LOW. Baseado em impacto competitivo × urgência.*

---

## Análise por Dimensão

*Para cada dimensão avaliada, identifica lacunas exclusivas do subject.*

### {DIMENSION_1}

| Concorrente | O que ele tem que {subject} não tem | Impacto |
|-------------|-------------------------------------|:-------:|
| {COMPETITOR_A} | {SPECIFIC_CAPABILITY_A} | {IMPACT} |
| {COMPETITOR_B} | {SPECIFIC_CAPABILITY_B} | {IMPACT} |

**Lacuna estrutural:** {DESCRIPTION_OF_ROOT_GAP}

---

### {DIMENSION_2}

| Concorrente | O que ele tem que {subject} não tem | Impacto |
|-------------|-------------------------------------|:-------:|
| {COMPETITOR_A} | {SPECIFIC_CAPABILITY_A} | {IMPACT} |

**Lacuna estrutural:** {DESCRIPTION_OF_ROOT_GAP}

---

*[Repetir para cada dimensão com lacunas identificadas]*

---

## Roadmap de Maturidade (5 Estágios)

*Progressão do subject em direção a eliminar as lacunas identificadas.*

| Estágio | Nome | Critério de entrada | Lacunas endereçadas |
|:-------:|------|---------------------|---------------------|
| 1 | Clareza | Definir e documentar gaps | {GAP_IDS_STAGE_1} |
| 2 | Repetibilidade | Processo reproduzível para mitigação | {GAP_IDS_STAGE_2} |
| 3 | Mensuração | Métricas de progresso definidas e medidas | {GAP_IDS_STAGE_3} |
| 4 | Ensino | Capacidade transferível para o time | {GAP_IDS_STAGE_4} |
| 5 | Escala | Solução sistêmica, não pontual | {GAP_IDS_STAGE_5} |

**Posição atual estimada de {subject}:** Estágio {CURRENT_STAGE} — {STAGE_RATIONALE}

---

## Riscos se as Lacunas Não Forem Corrigidas

| Risco | Horizonte | Probabilidade | Impacto | Mitigação imediata |
|-------|-----------|:-------------:|:-------:|-------------------|
| {RISK_1} | {TIMEFRAME} | {PROB} | {IMPACT} | {MITIGATION} |
| {RISK_2} | {TIMEFRAME} | {PROB} | {IMPACT} | {MITIGATION} |

---

## Ações Recomendadas (P0 e P1)

| # | Ação | Fecha lacuna | Impacto esperado | Prioridade |
|---|------|-------------|-----------------|:----------:|
| 1 | {ACTION_1} | {GAP_ID} | {EXPECTED_IMPROVEMENT} | P0 |
| 2 | {ACTION_2} | {GAP_ID} | {EXPECTED_IMPROVEMENT} | P1 |

---

## Metodologia

- **Identificação:** Baseada em comparison-matrix.json e análise de cobertura por dimensão
- **Grau de risco:** Impacto × Urgência (HIGH: impacto competitivo imediato; MED: vantagem crescente; LOW: nicho ou tendência)
- **Roadmap de maturidade:** Baseado em modelo Clareza → Repetibilidade → Mensuração → Ensino → Escala (operacional-to-institucional)
- **Confiança:** {CONFIDENCE_LEVEL} — baseado em {EVIDENCE_BASIS}

---

_Gerado por tech-research Phase 5.0 / research-bench Phase síntese | Template: gap-analysis-tmpl.md v1.0.0_
_Atomo separado de 02-research-report.md — NÃO embutido em §Caveats_
_Lacunas estruturais comparativas vs. concorrentes (para caveats analíticos, ver 02-research-report.md §Caveats)_
