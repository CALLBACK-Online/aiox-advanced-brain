# Task: Extract Rules

> Phase 2 of wf-extract-rules pipeline

**Task ID:** extract-rules
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Extract raw business rules from identified seams, classify each using the Ross taxonomy, build a Fact Model, and assign canonical RE-{DOMAIN}-{NNN} IDs with full source traceability
**Orchestrator:** @decoder-chief
**Primary Agent:** @michael-feathers (extraction) + @ronald-ross (classification)
**Supporting Agent:** @ronald-ross (fact model)
**Phase:** 2 (Extraction & Classification)
**Tier:** 1

---

## Inputs

```yaml
required:
  - name: "characterization_test_suite"
    description: "Passing characterization tests from Phase 1 (CT-{CONTEXT}-{NNN})"
  - name: "seam_map"
    description: "Seam map from characterize-legacy task — lists all files, classes, methods containing business logic"
  - name: "rule_location_index"
    description: "Rule Location Index from Phase 1 — every significant file with risk_level per method"
  - name: "glossary"
    description: "Ubiquitous language glossary from Phase 0 (minimum 15 terms per major context)"
  - name: "rule_type_inventory"
    description: "Expected Ross category distribution from Phase 0 classify-rules task"
  - name: "context_map"
    description: "Bounded context map from Phase 0 (Eric Evans) — names, boundaries, relationships"
optional:
  - name: "priority_areas"
    description: "High-priority areas to extract first (e.g., revenue, compliance, cross-domain)"
  - name: "architecture_classification"
    description: "Architecture pattern from Phase 1 — guides where rules are likely embedded"
  - name: "smell_to_rule_mapping"
    description: "Code smell to rule candidate mapping from Phase 1 — pre-identified extraction targets"
```

---

## Elicitation (elicit: true)

Before extracting, confirm with the user:

1. **Are all characterization tests from Phase 1 passing?** (VETO condition — do not proceed if NO)
2. **Is the glossary complete enough to classify rules?** (minimum 10 terms before classification begins)
3. **Are there rules you already know about that are NOT in the seam map?** (stakeholder-known rules that may have no visible seam)
4. **Are there multi-layer duplicates?** (same rule enforced in FE + BE + DB — triggers dedup matrix, see E7)

### Rules Present Only in Documentation or Stakeholder Knowledge

```
If business rules exist ONLY in documentation, contracts, or stakeholder interviews
(no corresponding code implementation found):
  1. Extract them as SHADOW RULES using the standard RE-{DOMAIN}-{NNN} format
  2. Set source_type: "documentation" | "stakeholder" | "policy_document"
  3. Set code_location: null
  4. Add note: "No code implementation found — rule may be missing from system"
  5. These rules are HIGH PRIORITY for validation in Phase 5 (they represent gaps)
  6. Tag with shadow_rule: true in the rule record
```

---

## Steps

### Step 1: Extract Raw Rules from Seams (Michael Feathers)

```
ACTION: Walk every seam in the Seam Map and extract raw business rules
OUTPUT: Raw rule list with full source traceability
AGENT: @michael-feathers

CRITICAL RULES:
  1. Extract what the code DOES, not what it SHOULD do
  2. One rule = one atomic fact or constraint. If a code block has 3 rules, produce 3 entries.
  3. Copy the code snippet verbatim — never paraphrase at this stage
  4. A rule MUST have a business_rule: true tag. Implementation details are NOT rules.
     Test: "Would a Product Owner care if this changed?" If not — skip it.
  5. Tag every rule with its bounded context from Phase 0 before moving to the next seam

Process per seam:
  1. Navigate to the seam location (file, class, method)
  2. Read the code path end-to-end — do not skip lines
  3. For each discrete conditional, calculation, or enforcement found:
     a. Copy the code snippet verbatim
     b. Write a first-pass English statement of what it does
     c. Note: file path, line number, method name, bounded context
     d. Assign a provisional business_rule: true | false tag
  4. Move to the next seam

Format per raw rule:
  raw_rule:
    provisional_id: "RC-{CONTEXT}-{NNN}"
    bounded_context: "Sales"
    file: "src/sales/OrderProcessor.java"
    line: 142
    method: "processOrder()"
    code_snippet: |
      if (order.getQuantity() > 100 && customer.getType() == CustomerType.VIP) {
        discount = BASE_DISCOUNT + VIP_BONUS;
      }
    first_pass_statement: "VIP customers with quantity over 100 receive an additional bonus on top of the base discount"
    characterization_test_ref: "CT-SALES-001"
    seam_ref: "SM-SALES-001"
    business_rule: true
    source_type: "code"  # code | documentation | stakeholder | policy_document
    shadow_rule: false
```

