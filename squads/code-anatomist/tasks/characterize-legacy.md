# Task: Characterize Legacy Code

> Phase 3 of wf-extract-rules pipeline

**Task ID:** characterize-legacy
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Create safety nets (characterization tests) and find seams in legacy code before extracting business rules
**Orchestrator:** @decoder-chief
**Primary Agent:** @michael-feathers
**Supporting Agent:** @martin-fowler
**Phase:** 1 (Characterization)
**Tier:** 1

---

## Inputs

```yaml
required:
  - name: "source_location"
    description: "Path to the legacy codebase"
    example: "/repos/order-mgmt/src/"
  - name: "context_map"
    description: "Context map from map-domain task (Phase 0 output)"
  - name: "rule_type_inventory"
    description: "Rule type inventory from classify-rules task (Phase 0 output)"
  - name: "source_mapping"
    description: "Source-to-context mapping from map-domain task"
optional:
  - name: "priority_areas"
    description: "High priority areas from classify-rules (extraction order)"
  - name: "language"
    description: "Programming language of the legacy system"
    example: "Java, C#, COBOL, Python, SQL"
```

---

## Elicitation (elicit: true)

Before characterizing, gather from the user:

1. **Can you run the legacy code locally?** (needed for characterization tests — if NO, see "Read-Only / Untestable Environments" section below)
2. **Is there a test suite already?** (even partial coverage helps)
3. **What's the deployment model?** (monolith, distributed, mainframe)
4. **Are there known fragile areas?** (code everyone is afraid to touch)

### Read-Only / Untestable Environments

```
If the codebase CANNOT be executed locally (mainframe, no local env, proprietary runtime):
  1. Mark test_status as UNTESTABLE (not UNTESTED) for all characterization tests
  2. Document the reason: "Environment: {reason code cannot run}"
  3. Use STATIC ANALYSIS FALLBACK:
     - Read code paths manually (trace logic without executing)
     - Identify rule candidates from code structure alone
     - Use code comments, variable names, and method signatures as evidence
     - Cross-reference with documentation and stakeholder interviews
  4. Characterization "tests" become CHARACTERIZATION TRACES:
     - Same format as CT-{CONTEXT}-{NNN} but with trace: true
     - input/output fields become expected_input/expected_output (inferred, not observed)
     - Add confidence_level: LOW | MEDIUM | HIGH
  5. CRITICAL: Static-only characterization carries LOWER confidence.
     Flag in output: "STATIC ANALYSIS ONLY — {N} traces require runtime validation"
```

---

## Steps

### Step 1: Architecture Pattern Identification (Martin Fowler)

```
ACTION: Identify the dominant architecture pattern
OUTPUT: Architecture classification with evidence
AGENT: @martin-fowler

Patterns to look for:
  - TRANSACTION SCRIPT: Business logic in procedural scripts/functions
    Signal: Large functions doing read-process-write, no domain objects
  - DOMAIN MODEL: Rich domain objects with behavior
    Signal: Classes with both data and business methods
  - TABLE MODULE: One class per table with all logic
    Signal: Classes named after tables with CRUD + business logic
  - SERVICE LAYER: Thin services orchestrating domain logic
    Signal: Service classes calling domain objects
  - ACTIVE RECORD: Objects that know how to persist themselves
    Signal: Domain objects with save(), load(), find() methods

Format:
  architecture:
    primary_pattern: "Transaction Script"
    evidence:
      - "OrderProcessor.java: 800-line processOrder() method"
      - "No domain objects — all logic in service functions"
      - "Database accessed directly from business logic"
    rule_implication: "Rules are EMBEDDED in procedural code — seams needed to isolate"
```

### Step 2: Write Characterization Tests (Michael Feathers)

