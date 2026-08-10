#!/usr/bin/env node
/**
 * validate-pipeline-emission.js — Mandamento 10 CI gate
 *
 * Scans outputs/slides-creator/{run_id}/ directories and verifies each run
 * emitted a pipeline-execution-log.yaml with >= MIN_RECORDS records.
 *
 * Usage:
 *   node squads/slides-creator/scripts/validate-pipeline-emission.js
 *   node squads/slides-creator/scripts/validate-pipeline-emission.js --run-id <id>
 *   node squads/slides-creator/scripts/validate-pipeline-emission.js --strict
 *   node squads/slides-creator/scripts/validate-pipeline-emission.js --json
 *
 * Exit codes:
 *   0 — all runs have valid pipeline-execution-log.yaml
 *   1 — at least one run is missing a log or has < MIN_RECORDS
 *   2 — IO or parse error
 *
 * Determinism: same filesystem state → same exit code + report. No network.
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const MIN_RECORDS = 8;
const VALID_EVENTS = new Set([
  'workflow_started',
  'phase_transition',
  'gate_verdict',
  'meta_axiom_breach',
  'deviation_logged',
  'killer_item_fired',
  'workflow_completion',
]);

function parseArgs(argv) {
  const args = { workspace: process.env.CLAUDE_PROJECT_DIR || process.cwd() };
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    const val = argv[i + 1];
    if (key === '--run-id') { args.runId = val; i++; }
    else if (key === '--workspace') { args.workspace = val; i++; }
    else if (key === '--strict') { args.strict = true; }
    else if (key === '--json') { args.json = true; }
    else if (key === '--help' || key === '-h') { args.help = true; }
  }
  return args;
}

function printHelp() {
  process.stdout.write(`validate-pipeline-emission.js — Mandamento 10 CI gate

Verifies that every outputs/slides-creator/{run_id}/ has a pipeline-execution-log.yaml
with >= ${MIN_RECORDS} records. Each record must declare a valid event from:
  ${[...VALID_EVENTS].join(' | ')}

Flags:
  --run-id <id>   Validate a single run instead of all
  --strict        Treat WARN (missing optional events) as failure
  --json          Emit machine-readable JSON
  -h, --help      Show this help

Exit: 0 pass | 1 fail | 2 error
`);
}

function listRunDirs(workspace) {
  const root = path.join(workspace, 'outputs', 'slides-creator');
  if (!fs.existsSync(root)) return [];
  return fs.readdirSync(root, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .filter(d => !d.name.startsWith('_') && !d.name.startsWith('.'))
    .map(d => path.join(root, d.name));
}

function parseRecordsFromYaml(yamlText) {
  // Minimal record counter — counts top-level `- event:` lines without requiring js-yaml dependency
  if (!yamlText) return { records: 0, events: [], parseError: null };
  const lines = yamlText.split(/\r?\n/);
  const events = [];
  for (const line of lines) {
    const m = line.match(/^\s*-\s*event:\s*([a-z_]+)\s*$/);
    if (m) events.push(m[1]);
  }
  return { records: events.length, events, parseError: null };
}

function validateRun(runDir) {
  const logPath = path.join(runDir, 'pipeline-execution-log.yaml');
  const result = {
    run_id: path.basename(runDir),
    log_path: logPath,
    log_exists: false,
    records: 0,
    events: [],
    has_workflow_started: false,
    has_workflow_completion: false,
    has_qa_verdict: false,
    invalid_events: [],
    verdict: 'FAIL',
    reasons: [],
  };

  if (!fs.existsSync(logPath)) {
    result.reasons.push(`pipeline-execution-log.yaml missing at ${logPath}`);
    return result;
  }
  result.log_exists = true;

  let yamlText;
  try {
    yamlText = fs.readFileSync(logPath, 'utf8');
  } catch (err) {
    result.reasons.push(`IO error reading ${logPath}: ${err.message}`);
    return result;
  }

  const parsed = parseRecordsFromYaml(yamlText);
  result.records = parsed.records;
  result.events = parsed.events;
  result.invalid_events = parsed.events.filter(e => !VALID_EVENTS.has(e));
  result.has_workflow_started = parsed.events.includes('workflow_started');
  result.has_workflow_completion = parsed.events.includes('workflow_completion');
  result.has_qa_verdict = parsed.events.some(e => e === 'gate_verdict');

  if (parsed.records < MIN_RECORDS) {
    result.reasons.push(`Only ${parsed.records} records (need >= ${MIN_RECORDS})`);
  }
  if (!result.has_workflow_started) {
    result.reasons.push('Missing workflow_started event');
  }
  if (!result.has_workflow_completion) {
    result.reasons.push('Missing workflow_completion event');
  }
  if (result.invalid_events.length > 0) {
    result.reasons.push(`Invalid events: ${result.invalid_events.join(', ')}`);
  }

  result.verdict = result.reasons.length === 0 ? 'PASS' : 'FAIL';
  return result;
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help) { printHelp(); process.exit(0); }

  let runDirs;
  if (args.runId) {
    const single = path.join(args.workspace, 'outputs', 'slides-creator', args.runId);
    if (!fs.existsSync(single)) {
      process.stderr.write(`ERROR: run dir not found: ${single}\n`);
      process.exit(2);
    }
    runDirs = [single];
  } else {
    runDirs = listRunDirs(args.workspace);
  }

  const results = runDirs.map(validateRun);
  const passCount = results.filter(r => r.verdict === 'PASS').length;
  const failCount = results.length - passCount;
  const summary = {
    total_runs: results.length,
    pass: passCount,
    fail: failCount,
    min_records_required: MIN_RECORDS,
    runs: results,
  };

  if (args.json) {
    process.stdout.write(JSON.stringify(summary, null, 2) + '\n');
  } else {
    process.stdout.write(`validate-pipeline-emission — ${results.length} run(s)\n`);
    for (const r of results) {
      const tag = r.verdict === 'PASS' ? 'PASS' : 'FAIL';
      process.stdout.write(`  [${tag}] ${r.run_id}: ${r.records} records${r.reasons.length ? ' — ' + r.reasons.join('; ') : ''}\n`);
    }
    process.stdout.write(`\nTotal: ${passCount} PASS / ${failCount} FAIL\n`);
  }

  process.exit(failCount === 0 ? 0 : 1);
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    process.stderr.write(`FATAL: ${err.stack || err.message}\n`);
    process.exit(2);
  }
}

module.exports = { parseArgs, parseRecordsFromYaml, validateRun, VALID_EVENTS, MIN_RECORDS };
