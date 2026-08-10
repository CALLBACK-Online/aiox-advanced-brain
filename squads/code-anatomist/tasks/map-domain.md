# Task: Map Domain (Bounded Contexts & Ubiquitous Language)

> Phase 2 of wf-extract-rules pipeline

**Task ID:** map-domain
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Opus
**Purpose:** Map bounded contexts, establish ubiquitous language glossary, and create context map using Eric Evans's DDD methodology
**Orchestrator:** @decoder-chief
**Primary Agent:** @eric-evans
**Phase:** 0 (Discovery)
**Tier:** 0

---

## Inputs

```yaml
required:
  - name: "system_name"
    description: "Name of the system being analyzed"
    example: "OrderManagement v2.3"
  - name: "source_location"
    description: "Path or repository URL of the codebase"
    example: "/repos/order-mgmt"
  - name: "primary_domain"
    description: "Main business domain"
    example: "Sales & Order Processing"
optional:
  - name: "stakeholders"
    description: "Business stakeholders available for vocabulary validation"
  - name: "existing_docs"
    description: "Existing documentation (functional specs, process maps, ERDs)"
  - name: "rule_type_inventory"
    description: "Output from classify-rules task (if already completed)"
```

---

## Elicitation (elicit: true)

Before mapping, gather from the user:

1. **How many teams/departments use this system?** (indicates number of bounded contexts)
2. **Are there terms used differently by different teams?** (signals context boundaries)
3. **Is there an existing data dictionary or ERD?** (accelerates glossary creation)
4. **Are there integrations with external systems?** (indicates anti-corruption layers)
5. **Who is the business owner/primary stakeholder for this domain?** (identifies accountability for rule decisions and validation sign-off)
6. **Does the agent have read access to the codebase?** (What is the root path? Are there restricted directories? If no code access, this task must rely on documentation and stakeholder interviews only.)

---

## Steps

### Step 1: Identify Bounded Contexts

```
ACTION: Analyze system structure to find natural boundaries
OUTPUT: Named bounded contexts with descriptions
GUIDANCE:
  Signals of context boundaries:
  - Different database schemas or tables prefixed differently
  - Separate modules/packages/namespaces
  - Different teams owning different parts
  - Same term meaning different things in different places
  - Integration points between subsystems
```

### Step 2: Create Ubiquitous Language Glossary

```
ACTION: Build glossary with minimum 15 terms per major context
OUTPUT: Glossary in standard format

Format per term:
  term: "Order"
  definition: "A confirmed request from a customer to purchase one or more products"
  context: "Sales"
  synonyms: ["purchase order", "PO"]  # terms used informally
  anti_terms: ["cart"]  # terms that are NOT the same thing
  source: "Interview with Sales Manager / OrderService.java:12"
  related_terms: ["Customer", "Product", "Line Item"]

GUIDANCE:
  - Listen for terms used DIFFERENTLY by different teams
  - "Customer" in Sales vs "Account" in Finance may be the same entity
  - Document the AUTHORITATIVE definition per context
  - If two contexts use the same word differently, document BOTH definitions
```

### Step 3: Create Context Map

```
ACTION: Map relationships between bounded contexts
OUTPUT: Context map showing relationships

Relationship types (Evans):
  - SHARED KERNEL: Two contexts share a subset of the model
  - CUSTOMER-SUPPLIER: One context depends on another's output
  - CONFORMIST: Downstream context conforms to upstream model
  - ANTI-CORRUPTION LAYER (ACL): Translation layer between contexts
  - SEPARATE WAYS: No relationship (independent)
  - OPEN HOST SERVICE: Upstream provides a protocol for integration
  - PUBLISHED LANGUAGE: Shared language for integration (API, events)

Format:
  context_map:
    - upstream: "Sales"
      downstream: "Fulfillment"
      relationship: "CUSTOMER-SUPPLIER"
      integration: "OrderPlaced event"
      acl_needed: true
      notes: "Sales defines Order, Fulfillment consumes it"
```

