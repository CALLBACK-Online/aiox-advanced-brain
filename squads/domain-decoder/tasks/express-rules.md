# Task: Express Rules in Structured Natural Language

> Phase 5 of wf-extract-rules pipeline

**Task ID:** express-rules
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Express every extracted rule in structured, unambiguous natural language using RuleSpeak sentence patterns (Graham Witt) and validate consistency (Ronald Ross)
**Orchestrator:** @decoder-chief
**Primary Agent:** @graham-witt
**Supporting Agent:** @ronald-ross
**Phase:** 4 (Expression)
**Tier:** 3

---

## Inputs

```yaml
required:
  - name: "decision_model"
    description: "Decision Model from Phase 3 (decisions → rule families → rules)"
  - name: "decision_tables"
    description: "DMN Decision Tables from Phase 3"
  - name: "glossary"
    description: "Ubiquitous Language Glossary (validated in Phase 0)"
  - name: "classified_rules"
    description: "Rules with Ross classification and source traceability"
optional:
  - name: "drds"
    description: "Decision Requirements Diagrams from Phase 3"
  - name: "stakeholders"
    description: "Business stakeholders for review"
```

---

## Elicitation (elicit: true)

Before expressing, gather from the user:

1. **Who is the primary audience?** (business analysts, compliance officers, developers, all)
2. **Is there a corporate style guide for policy documents?** (may affect sentence structure)
3. **Language?** (English, Portuguese, or bilingual — see Bilingual Guidance below)
4. **Are there existing rule statements to match in style?** (consistency with prior work)

### Bilingual Language Guidance

```
For codebases with mixed languages (e.g., PT-BR source code + EN documentation):
  1. Identify the PRIMARY language: the language of the source code identifiers
     and the majority of business documentation.
  2. Identify the SECONDARY language: used in comments, stakeholder interviews,
     or informal documentation.
  3. Rule of authority:
     - Technical terms (class names, method names, database fields): use PRIMARY language as-is
     - Business rule descriptions: use the language of the business stakeholders
       (typically the SECONDARY language if code is in EN but business is PT-BR)
  4. NEVER mix languages within a single rule statement.
     BAD:  "O customer MUST ter um valid email antes de placing an order."
     GOOD: "O cliente DEVE fornecer um endereco de email valido antes de registrar um pedido."
     GOOD: "A customer MUST provide a valid email address before placing an order."
  5. If the glossary has terms in both languages, reference both:
     term: "cliente (customer)" — use the PRIMARY language term in rule statements
```

---

## Steps

### Step 1: Apply RuleSpeak Sentence Patterns (Graham Witt)

```
ACTION: Express every rule using one of the standard sentence patterns
OUTPUT: All rules with final statement field filled
AGENT: @graham-witt

RuleSpeak Core Patterns:

  OBLIGATION:
    Pattern: "[Subject] MUST [verb phrase]."
    Example: "A customer MUST provide a valid email address before placing an order."
    Use for: Constraints that mandate action

  PROHIBITION:
    Pattern: "[Subject] MUST NOT [verb phrase]."
    Example: "An order MUST NOT be shipped without payment confirmation."
    Use for: Constraints that forbid action

  PERMISSION:
    Pattern: "[Subject] MAY [verb phrase]."
    Example: "A manager MAY override the discount limit for orders above R$10,000."
    Use for: Permissions and exceptions

  CONDITION:
    Pattern: "It is [required/prohibited/permitted] that [condition]."
    Example: "It is required that the total order value includes applicable taxes."
    Use for: Conditions and prerequisites

  DERIVATION:
    Pattern: "[Term] is [derived as] [expression]."
    Example: "The shipping rate is derived as base_rate multiplied by weight_factor."
    Use for: Computations and calculations

  FACT:
    Pattern: "[Subject] [verb] [object/complement]."
    Example: "Each customer belongs to exactly one customer tier."
    Use for: Structural facts (definitions, classifications)

  CONDITIONAL OBLIGATION:
    Pattern: "If [condition], then [subject] MUST [verb phrase]."
    Example: "If an order exceeds R$50,000, then it MUST be approved by two managers."
    Use for: Conditional constraints

  CONDITIONAL DERIVATION:
    Pattern: "If [condition], then [term] is [expression]."
    Example: "If the customer is VIP, then the discount is 15%."
    Use for: Conditional computations

Apply ONE pattern per rule. If a rule needs 'and', split into two rules.
```

### Step 2: Eliminate Ambiguity (Graham Witt)

