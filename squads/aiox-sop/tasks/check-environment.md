# Task: Check SOP Factory Environment Contract

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `check-environment` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-chief` |
| **Execution Type** | `Worker` |

## Metadata
```yaml
id: check-environment
name: "Check SOP Factory Environment Contract"
category: governance
agent: sop-chief
elicit: false
autonomous: true
description: "Resolve access tier, runtime mode, and source of truth before assuming enterprise or local_docs-canonical surfaces."
```

## Command

```bash
```

For canonical project context eligibility, provide an explicit business:

```bash
```

## Acceptance Criteria

- [ ] Contract includes `access_tier`, `runtime_mode`, `source_of_truth`, `reason`, and `evidence_paths`
- [ ] Contract is fail-closed when enterprise capability is not proven
- [ ] `aiox-sop` stays in `portable_docs_mode` when explicit business context is absent or readiness is not proven
- [ ] `aiox-sop` can enter `none_mode` when explicit business context and COO operations readiness are both proven

## Next Step

If the user wants business-aware analysis after the environment resolves to
`none_mode`, run `load-project context.md` to preload canonical
`identity/`, `strategy/`, and `tactical/` sources for that business.
