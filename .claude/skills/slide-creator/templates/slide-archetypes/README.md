# Slide Archetypes — McKinsey PPT Architect Elite

7 archetypal slide specifications imported from squad `slides-creator` (Wave B absorption 2026-04-20).

## Provenance

- **SoT (canonical):** `squads/slides-creator/templates/slide-archetypes/`
- **Skill copy:** `.claude/skills/slide-creator/templates/slide-archetypes/` (this directory) — imported 2026-05-20 (YOLO SKILL-2)
- **Resync command:** `cp squads/slides-creator/templates/slide-archetypes/*.md .claude/skills/slide-creator/templates/slide-archetypes/`

These archetypes are the **consulting-grade spec patterns** for each canonical slide type. Use them in Phase 5 (Select canonical templates) of the skill workflow as authoritative reference patterns alongside `templates/wireframes/` (60 HTML layouts).

## Archetype Catalog

| File | Archetype | Use Case |
|------|-----------|----------|
| `title.md` | Cover | First slide; project + audience + date framing |
| `executive-summary.md` | Top-of-pyramid | Single-slide deck thesis with 3-5 supporting pillars |
| `framework.md` | Conceptual | 2x2 matrix, pyramid, value chain, frameworks (McKinsey 7S, Porter, BCG) |
| `data.md` | Quantitative chart | Bar/line/scatter/area with data table + sources + interpretation |
| `timeline-roadmap.md` | Temporal | Multi-quarter/year roadmap with milestones + dependencies |
| `financial.md` | P&L/bridge/EBITDA waterfall | Numbers-heavy with side-by-side comparison |
| `appendix.md` | Source/methodology | Methodology, full citations, glossary, regulatory references |

## Relationship to Wireframes

These archetypes are **content patterns** (what goes on the slide). The 60 wireframes in `templates/wireframes/` are **layout patterns** (where it goes on the slide). Both compose:

```
slide = wireframe (layout) × archetype (content pattern) × theme (visual)
```

## Update Protocol

When the squad updates an archetype:

1. Squad commits change to `squads/slides-creator/templates/slide-archetypes/{name}.md`
2. Skill resyncs via `cp` (see Provenance above)
3. This README's "imported" date is updated

If the skill needs an archetype the squad doesn't have, propose addition in the squad first (PR to `squads/slides-creator/templates/slide-archetypes/`), then resync.

## SoT Manifest Entry

See `references/sot-manifest.yaml#archetypes` for canonical SoT declaration.