```
ACTION: Write characterization tests that document CURRENT behavior
OUTPUT: Passing test suite (minimum 5 per bounded context)
AGENT: @michael-feathers

CRITICAL RULES:
  1. Characterization tests document what the code DOES, not what it SHOULD do
  2. If a test reveals a bug, the test passes WITH the bug (document it, don't fix it)
  3. Cover the CRITICAL PATHS first (revenue, compliance, cross-domain)
  4. Each test should capture ONE behavior

Process:
  1. Pick a code path with suspected business rules
  2. Call it with sample inputs
  3. Record the actual output
  4. Write a test that asserts the actual output
  5. Run the test — it MUST pass (if not, your setup is wrong)
  6. Document what business rule this test reveals

Format per test:
  characterization_test:
    id: "CT-{CONTEXT}-{NNN}"
    bounded_context: "Sales"
    code_path: "OrderProcessor.processOrder()"
    file: "src/sales/OrderProcessor.java"
    line: 142
    input: "Order with quantity=150, customer_type=VIP"
    actual_output: "discount = 7.5%"
    business_rule_revealed: "VIP customers with quantity > 100 get 5% base + 2.5% VIP bonus"
    test_status: "PASSING"  # Valid values: PASSING | FAILING | UNTESTED | PARTIAL | UNTESTABLE
    notes: "Possible bug: non-VIP with quantity > 100 gets 0% — seems wrong"

  # test_status enum:
  #   PASSING    — Test written and passes (green)
  #   FAILING    — Test written but fails (documents a known issue)
  #   UNTESTED   — Test not yet written
  #   PARTIAL    — Test covers some paths but not all
  #   UNTESTABLE — Code cannot be executed (see Read-Only / Untestable Environments)
```

### Step 3: Find Seams (Michael Feathers)

```
ACTION: Identify seams — points where code can be split without full rewrite
OUTPUT: Seam map listing all seams with types
AGENT: @michael-feathers

Feathers' Seam Types:
  - OBJECT SEAM: Override a method in a subclass
  - PREPROCESSING SEAM: Change what gets compiled/included
  - LINK SEAM: Swap a dependency at link time
  - PARAMETER SEAM: Pass a different object to change behavior

Format:
  seam_map:
    - id: "SM-{CONTEXT}-{NNN}"
      location: "OrderProcessor.java:calculateDiscount()"
      type: "OBJECT_SEAM"
      description: "calculateDiscount() can be overridden to isolate pricing rules"
      rules_accessible: ["RE-SALES-001", "RE-SALES-002"]
      risk: "low"
      notes: "Method is public, no side effects"
```

### Step 4: Map Code Smells to Rule Candidates (Martin Fowler)

```
ACTION: Identify code smells that signal hidden business rules
OUTPUT: Code smell to rule candidate mapping
AGENT: @martin-fowler

Key mappings:
  | Code Smell | Rule Signal |
  |-----------|-------------|
  | Feature Envy | Rule about another domain leaking in |
  | Switch Statement | Decision rule (decision table candidate) |
  | Parallel Inheritance | Structural rule about hierarchy |
  | Long Method | Multiple rules bundled together |
  | Primitive Obsession | Business concept not modeled (missing domain term) |
  | Data Clumps | Related facts that form a business concept |
  | Shotgun Surgery | Cross-cutting rule spread across files |
  | Refused Bequest | Misclassified rule (wrong context) |

Format:
  smell_to_rule:
    - smell: "Switch Statement"
      location: "ShippingService.java:calculateRate()"
      description: "Switch on customer_tier (Gold, Silver, Bronze)"
      rule_candidate: "Shipping rate varies by customer tier — decision table"
      bounded_context: "Logistics"
      priority: "high"
```

### Step 4b: Minor Context Threshold Review

