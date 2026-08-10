# Slide Creator — Scripts

## extract-wireframe-schemas.js

Generates `templates/schemas/wireframe-schemas/*.schema.json` (1 per wireframe HTML)
from `templates/wireframes/*.html` + `templates/slide/function-library.yaml`.

Deterministic and idempotent. Re-running produces byte-identical output (sorted keys).

Pattern absorbed from presenton (Apache-2.0) — `SlideLayoutModel.json_schema()`.

### Run

```bash
node skills/slide-creator/templates/scripts/extract-wireframe-schemas.js
```

### Output

- 58 `*.schema.json` files under `templates/schemas/wireframe-schemas/` (one per wireframe).
- stdout summary: scan counts, schemas emitted, warnings (slots present in HTML but
  absent from `function-library.yaml`), sample paths.

### Rules respected

- `.claude/rules/extraction-no-fallbacks.md` — NEVER infers slot types not declared
  in `function-library.yaml`. Unknown slots default to `type: string` with a
  `x-aiox.warnings[]` marker; no synthetic `maxLength`, no implicit list expansion.
- `.claude/rules/kiss-no-overengineering.md` — single flat script, flat output
  directory, zero external deps beyond `js-yaml` (already in repo `node_modules`).
- `.claude/rules/portable-paths.md` — all paths resolved via `__dirname`; no
  machine-specific absolutes.
