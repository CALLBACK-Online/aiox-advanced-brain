# Session Heuristics Extraction — Quality Gate Checklist

> **Process:** SP-EXTRACT-SESSION-HEURISTICS
> **Version:** 4.1.0-gah-calibrate
> **Owner:** {owner_handle} (resolved at runtime)
> **Mode:** VALIDAR

---

## Phase 1: IDENTIFY — Varredura

- [ ] Sessão teve profundidade suficiente (≥ 5 candidatas brutas) [TKN-ESH-THR-002]
- [ ] As 5 categorias foram varridas:
  - [ ] Decisões pivot
  - [ ] Bugs/incidentes
  - [ ] Anti-patterns evitados
  - [ ] Patterns validados
  - [ ] Research insights
- [ ] Perguntas-guia CDM aplicadas (Critical Decision Method)
- [ ] Cada candidata tem pelo menos 1 frase de contexto

## Phase 1.5: GAH — Gate de Admissibilidade Heurística

- [ ] Para CADA candidata bruta, audit YAML gerado em `outputs/minds/gah-audits/{owner_slug}/`
- [ ] Test 1 (Vocabulary Strip) executado: `stack_specific_terms` listado + `rewritten_rule` produzido + `coherent/preserved/locked` decidido
- [ ] Test 2 (Cross-Domain) executado: 8 domínios avaliados + `literal_matches` contado
- [ ] Test 3 (Other-Human) executado: `stripped_version` + `utility_score` + `applicable_to_my_work` + `example_coherence` decidido
- [ ] Test 4 (Anti-Test) executado: `anti_rule` gerado + `anti_context_exists` decidido + `tension_axis` nomeado se yes
- [ ] Aggregate verdict (ADMIT / ADMIT_WITH_REWRITE_LIGHT / REWRITE_REQUIRED / REJECT) calculado
- [ ] Para REJECT, `destination_if_reject` classificado (pipeline_instance / task / checklist / rule / archive)
- [ ] Mode v1 FLAG: audits salvos, candidatas seguem TODAS para Phase 2 (operador revisa antes de Phase 5)

## Phase 2: FILTER — Pareto ao Cubo

- [ ] Classificação por zona aplicada (🔥 / 💎 / 🚀 / 💩)
- [ ] Ratio genérico ≤ 30% [TKN-ESH-THR-003]
- [ ] Teste de genericidade aplicado ("funciona sem contexto? → 💩")
- [ ] Candidatas 💩 descartadas com justificativa

## Phase 3: OVERLAP — Dedup

- [ ] Heurísticas existentes consultadas (`minds/{owner_slug}/heuristics/decision-cards.yaml`)
- [ ] Zero duplicatas criadas (overlap → update, não create) [TKN-ESH-BEH-001]
- [ ] Triangulação verificada (3+ sessões → promote zone) [TKN-ESH-BEH-002]

## Phase 4: FORMALIZE — Arquivos

- [ ] 100% das heurísticas têm [SOURCE:] rastreável [TKN-ESH-THR-001]
- [ ] Zero [INFERRED] sem evidência empírica
- [ ] Tipo válido usado [TKN-ESH-TAX-001]:
  - Decision | Veto | Architecture | Observability | State Management
- [ ] Formato padrão seguido:
  - [ ] Header (Type, Zone, Owner, Pattern, Source)
  - [ ] Purpose (1 frase)
  - [ ] Configuration YAML (name, zone, trigger, rule, evidence)
  - [ ] Decision Tree (IF/THEN/ELSE)
- [ ] Numeração contínua (sem gaps, sem sobreposição)
- [ ] anti_pattern documentado em cada heurística

## Phase 5: PERSIST — Commit

- [ ] MEMORY.md atualizado com referência (se aplicável ao projeto)
- [ ] Commit com mensagem padronizada: `feat(minds): add {PREFIX}_NNN-NNN ...`
- [ ] Push executado (se branch ativa)

## Phase 5.5: CALIBRATE — GAH Verdict vs Operator Decision

- [ ] Para CADA candidata bruta de Phase 1, 1 linha JSON appended em `outputs/minds/gah-audits/{owner_slug}/calibration.jsonl`
- [ ] `matches` calculado conforme tabela GAH verdict × operator_decision (SKILL.md Phase 5.5)
- [ ] `audit_path` aponta para o YAML existente (não criar log órfão sem audit)
- [ ] Promotion check executado: agrupado por `session` DISTINCT, last 3 sessions com ≥5 candidatas avaliadas
- [ ] Status emitido (calibration progress OU GAH PROMOTION CANDIDATE quando 3/3 sessions ≥ 0.80)

---

## Gate Decision

| Score | Verdict |
|-------|---------|
| 27+ checks / 31 | **PASS** — extração aprovada |
| 22-26 / 31 | **WARN** — revisar items faltantes |
| < 22 / 31 | **FAIL** — re-executar fases fracas |

**Mínimo hard:** Phase 4 items 1-2 (source traceability) são BLOCKER. Se qualquer um falha, extração inteira falha.

**Phase 1.5 (GAH) v1 FLAG:** GAH é advisory na primeira release — verdicts não bloqueiam, mas a checklist exige que TODOS os 4 testes sejam executados e o audit YAML seja gerado. Skip de testes é WARN.