```
ACTION: Review rule candidates classified as MINOR for false positives
OUTPUT: Escalation list for low-confidence minor rules
GUIDANCE:
  - Rules classified as MINOR with fewer than 2 context references
    (code locations where the rule is exercised) should be ESCALATED
    for human review — they may be false positives (noise, not rules)
  - Threshold: < 2 context references = potential false positive
  - Escalation action: Add to escalation_list with reason
  - Do NOT discard — escalate. The human decides if it's real.
  - Minor contexts with < 5 business logic files: 3 characterization
    tests are sufficient (instead of the normal 5 per context minimum)

Format:
  escalation_list:
    - rule_candidate: "RC-{CONTEXT}-{NNN}"
      context_references: N
      reason: "Only found in one utility method — may be implementation detail, not business rule"
      recommendation: "REVIEW"
```

### Step 5: Create Rule Location Index

```
ACTION: Compile all findings into a master index of where rules live
OUTPUT: Rule Location Index

Format:
  rule_location_index:
    system: "{system_name}"
    total_locations: N
    locations:
      - file: "src/sales/OrderProcessor.java"
        context: "Sales"
        methods_with_rules:
          - method: "processOrder()"
            line_range: "100-250"
            estimated_rules: 5
            risk_level: "HIGH"  # LOW | MEDIUM | HIGH | CRITICAL
            characterization_tests: ["CT-SALES-001", "CT-SALES-002"]
            seams: ["SM-SALES-001"]
            smells: ["Long Method", "Switch Statement"]

  # risk_level criteria:
  #   CRITICAL — Regulatory/compliance rules, revenue-impacting, no test coverage
  #   HIGH     — Cross-domain rules, high rule density, known fragile areas
  #   MEDIUM   — Single-domain rules with partial test coverage
  #   LOW      — Isolated rules with existing test coverage and clear seams
```

---

## Veto Conditions

- **VETO:** Do NOT extract rules in this phase. This phase only LOCATES and CHARACTERIZES.
- **VETO:** Do NOT write characterization tests that assert DESIRED behavior. They must assert ACTUAL behavior.
- **VETO:** Do NOT modify the legacy code. Characterization is READ-ONLY.
- **VETO:** Do NOT skip writing characterization tests. They are the safety net for Phase 2.
- **VETO:** Do NOT proceed to Phase 2 without at least 5 characterization tests per major context.

---

## Output

```yaml
artifact_path: "outputs/rules/{domain}/legacy-characterization.md"

deliverables:
  primary:
    - "Architecture Pattern Classification"
    - "Characterization Test Suite (all passing)"
    - "Seam Map"
    - "Rule Location Index"
  secondary:
    - "Code Smell to Rule Candidate Mapping"
    - "Fragile areas documentation"

quality_criteria:
  - "Architecture pattern documented with code evidence"
  - "All characterization tests passing (100% green)"
  - "Minimum 5 characterization tests per major bounded context"
  - "Seam map covers all high-priority areas"
  - "Rule Location Index covers every significant file with business logic"
```

---

## Completion Criteria

- [ ] Architecture pattern identified with evidence
- [ ] Characterization tests written and passing (min 5 per major context, 3 for minor contexts)
- [ ] Seam map complete for high-priority areas
- [ ] Code smell to rule candidate mapping done
- [ ] Rule Location Index compiled (with risk_level for each method)
- [ ] Minor context threshold review completed (Step 4b)
- [ ] No modifications to legacy code
- [ ] Ready for handoff to Phase 2 (extraction)

### Approval Gate

```
Characterization is APPROVED when ALL of the following are met:
  - >= 80% of identified rule locations have test_status != UNTESTED
    (PASSING, FAILING, PARTIAL, or UNTESTABLE with documented reason)
  - ALL rule locations with risk_level = CRITICAL have evidence
    (characterization test OR static analysis trace)
  - Escalation list (Step 4b) reviewed — no unresolved items
  - decoder-chief sign-off obtained
```

---

## Handoff

```yaml
next_agents: ["@ronald-ross", "@michael-feathers"]
next_phase: "Phase 2 - Extraction"
context_to_pass:
  - "Characterization Test Suite"
  - "Seam Map"
  - "Rule Location Index"
  - "Architecture Pattern Classification"
gate: "decoder-chief approves characterization before extraction begins"
```
