# eval-suite — Research Quality Evaluation (Sprint 0 Skeleton)

Story: STORY-RA-0.2 | Epic: EPIC-RESEARCH-INTELLIGENCE | Wave: 7

## What this is

A **minimal eval skeleton** that unblocks:
- RA-EXP.1 (KISS Gate 1 — falsifiable A/B quality delta)
- Sprint D (regression baseline for improvement validation)
- Future bench re-runs (reproducible scoring via rubric + LLM-judge)

## What this is NOT

This is explicitly NOT:
- Full Gartner-grade eval engineering
- Multi-judge consensus (single LLM judge per run)
- Regression test suite completa (3 fixtures, not production coverage)
- Automated CI integration (manual invocation only)
- Statistical significance testing
- Human-in-the-loop calibration workflow

See ADR-002 v2.0 and Advisory Council CF-1 for scope rationale.

## Components

```
eval-suite/
  rubric.yaml           — 5-dimension scoring rubric (0-20 pts each, total 0-100)
  llm_judge.py          — LLM-based evaluator (BYOK: Claude or OpenAI)
  regression_runner.sh  — Compares fixture score to baseline; exit 0/1
  fixtures/             — 3 synthetic fixtures (high/medium/low quality)
    README.md           — Selection criteria
    high-quality/       — Baseline: 82/100
    medium-quality/     — Baseline: 58/100
    low-quality/        — Baseline: 20/100
  results/              — Judge output JSON (gitignored except .gitkeep)
```

## Quick start

### Run judge on a fixture (dry-run, no LLM call)

```bash
cd <repo-root>
python3 squads/research/eval-suite/llm_judge.py \
  --research-dir squads/research/eval-suite/fixtures/high-quality \
  --dry-run
```

### Run judge on a real research run

```bash
# Set ANTHROPIC_API_KEY in environment first
python3 squads/research/eval-suite/llm_judge.py \
  --research-dir docs/research/2026-05-18-gold-bench-profile-fixture
```

### Run regression check on a fixture

```bash
bash squads/research/eval-suite/regression_runner.sh \
  --fixture squads/research/eval-suite/fixtures/high-quality \
  --dry-run
# exit 0 = no regression; exit 1 = regression detected
```

### Run regression against a real research run with explicit baseline

```bash
bash squads/research/eval-suite/regression_runner.sh \
  --fixture docs/research/2026-05-18-gold-bench-profile-fixture \
  --baseline 82 \
  --threshold 5
```

## Rubric dimensions

| Dimension | Max | What it measures |
|---|---|---|
| `coverage` | 20 | How completely sub-questions are addressed |
| `citation_quality` | 20 | Verifiability and diversity of sources |
| `claim_verifiability` | 20 | Confidence calibration and methodology |
| `narrative_coherence` | 20 | Structure, transitions, conclusion validity |
| `actionability` | 20 | Specificity and prioritization of recommendations |

Total: 100 pts.

## Provider configuration (BYOK)

| Provider | Env var | Default model |
|---|---|---|
| Claude (default) | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o` |

The judge records `model_used` in every result JSON for reproducibility.

## Results format

Results written to `eval-suite/results/{slug}-{timestamp}.json`:

```json
{
  "slug": "2026-05-18-gold-bench-profile-fixture",
  "scores": {
    "coverage": 18,
    "citation_quality": 17,
    "claim_verifiability": 16,
    "narrative_coherence": 17,
    "actionability": 15
  },
  "total": 83,
  "rationale_per_dim": { "coverage": "...", ... },
  "model_used": "claude/claude-sonnet-4-5",
  "timestamp": "20260519T120000Z",
  "research_dir": "docs/research/...",
  "rubric_version": "1.0"
}
```

## Regression semantics

A regression is detected when: `current_score < baseline - threshold` (default threshold=5).

The 5-point threshold matches the `validate:runner-lib-coverage` convention
(`coverage-baseline.json -5pts floor`) used elsewhere in the repo.

## Technical debt (deferred, not abandoned)

| Item | Rationale for deferral | Tracking |
|---|---|---|
| Real research run fixtures (not synthetic) | Synthetic avoids drift; real needed for calibration | RA-EXP.1 will generate real results |
| Multi-judge consensus | Single judge sufficient for Sprint 0 falsifiability | Future sprint, post RA-EXP.1 |
| CI/pre-push integration | Runs take 30-120s per fixture; manual acceptable now | Deferred to Sprint D |
| Statistical baseline calibration | Needs 10+ real runs to calibrate per dimension | After RA-EXP.1 runs accumulate |
