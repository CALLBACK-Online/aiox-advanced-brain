# Copy Brief Protocol — Mandatory Pre-Write Loading

> **Versão:** 1.0  
> **Guardian:** Copy Chief  
> **Regra:** nenhuma copy sobe para `FINAL` sem carregar o brief real do Hub.  
> **Violação:** copy sem brief completo é `DRAFT`.

---

## Princípio

O `copy-chief` não inventa dados. Ele extrai de fontes canônicas do
`docs/` e da camada opcional de campanha em
`docs/operational/campaigns/{campaign_slug}/` (ADR-012).

Se `campaign-brief.yaml` existir, ele governa a camada de campanha.
Se não existir, o protocolo pode montar apenas um brief implícito para:

1. diagnóstico
2. exploração
3. peça simples em modo `DRAFT`

Para trabalho estratégico, multi-asset, high-ticket ou qualquer entrega
`FINAL`, o `campaign_slug` precisa existir e o `Campaign Brief` precisa estar
persistido.

---

## Camada 1: Business + Brand Truth

Estes arquivos definem quem somos e como falamos.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 1 | `{business}/strategy/icp.yaml` | ICP, dores, desejos, gatilhos, objeções | **SIM** |
| 2 | `{business}/strategy/offerbook.yaml` | índice/shared offer truth | **SIM** |
| 3 | `{business}/strategy/pricing-strategy.yaml` | preço, tiers, ROI, ancoragem | Recomendado |
| 4 | `{business}/tactical/brand/brandbook.yaml` | voice DNA, forbidden words, promessa, onlyness, signature phrases | **SIM** |
| 5 | `{business}/tactical/brand/strategic-positioning.yaml` | posicionamento, categoria, contraste competitivo | Recomendado |
| 6 | `{business}/identity/founder-dna.yaml` | origem, filosofia e linguagem do fundador | Recomendado |
| 7 | `{business}/tactical/movement/` | narrativa identitária, crenças, vocabulário, objeções culturais | Quando aplicável |

**Path base:** `docs/`

---

## Camada 2: Product Truth

Estes arquivos definem o que estamos vendendo.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 8 | `{business}/L3-product/{product}/offerbook.yaml` | oferta completa, value stack, mecanismo, garantia | **SIM** |
| 9 | `{business}/L3-product/{product}/proof.yaml` | resultados, estudos de caso, prova agregada | **SIM** |
| 10 | `{business}/L3-product/{product}/testimonials.yaml` | depoimentos por tier, destruição de objeções | **SIM** |
| 11 | `{business}/L3-product/{product}/curriculum.yaml` | estrutura, módulos, entregáveis, promessa verificável | Recomendado; **SIM** para educacional |
| 12 | `{business}/L3-product/{product}/sales-process.yaml` | trigger comercial, etapas do funil, handoff | Quando existir |
| 13 | `{business}/L3-product/{product}/narrative/*` | product story, pitch narrative, brandscript, objection destroyers | Recomendado |

---

## Camada 3: Campaign Truth

Estes arquivos definem o recorte da campanha.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 14 | `docs/operational/campaigns/{campaign_slug}/campaign-brief.yaml` | objetivo, audiência, canais, constraints, success criteria | **SIM** para estratégico/high-ticket/FINAL |
| 15 | `docs/operational/campaigns/{campaign_slug}/message-architecture.yaml` | lógica de mensagem, promessa, mecanismo, prova | Recomendado; **SIM** para multi-asset/high-ticket |
| 16 | `docs/operational/campaigns/{campaign_slug}/copy/creative-brief.yaml` | ângulo, tom emocional, CTA, territórios criativos | Recomendado |
| 17 | `docs/operational/campaigns/{campaign_slug}/copy/assets/*.yaml` | briefing por deliverable | Quando existir |

---

## Fonte Da Verdade Por Estágio

| Estágio | Artefato primário | Fonte da verdade |
|---|---|---|
| Intake | `Campaign Brief` | `docs/operational/campaigns/{campaign_slug}/campaign-brief.yaml` |
| Brand/Product loading | `Business + Product truth` | `strategy`, `tactical/brand`, `L3-product/{product}` |
| Message Strategy | `Message Architecture` | `docs/operational/campaigns/{campaign_slug}/message-architecture.yaml` |
| Creative Direction | `Creative Brief` | `docs/operational/campaigns/{campaign_slug}/copy/creative-brief.yaml` |
| Asset Planning | `Asset Briefs` | `docs/operational/campaigns/{campaign_slug}/copy/assets/*.yaml` |
| Delivery | `Copy Deck / output final` | `outputs/copy/{business}/...` |
| Review | checklists + truth upstream | `squads/copy/checklists/` + fontes carregadas |

---

## Checklist Pré-Escrita

```text
BRIEF COMPLETO?
├── [ ] ICP carregado
├── [ ] Brandbook carregado
├── [ ] Offerbook do produto carregado
├── [ ] Proof carregado
├── [ ] Testimonials carregados
├── [ ] Pricing carregado quando existir
├── [ ] Curriculum carregado quando aplicável
├── [ ] Campaign Brief carregado quando o trabalho for estratégico ou FINAL
└── [ ] Message Architecture carregada quando a campanha exigir adaptação explícita
```

## Validação Pós-Escrita

- forbidden words revisadas
- promessa coerente com o positioning
- números e claims com fonte
- pelo menos uma camada real de prova
- dores e desejos do ICP refletidos na peça
- `premium-positioning-guardrails.md` aplicado
- `final-copy-readiness.md` aplicado

---

## Exemplo de Uso

**Pedido:** “Quero reescrever a sales page do `cohort_advanced`.”

**Carregar nesta ordem:**

1. `docs/strategy/icp.yaml`
2. `docs/tactical/brand/brandbook.yaml`
3. `docs/execution/{product}/offerbook.yaml`
4. `docs/execution/{product}/proof.yaml`
5. `docs/execution/{product}/testimonials.yaml`
6. `docs/execution/{product}/curriculum.yaml` se aplicável
7. `docs/operational/campaigns/{campaign_slug}/campaign-brief.yaml` se existir
8. `docs/operational/campaigns/{campaign_slug}/message-architecture.yaml` se existir

**Status operacional:**

- sem `campaign_slug` persistido: `DRAFT`
- com `campaign_slug` + `campaign-brief.yaml`: elegível para `FINAL` após review gates

---

## Regra Final

- Business truth vive em `strategy` e `tactical`
- Product truth vive em `L3-product/{product}`
- Campaign truth vive em `operational/campaigns/{campaign_slug}` (ADR-012)
- Delivery truth vive em `outputs/copy/{business}`

Sem essa separação, a copy perde rastreabilidade.
