# Design Exploration Cycle — Canonical Process

Applies to any design artifact creation work orchestrated by `@design-chief` or consumed from the `design-ops` provider.

Absorbed from `agenmod/claw-design` (2026-04-18), reshaped to fit the AIOX Process-mode contract.

## The Cycle (Seven Phases)

```
ASK → COLLECT → VOCALIZE → BUILD → SHOW EARLY → ITERATE → VERIFY
  ↑                                                   |
  └──── (loop until VERIFY passes or budget exhausted)┘
```

### 1. ASK — Clarifying Questions First

- Never start a build without a materialized brief. The canonical intake is `squads/design-ops/templates/design-brief-intake-tmpl.yaml`.
- If fewer than three `success_criteria` exist, STOP and ask. A brief without measurable outcomes produces unmeasurable artifacts.
- Ambiguity in the brief is a blocker, not a creative opportunity.

#### 1a. Divergence Willingness Gate (kind-aware)

Before proceeding to COLLECT, resolve the exploration posture with the requester. This is a **user-asked divergence gate** absorbed from claw-design (*"Are you interested in novel solutions, options using existing components, or a mix?"*) and refined by our deliverable-kind matrix.

Default exploration posture by `brief.context.surface_type`:

| Surface Type | Default Variants | Default Posture | Override Path |
|--------------|------------------|-----------------|---------------|
| `component` | 1 (DS-first) | Ask before generating novel variants | Set `brief.exploration.variants_required >= 2` with rationale |
| `html_prototype` | 3 | Divergent mandatory | — |
| `deck` | 3 | Divergent mandatory | — |
| `page` | 3 | Divergent mandatory | — |
| `dashboard` | 3 | Divergent mandatory | — |
| `email` | 2 | Constrained divergence | — |

- For `component`: `@design-chief` MUST ask the requester — *"DS-first only, novel variants, or a mix?"* — and record the answer in `brief.exploration.variants_required` before proceeding. A silent default to "3 variants" on a component brief is a routing violation.
- For non-component kinds: the default is divergent; the requester may narrow via `brief.exploration.exclude_patterns` or by setting `variants_required: 1` with explicit justification.

This gate supersedes the Wave B rule "N ≥ 3 mandatory for all kinds" and is canonicalized in `squads/design-ops/rules/ds-consistency-policy.md` (Divergent Exploration — Kind-Aware Policy).

### 2. COLLECT — Read Existing Resources

- Read every referenced file in `brief.existing_references`. All of them.
- Resolve project context contracts (`tokens.yaml`, `foundations.yaml`, `component-contracts.yaml`, `motion-primitives.yaml`) before writing code.
- Inspect `@aiox/ds-core` for components that already exist — REUSE > ADAPT > CREATE (IDS gate).
- Search for similar prior art in `outputs/design-ops/{business}/components/` and `apps/aiox-design-starter/`.

### 3. VOCALIZE — Assumptions Before Code

- State out loud every assumption the brief did not explicitly answer. Do this BEFORE writing code, not after.
- Classify each assumption: `user-confirmed`, `inferred-from-brand`, `inferred-from-system`, `guess`.
- Guesses must be flagged. They are the debt the brief intake failed to prevent.

### 4. BUILD — Divergent Before Convergent

- Produce N ≥ 3 variants along orthogonal axes (see `squads/design-ops/tasks/ds-build-component.md` Step 0).
- Never converge on the first variant because it "feels right." Convergence is decided by `brief.success_criteria`, not aesthetic preference.
- Each variant must pass the AI-trope gate (`squads/design-ops/checklists/dops-ai-trope-guardrails.yaml`) before progressing.

### 5. SHOW EARLY — Feedback Before Polish

- Surface the chosen variant (or the top 2) to the requester as soon as structure is in place — before final styling, before documentation, before tests.
- Early feedback prevents the entire loop from converging on the wrong answer. Polish applied to the wrong artifact is wasted motion.
- The show-early artifact is a working skeleton, not a wireframe. It must render and respond to basic interaction.

#### 5a. Before/After Visual Gate (NON-NEGOTIABLE for ANY visual change)