### Step 4: Map Sources to Contexts

```
ACTION: Assign every significant source file/module to a bounded context
OUTPUT: Source-to-context mapping

Format:
  source_mapping:
    - context: "Sales"
      modules:
        - path: "src/sales/"
          description: "Core sales logic"
        - path: "src/shared/pricing/"
          description: "Pricing calculations (shared with Marketing)"
      notes: "pricing/ spans two contexts - ACL candidate"

GUIDANCE:
  - If one module spans multiple contexts, note the ACL needed
  - Files in "shared/" or "common/" are red flags for missing context boundaries
  - Configuration files often contain cross-cutting rules
```

### Step 5: Validate with Stakeholders

```
ACTION: Review glossary and context map with at least one business stakeholder
OUTPUT: Validated glossary with stakeholder sign-off notes

GUIDANCE:
  - Read terms BACK to stakeholders: "When I say X, do you understand Y?"
  - If stakeholder corrects you, the stakeholder is RIGHT
  - Document disagreements between stakeholders (different contexts!)
  - Mark terms as VALIDATED or NEEDS_REVIEW
```

### Fallback: Stakeholders Unavailable

```
If no business stakeholders are available for validation (Step 5):
  1. Use alternative sources as PRIMARY evidence:
     - README files and inline documentation
     - docs/ folder contents (functional specs, process maps)
     - Code comments and docstrings
     - Commit messages mentioning business terms
     - Database column names and table comments
  2. Mark ALL glossary terms derived without stakeholder input as INFERRED
  3. Mark context boundaries derived from code-only analysis as INFERRED
  4. The task CAN proceed, but the output carries lower confidence
  5. Add a top-level note: "STAKEHOLDER REVIEW PENDING — {N} terms marked INFERRED"
  6. Escalate to decoder-chief: stakeholder validation must happen before Phase 2
```

---

## Veto Conditions

- **VETO:** Do NOT define terms without source evidence (code, docs, or stakeholder quote).
- **VETO:** Do NOT create a context map without identifying at least 2 bounded contexts.
- **VETO:** Do NOT proceed if the same term has conflicting definitions without documenting both in their respective contexts.
- **VETO:** Do NOT skip source-to-context mapping. Every significant module must have a context assignment.
- **VETO:** Do NOT proceed if shared modules exist without ACL documentation AND the domain has user-facing features — likely missed authorization rules. Document ACL candidates before continuing.

---

## Output

```yaml
artifact_path: "outputs/rules/{domain}/domain-map.md"

deliverables:
  primary:
    - "Context Map (bounded contexts + relationships)"
    - "Ubiquitous Language Glossary (min 15 terms per context)"
    - "Source-to-Context Mapping"
  secondary:
    - "Stakeholder validation notes"
    - "ACL candidates list"
    - "Ambiguous terms requiring resolution"

quality_criteria:
  - "Every major module assigned to a bounded context"
  - "Glossary has at least 15 validated terms per major context"
  - "Context map shows relationships with types"
  - "No terms without source evidence"
  - "Anti-corruption layer candidates identified"
```

---

## Completion Criteria

- [ ] Bounded contexts identified and named
- [ ] Ubiquitous language glossary created (min 15 terms per major context)
- [ ] Context map with relationship types
- [ ] Source-to-context mapping complete
- [ ] At least one stakeholder review (if stakeholders available)
- [ ] ACL candidates documented
- [ ] Ready for handoff to Phase 1

---

## Handoff

```yaml
next_agents: ["@martin-fowler", "@michael-feathers"]  # Sequential: Fowler (architecture) first, then Feathers (characterization tests)
next_task: "characterize-legacy.md"
context_to_pass:
  - "Context Map"
  - "Ubiquitous Language Glossary"
  - "Source-to-Context Mapping"
gate: "decoder-chief approves domain mapping before proceeding"
```
