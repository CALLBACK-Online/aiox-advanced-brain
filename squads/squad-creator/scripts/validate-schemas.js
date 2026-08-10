#!/usr/bin/env node
/**
 * validate-schemas.js — CLI Wrapper for AJV Schema Validation
 * EPIC-109 Wave 3 (C6)
 *
 * Usage:
 *   node scripts/validate-schemas.js <squad-path> [options]
 *
 * Options:
 *   --format json|text    Output format (default: text)
 *   --strict              Exit 1 on any validation failure (default: exits 0 on skip/warn)
 *
 * Discovery logic:
 *   Glob: schemas/*.schema.json in the squad directory
 *   Data matching convention: {name}.schema.json → look for {name}.json or {name}.yaml in:
 *     - data/
 *     - outputs/ (relative to squad path)
 *   If no data file found: skip with INFO
 *
 * Output (--format json) is compatible with validation-report.schema.json (C4 Wave 1).
 *
 * Exit codes:
 *   0 = all validations passed (or no schemas to validate)
 *   1 = at least one validation failed
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { validate } = require('./lib/ajv-validate');

// ─── Parse CLI arguments ─────────────────────────────────────────────────────

const args = process.argv.slice(2);
const squadPathArg = args.find(a => !a.startsWith('--'));
const formatArg = args.includes('--format') ? args[args.indexOf('--format') + 1] : 'text';
const strictMode = args.includes('--strict');

if (!squadPathArg) {
  process.stderr.write('Usage: node validate-schemas.js <squad-path> [--format json|text] [--strict]\n');
  process.exit(1);
}

const squadPath = path.resolve(squadPathArg);
const schemasDir = path.join(squadPath, 'schemas');

// ─── Discover schemas ────────────────────────────────────────────────────────

if (!fs.existsSync(schemasDir)) {
  output({ message: `No schemas/ directory found at ${schemasDir}. Nothing to validate.`, checks: [], summary: 'SKIP' });
  process.exit(0);
}

const schemaFiles = fs.readdirSync(schemasDir)
  .filter(f => f.endsWith('.schema.json'))
  .map(f => path.join(schemasDir, f));

if (schemaFiles.length === 0) {
  output({ message: 'No *.schema.json files found in schemas/. Nothing to validate.', checks: [], summary: 'SKIP' });
  process.exit(0);
}

// ─── Data discovery convention ───────────────────────────────────────────────

/**
 * Find the data file for a given schema base name.
 * Looks in: {squad}/data/{name}.json, {squad}/data/{name}.yaml,
 *            {squad}/outputs/{name}.json, {squad}/outputs/{name}.yaml
 *
 * @param {string} squadDir
 * @param {string} baseName — schema filename without .schema.json
 * @returns {string|null}
 */
function findDataFile(squadDir, baseName) {
  const candidates = [
    path.join(squadDir, 'data', `${baseName}.json`),
    path.join(squadDir, 'data', `${baseName}.yaml`),
    path.join(squadDir, 'data', `${baseName}.yml`),
    path.join(squadDir, 'outputs', `${baseName}.json`),
    path.join(squadDir, 'outputs', `${baseName}.yaml`),
    path.join(squadDir, 'outputs', `${baseName}.yml`),
  ];
  return candidates.find(c => fs.existsSync(c)) || null;
}

// ─── Run validations ─────────────────────────────────────────────────────────

const timestamp = new Date().toISOString();
const checks = [];
let totalFailed = 0;
let totalPassed = 0;
let totalSkipped = 0;