**For ANY change that alters rendered output — token edit, class removal, ban application, refactor, theme shift — ALWAYS generate a side-by-side BEFORE/AFTER preview and open it in the requester's browser BEFORE applying the change to source.**

- The preview is a standalone HTML that imports the **real tokens** (e.g. `apps/design/aiox/colors_and_type.css`), renders each affected case as **"como é" (left) vs "como fica" (right)**, labeled with the real selector name and the exact value delta.
- Group cases by category (keep / replace / remove) so the requester can approve at a glance.
- One representative specimen per category is sufficient when the same rule applies to N selectors — state which selectors the specimen stands for.
- **Open it via `open <file>.html`** — never ask the requester to read CSS to imagine the result.
- Apply to source ONLY after explicit visual approval. For Claude Design bundles, "apply to source" means writing the change into the change prompt/README, not editing the export.

**Why:** validated 2026-05-22 on the AIOX glow-ban calibration — the requester could not evaluate "ban glow" abstractly, but approved instantly once each case was shown before/after. Abstract design decisions produce wrong calls; visual diffs produce right ones.

**Anti-pattern:** "I'll just apply it, it's obviously better." Obvious to whom? Render both, let the eye decide.

### 6. ITERATE — Tweak Within the Chosen Direction

- Iteration applies only to the chosen variant. Iteration is not a re-exploration — that would require going back to Phase 4.
- Persist tweak decisions in the brief's `change_log` section so future maintainers can see the direction of travel.

### 7. VERIFY — Post-Build Gate

- Console errors: zero. Not "mostly zero." Zero.
- Responsive render: each viewport in `brief.verification.responsive_targets` must render without horizontal scroll and without overflow.
- A11y: WCAG AA floor. Contrast matrix computed, not asserted.
- Divergent exploration scratch artifact exists and references `success_criteria` at convergence point.

## Non-Negotiables

- **No skipping ASK.** A brief-less build is a policy violation.
- **No skipping VOCALIZE.** Silent assumptions become silent defects.
- **No single-variant BUILD.** N ≥ 3 is a hard minimum; a second variant alone is insufficient to prove a direction was chosen rather than defaulted.
- **No "polish before feedback" sequence.** SHOW EARLY is positionally rigid.
- **No "verify at the end only" mindset.** VERIFY runs at every phase boundary; the final VERIFY is a confirmation, not a discovery.

## Anti-Patterns

- **"I already know the answer."** — The ASK phase exists because you don't. If you do, write it down; if it holds up, proceed.
- **"Let me just prototype first."** — Prototyping without a brief produces art, not an artifact. Art is not a contract.
- **"We'll iterate on a single direction."** — Iteration converges; it does not diverge. If only one direction was explored, you iterated toward a local minimum of an unexplored space.
- **"Verification is a final step."** — No; it is a phase boundary. Skipping verification between phases lets broken state propagate.

## Binding to AIOX Process Mode

This cycle maps cleanly to `wf-provider-enrichment-from-external.yaml`:

| Cycle Phase | Workflow Step |
|-------------|---------------|
| ASK         | step-1-intake (elicitation gate) |
| COLLECT     | step-4-project context contracts (contracts gate) |
| VOCALIZE    | embedded in Step 0 of `ds-build-component.md` (assumption capture) |
| BUILD       | step-2-divergent-exploration → step-5-build |
| SHOW EARLY  | Before/After Visual Gate (§5a) — mandatory for any visual change |
| ITERATE     | (implicit — tracked via change_log in brief) |
| VERIFY      | step-3 (AI-trope gate) + step-6 (component quality) + step-7/8/9 (lint/typecheck/yaml) |

## Reference

- External source: `agenmod/claw-design` — claude-design-sys-prompt.txt (2026-04-18)
- Intake template: `squads/design-ops/templates/design-brief-intake-tmpl.yaml`
- AI-trope gate: `squads/design-ops/rules/ai-trope-guardrails.md`
- Workflow: `squads/design-ops/workflows/wf-provider-enrichment-from-external.yaml`
- Task embedding: `squads/design-ops/tasks/ds-build-component.md` Step 0
- Provenance: `squads/design-ops/data/design-heuristics-from-external-prompts.yaml`