```
ACTION: Scan every rule statement for ambiguous language and replace
OUTPUT: Ambiguity review log
AGENT: @graham-witt

BANNED WORDS (signal ambiguity — replace with precise terms):
  - "appropriate" → specify the exact criteria
  - "reasonable" → specify the threshold
  - "sufficient" → specify the minimum quantity
  - "timely" → specify the time limit (e.g., "within 24 hours")
  - "significant" → specify the threshold (e.g., "> R$10,000")
  - "adequate" → specify the minimum requirements
  - "proper" → specify the exact requirements or format
  - "valid" → specify what makes it valid (e.g., "non-expired, government-issued")
  - "applicable" → specify which cases apply
  - "authorized" → specify who authorizes and under what conditions
  - "current" → specify the recency requirement (e.g., "issued within 30 days")
  - "recent" → specify the time window (e.g., "within the last 7 days")
  - "usually" → remove or specify the exception
  - "generally" → remove or specify the exception
  - "normally" → remove or specify the exception
  - "often" → specify frequency or remove
  - "sometimes" → specify condition or remove
  - "may impact" → specify HOW it impacts
  - "could affect" → specify WHAT it affects
  - "etc." → list all items explicitly
  - "and/or" → use "or" (inclusive) or list separately
  - "as needed" → specify the trigger condition
  - "up to" → specify exact maximum

Format:
  ambiguity_log:
    - rule_id: "RE-SALES-003"
      original: "Customer must provide appropriate documentation"
      ambiguous_term: "appropriate"
      replacement: "Customer must provide government-issued photo ID and proof of address dated within 90 days"
      justification: "Policy document Section 3.2 specifies these exact requirements"
```

### Step 3: Validate Pattern Consistency (Ronald Ross)

```
ACTION: Review all rule statements for structural consistency
OUTPUT: Consistency review report
AGENT: @ronald-ross

Checks:
  1. ONE RULE = ONE SENTENCE. If it contains 'and' connecting two obligations, split it.
  2. CONSISTENT VOCABULARY. Use only terms from the glossary.
  3. CONSISTENT PATTERN. Same rule type = same sentence pattern.
  4. MODAL VERBS. Use MUST/MUST NOT/MAY consistently (never "should", "shall", "will").
  5. SUBJECT CLARITY. Every rule has an explicit subject (never "it" or "this").
  6. NO PASSIVE VOICE for obligations. "Customer MUST submit" not "Must be submitted".

Format:
  consistency_review:
    total_rules: N
    consistent: N
    issues_found:
      - rule_id: "RE-SALES-005"
        issue: "Uses 'shall' instead of 'MUST'"
        fix: "Replace 'shall' with 'MUST'"
      - rule_id: "RE-LOG-012"
        issue: "Contains 'and' connecting two obligations"
        fix: "Split into RE-LOG-012a and RE-LOG-012b"
```

### Step 4: Cross-Reference Glossary (Graham Witt)

```
ACTION: Verify every term in rule statements appears in the glossary
OUTPUT: Cross-reference check
AGENT: @graham-witt

Process:
  1. Extract all nouns and noun phrases from all rule statements
  2. Check each against the glossary
  3. If a term is NOT in the glossary:
     a. Add it to the glossary (with definition and source)
     b. OR rewrite the rule to use a defined term
  4. If a term is in the glossary but used with a DIFFERENT meaning:
     a. Document the conflict
     b. Resolve with stakeholder input

Format:
  glossary_check:
    total_terms_in_rules: N
    in_glossary: N
    missing_from_glossary:
      - term: "weight_factor"
        used_in: ["RE-LOG-001", "RE-LOG-005"]
        action: "Added to glossary with definition"
    definition_conflicts: []
```

### Step 5: Stakeholder Review Sample

```
ACTION: Select a representative sample (minimum 10% of rules) for stakeholder review
OUTPUT: Stakeholder review results
AGENT: @graham-witt

Selection criteria for sample:
  - At least 1 rule per bounded context
  - Include all high-priority rules
  - Include at least 1 of each rule type (constraint, computation, inference, etc.)
  - Prioritize rules that were ambiguous or complex

Review format:
  stakeholder_review:
    reviewer: "Name / Role"
    date: "YYYY-MM-DD"
    sample_size: N
    rules_reviewed: ["RE-SALES-001", "RE-LOG-003", ...]
    feedback:
      - rule_id: "RE-SALES-001"
        status: "APPROVED"
        notes: ""
      - rule_id: "RE-LOG-003"
        status: "NEEDS_REVISION"
        notes: "The threshold should be R$5,000 not R$10,000"
    overall_status: "APPROVED|NEEDS_REVISION"

REVIEW TIMEOUT POLICY:
  - Stakeholder review request sent on: {date}
  - Timeout: 48 hours (2 business days)
  - If no response within 48h:
    1. Escalate to decoder-chief with list of pending items
    2. For NON-CRITICAL rules: mark as PROVISIONAL and proceed
       (stakeholder can revise later without blocking pipeline)
    3. For CRITICAL rules (regulatory, revenue-impacting):
       Do NOT proceed — CRITICAL rules require explicit stakeholder sign-off
    4. Document in output: "PROVISIONAL — awaiting stakeholder review since {date}"
```

