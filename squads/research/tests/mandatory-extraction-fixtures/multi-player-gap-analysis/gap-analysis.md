# Gap Analysis — Fixture: Comparing 3 Research Agents vs. Manus (anchor)

**Type:** standalone gap-analysis atomo (multi-player research)
**Date:** 2026-05-19
**Run:** fixture-multi-player-gap-analysis
**Comparison pattern:** multi_player
**Source:** 02-research-report.md §2

> Ver análise completa de pesquisa: [./02-research-report.md](./02-research-report.md)

---

## Sumário das Lacunas Estruturais

Total: 2 lacunas identificadas | Alta prioridade: 1 | Média: 1 | Baixa: 0

| # | Lacuna | Grau de risco | Oportunidade se corrigida | Concorrente com vantagem |
|---|--------|:-------------:|--------------------------|--------------------------|
| 1 | Ausência de API ergonômica para integração programática | HIGH | Expansão de casos de uso enterprise | Exa Research API |
| 2 | Sem cobertura de domínios com forte componente visual/JS | MED | Melhoria em extração de SPAs e sites dinâmicos | Perplexity (visual fallback limitado) |

*Grau de risco: HIGH / MED / LOW. Baseado em impacto competitivo × urgência.*

---

## Análise por Dimensão

### API Ergonomics

| Concorrente | O que ele tem que Manus não tem | Impacto |
|-------------|--------------------------------|:-------:|
| Exa Research API | SDK nativo + endpoint REST documentado + rate limits públicos | HIGH |
| Perplexity | API pública com docs, SDK Python e JS | MED |

**Lacuna estrutural:** Manus carece de API ergonômica para consumo programático — requer automação manual de UI ou acesso via parceiros.

---

### Extraction Coverage (SPA/JS-heavy)

| Concorrente | O que ele tem que outros não têm | Impacto |
|-------------|----------------------------------|:-------:|
| Manus | Navegação visual ativa como fallback explícito (2/2 sessões) | LOW (Manus LIDERA aqui) |

**Lacuna estrutural:** Nenhuma (Manus lidera esta dimensão).

---

## Roadmap de Maturidade (5 Estágios)

| Estágio | Nome | Critério de entrada | Lacunas endereçadas |
|:-------:|------|---------------------|---------------------|
| 1 | Clareza | Definir gaps API e documentar requisitos mínimos | G1 |
| 2 | Repetibilidade | Processo reproduzível de integração via parceiros | G1 |
| 3 | Mensuração | Métricas de adoção API (calls/dia, latência p95) | G1, G2 |
| 4 | Ensino | SDK interno documentado para time de produto | G1 |
| 5 | Escala | API pública com SLA e roadmap público | G1 |

**Posição atual estimada de Manus:** Estágio 1 — API ainda não exposta publicamente; extração visual é diferencial, não lacuna.

---

## Riscos se as Lacunas Não Forem Corrigidas

| Risco | Horizonte | Probabilidade | Impacto | Mitigação imediata |
|-------|-----------|:-------------:|:-------:|-------------------|
| Perda de clientes enterprise para Exa (melhor integração programática) | 12 meses | MEDIA | ALTO | Lançar SDK beta fechado para early-adopters |
| Bloqueio em pipelines automatizados que requerem REST | 6 meses | ALTA | ALTO | Wrapper CLI intermediário como ponte |

---

## Ações Recomendadas (P0 e P1)

| # | Ação | Fecha lacuna | Impacto esperado | Prioridade |
|---|------|-------------|-----------------|:----------:|
| 1 | Lançar REST API pública (v1 minimal) com auth + rate limit | G1 | Adoção enterprise +40% | P0 |
| 2 | Documentar wrapper CLI público para automação sem SDK | G1 | Reduce churn em pipelines existentes | P1 |

---

## Metodologia

- **Identificação:** Baseada em matrices.yaml e análise de cobertura por dimensão
- **Grau de risco:** Impacto × Urgência (HIGH: impacto competitivo imediato; MED: vantagem crescente; LOW: nicho)
- **Roadmap de maturidade:** Baseado em modelo Clareza → Repetibilidade → Mensuração → Ensino → Escala
- **Confiança:** MEDIA — baseado em análise interpretiva single-pass de 3 candidates

---

_Gerado por tech-research Phase 5.0 | Template: gap-analysis-tmpl.md v1.0.0_
_Atomo separado de 02-research-report.md — NÃO embutido em §Caveats_
_Lacunas estruturais comparativas vs. concorrentes (para caveats analíticos, ver 02-research-report.md §Caveats)_
