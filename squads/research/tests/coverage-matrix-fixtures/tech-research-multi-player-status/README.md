# Fixture: tech-research multi-player + status code 4-níveis

**Story:** RA-F.2 AC-1, AC-2, AC-4, AC-6 — status enum compliance + recommendations atom.

**Trigger:** `comparison_pattern: multi_player` + `candidates_count: 5` → recommendations-by-use-case.md MANDATORY + every cell carries 4-level status.

## What this fixture exercises

| AC | Evidence |
|---|---|
| AC-1 — 4-level enum | `matrices.yaml#rows[].cells[player].status` ∈ {confirmed, partial, uncertain, not_present} |
| AC-2 — helper | `coverage_matrix_helper.normalize_status / status_to_score / status_to_symbol / validate_matrix` |
| AC-4 — recs atom | `recommendations-by-use-case.md` with 5 use cases + cross-table |
| AC-6 — validator | `output_validator.py --skill tech-research --enforcement warn` exits 0 with zero findings |

## Run the validator

This fixture intentionally OMITS the V1/V3 tech-research baseline files (README.md,
00-query-original.md, etc.) because it exercises ONLY the F.2 status-code +
recommendations contract. Use `--skill research-bench` to skip the baseline
file list (the F.2 hook runs on both skills equally per PO Condition 2):

```bash
python3 squads/research/scripts/tech-research/output_validator.py \
  --skill research-bench --enforcement warn \
  squads/research/tests/coverage-matrix-fixtures/tech-research-multi-player-status/
```

Expected: `valid: true`, zero status_code_findings, status_enum_compliance check status: PASS.

## Negative test (block mode without recommendations)

Remove `recommendations-by-use-case.md` then re-run with `--enforcement block`:

```bash
mv recommendations-by-use-case.md _archived-recs.md
python3 ... --enforcement block ... → expect exit 1
mv _archived-recs.md recommendations-by-use-case.md
```
