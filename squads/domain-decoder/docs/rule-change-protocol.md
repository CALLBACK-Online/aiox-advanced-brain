# Rule Change Protocol

**Version:** 1.0.0
**Squad:** domain-decoder
**Purpose:** Define the process for incremental updates to a published rule catalog.

---

## Triggering Events

A rule change process is triggered when ANY of the following occurs:

| Trigger | Example | Typical Scope |
|---------|---------|---------------|
| Code change that modifies business logic | Refactored discount calculation | Affected rules + related decision tables |
| New regulatory requirement | LGPD data retention mandate | New rules + glossary terms |
| Stakeholder feedback on existing rules | "Threshold should be R$5,000 not R$10,000" | Single rule update + re-validation |
| Bug found in rule extraction | Rule RE-SALES-003 traces to wrong source line | Source traceability correction |
| Contradiction discovered post-publication | Two rules conflict in edge case | Contradiction resolution + cross-references |
| Domain model change | New bounded context identified | Structural re-classification |

---

## Minimum Update Scope

When updating a rule, the following fields MUST be updated:

| Change Type | Minimum Update |
|-------------|---------------|
| Rule statement modified | `statement`, `last_modified`, `version`, `test_status` = RETEST |
| New rule added | Full rule YAML block, glossary check, classification, decision table (if applicable) |
| Rule deprecated | `status` = deprecated, `deprecation_reason`, `superseded_by` (if applicable) |
| Source traceability fix | `source.file`, `source.line`, `source.method`, `last_modified` |
| Decision table modified | Table content, `hit_policy` (if changed), related rule `last_modified` |
| Glossary term changed | Term definition, ALL rules referencing that term must be reviewed |

**Mandatory for ALL changes:**
- Update `last_modified` date on every touched rule
- Update `test_status` to RETEST on every modified rule
- Update related decision tables if rule conditions changed
- Add entry to catalog Revision History (Section 10)

---

## Re-validation Conditions

| Condition | Validation Required |
|-----------|-------------------|
| 1-3 rules changed | Run `rule-lint.js` on changed rules. Run SBVR validation on changed rules ONLY (subset). |
| 4-10 rules changed | Run `rule-lint.js` on all rules. Run SBVR validation on changed rules. Run consistency check across ALL rules (Section 6 of SBVR). |
| > 10 rules changed | Run FULL `extraction-quality` checklist. Run FULL `sbvr-validation` checklist. This is equivalent to a full re-extraction quality gate. |
| Glossary term changed | Review ALL rules referencing that term. Run SBVR vocabulary validation (Section 1). |
| New bounded context added | Run full `extraction-quality` for the new context. Existing contexts unaffected unless cross-references added. |
| Contradiction resolved | Run consistency validation (SBVR Section 6). Verify cross-references are bidirectional. |

---

## Version Numbering

Catalog versions follow: `catalog-v{major}.{minor}`

| Version Component | When to Increment | Example |
|-------------------|-------------------|---------|
| **major** | Structural changes: new bounded context, rule reclassification, decision model restructured | catalog-v1.0 -> catalog-v2.0 |
| **minor** | Rule updates: statement edits, new rules within existing structure, threshold changes | catalog-v1.0 -> catalog-v1.1 |

**Rules:**
- Major version resets minor to 0 (catalog-v2.0, not catalog-v2.3)
- Every published catalog snapshot is immutable -- changes create a new version
- Version history is tracked in the catalog's Revision History section (Section 10)
- Pre-publication iterations use suffix: `catalog-v1.0-draft.{N}` (e.g., catalog-v1.0-draft.3)

---

## Change Workflow

```
1. IDENTIFY trigger event
2. ASSESS scope (how many rules affected?)
3. APPLY minimum update scope (see table above)
4. RUN re-validation (see conditions above)
5. INCREMENT version number
6. UPDATE Revision History
7. PUBLISH updated catalog
```

---

## Roles

| Role | Responsibility |
|------|---------------|
| Change requester | Identifies trigger, provides evidence |
| decoder-chief | Assesses scope, assigns to agent, validates output |
| Assigned agent | Executes the change per minimum update scope |
| Stakeholder | Reviews changes to rules they own (for H-impact rules) |

---

*Rule Change Protocol v1.0.0*
*Squad: domain-decoder*
