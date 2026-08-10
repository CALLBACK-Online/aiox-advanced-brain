# Task: Classify Business Rules

> Phase 1 of wf-extract-rules pipeline

**Task ID:** classify-rules
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Classify all business rules in a system using Ronald Ross's taxonomy (RuleSpeak)
**Orchestrator:** @decoder-chief
**Primary Agent:** @ronald-ross
**Phase:** 0 (Discovery)
**Tier:** 0

---

## Inputs

```yaml
required:
  - name: "system_name"
    description: "Name of the system being analyzed"
    example: "OrderManagement v2.3"
  - name: "source_samples"
    description: "Sample code files, documents, or stored procedures (minimum 10-20 files)"
    example: "/repos/order-mgmt/src/core/"
optional:
  - name: "known_rule_areas"
    description: "Business areas suspected to contain rules"
    example: ["pricing", "credit approval", "shipping"]
  - name: "existing_glossary"
    description: "Existing glossary from map-domain task (if already completed)"
```

---

## Elicitation (elicit: true)

Before classifying, gather from the user:

1. **System type?** (source code, stored procedures, documents, ERP config, spreadsheets, tribal knowledge)
2. **Primary business domain?** (finance, sales, logistics, HR, etc.)
3. **Estimated rule density?** (low: <50, medium: 50-200, high: 200+)
4. **Are there known regulatory rules?** (compliance requirements that MUST be captured)
5. **Has map-domain already been completed?** (domain map is a required input — if not available, this task CANNOT start. Defer to map-domain first.)

---

## Steps

### Step 1: Sample Analysis

```
ACTION: Read 10-20 representative files from the source
OUTPUT: Initial impression of rule types present
GUIDANCE:
  - Look for if/then/else blocks (likely constraints or inferences)
  - Look for calculations/formulas (likely computations)
  - Look for event triggers (likely action enablers)
  - Look for process flows (likely behavioral rules)
  - Note which files have the MOST business logic density

SAMPLING HEURISTICS:
  Prefer directories (highest rule density):
    - domain/, core/, rules/, services/, lib/, models/, logic/
    - stored procedures, triggers, views (database layer)
  Exclude directories (noise, not business logic):
    - tests/, __tests__/, spec/, test-fixtures/
    - node_modules/, vendor/, dist/, build/
    - migrations/ (structural, not business rules)
    - DTOs/, types/, interfaces/ (data shape, not logic)
  If fewer than 10 files in preferred directories:
    - Expand to controllers/, handlers/, api/
    - Document the expanded scope in notes
```

### Step 2: Apply Ross Taxonomy

Classify each identified rule into one of these categories:

| Type | Definition | Code Signals |
|------|-----------|--------------|
| **CONSTRAINT** | Must always be true (validation, prohibition) | `if (!valid) throw`, `assert`, `validate()` |
| **COMPUTATION** | Derives a value (calculation, formula) | `result = a * b`, `calculateX()`, formulas |
| **INFERENCE** | Concludes a fact from other facts | `if (A && B) then C`, derived status |
| **ACTION ENABLER** | Triggers action when condition met | `if (condition) notify()`, event handlers |
| **BEHAVIORAL** | Governs how a process must be conducted | workflow steps, approval chains, sequencing |

### Step 3: Build Rule Type Inventory

```yaml
# Output format
rule_type_inventory:
  system: "{system_name}"
  date: "YYYY-MM-DD"
  classified_by: "ronald-ross"

  summary:
    total_rules_estimated: N
    constraints: N
    computations: N
    inferences: N
    action_enablers: N
    behavioral: N

  by_domain:
    - domain: "{bounded_context_name}"
      dominant_type: "constraint"
      estimated_count: N
      complexity: "low|medium|high"
      notes: "..."

  high_priority_areas:
    - area: "..."
      reason: "High rule density / regulatory / cross-domain"
```

### Step 4: Identify Rule Relationships

```
ACTION: Map which rules depend on other rules
OUTPUT: Dependency graph (which rules feed into which)
GUIDANCE:
  - Computations often feed into constraints (calculated value → validation)
  - Inferences often feed into action enablers (derived fact → trigger)
  - Look for chains: if A then B, if B then C
```

### Step 4b: Validate Dependency References

```
ACTION: Verify all cross-rule dependencies point to existing classified rules
OUTPUT: Dependency validation report
GUIDANCE:
  - Every rule referenced in a dependency chain must exist in the inventory
  - If rule density is medium or high (50+ rules), expect at least 3 cross-rule dependencies
  - Missing references indicate either:
    a. An unsampled file (go back to Step 1, expand sample set)
    b. A mis-classification (re-check the referenced rule type)
  - Log all orphaned references for follow-up in characterize-legacy
```

### Step 5: Prioritize Extraction Order

```
ACTION: Recommend extraction priority
OUTPUT: Ordered list of domains/areas to extract first
GUIDANCE:
  Priority criteria (highest to lowest):
  1. Regulatory/compliance rules (legal risk)
  2. Revenue-impacting rules (pricing, discounts)
  3. Cross-domain rules (affect multiple contexts)
  4. High-density areas (most rules per file)
  5. Frequently-changing rules (maintenance cost)
```

---

## Veto Conditions

- **VETO:** Do NOT classify without reading actual source samples. Blind classification is forbidden.
- **VETO:** Do NOT finalize if fewer than 10 source files were sampled — insufficient coverage for reliable classification.
- **VETO:** Do NOT assign a type if uncertain. Mark as `UNCLASSIFIED` with notes for human review.
- **VETO:** Do NOT mix Ross categories. One rule = one type. If a rule seems to be two types, it is two rules.
- **VETO:** Do NOT proceed to extraction (Phase 2) without completing this classification.
- **VETO:** Do NOT start classification if map-domain output is unavailable — domain context is required to assign rules to bounded contexts.

---

## Output

```yaml
artifact_path: "outputs/rules/{domain}/classified-rules.md"

deliverables:
  primary:
    - "Rule Type Inventory (YAML format as shown above)"
  secondary:
    - "High priority areas list with justification"
    - "Rule relationship/dependency notes"
    - "Extraction order recommendation"

quality_criteria:
  - "Every rule type in Ross taxonomy is addressed (even if count = 0)"
  - "At least 10 source samples were read before classifying"
  - "Dominant rule type per domain identified"
  - "Priority ranking with clear criteria"
```

---

## Completion Criteria

- [ ] At least 10 source files sampled before classification (matches quality_criteria)
- [ ] Ross taxonomy applied to all identified rule candidates
- [ ] Rule Type Inventory created in standard format
- [ ] Dependency references validated (Step 4b complete)
- [ ] High priority areas identified with justification
- [ ] Extraction order recommended
- [ ] No `UNCLASSIFIED` rules without explanatory notes
- [ ] Ready for handoff to Phase 1 (characterization)

---

## Handoff

```yaml
next_agent: "@michael-feathers"
next_task: "characterize-legacy.md"
context_to_pass:
  - "Rule Type Inventory"
  - "High priority areas"
  - "Extraction order"
gate: "decoder-chief approves classification before proceeding"
```