---

## Contradiction Resolution Protocol

Before expressing rules (Step 1), verify all contradictions from prior phases are resolved:

### Resolution Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `RESOLVED (scope_boundary)` | Contradiction exists because rules apply in different bounded contexts (e.g., rule A in module X, rule B in module Y) | Document the scope of each rule. Both rules remain valid within their context. |
| `UNRESOLVED (needs_human)` | Real contradiction that cannot be resolved by scoping -- requires human decision | Escalate with evidence: both rule statements, sources, and the conflict description. |

### Inline Annotation Format

Every resolved contradiction MUST have a bidirectional inline annotation in the rule statement output:

```
<!-- contradiction:RS-XXX resolved:scope_boundary ref:RS-YYY -->
```

Where:
- `RS-XXX` is the rule being annotated
- `resolved:scope_boundary` or `resolved:supersedes` is the resolution type
- `ref:RS-YYY` is the other rule in the contradiction pair

Both rules in the pair MUST carry the annotation (bidirectional cross-reference).

### Unresolved Contradictions

If any contradiction is `UNRESOLVED (needs_human)`:
- The pipeline MAY proceed to expression for non-affected rules
- The contradicting rules MUST be flagged in the output as PENDING_RESOLUTION
- The final delivery MUST list all unresolved contradictions in the Open Issues section

---

## Veto Conditions

- **VETO:** Do NOT express a rule using a term not in the glossary. Add the term first.
- **VETO:** Do NOT use ambiguous qualifiers (see banned words list). Replace with precise language.
- **VETO:** Do NOT write rules in passive voice for obligations. Use active voice with explicit subject.
- **VETO:** Do NOT combine two rules in one sentence with 'and'. One rule = one sentence.
- **VETO:** Do NOT use "should" or "shall". Use MUST/MUST NOT/MAY only.
- **VETO:** Do NOT proceed to Phase 5 without stakeholder review of at least 10% sample.
- **VETO:** Do NOT finalize if > 5% of rules use Conditional Derivation pattern without EXACTLY ONE derivation per condition branch — this indicates structural misapplication. A Conditional Derivation ("If X, then Y is Z") must have one and only one derived value per branch. Multiple derivations in one statement = multiple rules that need splitting.

---

## Output

```yaml
artifact_path: "outputs/rules/{domain}/rule-catalog.md"

deliverables:
  primary:
    - "All rules with final statement field (RuleSpeak format)"
    - "Ambiguity review log"
    - "Consistency review report"
    - "Glossary cross-reference check"
  secondary:
    - "Stakeholder review results"
    - "Updated glossary (with new terms found during expression)"

quality_criteria:
  - "Every rule has a final statement in RuleSpeak format"
  - "Zero ambiguous qualifiers in any rule statement"
  - "All terms in rule statements appear in glossary"
  - "Pattern consistency confirmed across all rules"
  - "At least 10% of rules reviewed by business stakeholder"
  - "No passive voice in obligation rules"
```

---

## Completion Criteria

- [ ] All rules expressed in RuleSpeak sentence patterns
- [ ] Ambiguity review complete — zero banned words in FINAL output (the `statement` field of each rule must pass a pre-lint check against the banned words list before being considered complete)
- [ ] Pattern consistency validated by Ronald Ross
- [ ] Glossary cross-reference complete (no missing terms)
- [ ] Stakeholder review of minimum 10% sample (or PROVISIONAL status with timeout documented)
- [ ] No Conditional Derivation misapplication (each branch has exactly one derivation)
- [ ] All contradictions have resolution status (RESOLVED or UNRESOLVED) with inline cross-references
- [ ] `node squads/domain-decoder/scripts/rule-lint.js` passes on final rules-expressed.md (exit code 0)
- [ ] Cold reader validation: 10 random rules comprehensible by non-participant (>= 8/10 pass)
- [ ] Ready for handoff to Phase 5 (validation & delivery)

---

## Handoff

```yaml
next_agent: "@decoder-chief"
next_phase: "Phase 5 - Validation & Delivery"
context_to_pass:
  - "All rule statements (final)"
  - "Updated glossary"
  - "Ambiguity and consistency reports"
  - "Stakeholder review results"
gate: "decoder-chief runs SBVR validation and extraction quality checklists"
```
