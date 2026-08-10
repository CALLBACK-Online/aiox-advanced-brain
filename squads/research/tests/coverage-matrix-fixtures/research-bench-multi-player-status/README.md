# Fixture: research-bench multi-player + status code 4-níveis

**Story:** RA-F.2 AC-1, AC-2, AC-4, AC-6 — research-bench variant of the status-code fixture.

## What this fixture exercises

Same contract as `tech-research-multi-player-status/` but with bench-flavoured
filenames (`comparison-matrix.json` + bench criteria + bench recommendations).

## Run the validator

```bash
python3 squads/research/scripts/tech-research/output_validator.py \
  --skill research-bench --enforcement warn \
  squads/research/tests/coverage-matrix-fixtures/research-bench-multi-player-status/
```

Expected: `valid: true`, zero status_code_findings, zero warnings.