### Step 2: Classify Each Raw Rule (Ronald Ross)

```
ACTION: Apply Ross taxonomy to every rule with business_rule: true
OUTPUT: Classified rule list — each rule has a Ross category
AGENT: @ronald-ross

Ross Taxonomy (5 categories):
  - CONSTRAINT:
      definition: Must always be true. A violation is an error or prohibition.
      signals: "must", "cannot", "is required to", validation logic, guard clauses
      examples: "Order total must not exceed credit limit", "Discount cannot exceed 50%"

  - COMPUTATION:
      definition: Derives a value from other facts using a formula or calculation.
      signals: Arithmetic expressions, percentage calculations, aggregate functions
      examples: "Total price = unit price × quantity × (1 - discount rate)"

  - INFERENCE:
      definition: Concludes a new fact from existing facts via if-then derivation.
      signals: Conditional assignments, status derivations, eligibility conclusions
      examples: "If customer has 3+ late payments, conclude: high-risk customer"

  - ACTION ENABLER:
      definition: Triggers a process or action when a condition is met.
      signals: Event triggers, workflow initiators, state transitions, notifications
      examples: "When order total exceeds $10,000, trigger manager approval workflow"

  - BEHAVIORAL:
      definition: Governs how a process must be conducted (sequence, timing, actor).
      signals: Process order constraints, SLA requirements, role-based responsibilities
      examples: "Refund request must be reviewed by finance before processing"

Classification rules:
  - Every rule gets EXACTLY ONE primary category
  - If a rule appears to fit two categories, it must be split into two separate rules
  - Classification is based on the rule's INTENT, not its code form
  - Document classification reasoning in the notes field when non-obvious

Format:
  rule:
    provisional_id: "RC-SALES-001"
    ross_category: "COMPUTATION"
    classification_reasoning: "Derives a monetary value (discount) from input facts (quantity, customer type) using an arithmetic formula"
    confidence: HIGH  # HIGH | MEDIUM | LOW
    notes: "Could superficially appear as INFERENCE (the condition), but the core behavior is value derivation"
```

### Step 3: Build Fact Model (Ronald Ross)

```
ACTION: Construct the Fact Model — terms as nodes, fact types as edges, rules as constraints on facts
OUTPUT: Fact Model document linking glossary terms to extracted rules
AGENT: @ronald-ross

GUIDANCE:
  - Start from the Phase 0 glossary. Each glossary term is a potential FACT TYPE NODE.
  - Add FACT TYPES discovered during extraction (relationships between terms).
  - Map each classified rule to the facts it constrains, derives, or operates on.
  - The Fact Model is the bridge between the glossary (vocabulary) and the rule catalog (behavior).

Fact Model structure:
  fact_model:
    bounded_context: "Sales"
    terms:
      - id: "FT-SALES-001"
        name: "Customer"
        definition: "A party that places orders. Source: glossary."
        related_terms: ["Order", "CustomerType", "CreditLimit"]
    fact_types:
      - id: "FT-SALES-REL-001"
        subject: "Customer"
        predicate: "places"
        object: "Order"
        source: "Extracted from OrderProcessor.processOrder()"
    rule_to_fact_mapping:
      - rule_provisional_id: "RC-SALES-001"
        facts_constrained: ["FT-SALES-001", "FT-SALES-REL-001"]
        facts_derived: ["FT-SALES-002"]
        facts_referenced: ["FT-SALES-003"]

Completeness expectation:
  - Minimum: every rule maps to at least ONE fact node
  - Ideal: every fact node has at least ONE rule that references or constrains it
  - Orphaned fact nodes (no rules) are documented as "vocabulary without behavior"
  - Orphaned rules (no fact mapping) MUST be resolved before Phase 3
```

