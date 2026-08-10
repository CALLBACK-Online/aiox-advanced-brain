#!/usr/bin/env node
/**
 * extract-wireframe-schemas.js
 *
 * Generates one JSON Schema (draft-07) per wireframe HTML in
 * `templates/wireframes/` from:
 *   1. `{{slot}}` placeholders extracted via regex from the HTML
 *   2. slot metadata declared in `templates/slide/function-library.yaml`
 *      (matched by snake_case function id ↔ kebab-case wireframe filename)
 *
 * Pattern absorbed from presenton (Apache-2.0):
 *   bench/presenton/servers/nextjs/lib/compile-template-schema.ts
 *   → SlideLayoutModel.json_schema()
 *
 * RULES (respect .claude/rules/extraction-no-fallbacks.md):
 *   - NEVER infer slot types not declared in function-library.
 *   - Default fallback for unknown slots is `type: string` WITHOUT maxLength,
 *     plus a `x-sinkra-warning: slot_not_in_function_library` marker.
 *   - Function-library is the only authoritative source of slot metadata.
 *
 * KISS — flat output, single file, zero external deps beyond js-yaml
 * (already in repo node_modules).
 *
 * Idempotent: re-running produces byte-identical output (sorted keys,
 * deterministic ordering).
 *
 * Usage:
 *   node .claude/skills/slide-creator/templates/scripts/extract-wireframe-schemas.js
 */

'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// ---------------------------------------------------------------------------
// Paths (script lives in templates/scripts/, output in templates/schemas/...)
// ---------------------------------------------------------------------------
const SCRIPT_DIR = __dirname;
const TEMPLATES_DIR = path.resolve(SCRIPT_DIR, '..');
const WIREFRAMES_DIR = path.join(TEMPLATES_DIR, 'wireframes');
const SCHEMAS_DIR = path.join(TEMPLATES_DIR, 'schemas', 'wireframe-schemas');
const FUNCTION_LIBRARY = path.join(TEMPLATES_DIR, 'slide', 'function-library.yaml');
// PR-W3i — canonical N:M wireframe→function join. Resolving function_ref via
// this map (instead of the filename↔id heuristic) eliminates the 734
// false-positive warnings from PR-2 (finding F-2).
const WIREFRAME_FUNCTION_MAP = path.join(
  TEMPLATES_DIR,
  'slide',
  'wireframe-function-map.yaml',
);

const REPO_REL = (abs) => path.relative(path.resolve(SCRIPT_DIR, '../../../../..'), abs);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function snakeToKebab(s) {
  return s.replace(/_/g, '-');
}

function kebabToSnake(s) {
  return s.replace(/-/g, '_');
}

/**
 * Extract unique `{{slot_name}}` placeholders from HTML in order of appearance.
 * Returns ordered array; preserves first-seen ordering for deterministic output.
 */
function extractSlotsFromHtml(html) {
  const seen = new Set();
  const ordered = [];
  const re = /\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const name = m[1];
    if (!seen.has(name)) {
      seen.add(name);
      ordered.push(name);
    }
  }
  return ordered;
}

/**
 * Build a property descriptor for a given slot name using function-library metadata.
 *
 * Decision tree:
 *   1. Find a function-library slot whose `name` exactly matches → use its type.
 *   2. If not found, try numbered-list expansion: e.g. `challenge_1` → list slot
 *      `challenges`. We DO NOT auto-infer (rule: no fallbacks); instead we mark
 *      the slot as a string with a warning.
 *   3. Default: { type: string } + warning.
 *
 * Hybrid enrichment rules:
 *   - function-library `type: list`  → JSON Schema `type: array, items: string`
 *   - function-library `type: image` → JSON Schema object with src + alt
 *   - function-library `type: text`  (or absent) → JSON Schema `type: string`
 *   - function-library `max_chars`   → JSON Schema `maxLength`
 *   - function-library `role`        → injected as `description`
 *
 * Returns: { property: <jsonSchemaProperty>, warning?: string }
 */
