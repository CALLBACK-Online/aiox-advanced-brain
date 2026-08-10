# Task: ETL Generate Artifacts

task_id: etl-generate-artifacts
```yaml
task:
  task_id: etl-generate-artifacts
  id: etl-generate-artifacts
  name: ETL Generate Artifacts (Layer 4)
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: false
  output_format: yaml
  workflow: etl-deep-pass-pipeline
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace/businesses/{slug}/
- squads/c-level/data/imersao-business-map.yaml
Output:
- evidence/generated-artifacts-summary.yaml
pre_condition:
- Bootstrap executado ou contexto do business carregado.
post_condition:
- Decisão ou artefato registrado com handoff explícito para a próxima etapa.
performance:
- Responder sem inventar dados e escalar bloqueios estruturais imediatamente.
Error Handling:
- Escalar blockers estruturais imediatamente e interromper a execução quando o input canônico estiver inconsistente.
Completion Criteria:
- [ ] Output produzido no caminho esperado.
- [ ] Critérios de completude registrados.

## Descricao

Layer 4 do deep pass pipeline. Cria todos os arquivos consumiveis pelos squads a partir dos dados enriquecidos nas Layers 1-3. Usa `workspace/businesses/thiago_nishikata/` como gold standard de referencia (40 arquivos, 5849 linhas). Gera artefatos de brand, product, narrative e movement.

## Prerequisites

- Layers 1-3 executadas com sucesso para o business.
- Dados enriquecidos disponiveis no workspace (`L0-identity/`, `L1-strategy/`, `L2-tactical/`, `L3-product/`).
- Gold standard disponivel: `workspace/businesses/thiago_nishikata/`.
- `completeness-manifest.yaml` com metricas atualizadas.

## Usage

```
*etl-generate-artifacts {slug}
```

**Reference:** `workspace/businesses/thiago_nishikata/` (gold standard — 40 files, 5849 lines)

## Execution Flow

### Fase 1: Gerar artefatos de brand

1. Ler dados consolidados de `L2-tactical/brand/brandbook.yaml`, `L2-tactical/brand/domain-decision.yaml` e design tokens da Layer 2.
2. Gerar ou atualizar `workspace/businesses/{slug}/L2-tactical/brand/brandbook.yaml`:
   - Archetype mix (inferido do posicionamento e voz).
   - Voice pillars (always_use, avoid_use, forbidden_words).
   - Visual identity (cores, fontes, Tailwind classes — de Layer 2).
   - Social proof (numeros verificados de Layer 3).
   - Brand pillars (extraidos do site ou inferidos).
3. Gerar ou atualizar `workspace/businesses/{slug}/L2-tactical/brand/domain-decision.yaml`:
   - Categoria, onlyness, diferenciacao (vs concorrentes).
   - Competitive moat, message hierarchy.
   - CEO/founder quotes verificadas (de Layer 3).
4. Usar gold standard como template de estrutura.

### Fase 2: Gerar artefatos de produto

1. Para cada produto identificado em `products_list`:
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/offerbook.yaml`:
     - Oferta estruturada: entregaveis, bonus, garantia, pricing.
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/proof.yaml`:
     - Resultados financeiros verificados, estatisticas com fonte e data.
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/testimonials.yaml`:
     - Depoimentos estruturados por categoria (consumer, partner, proof hooks).
2. Reestruturar: se o offerbook ainda estiver centralizado no shared layer, distribuir detalhes por produto em `L3-product/`.
3. Atualizar `workspace/businesses/{slug}/L1-strategy/offerbook.yaml` como indice compartilhado apontando para `L3-product/{product}/offerbook.yaml`.

### Fase 3: Gerar artefatos narrativos