### Step 4: Assign Canonical IDs and Tag with Source Traceability (Michael Feathers)

```
ACTION: Replace provisional RC-{CONTEXT}-{NNN} IDs with canonical RE-{DOMAIN}-{NNN} IDs
OUTPUT: Final rule list — every rule has canonical ID, source traceability, classification, and fact mapping
AGENT: @michael-feathers

ID Format: RE-{DOMAIN}-{NNN}
  - DOMAIN: bounded context name in UPPERCASE (e.g., SALES, LOGISTICS, BILLING)
  - NNN: sequential number starting from 001, zero-padded
  - Examples: RE-SALES-001, RE-LOGISTICS-023, RE-BILLING-007

Tagging requirements per rule (non-negotiable):
  - id: canonical RE-{DOMAIN}-{NNN}
  - bounded_context: context name (from context map)
  - source_file: file path (repo-relative)
  - source_line: line number (integer)
  - source_method: method or function name
  - ross_category: CONSTRAINT | COMPUTATION | INFERENCE | ACTION_ENABLER | BEHAVIORAL
  - characterization_test_refs: list of CT-{CONTEXT}-{NNN} that cover this rule
  - seam_ref: SM-{CONTEXT}-{NNN} where this rule was found
  - fact_model_refs: list of FT-{CONTEXT}-{NNN} nodes this rule operates on
  - business_rule: true  # Only rules tagged true reach this step
  - shadow_rule: true | false

Final rule record format:
  rule:
    id: "RE-SALES-001"
    bounded_context: "Sales"
    source_file: "src/sales/OrderProcessor.java"
    source_line: 142
    source_method: "processOrder()"
    code_snippet: |
      if (order.getQuantity() > 100 && customer.getType() == CustomerType.VIP) {
        discount = BASE_DISCOUNT + VIP_BONUS;
      }
    first_pass_statement: "VIP customers with quantity over 100 receive an additional bonus on top of the base discount"
    ross_category: "COMPUTATION"
    classification_reasoning: "Derives a monetary value (discount) from input facts"
    characterization_test_refs: ["CT-SALES-001"]
    seam_ref: "SM-SALES-001"
    fact_model_refs: ["FT-SALES-001", "FT-SALES-REL-001"]
    business_rule: true
    shadow_rule: false
    source_type: "code"
    status: "extracted"  # extracted | duplicate | superseded
```

### Step 4b: Deduplication Matrix

```
ACTION: Identify and consolidate rules that exist in multiple layers (FE + BE + DB)
OUTPUT: Dedup matrix — canonical rule → all source locations
GUIDANCE:
  - A rule enforced in 3 places (front-end validation, back-end service, DB constraint)
    is ONE rule with multiple enforcement points — not 3 rules
  - The canonical ID is the one closest to the authoritative enforcement layer
    (DB > BE > FE, unless domain logic dictates otherwise)
  - Duplicate entries get status: "duplicate" and a canonical_id reference
  - The dedup matrix file MUST be saved at: outputs/decoded/{slug}/extraction/dedup-matrix.md

Format:
  dedup_matrix:
    - canonical_id: "RE-SALES-001"
      canonical_layer: "BE"
      enforcement_points:
        - layer: "FE"
          file: "src/components/OrderForm.tsx"
          line: 88
          duplicate_id: "RE-SALES-001-FE"
        - layer: "DB"
          file: "db/constraints/orders.sql"
          line: 14
          duplicate_id: "RE-SALES-001-DB"
      consolidation_note: "Same constraint enforced at 3 layers. Canonical = BE service."
```

