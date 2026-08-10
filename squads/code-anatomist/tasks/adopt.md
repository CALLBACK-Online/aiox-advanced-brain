# Task: Adopt Pattern

> Molecule M3-Adopt — Proposta formal de adoção de padrão de projeto de referência

**Task ID:** adopt
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Gerar proposta formal de adoção de um padrão identificado em projeto de referência, com análise de impacto, plano de implementação e handoff inter-BU para @architect
**Orchestrator:** @decoder-chief
**Primary Agent:** @rick-kazman (architecture analysis) + @simon-brown (C4 visualization)
**Phase:** Post-comparison (M3)
**Tier:** 2

---

## Inputs

```yaml
required:
  - name: "source_slug"
    description: "Projeto de referência que contém o padrão"
    example: "n8n"
  - name: "pattern_description"
    description: "Descrição do padrão a adotar (ou referência ao delta-report)"
    example: "Worker pool com concurrency control e dead-letter queue"
optional:
  - name: "delta_report"
    description: "Path para delta-report.yaml de um *compare anterior"
    example: "outputs/decoded/allfluence/comparisons/n8n/delta-report.yaml"
  - name: "target_module"
    description: "Módulo AllFluence onde o padrão seria aplicado"
    example: "apps/worker"
  - name: "target_slug"
    description: "Projeto alvo (default: allfluence)"
    default: "allfluence"
```

---

## Elicitation (elicit: true)

Before proposing adoption, gather from the user:

1. **Qual padrão?** (descrição ou referência a finding no delta-report)
2. **De qual projeto?** (slug da referência)
3. **Para qual módulo AllFluence?** (apps/api, apps/worker, packages/db, etc.)
4. **Objetivo?** (performance, modifiability, security, maintainability)
5. **Constraint?** (timeline, effort máximo, backward compatibility obrigatória?)

---

## Steps

### Step 1: Extract Pattern from Reference

1. Ler extração do source_slug para entender o padrão:
   - `phase-2-extraction/` → como está implementado (deps, structure)
   - `phase-3-fusion/` → como se encaixa na arquitetura (C4)
   - `phase-5-domain/` → regras de negócio envolvidas
   - `phase-6-synthesis/` → decisões arquiteturais (Arc42, ATAM)
2. Documentar: componentes do padrão, dependências, trade-offs

### Step 2: Analyze Target State

1. Ler extração do target_slug (allfluence) para o módulo alvo:
   - Mesmas fases acima, filtradas pelo target_module
2. Documentar: estado atual, gaps, o que precisa mudar

### Step 3: Impact Analysis

| Dimensão | Análise |
|----------|---------|
| **Compatibility** | O padrão é compatível com nosso stack? (React 19, FastAPI, Supabase, Node.js) |
| **Breaking changes** | Quais interfaces mudam? Quais consumidores são afetados? |
| **Effort** | Estimativa em dev-days (S/M/L/XL) |
| **Risk** | O que pode dar errado? Rollback possível? |
| **Value** | Qual quality attribute melhora? Quanto? |

### Step 4: Generate Adaptation Notes

O padrão NÃO é copiado — é ADAPTADO:
- O que manter do padrão original
- O que mudar para o contexto AllFluence
- O que descartar (não se aplica ao nosso contexto)

### Step 5: Generate C4 Diagrams (Before/After)

@simon-brown gera:
- C4 Container/Component BEFORE (estado atual do módulo alvo)
- C4 Container/Component AFTER (com padrão adotado)
- Highlight das mudanças

### Step 6: Generate Adoption Proposal

Escrever `outputs/decoded/{target_slug}/adoptions/{source_slug}-{pattern}/adoption-proposal.yaml`

### Step 7: Generate Inter-BU Handoff

```yaml
handoff:
  from: "@decoder-chief"
  to: "@architect"
  scope: inter_bu
  signoff:
    required: true
    approver: "Pedro Valério"
    approved_at: null
    approved: false
  lifecycle_state: created
  artifacts:
    - id: "adoption-proposal"
      type: "adoption-proposal"
      status: draft
```

**HALT:** Notificar usuário para review e signoff antes de handoff.

---

## Output

```yaml
output:
  file: "outputs/decoded/{target_slug}/adoptions/{source_slug}-{pattern}/adoption-proposal.yaml"
  template: "templates/adoption-proposal-tmpl.yaml"
  artifact_contract: "adoption-proposal"
  lifecycle_state: draft
  handoff_scope: inter_bu
```

---

## Veto Conditions

1. **Sem extração do source:** Projeto referência não extraído → HALT, recomendar `*extract-full` primeiro
2. **Sem baseline do target:** AllFluence não tem auto-extração → HALT, recomendar `*extract-full allfluence`
3. **Stack incompatível:** Padrão requer tecnologia que AllFluence não usa e adoção seria breaking → WARN
4. **Effort > XL:** Se estimativa > 20 dev-days → ESCALATE para @architect antes de prosseguir
5. **Sem delta-report:** Se *compare não foi executado antes → WARN, recomendar *compare primeiro
6. **Signoff ausente:** NUNCA gerar handoff sem signoff humano → HALT até aprovação

---

## Completion Criteria

- [ ] Padrão do source documentado com componentes e trade-offs
- [ ] Estado atual do target documentado
- [ ] Impact analysis completa (5 dimensões)
- [ ] Adaptation notes (keep/change/discard)
- [ ] C4 Before/After diagrams gerados
- [ ] Adoption proposal salva com lifecycle_state: draft
- [ ] Handoff inter-BU template criado
- [ ] Usuário notificado para signoff

---

## Handoff

| Para | Quando | Artifact | Scope |
|------|--------|----------|-------|
| **Pedro Valério** | Proposal ready | adoption-proposal.yaml | HUMAN SIGNOFF (inter-BU) |
| **@architect** | Após signoff humano | adoption-proposal.yaml + handoff | inter_bu |
| **@pm** | Após @architect approve | ADR + story candidates | intra_bu |
| **@sm** | Após @pm creates epic | stories derivadas | intra_bu |
