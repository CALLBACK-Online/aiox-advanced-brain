# Business Rules Catalog

**System:** {system_name}
**Domain:** {domain}
**Version:** {version}
**Date:** {date}
**Extraction Squad:** domain-decoder
**Orchestrator:** Rules Chief

---

## Como Usar Este Template

> **Replace all `{field_name}` placeholders with actual values. Do not leave any placeholder unfilled. If a section does not apply, write 'N/A' with reason. Never delete a section.**

### Passo a Passo

1. **Copiar** este arquivo para o diretorio do catalogo de destino
2. **Renomear** para `rule-catalog-{domain}.md` (ex: `rule-catalog-billing.md`)
3. **Preencher** a secao Document Control com os metadados do dominio
4. **Popular** as regras seguindo os exemplos concretos na secao "Exemplo Completo (YAML)"
5. **Validar** usando os checklists `sbvr-validation.md` e `extraction-quality.md`

### Placeholders Obrigatorios

| Placeholder | Descricao | Exemplo |
|-------------|-----------|---------|
| `{system_name}` | Nome do sistema sendo analisado | `MMOS Pipeline` |
| `{domain}` | Dominio de negocio principal | `agent_orchestration` |
| `{version}` | Versao do catalogo (semver) | `1.0.0` |
| `{date}` | Data da extracao (ISO 8601) | `2026-02-19` |
| `{DOMINIO}` | Prefixo do dominio para IDs de regra (UPPERCASE) | `BILLING`, `AGENT_ORCH` |

### Convencao de Nomes

- **Rule IDs:** `RE-{DOMINIO}-{NNN}` — sequencial, numerico de 3 digitos (ex: `RE-BILLING-001`)
- **Rule Slugs:** `{domain}_{action}_{condition}` — snake_case para legibilidade (ex: `billing_approve_credit`)
- Ambas as formas sao validas. O ID e canonical e imutavel; o slug e humano e pode mudar.

---

## Document Control

| Field | Value |
|-------|-------|
| System Name | {system_name} |
| Primary Domain | {domain} |
| Extraction Date | {date} |
| Catalog Version | {version} |
| SBVR Validation Score | {sbvr_score} / 44 ({sbvr_pct}%) |
| Extraction Quality Score | {quality_score} / 51 ({quality_pct}%) |
| Total Rules | {total_rules} |
| Bounded Contexts | {context_count} |
| Decision Tables | {dt_count} |
| Status | {status} |

---

## 1. Glossary of Business Terms

*All terms used in rule statements MUST appear here. Terms not in this glossary must not appear in rule statements.*

| Term | Definition | Bounded Context | Synonyms | Source |
|------|-----------|----------------|----------|--------|
| {term} | {definition} | {bounded_context} | {synonyms_or_none} | {source} |
| | | | | |

> Instructions: List every business term in alphabetical order. "Source" is the SME, document, or code location where this term was confirmed. Include homonyms with their context disambiguation in parentheses.

---

## 2. Bounded Contexts

*Bounded contexts define the scope within which a term has its specific meaning and a rule applies.*

| Context Name | Description | Primary Owner | Source Systems | Upstream | Downstream |
|-------------|-------------|---------------|---------------|----------|------------|
| {context_name} | {description} | {business_owner} | {source_systems} | {upstream_contexts} | {downstream_contexts} |
| | | | | | |

> **Format — Source Systems:** Formato: nome do sistema seguido de versao entre parenteses. Ex: `ERP-SAP (v4.2)`, `Auth-Service (v2.1.0)`. Para sistemas sem versao: `Legacy-Billing (unknown)`. Listar um sistema por celula; multiplos separados por virgula.

### Context Map

```
{context_map_diagram}

Example:
  [Ordering] ---(Customer Relationship)--- [CRM]
  [Ordering] ---(Product Catalog)--- [Inventory]
  [Ordering] ---(Payment)--- [Finance]
```

---

## 3. Rules by Category

*Rules are organized by the Ross taxonomy. Within each category, rules are grouped by bounded context.*

