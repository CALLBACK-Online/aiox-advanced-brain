# 7 Princípios Invioláveis (P1-P7) — Referência

> **SoT:** `squads/slides-creator/data/principios-invioláveis.md` (canonical).
> Este arquivo é uma síntese para uso offline da skill quando o monorepo do squad não está disponível. Mudanças canônicas DEVEM ser feitas no squad.

Os 7 invariantes governam toda emissão de slide e são enforced em 3 layers (code / schema / validator). Violação é QA FAIL automático — não negociável.

---

## P1 — Fidelidade aos dados

**Regra:** Qualquer número, citação, fato ou claim mostrado em slide DEVE ser rastreável a uma fonte (`source_ref`) no evidence ledger.

**Enforcement:** `code` (validate-evidence-ledger Worker).
**Failure mode:** "Número/citação não rastreável à fonte = QA FAIL".
**Killer item ligado:** KI-03 (claim crítico sem fonte APA-complete) + KI-11 (Evidence Ledger verdict FAIL).
**Anti-pattern:** Inventar percentuais "típicos" para preencher slide. Sempre cite ou marque `[TODO: cite]`.

---

## P2 — Especificação obsessiva

**Regra:** Toda SlideSpec emitida DEVE conter hex colors explícitos, grid_coord para cada elemento posicionado, e pt_size para cada bloco tipográfico.

**Enforcement:** `schema` (slide-spec-schema.yaml).
**Failure mode:** "SlideSpec sem hex/grid_coord/pt_size = schema validation FAIL".
**Anti-pattern:** "primary color from theme" sem o hex resolvido. Sempre resolve antes de emitir.

---

## P3 — Pyramid Principle + MECE

**Regra:** Cada deck DEVE seguir Minto Pyramid (governing thought topo → 3-5 supporting → details) com MECE em cada nível (Mutually Exclusive, Collectively Exhaustive).

**Enforcement:** `validator` (validate-pyramid + run-vertical-test).
**Failure mode:** "Vertical test falha OU MECE violado = QA FAIL".
**Killer items ligados:** KI-08 (slide sem função narrativa), KI-09 (slide count > 2x slide-function-map).
**Anti-pattern:** Outline literal copy → deck (cada bullet vira slide). Pyramid exige compressão narrativa.

---

## P4 — Action Titles obrigatórios

**Regra:** Todo título de slide DEVE ser uma **proposição completa que move o argumento adiante** ("Receita cresceu 32% YoY impulsionada por enterprise"), nunca um tópico descritivo ("Análise de receita").

**Enforcement:** `validator` (validate-action-title + validate-action-title-rhetoric).
**Failure mode:** "Título descritivo (ex: 'Análise de market share') = QA FAIL".
**Killer item ligado:** KI-07 (action title classificado como descriptive_violation).
**Anti-pattern:** Títulos categoriais ("Mercado", "Resultados", "Próximos passos"). Force verbos+predicados.

---

## P5 — Enumeração universal

**Regra:** Todo visual (gráfico, tabela, figura, imagem) DEVE ter ID único enumerado (Gráfico 1, Tabela 2.3, Figura 4-A) referenciável no body text e na lista de exhibits.

**Enforcement:** `validator` (validate-enumeration-universal).
**Failure mode:** "Qualquer visual sem ID = QA FAIL".
**Anti-pattern:** "Como mostra o gráfico acima" sem ID resolvível. Use sempre "Gráfico N".

---

## P6 — Citação completa APA

**Regra:** Toda citação DEVE conter os 5 campos canônicos: `{org, title, date, url, access_date}`. APA business style, não APA acadêmico estrito.

**Enforcement:** `schema` (sources-apa.schema.yaml).
**Failure mode:** "Citação sem {org, title, date, url, access_date} = schema FAIL".
**Killer item ligado:** KI-03.
**Anti-pattern:** "(McKinsey, 2023)" sem URL nem access_date. Sempre os 5 campos.

---

## P7 — Prompts IA completos (10 componentes)

**Regra:** Toda invocação de LLM dentro do pipeline DEVE compor prompt com 10 componentes canônicos: `{role, context, task, audience, constraints, format, examples, evaluation_criteria, escape_hatch, success_check}`.

**Enforcement:** `schema` (ai-prompts.schema.yaml).
**Failure mode:** "Prompt IA com <10 componentes = schema FAIL".
**Anti-pattern:** Prompt curto sem evaluation_criteria nem escape_hatch. Use o template completo.

---

## Resumo enforcement

| Princípio | Layer | Killer Items | Validator(s) |
|-----------|-------|--------------|--------------|
| P1 | code | KI-03, KI-11 | validate-evidence-ledger |
| P2 | schema | — | slide-spec-schema.yaml |
| P3 | validator | KI-08, KI-09 | validate-pyramid, run-vertical-test |
| P4 | validator | KI-07 | validate-action-title, validate-action-title-rhetoric |
| P5 | validator | — | validate-enumeration-universal |
| P6 | schema | KI-03 | sources-apa.schema.yaml + validate-fontes-apa |
| P7 | schema | — | ai-prompts.schema.yaml |

## Como a skill aplica

A skill workflow (Quick Workflow no SKILL.md) respeita estes invariantes em:

- **Phase 4 (slide-function-map):** P3 + P4 enforced (cada slide function = action_title + audience_movement).
- **Phase 5 (canonical templates):** P5 enforced (visual enumeration via template-selection-guide).
- **Phase 7 (design direction):** P2 enforced (hex resolution, density limits, type scale).
- **Phase 8 (deck spec):** P1 + P5 + P6 enforced (evidence_ref per claim, visual IDs, APA citations).
- **Phase 10 (critique):** All P1-P7 re-verified before delivery.
- **Phase 11 (package):** QA report MUST include compliance line per P1-P7.

## Resync

Sempre que a versão canônica em `squads/slides-creator/data/principios-invioláveis.md` for atualizada (revisão de invariantes pelo slide-chief), este arquivo DEVE ser ressincronizado. Última sync: 2026-05-20.
