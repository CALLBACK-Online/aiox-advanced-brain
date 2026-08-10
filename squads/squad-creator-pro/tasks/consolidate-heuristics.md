---
task-id: consolidate-heuristics
name: "Consolidate Heuristics"
version: 1.0.0
execution_type: Agent
model: Opus
model_rationale: "Semantic deduplication and conflict detection across heuristic families requires deep comprehension."
haiku_eligible: false
estimated-time: 30 min
complexity: high

inputs:
  required:
    - minds_path: "Path to minds/ directory with heuristic files"
  optional:
    - source: "skill_execution — include .aiox/learning/entries/ observations"
    - owner: "Filter to specific mind owner (e.g., oalanicolas, pedro_valerio)"

outputs:
  primary:
    - inventory_report: "Complete heuristic inventory with counts, families, and status"
    - dedup_candidates: "List of duplicate/near-duplicate heuristics with similarity scores"
    - conflict_scan: "Inter-owner and intra-owner conflicts detected"
    - merge_archive_candidates: "Recommendations for merge, archive, or promotion"

elicit: true
---
<!-- SINKRA_TASK_METADATA:START -->
```yaml
sinkra_task_metadata:
  task_id: consolidate-heuristics
  task_name: Consolidate Heuristics
  status: pending
  responsible_executor: '@heuristic-ops'
  execution_type: Agent
  estimated_time: 30m
  domain: Operational
  input:
  - minds_path
  - source (optional)
  - owner (optional)
  output:
  - inventory_report
  - dedup_candidates
  - conflict_scan
  - merge_archive_candidates
  action_items:
  - Scan all minds/{owner}/heuristics/ directories
  - Build complete inventory with counts per family (KE, BS, PA, PM)
  - Run Jaccard similarity scan for dedup candidates (threshold >= 0.6)
  - Detect intra-owner conflicts (same topic, contradictory advice)
  - Detect inter-owner conflicts (cross-owner perspective clashes)
  - If --source skill_execution, also scan .aiox/learning/entries/
  - Generate merge/archive/promote recommendations
  acceptance_criteria:
  - Inventory covers 100% of heuristic files in minds/
  - Dedup candidates have similarity scores with exact file references
  - No false positives in conflict scan (each conflict cites both sources)
  - Merge candidates include rationale and target family
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: approval_required
  escalation_priority: high
  coherence_threshold: 0.90
  error_behavior: raise
```
<!-- SINKRA_TASK_METADATA:END -->

<!-- SINKRA_CONTRACT:START -->
```yaml
sinkra_contract:
  Domain: Operational
  atomic_layer: Atom
  executor: Agent
  pre_condition: "minds/ directory exists with at least 1 owner subdirectory containing heuristic files."
  post_condition: "inventory_report generated with exact counts, dedup_candidates with similarity scores, conflict_scan with evidence pairs."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- SINKRA_CONTRACT:END -->


# Task: Consolidate Heuristics

## Purpose

Complete inventory, deduplication scan, conflict detection, and merge/archive candidate generation for all heuristic files across mind owners.

## Steps

1. **Inventory:** Scan `minds/{owner}/heuristics/` for all `.md` files. Count per family (KE, BS, PA, PM).
2. **Dedup Scan:** Compare titles + content of all heuristics within and across owners. Flag pairs with Jaccard similarity >= 0.6.
3. **Conflict Scan:** Identify heuristics that address the same topic but give contradictory guidance. Tag as `intra_owner` or `inter_owner`.
4. **Merge/Archive Candidates:** For each dedup pair, recommend: merge (combine into one), archive (mark older as superseded), or keep (distinct perspectives).
5. **Dual Source (optional):** If `--source skill_execution`, also scan `.aiox/learning/entries/` for unprocessed observations from the learning digester.

## Governance Rules (from RT-HEURISTIC-OPS-001)

- INV-01: NUNCA deletar arquivos L3 (.md) — apenas status: archived ou superseded
- INV-03: NUNCA merge cross-owner — usar canonical_ref para preservar perspectiva
- INV-04: Consolidação é P0 — base limpa ANTES de batch runner

## Output Format

```yaml
inventory:
  total_heuristics: N
  by_owner: { oalanicolas: N, pedro_valerio: N }
  by_family: { KE: N, BS: N, PA: N, PM: N }

dedup_candidates:
  - pair: [file_a, file_b]
    similarity: 0.XX
    recommendation: merge|archive|keep
    rationale: "..."

conflicts:
  - type: intra_owner|inter_owner
    heuristic_a: { file, title, stance }
    heuristic_b: { file, title, stance }
    resolution: "..."
```