> **Pipeline Protocol:** A execucao do pipeline segue desenvolvimento orientado por stories: cada fase mapeia para uma task da story, com gates de validacao em cada transicao. Regras de orquestracao (ex: RS-AGENT_ORCH-005) devem referenciar o gate correspondente.

---

### 3.1 Structural Rules

*What IS true: definitions, derivations, fact types. These rules define the business vocabulary in rule form.*

| ID | Subtype | Statement | Bounded Context | Source | Related Terms |
|----|---------|-----------|----------------|--------|---------------|
| RE-{DOMINIO}-{NNN} | definition / derivation / fact | {rule_statement} | {context} | {file}:{line} | {terms} |
| | | | | | |

> **Format — Related Terms:** Listar 2-5 termos do glossario relacionados a esta rule. Formato: comma-separated, lowercase. Ex: `ordem_compra, aprovacao, limite_credito`. Se < 2 termos: revisar glossario — provavelmente faltam termos. Todos os termos listados DEVEM estar definidos na Secao 1 (Glossary).

**Subtype guide:**
- `definition` — defines what a term means in rule form ("A Premium Customer is a customer whose...")
- `derivation` — derives a value from other facts ("Total Order Value is the sum of...")
- `fact` — asserts a relationship between terms ("A Customer may place many Orders")

---

### 3.2 Behavioral Rules

*What MUST be true: constraints, prohibitions, obligations, enablers. These govern what is allowed.*

| ID | Subtype | Statement | Bounded Context | Source | Related Terms |
|----|---------|-----------|----------------|--------|---------------|
| RE-{DOMINIO}-{NNN} | constraint / enabler / computation | {rule_statement} | {context} | {file}:{line} | {terms} |
| | | | | | |

**Subtype guide:**
- `constraint` — restricts what is allowed ("An Order MUST have at least one line item")
- `prohibition` — explicitly forbids ("A cancelled Order MUST NOT be reactivated")
- `enabler` — grants permission ("A Premium Customer MAY place orders without deposit")
- `computation` — calculates a value with obligation ("Shipping cost MUST be calculated as...")

> **Cross-cutting CONSTRAINT rules:** CONSTRAINT rules que aparecem em 3+ modules devem ter Decision Table dedicada (Secao 4) com `enforcement_method` especificado. Marcar como `[cross-module]` na Traceability Matrix e documentar todos os modules afetados na coluna Module/Class.

---

### 3.3 Decision Rules

*How conclusions are reached: conditional logic, inference chains, decision tables.*

| ID | Subtype | Statement | Decision Table | Bounded Context | Source |
|----|---------|-----------|----------------|----------------|--------|
| RE-{DOMINIO}-{NNN} | inference / action_enabler / behavioral | {rule_statement} | {dt_id_or_none} | {context} | {file}:{line} |
| | | | | | |

**Subtype guide:**
- `inference` — concludes a fact from conditions ("If a customer has no late payments for 12 months, then...")
- `action_enabler` — triggers an action ("When inventory drops below reorder point, then notify purchasing")
- `behavioral` — governs how a process is conducted ("Credit approval MUST require two approvers if amount exceeds...")

---

## 4. Decision Tables

*Formal DMN decision tables for all computational and conditional rules. Each table has a hit policy.*

---

### DT-{dt_id}: {decision_name}

**Bounded Context:** {context}
**Hit Policy:** {hit_policy} — {hit_policy_explanation}
**Governing Rules:** {related_rule_ids}
**Source:** {source_location}

| {condition_1} | {condition_2} | {condition_n} | {conclusion_1} | {conclusion_n} |
|:-------------|:-------------|:-------------|:--------------|:--------------|
| {val} | {val} | {val} | {val} | {val} |
| | | | | |

