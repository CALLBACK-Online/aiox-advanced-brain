# Extraction Quality Checklist

**Purpose:** Validate that the extraction PROCESS was executed correctly — covering all theoretical frameworks, all experts consulted, all methods applied
**When to use:** AFTER all phases complete, ALONGSIDE sbvr-validation.md, BEFORE final delivery
**Tool type:** Checklist (not an agent)
**Command:** `*quality-check` (run via decoder-chief)

---

## How to Use This Checklist

This checklist validates the PROCESS, not the output. SBVR validation checks the rules themselves. This checklist checks whether the right methods were applied in the right order.

Work through all 8 sections. Each maps to a specific theoretical framework and the agent who applies it.

- Mark `[x]` for completed
- Mark `[-]` for not applicable (with reason in parentheses)
- Mark `[ ]` for missing — these must be completed before delivery

---

## 1. Legacy Code Characterization (Michael Feathers)

*Framework: "Working Effectively with Legacy Code" — M. Feathers (2004)*
*Agent: @michael-feathers*

- [ ] Legacy code has been physically located and inventoried (file list with paths)
- [ ] Architecture pattern identified (Transaction Script, Domain Model, Table Module, Service Layer, or other)
- [ ] "Seams" identified — points where code behavior can be observed without full execution
- [ ] Characterization tests written for at least the top 5 critical code paths
- [ ] Characterization tests are passing (current behavior is locked)
- [ ] Code smells mapped to business rule candidates (God Class, Feature Envy, Large Method → rule locations)
- [ ] Technical debt that obscures rules is documented (not necessarily fixed — just documented)
- [ ] Characterization tests reviewed to distinguish business rules (intentional business logic) from bugs (implementation defects). Ambiguous items flagged as AMBIGUOUS with justification.

**Section score: __ / 8**
**Agent responsible:** @michael-feathers
**If incomplete:** Run `*characterize-legacy` before proceeding

---

## 2. Bounded Context Mapping (Eric Evans)

*Framework: "Domain-Driven Design" — E. Evans (2003)*
*Agent: @eric-evans*

- [ ] All bounded contexts in the system are identified and named
- [ ] Context Map created (visual or textual representation of context relationships)
- [ ] Ubiquitous Language glossary started — at least 15 terms per major context
- [ ] Terms with different meanings in different contexts are flagged (same word, different concept)
- [ ] Integration points between bounded contexts identified and documented (OPTIONAL: aggregate roots, only if domain-map included aggregate analysis — skip if not applicable)
- [ ] Anti-corruption layers documented where contexts interact with different vocabularies
- [ ] "Shared kernel" areas identified (concepts truly shared across contexts)

**Section score: __ / 7**
**Agent responsible:** @eric-evans
**If incomplete:** Run `*map-domain` before proceeding

---

## 3. Rule Classification (Ronald Ross)

*Framework: "Business Rule Concepts" — R. Ross (4th edition)*
*Agent: @ronald-ross*

- [ ] All extracted rules classified using Ross taxonomy (constraint, computation, inference, action enabler, behavioral)
- [ ] RuleSpeak sentence patterns applied consistently to all rule statements
- [ ] Rule families identified — groups of related rules that form a coherent policy
- [ ] Rule dependencies documented (rule A cannot be evaluated without rule B)
- [ ] Derivation rules separated from constraint rules (derived facts vs. enforced conditions)
- [ ] Decision rules separated from process rules (WHAT to decide vs. WHEN to act)
- [ ] Each rule has a unique ID in format `RE-{DOMINIO}-{NNN}`

**Section score: __ / 7**
**Agent responsible:** @ronald-ross
**If incomplete:** Run `*classify-rules` before proceeding

---

## 4. Decision Modeling (Barbara von Halle)

*Framework: "Business Rule Revolution" — B. von Halle & L. Goldberg (2009)*
*Agent: @barbara-von-halle*

- [ ] Decision Model created — rule families organized into connected business decisions
- [ ] Each rule family has a named "Business Decision" as its organizing concept
- [ ] Rule connections documented (how conclusions from one rule feed into another)
- [ ] Rule sets with conflicting outcomes identified and resolved with priority order
- [ ] All identified contradictions have formal status: RESOLVED (scope_boundary) with documented scope per rule, or UNRESOLVED (needs_human) with escalation evidence. Inline cross-references (`<!-- contradiction:RS-XXX resolved:... ref:RS-YYY -->`) are bidirectional.
- [ ] Business motivation documented for each Decision (WHY this decision exists). Verify that model-decisions output includes `business_owner` for each decision table (dependency: Story 1.1 T3, via map-domain elicitation question 5)
- [ ] Rule owners identified (which business unit is responsible for each rule family). Verify that map-domain output identifies stakeholders by area via `business_owner` field (dependency: Story 1.1 T3). If absent, extraction quality score reduces by 5 points.

**Section score: __ / 7**
**Agent responsible:** @barbara-von-halle
**If incomplete:** Run `*model-decisions` before proceeding

---

## 5. DMN Formalization (James Taylor)

