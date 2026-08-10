# Research Report — Comparing 3 Research Agents (multi_player)

**Slug:** fixture-multi-player-gap-analysis
**Comparison pattern:** multi_player
**Candidates:** Perplexity Deep Research, Manus Deep Research, Exa Research API

---

## 1. O Que Já Existe

Three production-grade research agents compete in the deep-research category, each with a different sweet spot.

- [Perplexity Deep Research](https://perplexity.ai) — 2026 — balanced grounding + synthesis with strong API.
- [Manus Deep Research](https://manus.im) — 2026 — strongest extraction robustness + sub-query decomposition; weakest API surface.
- [Exa Research API](https://exa.ai) — 2026 — strongest API ergonomics; weakest extraction robustness (no visual fallback).

## 2. Comparative Analysis

See `matrices.yaml` for the full feature-depth-by-candidate matrix. Headline:

- Manus wins on **source grounding**, **query decomposition**, and **extraction robustness** (5/5/5) but loses on API (2).
- Exa wins on **API ergonomics** (5) but is weakest on **extraction robustness** (2).
- Perplexity is the balanced middle.

## 3. Recommendations

Use Manus for high-stakes scientific research where extraction fidelity matters; use Exa when SDK ergonomics and integration speed dominate; use Perplexity for production-ready balanced workloads.

---

## 11. Caveats

- All scoring is single-pass interpretive (see `matrices.yaml#scoring_calibration`); not an empirical benchmark.
- API ergonomics scored against developer experience in 2026-05; subject to change.

---

**Ver análise dedicada de lacunas:** [./gap-analysis.md](./gap-analysis.md)