> Hit Policy Reference:
> - U (Unique): exactly one row matches — inputs are non-overlapping
> - F (First): first matching row wins — priority order matters
> - P (Priority): output with highest declared priority wins
> - A (Any): all matching rows must agree on output
> - C (Collect): all matching outputs collected (with optional aggregation: C+, C<, C>, C#)
> - R (Rule order): outputs returned in rule order
> - O (Output order): outputs returned in output priority order

---

## 5. Rule Details (Full YAML)

*Machine-readable representation of every rule. One block per rule.*

```yaml
# ─────────────────────────────────────────────
# Rule: RE-{DOMINIO}-{NNN}
# ─────────────────────────────────────────────
- rule:
    id: "RE-{DOMINIO}-{NNN}"
    name: "{descriptive_name}"
    type: "constraint | computation | inference | action_enabler | behavioral | definition | derivation"
    domain: "{bounded_context_name}"
    version: "1.0.0"
    status: "extracted | validated | approved"

    statement: |
      {rule_statement_in_RuleSpeak}

    source:
      file: "{relative/path/to/source.ext}"
      line: {line_number}
      method: "{method_or_function_name}"
      snippet: |
        {verbatim_code_snippet}

    decision_table:
      # Include only if rule is modeled as a decision table
      table_id: "DT-{id}"
      hit_policy: "{U|F|P|A|C|R|O}"
      conditions:
        - name: "{condition_name}"
          type: "{string|integer|decimal|boolean|date}"
      outcomes:
        - name: "{outcome_name}"
          type: "{string|integer|decimal|boolean|date}"

    validation:
      sbvr_passed: {true|false}
      reviewed_by: "{agent_id}"
      validated_date: "YYYY-MM-DD"
      stakeholder_confirmed: {true|false}
      stakeholder_name: "{name_or_null}"

    metadata:
      extracted_by: "michael-feathers"
      classified_by: "ronald-ross"
      modeled_by: "barbara-von-halle"
      formalized_by: "james-taylor"
      expressed_by: "graham-witt"
      extraction_date: "YYYY-MM-DD"
      last_modified: "YYYY-MM-DD"
```

### Exemplo Completo (YAML)

*Dois exemplos reais preenchidos: um DERIVATION e um CONSTRAINT. Use como referencia ao popular o catalogo.*

```yaml
# ─────────────────────────────────────────────
# Exemplo 1: DERIVATION rule
# Demonstra uma regra de derivacao com decision table
# ─────────────────────────────────────────────
- rule:
    # Identificador unico: prefixo RE + dominio UPPERCASE + sequencial 3 digitos
    id: "RE-AGENT_ORCH-003"
    # Nome descritivo em linguagem de negocio
    name: "Pipeline Quality Score Derivation"
    # Tipo da regra conforme taxonomia Ross
    type: "derivation"
    # Bounded context onde esta regra se aplica
    domain: "agent_orchestration"
    # Versionamento semantico da regra
    version: "1.0.0"
    # Ciclo de vida: extracted -> validated -> approved
    status: "validated"

    # Statement em RuleSpeak: preciso, sem ambiguidade
    statement: |
      The pipeline_quality_score of a Rule Catalog is derived as the
      weighted sum of sbvr_validation_score (weight 0.6) and
      extraction_quality_score (weight 0.4), rounded to two decimal places.

    source:
      # Path relativo ao root do projeto
      file: "squads/domain-decoder/checklists/extraction-quality.md"
      line: 12
      method: "calculate_quality_score"
      # Trecho exato do codigo-fonte
      snippet: |
        quality_score = (sbvr_score * 0.6) + (extraction_score * 0.4)
        return round(quality_score, 2)

    decision_table:
      # Referencia a decision table na Secao 4
      table_id: "DT-ORCH-001"
      # Unique: exatamente uma linha faz match
      hit_policy: "U"
      conditions:
        - name: "sbvr_validation_score"
          type: "decimal"
        - name: "extraction_quality_score"
          type: "decimal"
      outcomes:
        - name: "pipeline_quality_score"
          type: "decimal"
        - name: "quality_tier"
          type: "string"

    validation:
      sbvr_passed: true
      reviewed_by: "ronald-ross"
      validated_date: "2026-02-15"
      stakeholder_confirmed: true
      stakeholder_name: "decoder-chief"

    metadata:
      extracted_by: "michael-feathers"
      classified_by: "ronald-ross"
      modeled_by: "barbara-von-halle"
      formalized_by: "james-taylor"
      expressed_by: "graham-witt"
      extraction_date: "2026-02-10"
      last_modified: "2026-02-15"

# ─────────────────────────────────────────────
# Exemplo 2: CONSTRAINT rule
# Demonstra uma regra restritiva sem decision table
# ─────────────────────────────────────────────
- rule:
    id: "RE-AGENT_ORCH-007"
    name: "Mandatory Glossary Term Coverage"
    # CONSTRAINT: restringe o que e permitido
    type: "constraint"
    domain: "agent_orchestration"
    version: "1.0.0"
    status: "approved"

    statement: |
      A Rule Catalog MUST NOT contain any term in a rule statement
      that is not defined in the Glossary of Business Terms (Section 1).
      It is obligatory that each term used in two or more rule statements
      appears in the Glossary with a single canonical definition.

    source:
      file: "squads/domain-decoder/checklists/sbvr-validation.md"
      line: 28
      method: "validate_glossary_coverage"
      snippet: |
        for term in rule.related_terms:
            if term not in glossary:
                raise ValidationError(f"Term '{term}' not in glossary")

    # Sem decision table — constraint simples, nao condicional
    decision_table: null

    validation:
      sbvr_passed: true
      reviewed_by: "ronald-ross"
      validated_date: "2026-02-16"
      stakeholder_confirmed: true
      stakeholder_name: "decoder-chief"

    metadata:
      extracted_by: "michael-feathers"
      classified_by: "ronald-ross"
      modeled_by: "barbara-von-halle"
      formalized_by: "james-taylor"
      expressed_by: "graham-witt"
      extraction_date: "2026-02-10"
      last_modified: "2026-02-16"
```

---

## 6. Traceability Matrix

*Every rule must appear here. This matrix enables impact analysis: if one thing changes, what rules are affected?*

| Rule ID | Rule Name | Source File | Line | Module / Class | SME / Owner | Policy / Document | Decision Table |
|---------|-----------|-------------|------|---------------|-------------|-------------------|---------------|
| RE-{DOMINIO}-{NNN} | {name} | {file_path} | {line} | {module} | {sme} | {policy_ref_or_none} | {dt_id_or_none} |
| | | | | | | | |

> **Format — Module / Class:** Formato: `module/class` usando path relativo ao root do projeto. Ex: `auth/UserPermissions`, `billing/InvoiceCalculator`. Para rules cross-module: listar modulo primario + tag `[cross-module]`. Ex: `orchestration/PipelineRunner [cross-module]`. Usar nomes fully-qualified quando disponivel: `billing.pricing.calculator` (Python) ou `com.company.billing.PricingService` (Java).

---

## 7. Rule Dependencies

*Rules that depend on other rules. If Rule A is changed, Rule B may need review.*

| Rule ID | Depends On | Dependency Type | Notes |
|---------|-----------|-----------------|-------|
| RE-{DOMINIO}-{NNN} | RE-{DOMINIO}-{MMM} | prerequisite / input / conflict / override | {explanation} |
| | | | |

**Dependency type guide:**
- `prerequisite` — Rule A must be satisfied for Rule B to be evaluated
- `input` — conclusion of Rule A is an input to Rule B
- `conflict` — Rule A and Rule B govern the same situation (resolution documented)
- `override` — Rule A takes precedence over Rule B when both apply

### Split Candidates

*Rules que excedem limites de complexidade devem ser avaliadas para decomposicao em sub-rules.*

**Criterios para split:**
- Rule statement com mais de 3 condition branches (IF/WHEN/UNLESS)
- Rule statement com mais de 50 palavras
- Rule que governa mais de 2 bounded contexts simultaneamente

| Rule ID | Motivo do Split | Sub-rules Propostas | Status |
|---------|----------------|---------------------|--------|
| {rule_id} | {criterio_violado} | {sub_rule_ids_propostos} | pending / approved / rejected |
| | | | |

> **Nota:** Naming convention no catalogo: `snake_case` para colunas de banco de dados e identificadores internos, `kebab-case` para nomes de arquivos de agentes (ex: `decoder-chief.md`). Ambas as convencoes coexistem — use a adequada ao contexto.

---

## 8. Statistics

```
TOTALS
──────────────────────────────────────────────
Total Rules Extracted:          {total_rules}
  ├── Structural Rules:         {structural_count}
  │     ├── Definitions:        {def_count}
  │     ├── Derivations:        {deriv_count}
  │     └── Fact Types:         {fact_count}
  ├── Behavioral Rules:         {behavioral_count}
  │     ├── Constraints:        {constraint_count}
  │     ├── Prohibitions:       {prohibition_count}
  │     ├── Enablers:           {enabler_count}
  │     └── Computations:       {computation_count}
  └── Decision Rules:           {decision_count}
        ├── Inferences:         {inference_count}
        ├── Action Enablers:    {action_count}
        └── Behavioral:         {behavioral_decision_count}

COVERAGE
──────────────────────────────────────────────
Bounded Contexts Mapped:        {context_count}
Decision Tables Created:        {dt_count}
Rules with Decision Tables:     {rules_with_dt}
Rules with Stakeholder Sign-off:{rules_validated}

QUALITY
──────────────────────────────────────────────
SBVR Validation Score:          {sbvr_score} / 44  ({sbvr_pct}%)
SBVR Critical Items Passed:     {sbvr_criticals} / 5
Extraction Quality Score:       {quality_score} / 51  ({quality_pct}%)
Quality Auto-fail Conditions:   {auto_fails} / 6 (must be 0)

PASS/FAIL
──────────────────────────────────────────────
SBVR:                           {PASS|FAIL}
Extraction Quality:             {PASS|FAIL}
Overall:                        {PASS|FAIL}
```

---

## 9. Open Issues

*Known gaps, unresolved contradictions, rules requiring further stakeholder confirmation.*

| Issue ID | Type | Description | Rule(s) Affected | Owner | Due Date | Status | Opened Date | Assigned To | Resolution Target |
|---------|------|-------------|-----------------|-------|----------|--------|-------------|-------------|-------------------|
| ISSUE-{NNN} | gap / contradiction / ambiguity / needs_validation | {description} | {rule_ids} | {owner} | {date} | open | {opened_date} | {assigned_to} | {resolution_target} |
| | | | | | | | | | |

### Politica de Aging e Escalation

| Idade da Issue | Classificacao | Acao Requerida |
|---------------|---------------|----------------|
| 0-7 dias | **NEW** | Responsavel (`assigned_to`) deve investigar e documentar causa raiz |
| 8-14 dias | **AGING** | Escalar para squad lead; squad lead deve reclassificar ou atribuir novo responsavel |
| 15-30 dias | **STALE** | Requer decisao formal: resolver, reclassificar como `wontfix`, ou escalar para stakeholder |
| 30+ dias | **CRITICAL** | Bloqueia proxima release do catalogo. Issues de contradiction com status `open` sao **DELIVERY BLOCKERS** |

**Caminho de escalation:** `owner` -> `squad lead` -> `stakeholder` -> `product owner`

**Regras adicionais:**
- Issues do tipo `contradiction` com status `open` sao DELIVERY BLOCKERS independente da idade
- Issues do tipo `gap` abertas ha mais de 30 dias devem ser revisadas pelo `decoder-chief`
- Toda issue deve ter `opened_date`, `assigned_to` e `resolution_target` preenchidos
- Status validos: `open`, `investigating`, `resolved`, `wontfix`, `escalated`

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | {date} | decoder-chief | Initial extraction |
| | | | |

---

*Business Rules Catalog — Generated by domain-decoder squad*
*Template version: 1.1.0*
*Standard: OMG SBVR 1.5 | Framework: Ross, Evans, Feathers, von Halle, Taylor, Fowler, Witt*
