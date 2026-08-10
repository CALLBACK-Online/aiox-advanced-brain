# Attribution — slide-creator visual taxonomy absorption

This document records the upstream provenance of visual taxonomy data absorbed into the `slide-creator` skill. All absorbed content is **taxonomy-only** (no SVG, no executable code, no rendering scripts) and is reorganized into AIOX-native YAML schemas.

## Upstream

- **Project:** ppt-master
- **Repository:** https://github.com/hugohe3/ppt-master
- **Commit SHA:** `3dab7baa30d9aab6bd8607f1ed06a3d1a5c4c9af`
- **License:** MIT
- **Absorbed on:** 2026-05-19
- **Absorbed under:** STORY-SLDC-VIS-001 (PR-1 of Wave 1, slides anchor visual lift)

## License — MIT Notice

ppt-master is distributed under the MIT License. Per the license:

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The MIT license text and upstream copyright notice are preserved here. Every absorbed artifact carries:

- A top-level `source_attribution` block citing `origin: ppt-master`, the canonical `origin_repo`, the immutable `origin_commit_sha`, `license: MIT`, and the `absorbed_at` date.
- A per-entry `upstream_ref` field pointing back to the exact file at the pinned commit, allowing any consumer (human or LLM) to trace any taxonomy claim back to its source on GitHub.

## Scope

Only the following ppt-master surface areas were absorbed:

| Upstream path (relative to `skills/ppt-master/`) | AIOX target | Purpose |
|---|---|---|
| `templates/layouts/<family>/design_spec.md` (17 dirs) | `skills/slide-creator/templates/theme/visual-style-families.yaml` | Visual style family taxonomy — design tone, use cases, color palette, typography, page structure principles, cultural context |
| `references/image-renderings/<style>.md` (20 files) | `skills/slide-creator/templates/visual/image-rendering-styles.yaml` | Image rendering aesthetic taxonomy — material, line quality, depth, mood, paragraph-ready style descriptions |
| `references/image-type-templates/<type>.md` (15 files) | `skills/slide-creator/templates/visual/image-type-templates.yaml` | Image type composition taxonomy — composition skeletons, sub-structures, text-policy variants, use cases |

## Explicitly NOT absorbed

To respect the KISS principle and minimize derivative risk, the following ppt-master artifacts were **not** absorbed in PR-1:

- SVG template files (`templates/layouts/*/*.svg`)
- Python scripts (`scripts/template_import/`, `scripts/finalize_svg.py`)
- Image assets (logos, cover backgrounds)
- Few-shot prompt snippets (text examples remain in upstream)
- Component XML snippets (kept upstream; AIOX renders via its own pipeline)
- The chart taxonomy (`templates/charts/`) — covered separately via `visual/charts-and-diagrams.yaml`

If a future PR needs any of the above, treat it as a new absorption event with its own ATTRIBUTION line + commit SHA pin.

## Provenance fidelity

The absorption is taxonomy-faithful, not literal:

1. **No fabrication.** Color hex values, font stacks, typography hierarchies, and design principles in the absorbed YAML are extracted verbatim from each `design_spec.md`. When a `design_spec.md` does not declare a value, the corresponding YAML field is either omitted entirely or marked `null  # extraction_gap(<reason>)` — consistent with the `extraction-no-fallbacks.md` rule.
2. **No defaults injected.** Universal shadcn-ui baselines, generic Tailwind scales, and synthesized hover-state hexes are forbidden in the extraction layer per `extraction-no-fallbacks.md`. Application-level fallbacks live in the render pipeline (`apps/design`, runtime contracts), never here.
3. **Chinese-named families preserved.** Upstream uses Chinese identifiers for several families (e.g. `中国电建_常规`, `招商银行`, `重庆大学`). These are preserved as YAML quoted strings to maintain a 1:1 mapping to upstream — never transliterated, never anglicized in the `id` field. A human-readable `label` field carries the English name.

## Verification

To verify any absorbed claim against the upstream source:

```
upstream_ref:  https://github.com/hugohe3/ppt-master/blob/3dab7baa30d9aab6bd8607f1ed06a3d1a5c4c9af/<path>
```

Each per-entry `upstream_ref` is canonical and immutable. The pinned commit will never move under AIOX; any upstream update is handled via a new absorption event with a new SHA.

## Wave 1 context

This absorption is **PR-1** of the slide-creator anchor lift wave:

- PR-1 (this PR) — taxonomy absorption (visual families, rendering styles, image types)
- PR-2 — 58 wireframe JSON schemas (separate story)
- PR-3 — runtime audit doc (separate story)

The taxonomy absorbed here is consumed by PR-2 schemas (`compatible_with_visual_style`) and validated by PR-3 audit gates. See `docs/bench/<bench-slug>/` for the benchmark methodology that motivated this work and the +5.8 visual-style point lift target.

---

*ATTRIBUTION v1.0 — slide-creator | 2026-05-19 | STORY-SLDC-VIS-001*
