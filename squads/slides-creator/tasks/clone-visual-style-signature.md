# clone-visual-style-signature

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Tactical -->

## SINKRA Validation Metadata

```yaml
task: clone-visual-style-signature
atomic_layer: Atom
responsavel_type: Clone
Domain: Tactical
Input:
  - name: reference_deck_or_brandbook
    type: object
Output:
  - name: visual_style_signature
    type: YAML
Pre_conditions:
  - reference_deck_or_brandbook provided
Post_conditions:
  - visual_style_signature emitted with explicit source boundaries
Acceptance_criteria:
  - signature captures reusable visual heuristics without copying protected assets
  - human_in_loop review approves brand fidelity before downstream use
Performance:
  duration_target: "<5 min for one reference deck"
Error_handling:
  strategy: fail fast when reference rights or fidelity are ambiguous
fallback: Human
```

## Purpose

Extract a bounded visual style signature from an allowed reference deck or brandbook so the
deck can preserve design intent without silently copying proprietary assets or layout internals.

This task is optional and only runs when the operator provides a reference and explicitly asks
for style adaptation.