*Framework: "Real-World Decision Modeling with DMN" — J. Taylor & J. Purchase (2016)*
*Agent: @james-taylor*

- [ ] Decision Requirements Diagram (DRD) created showing all decisions and their dependencies
- [ ] Decision tables created for all computational and conditional rules
- [ ] Hit policies specified for every decision table (U, F, P, A, C, R, or O)
- [ ] All condition combinations covered — no gaps in decision tables (completeness check)
- [ ] No overlapping rows in Unique (U) or First (F) hit policy tables
- [ ] Input expressions use only vocabulary terms from the glossary
- [ ] Output expressions produce values consistent with fact types

**Section score: __ / 7**
**Agent responsible:** @james-taylor
**If incomplete:** Run `*formalize-dmn` before proceeding

---

## 6. Architectural Pattern Identification (Martin Fowler)

*Framework: "Patterns of Enterprise Application Architecture" — M. Fowler (2002)*
*Agent: @martin-fowler*

- [ ] Primary architecture pattern identified and documented (from Fowler's catalog)
- [ ] Pattern correctly matched to codebase evidence (not assumed)
- [ ] Rule locations mapped to architectural layers (where do rules live: UI, domain, DB?)
- [ ] Rules embedded in wrong layers identified (e.g., business rules in SQL queries or UI controllers)
- [ ] Recommended target pattern for modernization documented
- [ ] Migration path from current to target pattern outlined (even if implementation is out of scope)

**Section score: __ / 6**
**Agent responsible:** @martin-fowler
**If incomplete:** Run `*identify-patterns` before proceeding

---

## 7. Rule Expression Without Ambiguity (Graham Witt)

*Framework: "Writing Effective Business Rules" — G. Witt (2012)*
*Agent: @graham-witt*

- [ ] Every rule statement reviewed and rewritten for clarity
- [ ] All ambiguous terms eliminated (`appropriate`, `reasonable`, `timely`, `significant`, `usually`, `generally`)
- [ ] Quantifiers made explicit (`all`, `at least one`, `exactly one`, `no`) — never implicit
- [ ] Temporal conditions stated precisely (not "soon" but "within 3 business days")
- [ ] Conditional structures use consistent pattern: "If [condition], then [obligation/prohibition]"
- [ ] Passive voice eliminated where it obscures the subject of obligation
- [ ] Rules reviewed by at least one business stakeholder for readability confirmation
- [ ] Cold reader validation performed: 10 random rules presented to a non-participant reader (agent or human with no pipeline context). Scoring: >= 8/10 comprehended in < 30 seconds = PASS, 6-7 = CONDITIONAL PASS (revise failed rules), < 6 = FAIL (return to express-rules). Record cold_reader_score in quality-score output.

**Section score: __ / 8**
**Agent responsible:** @graham-witt
**If incomplete:** Run `*express-rules` before proceeding

---

## 8. SBVR Validation (Tool)

*Standard: OMG SBVR 1.5*
*Tool: sbvr-validation.md*

- [ ] SBVR validation checklist executed (sbvr-validation.md)
- [ ] SBVR score achieved: 85%+ (38/45 items)
- [ ] All 5 CRITICAL items in SBVR checklist passed
- [ ] Any SBVR failures addressed and checklist re-run

**Section score: __ / 4**
**If incomplete:** Run `*sbvr-check` before proceeding

---

## Scoring Summary

| Section | Framework | Agent | Items | Score |
|---------|-----------|-------|-------|-------|
| 1. Legacy Code Characterization | M. Feathers | @michael-feathers | 8 | __ / 8 |
| 2. Bounded Context Mapping | E. Evans | @eric-evans | 7 | __ / 7 |
| 3. Rule Classification | R. Ross | @ronald-ross | 7 | __ / 7 |
| 4. Decision Modeling | B. von Halle | @barbara-von-halle | 7 | __ / 7 |
| 5. DMN Formalization | J. Taylor | @james-taylor | 7 | __ / 7 |
| 6. Architectural Pattern Identification | M. Fowler | @martin-fowler | 6 | __ / 6 |
| 7. Rule Expression | G. Witt | @graham-witt | 8 | __ / 8 |
| 8. SBVR Validation | OMG SBVR 1.5 | Tool | 4 | __ / 4 |
| **TOTAL** | | | **54** | **__ / 54** |

---

## Pass/Fail Determination

**Pass threshold:** 46/54 (85%)

**Automatic failure conditions (any one of these fails the entire checklist):**

| Code | Condition |
|------|-----------|
| AF-1 | Characterization tests not written (Section 1, item 4) |
| AF-2 | Bounded contexts not mapped (Section 2, item 1) |
| AF-3 | No rule classification applied (Section 3, item 1) |
| AF-4 | No unique IDs assigned (Section 3, item 7) |
| AF-5 | SBVR validation not executed (Section 8, item 1) |
| AF-6 | SBVR score below 85% (Section 8, item 2) |

```
Auto-fail conditions triggered: __ / 6 (must be 0 to pass)
Total score:                     __ / 54  (__%)

PASS threshold:                  46 / 54 (85%)
Auto-fail threshold:             0 failures

Final result: [ ] PASS  [ ] FAIL
Failure reason (if failed): ___________________
```

---

## Modelo de Scoring Parcial

When optional items are skipped (marked `[-]`), the scoring adjusts dynamically:

```
applicable_items = total_items - skipped_optional_items
score = (passed_items / applicable_items) * 100
```

- Each checked item `[x]` = 1 point
- Each unchecked item `[ ]` = 0 points
- Each skipped item `[-]` = removed from denominator (not counted against score)
- There is NO section-level pass/fail. Each item is evaluated individually.
- The 85% threshold applies to the adjusted score (applicable items only)
- Auto-fail conditions (AF-1 through AF-6) are NEVER optional and cannot be skipped

**Example:** If 54 total items, 3 marked as `[-]` (not applicable), then applicable = 51. Pass threshold = ceil(51 * 0.85) = 44.

---

## After Failing

Identify which sections are incomplete and run the corresponding command:

| Failed Section | Action |
|---------------|--------|
| Section 1 (Feathers) | `*characterize-legacy` |
| Section 2 (Evans) | `*map-domain` |
| Section 3 (Ross) | `*classify-rules` |
| Section 4 (Von Halle) | `*model-decisions` |
| Section 5 (Taylor) | `*formalize-dmn` |
| Section 6 (Fowler) | `*identify-patterns` |
| Section 7 (Witt) | `*express-rules` |
| Section 8 (SBVR) | `*sbvr-check` |

After completing the missing work, re-run this checklist with `*quality-check`.

### Re-spawn Context Template

When re-spawning an agent to fix failures, include this context block:

```yaml
re_spawn_context:
  checklist: "extraction-quality"
  run_date: "YYYY-MM-DD"
  result: "FAIL"
  score: "__/52 (__%)"
  failed_items:
    - section: "{section number and name}"
      item: "{specific checklist item that failed}"
      severity: "AUTO_FAIL | BELOW_THRESHOLD"
      agent_responsible: "{agent name responsible for this section}"
  original_agent: "{agent that was running when failure occurred}"
  input_artifacts:
    - path: "{path to the artifact that was validated}"
      description: "{what this artifact contains}"
  suggested_fix_action: |
    {Specific instruction for the re-spawned agent, e.g.:
    "Section 4 (Decision Modeling) is missing business motivation
    for decisions DEC-SALES-001 and DEC-LOG-002. Run *model-decisions
    on the existing decision model and add the 'motivation' field
    to each decision entry."}
```

This context ensures the re-spawned agent has full awareness of what failed, why, and what artifacts to read before attempting fixes.

---

## Section 9: Process Enforcement (10 items)

_Framework: Enforcement Rules v1.0 (learned from production executions)_

Each item below is an auto-fail if violated. These rules exist because they were broken in practice.

| # | Check | PASS Criteria | Auto-Fail? |
|---|-------|--------------|------------|
| 9.1 | Every phase spawned a dedicated agent (no synthesizing from context) | Agent tool call visible in execution log for each phase | AF-7 |
| 9.2 | Every phase saved output to disk before gate ran | `ls outputs/decoded/{slug}/{phase}/` confirms files exist | AF-8 |
| 9.3 | Business rules separated from implementation details | Each rule tagged business_rule: true/false, count uses only true | No |
| 9.4 | SBVR checklist applied item-by-item (45 items with PASS/FAIL) | Validation output contains 45+ scored items | AF-9 |
| 9.5 | Characterization tests delivered (if Phase 1 executed) | `ls outputs/decoded/{slug}/characterization/tests/` has files | AF-10 |
| 9.6 | All bounded contexts received equal pipeline treatment | Each context has dedicated output files per phase | No |
| 9.7 | Cross-layer deduplication matrix exists | `extraction/dedup-matrix.md` maps FE -> BE -> SQL per rule | No |
| 9.8 | Output path is outputs/decoded/{slug}/ (correct contract) | No artifacts in outputs/code-anatomist/ or other paths | AF-11 |
| 9.9 | Phase gates ran as Bash commands with visible output | ls + wc + grep commands executed and logged per gate | AF-12 |
| 9.10 | Input collection completed (Q1-Q5 answered) before first agent | Q1-Q5 values documented in discovery/ output | No |

**Auto-Fail Conditions (AF-7 to AF-12):**
- AF-7: Phase output synthesized without spawning agent = FAIL entire pipeline
- AF-8: Output existed only in context window, not on disk = FAIL phase
- AF-9: SBVR score self-assigned without checklist = FAIL validation
- AF-10: Characterization tests promised but not delivered = FAIL Phase 1
- AF-11: Artifacts in wrong path = FAIL delivery
- AF-12: Gates declared passed without running verification commands = FAIL gate

---

*Extraction Quality Checklist v1.1.0*
*Frameworks: Feathers, Evans, Ross, von Halle, Taylor, Fowler, Witt, OMG SBVR*
*Squad: code-anatomist*
*Used by: decoder-chief (command: *quality-check)*