function buildPropertyForSlot(slotName, fnLibSlots) {
  // 1. Exact match in function-library
  const direct = fnLibSlots.find((s) => s.name === slotName);
  if (direct) {
    return { property: slotToJsonSchema(direct), warning: null, libSlot: direct };
  }

  // 2. Slot not in function-library — emit minimal string property + warning
  //    We do NOT infer numbered-list expansions automatically (no-fallbacks rule).
  //    Wireframes commonly expand list slots into numbered placeholders
  //    (e.g. `principles` list → `principle_1`, `principle_2`). The schema
  //    records each as a string. Generation tooling joins them at render time.
  return {
    property: { type: 'string' },
    warning: 'slot_not_in_function_library',
    libSlot: null,
  };
}

/**
 * Convert a function-library slot object to a JSON Schema property fragment.
 */
function slotToJsonSchema(slot) {
  const out = {};
  const t = slot.type || 'text';

  if (t === 'list') {
    out.type = 'array';
    out.items = { type: 'string' };
  } else if (t === 'image') {
    out.type = 'object';
    out.properties = {
      src: { type: 'string', format: 'uri' },
      alt: { type: 'string' },
    };
    out.required = ['src'];
    out.additionalProperties = false;
  } else {
    // text (default)
    out.type = 'string';
  }

  if (slot.max_chars != null) {
    // Only meaningful on strings; for arrays it would constrain serialized form,
    // which is not standard. Emit only on string-typed properties.
    if (out.type === 'string') out.maxLength = slot.max_chars;
  }

  if (slot.role) {
    out.description = String(slot.role);
  }

  return out;
}

/**
 * Sort object keys deterministically for reproducible JSON output.
 * Recursive — applies to nested objects but not arrays.
 */
