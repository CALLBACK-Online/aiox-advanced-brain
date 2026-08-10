# Domain Decoder — Phase {FORCE_PHASE}

System: **{SYSTEM_SLUG}** | Source: `{SOURCE_PATH}` | Output: `{SYSTEM_DIR}`

## What To Do

1. Read the **Task Instructions** below (already injected — do NOT re-read the task file)
2. Read the **Agent Expertise** below (already injected — do NOT re-read the agent file)
3. Read source files at `{SOURCE_PATH}` — start with config.yaml, then agents/, tasks/, workflows/, data/
4. Use the **Write tool** to create each mandatory artifact listed for your phase
5. Write a LONG, DETAILED text response (this is also saved as `phase{FORCE_PHASE}-output.md`)
6. End with `<promise>PHASE_COMPLETE</promise>`

**Both the Write artifacts AND your text response matter.** Be thorough — under 3000 chars is incomplete.

---

## Agent Expertise (Who You Are)

{AGENT_SUMMARY}

---

## Task Instructions (What To Do)

{TASK_CONTENT}

---

## Phase {FORCE_PHASE} — Mandatory Write Artifacts

### If Phase 0 (Discovery):
- `{SYSTEM_DIR}/discovery/context-map.md` — Bounded contexts with glossary (15+ terms per context), relationships, ASCII diagram
- `{SYSTEM_DIR}/discovery/source-mapping.yaml` — Files mapped to bounded contexts
- `{SYSTEM_DIR}/discovery/rule-type-inventory.md` — Ross taxonomy (CONSTRAINT, COMPUTATION, INFERENCE, ACTION_ENABLER, BEHAVIORAL) with estimated counts per context

### If Phase 1 (Characterization):
- `{SYSTEM_DIR}/characterization/architecture-classification.md` — Pattern name + 3+ evidence citations (file:line)
- `{SYSTEM_DIR}/characterization/seam-map.md` — All seams with type, location, isolation priority (HIGH/MED/LOW)
- `{SYSTEM_DIR}/characterization/rule-location-index.md` — Every file containing business rules, with rule type hints

### If Phase 2 (Extraction):
- `{SYSTEM_DIR}/extraction/classified-rules.md` — EVERY rule: ID, Ross category, source file:line, statement, confidence
- `{SYSTEM_DIR}/extraction/fact-model.md` — Terms and fact types by bounded context
- `{SYSTEM_DIR}/extraction/dedup-matrix.md` — Duplicate/overlap analysis across contexts

### If Phase 3 (Modeling):
- `{SYSTEM_DIR}/modeling/decision-model.md` — Business decisions (DEC-{CONTEXT}-{NNN}) with rule families
- `{SYSTEM_DIR}/modeling/decision-tables-dmn.md` — DMN tables with hit policies (Unique/First/Priority/Collect)
- `{SYSTEM_DIR}/modeling/validation-report.md` — Orphan rules, contradictions, coverage gaps

### If Phase 4 (Expression):
- `{SYSTEM_DIR}/expression/rules-expressed-rulespeak.md` — ALL rules in RuleSpeak (MUST/MUST NOT/MAY patterns)
- `{SYSTEM_DIR}/expression/ambiguity-log.md` — Banned words found and how replaced

### If Phase 5 (Validation):
{CHECKLIST_CONTENT}
Write artifacts:
- `{SYSTEM_DIR}/validation/sbvr-checklist.md` — 45 items, each PASS/FAIL with evidence
- `{SYSTEM_DIR}/validation/extraction-quality.md` — 54 items with evidence
- `{SYSTEM_DIR}/validation/final-rule-catalog.md` — Complete catalog with traceability

---

## Rules

- **E3:** Only BUSINESS rules (would a PO care if this changed?). No code patterns or style rules.
- **E6:** ALL bounded contexts get equal treatment through every phase.
- **E7:** Phase 2 must include dedup analysis.

## Budget

You have ~{MAX_TURNS} tool turns. Spend them on:
1. Reading SOURCE files (config.yaml, agents/, tasks/, data/) — this is your primary work
2. Writing mandatory artifact files with Write tool
3. Do NOT re-read task instructions or agent summaries — they are already above

## Prior Phase Context

Prior phase outputs are injected below — they are already in your context.
**Do NOT re-read prior outputs.** Spend your turns on reading SOURCE files and writing artifacts.
