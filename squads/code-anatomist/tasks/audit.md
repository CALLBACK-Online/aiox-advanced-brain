# Task: Self-Audit

> Molecule M2-Analyze — Self-analysis usando baseline extraction

**Task ID:** audit
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Sonnet
**Purpose:** Analisar a auto-extração do AllFluence (outputs/decoded/allfluence/) para detectar drift, inconsistências e gaps comparando contra o código real atual
**Orchestrator:** @decoder-chief
**Primary Agent:** @gail-murphy (Reflexion Models — conformance checking)
**Phase:** Post-extraction (M2)
**Tier:** 3

---

## Inputs

```yaml
required:
  - name: "slug"
    description: "Slug do projeto a auditar (default: allfluence)"
    example: "allfluence"
optional:
  - name: "scope"
    description: "Módulo/app específico para auditar (default: all)"
    example: "apps/api"
  - name: "dimension"
    description: "Dimensão para auditar (default: all)"
    valid_values: ["architecture", "dependencies", "data", "domain", "api", "infra", "all"]
  - name: "against"
    description: "Comparar contra código atual (live) ou contra outra extração"
    default: "live"
    valid_values: ["live", "extraction"]
```

---

## Elicitation (elicit: true)

Before auditing, gather from the user:

1. **Qual projeto?** (default: allfluence)
2. **Escopo?** (all, ou módulo específico como apps/api, apps/web, packages/db)
3. **Foco?** (architecture drift, dependency drift, data drift, domain drift, ou all)
4. **Comparar contra?** (live = código atual no filesystem, extraction = outra extração)

---

## Steps

### Step 1: Validate Baseline Exists

```bash
ls outputs/decoded/{slug}/phase-0-scoping/
ls outputs/decoded/{slug}/phase-6-synthesis/
```

**VETO:** Se extração baseline não existe → HALT, recomendar `*extract-full` primeiro.

### Step 2: Check Baseline Freshness

Ler `outputs/decoded/{slug}/phase-0-scoping/scope-document.yaml` → verificar `analysis_date`.
- Se > 90 dias → WARN: "Baseline stale — consider re-extraction"
- Se > 180 dias → VETO: "Baseline too old — re-extract before audit"

### Step 3: Architecture Drift Check

Usando @gail-murphy Reflexion Model:
1. **High-level model:** C4 Container diagram de `phase-3-fusion/c4-container.md`
2. **Source mapping:** Mapear containers → diretórios atuais do código
3. **Extract actual:** Ler imports/dependencies atuais do código vivo
4. **Compute reflexion:** Convergências (✅), Divergências (❌), Ausências (⚠️)

### Step 4: Dependency Drift Check

1. Comparar `phase-2-extraction/dependency-graph.md` com imports atuais
2. Identificar: novas dependências não no baseline, dependências removidas, versões mudaram

### Step 5: Data Model Drift Check

1. Comparar `phase-2-extraction/er-diagram.md` com migrations atuais em `packages/db/migrations/`
2. Identificar: tabelas novas, colunas adicionadas/removidas, RLS policies mudaram

### Step 6: Domain Drift Check

1. Comparar `phase-5-domain/domain-map.yaml` com bounded contexts atuais
2. Identificar: novos aggregates, regras mudaram, contexts consolidados/separados

### Step 7: Generate Conformance Delta

Escrever `outputs/decoded/{slug}/audits/{date}/conformance-delta.yaml` usando template.

---

## Output

```yaml
output:
  file: "outputs/decoded/{slug}/audits/{YYYY-MM-DD}/conformance-delta.yaml"
  template: "templates/conformance-delta-tmpl.yaml"
  artifact_contract: "conformance-delta"
  lifecycle_state: draft
```

---

## Veto Conditions

1. **No baseline:** Extração não existe → HALT
2. **Baseline > 180 dias:** Muito stale para audit confiável → HALT
3. **Código inacessível:** Source path do projeto não existe no filesystem → HALT (só funciona com projetos locais)
4. **Scope inválido:** Módulo especificado não existe no projeto → HALT

---

## Completion Criteria

- [ ] Reflexion Model computado (convergences, divergences, absences)
- [ ] Drift ratio calculado por dimensão
- [ ] Severity classificada para cada divergência
- [ ] Conformance delta salvo em `audits/{date}/`
- [ ] Recomendações de ação para cada divergência HIGH+

---

## Handoff

| Para | Quando | Artifact |
|------|--------|----------|
| @decoder-chief | Audit completo | conformance-delta.yaml |
| @architect | Drift arquitetural HIGH detectado | divergências de arquitetura |
| *compare task | Audit revela necessidade de comparar com referência | conformance-delta como input |
| *adopt task | Drift aponta para padrão melhor em projeto de referência | divergência + referência |