function sortKeysDeep(obj) {
  if (Array.isArray(obj)) {
    return obj.map(sortKeysDeep);
  }
  if (obj && typeof obj === 'object') {
    const out = {};
    for (const k of Object.keys(obj).sort()) {
      out[k] = sortKeysDeep(obj[k]);
    }
    return out;
  }
  return obj;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  // Load function-library
  const fnLibRaw = fs.readFileSync(FUNCTION_LIBRARY, 'utf8');
  const fnLib = yaml.load(fnLibRaw);
  if (!fnLib || !Array.isArray(fnLib.slide_templates)) {
    console.error('FATAL: function-library.yaml has no `slide_templates[]`');
    process.exit(1);
  }

  // Index function entries by both snake_case id and kebab-case id for lookup
  const fnIndex = new Map();
  for (const fn of fnLib.slide_templates) {
    if (!fn.id) continue;
    fnIndex.set(fn.id, fn); // snake_case
    fnIndex.set(snakeToKebab(fn.id), fn); // kebab-case
  }

  // PR-W3i — load the canonical wireframe→function map. This is the
  // authoritative join (N:M by design). wireframe-id → primary_function
  // (a function-library id). Resolving through this map eliminates the
  // filename↔id false-positive warnings.
  const wfFnMap = new Map();
  try {
    const mapRaw = fs.readFileSync(WIREFRAME_FUNCTION_MAP, 'utf8');
    const parsed = yaml.load(mapRaw);
    if (parsed && Array.isArray(parsed.wireframes)) {
      for (const w of parsed.wireframes) {
        if (w.id && w.primary_function) {
          wfFnMap.set(w.id, w.primary_function);
        }
      }
    }
  } catch {
    // Map absent → fall back to filename heuristic (legacy behavior).
    // Not fatal: the map is an optimization, not a hard dependency.
  }

  // Enumerate wireframes
  const wireframes = fs
    .readdirSync(WIREFRAMES_DIR)
    .filter((f) => f.endsWith('.html'))
    .sort();

  let emitted = 0;
  const withWarnings = [];
  const noSlots = [];
  const noFunctionMatch = [];
  const writtenPaths = [];

  for (const file of wireframes) {
    const wfId = file.replace(/\.html$/, ''); // kebab-case id
    const snakeId = kebabToSnake(wfId);
    const html = fs.readFileSync(path.join(WIREFRAMES_DIR, file), 'utf8');
    const slots = extractSlotsFromHtml(html);

    if (slots.length === 0) noSlots.push(wfId);

    // PR-W3i — resolve function via the canonical N:M map FIRST. Fall back
    // to the legacy filename↔id heuristic only when the map has no entry
    // (keeps the script working if the map is incomplete).
    const mappedFnId = wfFnMap.get(wfId);
    const fn =
      (mappedFnId && fnIndex.get(mappedFnId)) ||
      fnIndex.get(wfId) ||
      fnIndex.get(snakeId);
    if (!fn) noFunctionMatch.push(wfId);

    const fnLibSlots = (fn && Array.isArray(fn.slots) ? fn.slots : []);

    // Build properties
    const properties = {};
    const required = [];
    const warnings = [];

    for (const slotName of slots) {
      const { property, warning } = buildPropertyForSlot(slotName, fnLibSlots);
      properties[slotName] = property;
      if (warning) warnings.push({ slot: slotName, warning });
    }

    // If function-library declared a slot as required AND it appears in the HTML,
    // mark it in `required[]`. If function-library declared required but HTML
    // doesn't reference it (rare — usually HTML expands lists into numbered
    // placeholders), we do NOT add to required.
    for (const slot of fnLibSlots) {
      if (slot.required && properties[slot.name]) {
        required.push(slot.name);
      }
    }

    // x-sinkra warnings — record slots not found in function-library
    // (this is informational, not blocking).
    const xWarnings = warnings.map((w) => w.slot);

    // Description from function-library (use pick_when[0] if available)
    let description = `JSON Schema for wireframe ${wfId}.html`;
    if (fn && Array.isArray(fn.pick_when) && fn.pick_when.length > 0) {
      description = String(fn.pick_when[0]).trim();
    }

    const schema = {
      $schema: 'http://json-schema.org/draft-07/schema#',
      $id: `sinkra://slide-creator/wireframes/${wfId}.schema.json`,
      title: wfId,
      description,
      type: 'object',
      properties,
      additionalProperties: false,
      'x-sinkra': {
        wireframe_ref: `templates/wireframes/${file}`,
        function_ref: fn ? fn.id : null,
        absorbed_pattern_from: 'presenton (Apache-2.0)',
        slot_count: slots.length,
        warnings: xWarnings.length > 0 ? xWarnings : null,
      },
    };

    if (required.length > 0) {
      // Insert before properties (alphabetical sort will reorder later)
      schema.required = required.slice().sort();
    }

    // Deterministic key ordering
    const sorted = sortKeysDeep(schema);
    const outFile = path.join(SCHEMAS_DIR, `${wfId}.schema.json`);
    const outJson = JSON.stringify(sorted, null, 2) + '\n';
    fs.writeFileSync(outFile, outJson, 'utf8');

    writtenPaths.push(outFile);
    emitted++;
    if (xWarnings.length > 0) {
      withWarnings.push({ id: wfId, slots: xWarnings });
    }
  }

  // ---------------------------------------------------------------------------
  // stdout summary
  // ---------------------------------------------------------------------------
  console.log('extract-wireframe-schemas — summary');
  console.log('-----------------------------------');
  console.log(`Wireframes scanned         : ${wireframes.length}`);
  console.log(`Schemas emitted            : ${emitted}`);
  console.log(`No {{slot}} placeholders   : ${noSlots.length} ` +
    (noSlots.length > 0 ? `(${noSlots.join(', ')})` : ''));
  console.log(`No function-library match  : ${noFunctionMatch.length} ` +
    (noFunctionMatch.length > 0 ? `(${noFunctionMatch.join(', ')})` : ''));
  console.log(`Schemas with warnings      : ${withWarnings.length}`);
  if (withWarnings.length > 0) {
    console.log('');
    console.log('Warnings detail (slots present in HTML but not in function-library):');
    for (const w of withWarnings) {
      console.log(`  - ${w.id}: ${w.slots.join(', ')}`);
    }
  }
  console.log('');
  console.log(`Output dir                 : ${REPO_REL(SCHEMAS_DIR)}`);
  console.log(`Sample files (first 5)     :`);
  for (const p of writtenPaths.slice(0, 5)) {
    console.log(`  - ${REPO_REL(p)}`);
  }
}

main();
