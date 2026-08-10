# SOP Factory Architecture

## Intent

`aiox-sop` turns operational knowledge into structured SOP artifacts for humans and AI systems. It is enterprise-aware locally, but it must remain safe when copied into a less capable repository.

## Architecture Layers

1. Orchestrator layer: `sop-chief` routes requests and enforces quality.
2. Specialist layer: analyst, creator, extractor, ML architect, auditor.
3. Workflow layer: creation, audit, and extraction pipelines.
4. Runtime contract layer: environment detection decides which context surfaces may be used.

## Environment Contract

The squad resolves a shared contract with these fields:

- `access_tier`: `opensource|pro|enterprise`
- `runtime_mode`: `portable_docs_mode|none_mode`
- `source_of_truth`: `docs_projection|project_canonical`
- `reason`
- `evidence_paths`

Decision rules:

- `enterprise` requires explicit proof.
- `pro` is allowed when the Pro pack exists and enterprise is not proven.
- `portable_docs_mode` remains the default when explicit business context is absent or readiness is not proven.
- `none_mode` is allowed only when explicit runtime context and canonical quality readiness are both proven.

## Optional LocalDocs Business Context

When `none_mode` is proven for an explicit `business`, `aiox-sop`
may load a business-aware context snapshot before analysis, extraction, or
audit work that needs real `identity`/`strategy` data.

Canonical business context surfaces:

- `docs/identity/company-dna.yaml`
- `docs/strategy/icp.yaml`
- `docs/strategy/offerbook.yaml` when present
- `docs/strategy/team-structure.yaml`
- `docs/strategy/pricing-strategy.yaml`
- `docs/strategy/kpi-scorecards.yaml`
- `docs/strategy/commission-design.yaml` when present
- `docs/templates/strategy/`

Loader surface:

- `squads/aiox-sop/scripts/load-project context.cjs`
- `squads/aiox-sop/tasks/load-project context.md`

This context remains read-first, but the same readiness gate also unlocks the
canonical machine-readable publish surface at
`docs/sops/`.

## Non-Sensitive Projection

Portable mode consumes:

- `docs/squad/aiox-sop/operational-projection.yaml`

This projection may describe safe outputs, mode rules, and evidence surfaces, but it must not embed private local_docs topology.

## Output Zones

- `docs/sops/`: canonical shared-safe markdown SOPs and draft SOPs
- `docs/sops/`: canonical machine-readable SOPs for an explicit business in `none_mode`
- `outputs/aiox-sop/`: auxiliary generated artifacts
- `outputs/aiox-sop/extractions/`: extraction reports, confidence maps, and review aids
- `outputs/aiox-sop/audits/`: audit reports and dashboards
- `outputs/aiox-sop/analysis/`: analysis and benchmark reports
- `outputs/aiox-sop/converted/`: conversion validation reports and non-canonical byproducts
- `outputs/aiox-sop/checklists/`: generated checklists
- `outputs/aiox-sop/certificates/`: certification artifacts
- `squads/aiox-sop/outputs/`: retained reference packages; not a canonical runtime output zone

## Current Constraint

`aiox-sop` now has canonical readiness support in the COO resolver through the `operations` context. The correct runtime behavior is:

- without explicit `business`, runtime remains `portable_docs_mode`
- with explicit `business` and ready operations namespace, runtime may become `none_mode`
- shared-safe docs projection remains the default fallback source of truth
- markdown SOP publication does not require local_docs write access
- YAML/JSON SOP publication requires explicit `business` and the canonical project context gate
