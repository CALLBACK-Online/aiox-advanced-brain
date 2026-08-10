# SBVR Validation Checklist

**Purpose:** Validate extracted business rules against the OMG SBVR 1.5 standard
**When to use:** AFTER all rules are extracted and expressed, BEFORE final delivery
**Tool type:** Checklist (not an agent)
**Standard:** OMG SBVR 1.5 (Semantics of Business Vocabulary and Business Rules)
**Command:** `*sbvr-check`

---

## How to Use This Checklist

1. Run this checklist AFTER `*express-rules` (Graham Witt) completes
2. Work through sections 1-8 in order
3. Mark each item `[x]` when confirmed, `[-]` when not applicable
4. Calculate score at the end
5. PASS threshold is 38/45 (85%+)
6. Any CRITICAL item failure is an automatic disqualifier — fix before delivering

---

## 1. Vocabulary Validation

*Business vocabulary is the foundation. Rules are only as good as their terms.*

- [ ] All business terms used in rules are formally defined with precise definitions
- [ ] Each term has exactly one meaning within its bounded context
- [ ] Terms use noun phrases (not verbs or standalone adjectives)
- [ ] Synonyms are documented with canonical term identified and cross-referenced
- [ ] Homonyms are identified with context disambiguation (e.g., "Order" in Sales vs. Warehouse)
- [ ] Terms are organized by bounded context / subject area
- [ ] Definitions avoid circular references (term A defined using term B, B defined using A)

**Section score: __ / 7**

---

## 2. Fact Type Validation

*Fact types capture the relationships between business terms. They are the grammar of the business.*

- [ ] Relationships between terms are documented as named fact types
- [ ] Fact types use verb phrases connecting subject and object terms (e.g., "Customer places Order")
- [ ] Cardinality is specified for each fact type (one-to-one, one-to-many, many-to-many)
- [ ] Each fact type is necessary — no redundant or derivable facts
- [ ] Fact types are consistent across bounded contexts (no contradictory relationship definitions)

**Section score: __ / 5**

---

## 3. Rule Expression Validation

*This is the heart of SBVR compliance. Every rule must be precise, atomic, and unambiguous.*

- [ ] **[CRITICAL]** Rules use only vocabulary terms defined in the glossary
- [ ] Rules are expressed in structured natural language (RuleSpeak or equivalent)
- [ ] **[CRITICAL]** Each rule expresses exactly one constraint or obligation (atomic — no "and" combining two rules, no semicolons combining statements). Compound rules must be split or annotated with `<!-- compound:intentional reason="..." -->`
- [ ] Rules use modal verbs correctly:
  - `MUST` / `MUST NOT` for obligations and prohibitions
  - `MAY` for permissions
  - `SHOULD` only for non-normative recommendations (subtype: guideline). For normative constraints, use only MUST/MUST NOT/MAY per SBVR specification. Note: express-rules.md prohibits SHOULD entirely — when running SBVR validation, SHOULD is permitted ONLY if the rule is classified as a guideline recommendation, not a constraint. See express-rules.md Section "Modal Verbs" for full guidance.
- [ ] Rules are free of implementation details (no class names, method names, database columns)
- [ ] Rules are free of ambiguous qualifiers (`appropriate`, `reasonable`, `sufficient`, `timely`, `significant`)
- [ ] **[CRITICAL]** Each rule cites its source of authority (code location, policy document, or SME name)

**Section score: __ / 7**

---

## 4. Rule Classification Validation

*Every rule must be classified. Misclassification leads to wrong implementation strategy.*

- [ ] Each rule is classified into exactly one primary category
- [ ] **Structural rules** correctly identified: definitions, facts, derivations (what IS true)
- [ ] **Behavioral rules** correctly identified: constraints, enablers, computations (what MUST be true)
- [ ] **Decision rules** correctly identified: tables, trees, inference chains (how conclusions are reached)
- [ ] Classification is consistent — same pattern of rule classified the same way throughout

**Section score: __ / 5**

---

## 5. Completeness Validation

*A partial rule catalog is worse than no catalog — it creates false confidence.*

- [ ] All bounded contexts identified in domain mapping (Eric Evans phase) are covered. Verify against `outputs/rules/{domain}/domain-map.md`
- [ ] No known rules are missing from documentation (verified against source inventory)
- [ ] Decision tables are complete — all condition combinations have a defined outcome (no gaps)
- [ ] Exception rules are documented (what happens when the normal rule cannot apply)
- [ ] Default behaviors are documented (what happens in absence of a specific rule)
- [ ] Edge cases from characterization tests (Michael Feathers phase) are covered by rules
- [ ] Extraction completeness: Rule Location Index covers >= 90% of source files classified in classify-rules output

**Section score: __ / 7**

---

## 6. Consistency Validation

*Contradictory rules cannot both be implemented. Redundant rules create maintenance nightmares.*

- [ ] **[CRITICAL]** No contradictory rules exist (two rules that cannot both be satisfied simultaneously)
- [ ] No redundant rules (same constraint expressed differently in two places — pick one, reference the other)
- [ ] Terminology is consistent across all rules (same concept uses same term everywhere)
- [ ] Rule numbering follows standard format: `RE-{DOMINIO}-{NNN}` (e.g., `RE-CREDITO-001`)
- [ ] Cross-references between related rules are complete and bidirectional

