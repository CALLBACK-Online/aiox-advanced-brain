# Task: Multi-Project Comparison & Architecture Synthesis

> Workflow orchestrator task for wf-multi-compare.yaml

**Task ID:** multi-compare
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Comparar múltiplos projetos extraídos contra o baseline AllFluence, resolver conflitos e gerar proposta arquitetural unificada
**Orchestrator:** @decoder-chief
**Workflow:** wf-multi-compare.yaml
**Phase:** M2-Analyze (extended)
**Tier:** 2

---

## Inputs

```yaml
required:
  - name: "groups"
    description: "Grupos de comparação (módulos AllFluence → referências)"
    example:
      - group_id: G1
        name: "Cloud Agents"
        target_modules: ["apps/clickup-engine", "apps/worker", "services/*"]
        references: ["n8n", "dify"]
        dimensions: ["architecture", "dependencies", "api"]
        objective: "Worker architecture, queue processing, webhook handling"
optional:
  - name: "max_effort"
    description: "Esforço máximo por adoção individual"
    default: "L"
    valid_values: ["S", "M", "L", "XL"]
  - name: "priority_order"
    description: "Ordem de prioridade entre grupos para resolução de conflitos"
    default: "order of definition"
```

---

## Elicitation (elicit: true)

Before executing, gather from the user:

1. **Quais grupos de comparação?** (módulos AllFluence → referências por grupo)
2. **Objetivo de cada grupo?** (feature inspiration, refactor guidance, pattern adoption)
3. **Prioridade entre grupos?** (para resolução de conflitos inter-grupo)
4. **Constraint de esforço?** (S/M/L/XL máximo por adoção individual)
5. **Baseline atualizado?** (outputs/decoded/allfluence/ < 90 dias?)

---

## Steps

### Step 1: Validate All Baselines

```bash
# Check baseline
ls outputs/decoded/allfluence/phase-0-scoping/
# Check each reference
for slug in {all_references}; do
  ls outputs/decoded/$slug/phase-0-scoping/ 2>/dev/null || echo "MISSING: $slug"
done
```

**VETO:** Se baseline AllFluence não existe → HALT com "Run *extract-full allfluence first"
**WARN:** Se referência falta → excluir do grupo com aviso

### Step 2: Execute Parallel Comparisons

Para cada grupo, para cada referência:
1. Chamar task `compare.md` com (allfluence, {reference}, {dimensions})
2. Coletar delta-report em `outputs/decoded/allfluence/comparisons/{slug}/`

**Execução paralela por grupo** — todos os compares de G1 podem rodar junto com G2.

### Step 3: Consolidate per Group

Para cada grupo:
1. Ler todos delta-reports das referências do grupo
2. Agrupar deltas por módulo AllFluence alvo
3. Identificar **convergências** (2+ referências → mesmo padrão)
4. Identificar **divergências** (referências conflitam)
5. Identificar **únicos** (apenas 1 referência)
6. Rankear por impacto × esforço
7. Gerar `group-report.yaml` usando template

### Step 4: Resolve Conflicts

Para cada divergência (intra-grupo e inter-grupo):
1. Listar abordagens concorrentes com prós/cons
2. Aplicar ATAM trade-off analysis:
   - Quality attributes afetados
   - Sensibilidade de cada abordagem
   - Compatibilidade com stack AllFluence
3. Considerar constraint de esforço do usuário
4. Decidir: abordagem A, B, ou híbrido
5. Registrar decisão + justificativa

**ESCALATE para humano se:**
- Conflito envolve segurança (auth, RLS, permissions)
- Conflito causa breaking change em 3+ módulos
- Trade-off é genuinamente 50/50

### Step 5: Generate Unified Proposal

1. Consolidar todas convergências aprovadas + conflitos resolvidos
2. Gerar C4 Container BEFORE (do phase-3-fusion do allfluence)
3. Gerar C4 Container AFTER (com adoções aplicadas)
4. Para cada módulo afetado: C4 Component before/after
5. Priorizar adoções em waves (dependências respeitadas)
6. Estimar esforço total + roadmap
7. Gerar ADR drafts para decisões significativas
8. Gerar story candidates no formato @po

### Step 6: Generate Handoff

1. Gerar unified-proposal.yaml usando template
2. Gerar handoff inter-BU para @architect
3. Apresentar resumo executivo ao usuário
4. **HALT** para signoff humano no G-SYNTHESIS gate

---

## Output

```yaml
output:
  primary: "outputs/decoded/allfluence/multi-compare/unified-proposal.yaml"
  secondary:
    - "outputs/decoded/allfluence/multi-compare/{group_id}/group-report.yaml"  # per group
    - "outputs/decoded/allfluence/multi-compare/conflict-resolution.yaml"
    - "outputs/decoded/allfluence/multi-compare/handoff-to-architect.yaml"
  templates:
    - "templates/group-report-tmpl.yaml"
    - "templates/unified-proposal-tmpl.yaml"
    - "templates/adoption-proposal-tmpl.yaml"
  artifact_contract: "unified-proposal"
  lifecycle_state: draft
```

---

## Veto Conditions

1. **No baseline:** AllFluence extraction não existe → HALT
2. **Baseline stale > 180 dias:** Dados muito antigos → HALT, re-extract
3. **< 2 referências por grupo:** Sem convergência possível → WARN (reduz confiança)
4. **Conflict involves security:** Auth/RLS/permissions → ESCALATE humano obrigatório
5. **Breaking change 3+ modules:** Risco alto → ESCALATE humano obrigatório
6. **Total effort > XL:** Proposta muito grande → recomendar split em fases

---

## Completion Criteria

- [ ] Todos delta-reports gerados (1 por referência)
- [ ] Todos group-reports gerados (1 por grupo)
- [ ] Conflitos resolvidos ou escalados
- [ ] C4 before/after gerados
- [ ] Unified proposal com roadmap em waves
- [ ] Story candidates derivados
- [ ] ADR drafts para decisões significativas
- [ ] Handoff inter-BU com signoff template
- [ ] Resumo executivo apresentado ao usuário

---

## Handoff

| Para | Quando | Artifact | Scope |
|------|--------|----------|-------|
| **Pedro Valério** | Proposal ready | unified-proposal.yaml | HUMAN SIGNOFF (G-SYNTHESIS) |
| **@architect** | Após signoff humano | unified-proposal + handoff | inter_bu |
| **@pm** | Após @architect approve | story candidates + ADRs | intra_bu |