for (const schemaFile of schemaFiles) {
  const schemaFileName = path.basename(schemaFile);
  const baseName = schemaFileName.replace(/\.schema\.json$/, '');
  const dataFile = findDataFile(squadPath, baseName);

  if (!dataFile) {
    checks.push({
      id: `schema-${baseName}`,
      name: `Validate ${baseName}`,
      result: 'SKIP',
      blocking: false,
      message: `No data file found for schema ${schemaFileName}. Skipped.`,
      schema: schemaFile,
    });
    totalSkipped++;
    if (formatArg === 'text') {
      process.stdout.write(`[INFO] SKIP: ${schemaFileName} — no matching data file\n`);
    }
    continue;
  }

  const result = validate(schemaFile, dataFile);

  const checkResult = result.degraded ? 'SKIP' : (result.valid ? 'PASS' : 'FAIL');

  checks.push({
    id: `schema-${baseName}`,
    name: `Validate ${baseName}`,
    result: checkResult,
    blocking: !result.degraded,
    message: result.degraded
      ? 'AJV not available — graceful degradation (skip)'
      : (result.valid ? 'Schema validation passed' : `${result.errors.length} error(s) found`),
    location: dataFile,
    schema: schemaFile,
    errors: result.errors,
  });

  if (result.degraded || result.valid) {
    if (result.degraded) totalSkipped++;
    else totalPassed++;

    if (formatArg === 'text') {
      process.stdout.write(`[${checkResult}] ${schemaFileName} → ${path.basename(dataFile)}\n`);
    }
  } else {
    totalFailed++;
    if (formatArg === 'text') {
      process.stdout.write(`[FAIL] ${schemaFileName} → ${path.basename(dataFile)}\n`);
      result.errors.forEach(e => {
        process.stdout.write(`       ${e.instancePath || '/'}: ${e.message}\n`);
      });
    }
  }
}

// ─── Build summary ───────────────────────────────────────────────────────────

const total = checks.length;
const overallVerdict = totalFailed > 0 ? 'FAIL' : (totalPassed > 0 ? 'PASS' : 'SKIP');

const squadConfigPath = path.join(squadPath, 'config.yaml');
const squadName = path.basename(squadPath);

// Try to read version from config.yaml
let squadVersion = '0.0.0';
try {
  const configRaw = fs.readFileSync(squadConfigPath, 'utf8');
  const vMatch = configRaw.match(/version:\s*["']?([^"'\n]+)["']?/);
  if (vMatch) squadVersion = vMatch[1].trim();
} catch (_) {}

const report = {
  squad_name: squadName,
  version: squadVersion,
  timestamp,
  total_checks: total,
  passed: totalPassed,
  failed: totalFailed,
  skipped: totalSkipped,
  blocking_passed: totalFailed === 0,
  final_score: total > 0 ? (totalPassed / Math.max(total - totalSkipped, 1)) * 10 : 10,
  verdict: overallVerdict,
  dimensions: {
    schema_validation: {
      weight: 1.0,
      score: total > 0 ? totalPassed / Math.max(total - totalSkipped, 1) : 1,
      weighted_score: total > 0 ? (totalPassed / Math.max(total - totalSkipped, 1)) * 10 : 10,
      details: `${totalPassed}/${total - totalSkipped} schemas valid`,
    },
  },
  checks,
  recommended_actions: totalFailed > 0
    ? checks.filter(c => c.result === 'FAIL').map(c => `Fix schema violations in ${c.location}`)
    : [],
};

// ─── Output ──────────────────────────────────────────────────────────────────

function output(data) {
  if (formatArg === 'json') {
    process.stdout.write(JSON.stringify(data, null, 2) + '\n');
  }
}

output(report);

if (formatArg === 'text') {
  process.stdout.write(`\n── Summary ─────────────────────────────────────────────\n`);
  process.stdout.write(`  Total:   ${total}\n`);
  process.stdout.write(`  Passed:  ${totalPassed}\n`);
  process.stdout.write(`  Failed:  ${totalFailed}\n`);
  process.stdout.write(`  Skipped: ${totalSkipped}\n`);
  process.stdout.write(`  Verdict: ${overallVerdict}\n`);
}

// Exit code logic
if (strictMode && totalFailed > 0) {
  process.exit(1);
} else if (!strictMode && totalFailed > 0) {
  process.exit(1); // AJV invalid always = exit 1 (override rule)
}
process.exit(0);
