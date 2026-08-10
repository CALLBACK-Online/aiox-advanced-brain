# Task: Model Decisions (Decision Model + DMN)

> Phase 4 of wf-extract-rules pipeline

**Task ID:** model-decisions
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Organize extracted rules into a formal Decision Model (von Halle) and express computational rules as DMN decision tables (Taylor)
**Orchestrator:** @decoder-chief
**Primary Agents:** @barbara-von-halle, @james-taylor
**Phase:** 3 (Modeling)
**Tier:** 1-2

---

## Inputs

```yaml
required:
  - name: "classified_rules"
    description: "Rules extracted and classified in Phase 2 (with Ross taxonomy and traceability)"
  - name: "glossary"
    description: "Ubiquitous Language Glossary from Phase 0"
  - name: "context_map"
    description: "Bounded Context Map from Phase 0"
optional:
  - name: "fact_model"
    description: "Fact model from Phase 2 (terms → facts → rules)"
  - name: "stakeholders"
    description: "Business stakeholders available for decision validation"
```

---

## Elicitation (elicit: true)

Before modeling, gather from the user:

1. **How many major business decisions does this system make?** (e.g., approve credit, calculate price, assign tier)
2. **Are there decisions that feed into other decisions?** (chained decisions)
3. **What's the target audience for decision tables?** (business analysts, developers, both)
4. **Are there existing decision tables or matrices?** (spreadsheets, config files) **VETO RISK:** If legacy decision tables exist, they MUST be imported and reconciled before creating new ones — risk of duplication and contradiction. Document all existing tables found.

---

## Steps

### Step 1: Identify Business Decisions (Barbara von Halle)

```
ACTION: From the classified rules, identify the BUSINESS DECISIONS being made
OUTPUT: Decision inventory
AGENT: @barbara-von-halle

GUIDANCE:
  A business decision is a QUESTION the system answers:
  - "Is this customer eligible for credit?"
  - "What shipping rate applies?"
  - "Should this order be flagged for review?"

  Rules GOVERN decisions. A decision without rules is an empty question.
  Rules without a decision are orphaned logic.

Format:
  decisions:
    - id: "DEC-{CONTEXT}-{NNN}"
      name: "Determine Shipping Rate"
      question: "What shipping rate applies to this order?"
      context: "Logistics"
      governing_rules: ["RE-LOG-001", "RE-LOG-002", "RE-LOG-003"]
      inputs: ["customer_tier", "order_weight", "destination_zone"]
      output: "shipping_rate (decimal)"
      frequency: "Per order"
      business_impact: "high"
```

### Step 2: Create Rule Families (Barbara von Halle)

```
ACTION: Group related rules into Rule Families under each decision
OUTPUT: Decision Model with rule families
AGENT: @barbara-von-halle

Von Halle's Decision Model structure:
  1. BUSINESS DECISION — The question being answered
  2. RULE FAMILY — Group of rules that together answer the decision
  3. RULE CONNECTIONS — How decision outputs feed into other decisions

GUIDANCE:
  - A Rule Family contains rules that share the SAME condition columns
  - If conditions differ, it's a DIFFERENT rule family
  - One decision can have multiple rule families (e.g., eligibility + pricing)
  - Rule families should be ATOMIC — no mixing unrelated conditions

Format:
  decision_model:
    - decision: "DEC-LOG-001"
      name: "Determine Shipping Rate"
      rule_families:
        - family: "Base Rate by Zone"
          conditions: ["destination_zone"]
          rules: ["RE-LOG-001", "RE-LOG-002"]
        - family: "Tier Discount"
          conditions: ["customer_tier"]
          rules: ["RE-LOG-003"]
      connections:
        feeds_into: ["DEC-SALES-003"]  # Shipping cost feeds into total price
```

### Step 3: Build Decision Tables (James Taylor)

```
ACTION: Express each Rule Family as a DMN decision table
OUTPUT: DMN decision tables with hit policies
AGENT: @james-taylor

Hit Policy Selection:
  U (Unique)    — Exactly one row matches (non-overlapping conditions)
  F (First)     — First matching row wins (priority-ordered)
  P (Priority)  — Output with highest declared priority
  A (Any)       — All matching rows must agree (redundancy expected)
  C (Collect)   — Collect all matching outputs (multi-value results)
  R (Rule order) — Outputs in rule order (sequence matters)
  O (Output order) — Outputs in output priority (ranked lists)

EDGE CASE GUIDANCE:
  - Decision table with 1 row: This is probably a CONSTRAINT, not a DECISION.
    Reclassify as a constraint rule and remove from decision modeling.
    A decision implies choosing between alternatives — one row = no choice.
  - Decision table with 50+ rows: Too large to be useful as a single table.
    Break into sub-tables by condition group (e.g., by customer_tier first,
    then by destination_zone within each tier). Each sub-table should have
    a maximum of ~20 rows for readability.

Format:
  decision_table:
    id: "DT-{CONTEXT}-{NNN}"
    name: "Base Shipping Rate by Zone"
    decision: "DEC-LOG-001"
    hit_policy: "U"
    inputs:
      - name: "destination_zone"
        type: "string"
        allowed_values: ["Local", "Regional", "National", "International"]
    outputs:
      - name: "base_rate"
        type: "decimal"
    rules:
      - conditions: { destination_zone: "Local" }
        outputs: { base_rate: 5.00 }
      - conditions: { destination_zone: "Regional" }
        outputs: { base_rate: 12.50 }
      - conditions: { destination_zone: "National" }
        outputs: { base_rate: 25.00 }
      - conditions: { destination_zone: "International" }
        outputs: { base_rate: 50.00 }
    completeness: "All 4 zones covered — COMPLETE"
    source_rules: ["RE-LOG-001"]
```