**Section score: __ / 5**

---

## 7. Traceability Validation

*Every rule must be traceable to origin. Without traceability, the catalog cannot be maintained.*

- [ ] **[CRITICAL]** Each rule has a unique identifier in format `RE-{DOMINIO}-{NNN}`
- [ ] Each rule traces to at least one source: code file + line number, policy document section, or named SME
- [ ] Dependencies between rules are documented (rule A requires rule B to hold)
- [ ] Rules that share a decision table are cross-referenced to each other
- [ ] Impact analysis is possible: given a change to rule X, affected rules can be identified

**Section score: __ / 5**

---

## 8. Stakeholder Readability Validation

*Rules must be read by two audiences: business stakeholders who own them and engineers who implement them.*

- [ ] Business stakeholders (non-technical) can understand each rule statement without explanation
- [ ] Technical stakeholders have enough information to implement each rule unambiguously
- [ ] No unexplained jargon — every domain-specific term appears in the glossary
- [ ] Format is consistent and scannable (all rules follow same structure)

**Section score: __ / 4**

---

## Scoring Summary

| Section | Items | Score |
|---------|-------|-------|
| 1. Vocabulary Validation | 7 | __ / 7 |
| 2. Fact Type Validation | 5 | __ / 5 |
| 3. Rule Expression Validation | 7 | __ / 7 |
| 4. Rule Classification Validation | 5 | __ / 5 |
| 5. Completeness Validation | 7 | __ / 7 |
| 6. Consistency Validation | 5 | __ / 5 |
| 7. Traceability Validation | 5 | __ / 5 |
| 8. Stakeholder Readability | 4 | __ / 4 |
| **TOTAL** | **45** | **__ / 45** |

> **Pass threshold: 38/45 (85%)**

---

## Pass/Fail Determination

**CRITICAL items — automatic failure if ANY of these are unchecked:**

| # | Critical Item | Section |
|---|---------------|---------|
| C1 | Rules use only defined vocabulary terms | 3 |
| C2 | Each rule is atomic (one constraint only) | 3 |
| C3 | Each rule cites its source of authority | 3 |
| C4 | No contradictory rules exist | 6 |
| C5 | Each rule has a unique identifier | 7 |

**Overall result:**

```
Critical items passed:  __ / 5
Total score:            __ / 45  (__%)

PASS threshold:         38 / 45 (85%)
Critical threshold:     5 / 5 (all must pass)

Final result: [ ] PASS  [ ] FAIL
Failure reason (if failed): ___________________
```

---

## Modelo de Scoring Parcial

When items are marked as not applicable `[-]`, the scoring adjusts dynamically:

```
applicable_items = total_items - skipped_items
score = (passed_items / applicable_items) * 100
```

- Each checked item `[x]` = 1 point
- Each unchecked item `[ ]` = 0 points
- Each skipped item `[-]` = removed from denominator (not counted against score)
- There is NO section-level pass/fail. Each item is evaluated individually.
- The 85% threshold applies to the adjusted score (applicable items only)
- CRITICAL items (C1-C5) are NEVER optional and cannot be skipped

---

## After Failing

If the checklist fails:

1. **Critical failure** → Return to the agent responsible for that section
   - Vocabulary issues → @eric-evans or @graham-witt
   - Atomicity / expression issues → @graham-witt
   - Missing sources → @michael-feathers
   - Contradictions → @ronald-ross + @barbara-von-halle
   - Missing IDs → @decoder-chief (administrative fix)

2. **Score below threshold** → Identify lowest-scoring sections, address them, re-run checklist

3. **Stakeholder review rejection** → If a stakeholder rejects the validation: create a specific issue list detailing each rejected item, return to the `*express-rules` agent with the exact list of rules to correct. Do NOT revalidate the entire batch — only re-run `*sbvr-check` on the corrected subset.

4. **Re-run command:** `*sbvr-check` after fixes are applied

### Re-spawn Context Template

When re-spawning an agent to fix failures, include this context block:

```yaml
re_spawn_context:
  checklist: "sbvr-validation"
  run_date: "YYYY-MM-DD"
  result: "FAIL"
  score: "__/45 (__%)"
  failed_items:
    - section: "{section number and name}"
      item: "{specific checklist item that failed}"
      severity: "CRITICAL | BELOW_THRESHOLD"
  original_agent: "{agent name that produced the failing output}"
  input_artifacts:
    - path: "{path to the artifact that was validated}"
      description: "{what this artifact contains}"
  suggested_fix_action: |
    {Specific instruction for the re-spawned agent, e.g.:
    "Review rules RE-SALES-003 and RE-SALES-007 — both use terms
    not found in the glossary. Either add terms to glossary or
    rewrite rules using existing defined terms."}
```

This context ensures the re-spawned agent has full awareness of what failed, why, and what artifacts to read before attempting fixes.

---

*SBVR Validation Checklist v1.0.0*
*Standard: OMG SBVR 1.5*
*Squad: code-anatomist*
*Used by: decoder-chief (command: *sbvr-check)*