---

## Veto Conditions

- **VETO:** Do NOT begin extraction without a passing characterization test suite from Phase 1. Zero tests = zero protection against breaking changes during extraction.
- **VETO:** Do NOT classify rules before the Phase 0 glossary is available. Classification without defined terms produces wrong taxonomy assignments.
- **VETO:** Do NOT assign a final RE-{DOMAIN}-{NNN} ID to a rule tagged business_rule: false. Implementation details are not rules.
- **VETO:** Do NOT proceed to Phase 3 (Decision Modeling) if any rule is missing source_file, source_line, or source_method. Traceability is non-negotiable.
- **VETO:** Do NOT merge rules from different bounded contexts into a single rule record. One rule = one context.
- **VETO:** Do NOT skip the dedup matrix when multi-layer enforcement is found (see E7 enforcement rule).

---

## Output

```yaml
artifact_path: "outputs/decoded/{slug}/extraction/"

deliverables:
  primary:
    - "Raw Rule List (all seams traversed, all rules tagged)"
    - "Classified Rule List (Ross taxonomy applied to all rules)"
    - "Fact Model (per bounded context)"
    - "Final Rule Catalog — extraction section (all rules with canonical IDs)"
  secondary:
    - "Dedup Matrix (outputs/decoded/{slug}/extraction/dedup-matrix.md)"
    - "Shadow Rule List (rules found only in documentation or stakeholder knowledge)"

quality_criteria:
  - "Every rule has a unique RE-{DOMAIN}-{NNN} ID"
  - "Every rule has file + line + method traceability"
  - "Every rule has exactly one Ross category with documented reasoning"
  - "Every rule maps to at least one Fact Model node"
  - "Every rule is assigned to exactly one bounded context"
  - "No rules exist without a characterization test reference (UNTESTABLE is acceptable with reason)"
  - "Dedup matrix present if multi-layer enforcement was found"
```

---

## Completion Criteria

- [ ] All seams from the Seam Map traversed (none skipped)
- [ ] Every rule encountered has business_rule: true | false tag
- [ ] All rules with business_rule: true have a Ross classification with reasoning
- [ ] Fact Model built for each bounded context (at least one node per rule)
- [ ] Canonical RE-{DOMAIN}-{NNN} IDs assigned to all extracted rules
- [ ] Source traceability complete (file + line + method) for every non-shadow rule
- [ ] Shadow rules documented separately with source_type and shadow_rule: true
- [ ] Dedup matrix created if multi-layer enforcement detected
- [ ] No rules from different bounded contexts merged into a single record
- [ ] Ready for handoff to Phase 3 (Decision Modeling with @barbara-von-halle)

### Approval Gate

```
Extraction is APPROVED when ALL of the following are met:
  - 100% of rules have a canonical RE-{DOMAIN}-{NNN} ID
  - 100% of rules have source_file + source_line traceability (or shadow_rule: true)
  - 100% of rules have a Ross classification with at least one-sentence reasoning
  - Fact Model exists for every major bounded context (even if incomplete)
  - Dedup matrix file present at outputs/decoded/{slug}/extraction/dedup-matrix.md
    (may be empty if no multi-layer duplication found — must exist as a file)
  - decoder-chief sign-off obtained
```

---

## Handoff

```yaml
next_agents: ["@barbara-von-halle", "@james-taylor"]
next_phase: "Phase 3 - Decision Modeling"
context_to_pass:
  - "Classified Rule List (with canonical IDs)"
  - "Fact Model (per bounded context)"
  - "Dedup Matrix"
  - "Shadow Rule List"
  - "Characterization Test Suite (carry forward from Phase 1)"
gate: "decoder-chief approves extraction before decision modeling begins"
```