### Step 4: Create Decision Requirements Diagrams (James Taylor)

```
ACTION: Create DRDs showing decision dependencies
OUTPUT: DRD per bounded context (Mermaid format)
AGENT: @james-taylor

GUIDANCE:
  DRDs show WHAT decisions exist and HOW they depend on each other.
  Not HOW the decision is made (that's the decision table).

  DRD Elements:
  - Rectangle: Decision
  - Oval: Input Data
  - Arrow: "requires" relationship
  - Rounded Rectangle: Knowledge Source

Example (Mermaid):
  graph TD
    A[Customer Tier] --> B{Determine Shipping Rate}
    C[Order Weight] --> B
    D[Destination Zone] --> B
    B --> E{Calculate Total Price}
    F[Product Subtotal] --> E
    G[Tax Rules] --> E
```

### Step 5: Validate Completeness & Consistency (Barbara von Halle)

```
ACTION: Audit the decision model for gaps, contradictions, and orphans
OUTPUT: Validation report
AGENT: @barbara-von-halle

Check for:
  ORPHANED RULES — Rules not assigned to any decision
    Action: Find the decision or create one
  EMPTY DECISIONS — Decisions with no governing rules
    Action: Find the rules or remove the decision
  CONTRADICTIONS — Two rules that cannot both be satisfied
    Action: Document conflict, propose resolution
  GAPS — Decision table with uncovered condition combinations
    Action: Add missing rows or document as "not applicable"
  CIRCULAR DEPENDENCIES — Decision A feeds B feeds A
    Action: Break the cycle, identify the root decision

Format:
  validation_report:
    orphaned_rules: []
    empty_decisions: []
    contradictions: []
    gaps:
      - table: "DT-LOG-001"
        missing: "destination_zone = 'Military APO' not covered"
        recommendation: "Add row or classify under International"
    circular_dependencies: []
    status: "PASS|FAIL"
    notes: "..."
```

---

## Veto Conditions

- **VETO:** Do NOT create decision tables without first identifying the business decision they serve.
- **VETO:** Do NOT choose a hit policy arbitrarily. Document WHY the selected hit policy is correct.
- **VETO:** Do NOT leave decision tables with uncovered condition combinations without documenting the gap.
- **VETO:** Do NOT mix rules from different bounded contexts in the same decision table.
- **VETO:** Do NOT proceed to Phase 4 if validation report has CONTRADICTIONS unresolved.
- **VETO:** Do NOT finalize if any classified rule has zero decision table assignment — orphaned rules indicate incomplete modeling. Every rule must belong to a decision.
- **VETO:** Do NOT finalize if any decision table has zero associated rules — empty decisions indicate a modeling artifact, not a real business decision. Remove or find the missing rules.
- **VETO:** Do NOT finalize if circular dependencies are detected between decision tables (Decision A feeds B feeds A). Break the cycle and identify the root decision before proceeding.
- **VETO:** Do NOT start modeling if the fact model from characterize-legacy (Phase 2) is missing or incomplete (< 50% of entities mapped). The fact model provides the vocabulary for decision inputs and outputs.

---

## Output

```yaml
artifact_path: "outputs/rules/{domain}/decision-model.md"

deliverables:
  primary:
    - "Decision Model (decisions → rule families → rules)"
    - "DMN Decision Tables (one per rule family)"
    - "Decision Requirements Diagrams (one per context)"
    - "Validation Report (gaps, contradictions, orphans)"
  secondary:
    - "Hit policy justification per table"
    - "Decision chain documentation"

output_fields:
  business_owner:
    description: "The business owner/stakeholder responsible for this domain's rule decisions"
    source: "Captured during map-domain elicitation (question 5)"
    format: "Name — Role — Department"
    example: "Maria Santos — Head of Sales — Commercial"
    usage: "Referenced in decision tables for sign-off authority and rule change approvals"

quality_criteria:
  - "Every extracted rule assigned to a decision"
  - "Every decision table has a documented hit policy with justification"
  - "DRDs created for all major contexts"
  - "No unresolved contradictions"
  - "No orphaned rules"
  - "Decision tables have completeness check"
  - "business_owner field populated from map-domain output"
```

---

## Completion Criteria

- [ ] All business decisions identified and documented
- [ ] Rule families created under each decision
- [ ] Decision tables built with correct hit policies
- [ ] DRDs created per bounded context
- [ ] Validation report: no contradictions, no orphans
- [ ] Gaps documented with recommendations
- [ ] Ready for handoff to Phase 4 (expression)

---

## Handoff

```yaml
next_agents: ["@graham-witt", "@ronald-ross"]
next_task: "express-rules.md"
context_to_pass:
  - "Decision Model"
  - "Decision Tables (DMN format — RECOMMENDED but not REQUIRED; purely behavioral rules may not need DMN tables)"
  - "DRDs"
  - "Validation Report"
gate: "decoder-chief approves modeling before expression begins"
note: "DMN decision tables are the RECOMMENDED format for computational and conditional rules. Purely behavioral rules (workflow sequencing, approval chains) may be expressed as process descriptions without DMN notation. The express-rules phase must work regardless of whether DMN tables are present."
```