1. Para cada produto:
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/narrative/brandscript.yaml`:
     - Estrutura SB7 (StoryBrand): character, problem (villain/external/internal/philosophical), guide, plan, CTA, success, failure, one-liner.
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/narrative/objection-destroyers.yaml`:
     - Top 8-10 objecoes com reframe, proof e source.
     - Extraidas do call de vendas (Layer 1) + UGC (Layer 3).
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/narrative/product-story.yaml`:
     - Origin story, proof, transformation, vision.
   - Gerar `workspace/businesses/{slug}/L3-product/{product}/narrative/pitch-narrative.yaml`:
     - Pitch estruturado de 30s, 2min e completo.
2. Fontes: dados do call de vendas (Layer 1), proof (Layer 3), testimonials (Layer 3).

### Fase 4: Gerar artefatos de movement

1. Avaliar maturidade do business: se early-stage demais, **SKIP** esta fase com justificativa documentada.
2. Se business maduro o suficiente, gerar:
   - `workspace/businesses/{slug}/L2-tactical/movement/system/cosmology.yaml` — central cause, trueline, axioms, worldview before/after.
   - `workspace/businesses/{slug}/L2-tactical/movement/foundation/tribe-identity.yaml` — archetypes, transformation arc, semantic clusters.
   - `workspace/businesses/{slug}/L2-tactical/movement/identity/leaders.yaml` — perfis de lideranca, top values, signature expressions.
   - `workspace/businesses/{slug}/L2-tactical/movement/system/mrd-bank/doctrines.yaml` — 8-12 crencas com evidencia.
   - `workspace/businesses/{slug}/L2-tactical/movement/system/mrd-bank/myths.yaml` — 8-12 mitos: origin, proof, community, antagonism.
   - `workspace/businesses/{slug}/L2-tactical/movement/system/mrd-bank/rites.yaml` — 10-15 rituais com identity arc.
   - `workspace/businesses/{slug}/L2-tactical/movement/system/mrd-bank/vocabulary.yaml` — 20-35 termos S/A/B/C.
   - `workspace/businesses/{slug}/L2-tactical/movement/reading/fenomenologia-cultural.yaml` — leitura cultural, worldview, core beliefs, narrative disputes.
3. Usar gold standard `thiago_nishikata/L2-tactical/movement/` como referencia de estrutura.

### Fase 5: Finalizar e reportar

1. Atualizar `workspace/businesses/{slug}/L4-operational/evidence/completeness-manifest.yaml`:
   - Completude por arquivo e por squad (Copy, Traffic, Design, Content, Movement).
   - Delta report: o que mudou desde a ultima execucao.
   - Squad readiness: quais squads podem operar com os dados atuais.
2. Atualizar `workspace/businesses/{slug}/L4-operational/evidence/source-registry.yaml`:
   - Registrar todos os artefatos gerados com timestamp.
3. Gerar resumo de execucao em `workspace/businesses/{slug}/L4-operational/evidence/etl-run-envelope.yaml`:
   - Total de arquivos gerados, linhas totais, comparacao com gold standard.

**Gate:** Completude geral >= 85%. Se abaixo, listar gaps e recomendar fontes adicionais.

## Acceptance Criteria

1. `L2-tactical/brand/brandbook.yaml` e `L2-tactical/brand/domain-decision.yaml` gerados.
2. Ao menos 1 produto com `offerbook.yaml`, `proof.yaml` e `testimonials.yaml`.
3. Artefatos narrativos gerados (brandscript, objection-destroyers) para ao menos 1 produto.
4. Movement gerado OU skip documentado com justificativa (business early-stage).
5. `L1-strategy/offerbook.yaml` atualizado como indice shared-to-product (quando aplicavel).
6. `completeness-manifest.yaml` atualizado com squad readiness e delta report.
7. Completude geral >= 85%.

## Outputs

| Tipo | Arquivos |
|------|----------|
| Brand | `L2-tactical/brand/brandbook.yaml`, `L2-tactical/brand/domain-decision.yaml` |
| Product | `L3-product/*/offerbook.yaml`, `proof.yaml`, `testimonials.yaml` |
| Narrative | `L3-product/*/narrative/brandscript.yaml`, `objection-destroyers.yaml`, `product-story.yaml`, `pitch-narrative.yaml` |
| Movement | `L2-tactical/movement/system/cosmology.yaml`, `L2-tactical/movement/foundation/tribe-identity.yaml`, `L2-tactical/movement/identity/leaders.yaml`, `L2-tactical/movement/system/mrd-bank/*.yaml`, `L2-tactical/movement/reading/fenomenologia-cultural.yaml` |
| Evidence | `L4-operational/evidence/completeness-manifest.yaml`, `L4-operational/evidence/source-registry.yaml`, `L4-operational/evidence/etl-run-envelope.yaml` |

## Referencia

Gold standard: `workspace/businesses/thiago_nishikata/` (40 files, 5849 lines).

---

*Task do Squad C-Level - COO Orchestrator*
