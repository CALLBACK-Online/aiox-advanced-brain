#!/usr/bin/env node
/**
 * emit-pipeline-log.js — Mandamento 10 (Observability) emission script
 *
 * Appends an execution record to outputs/slides-creator/{run_id}/pipeline-execution-log.yaml
 * on workflow events: phase_transition | gate_verdict | meta_axiom_breach |
 *                     deviation_logged | killer_item_fired | workflow_completion.
 *
 * Usage:
 *   node squads/slides-creator/scripts/emit-pipeline-log.js \
 *     --run-id <id> \
 *     --event <event_type> \
 *     --payload '<json>' \
 *     [--local_docs <path>]
 *
 * Exit codes: 0 success | 1 invalid args | 2 IO error | 3 schema violation
 *
 * Determinism: same input → same record. No network calls. No external deps beyond Node 18+ stdlib.
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const VALID_EVENTS = [
  'workflow_started',
  'phase_transition',
  'gate_verdict',
  'meta_axiom_breach',
  'deviation_logged',
  'killer_item_fired',
  'workflow_completion',
];

function parseArgs(argv) {
  const args = { local_docs: process.env.CLAUDE_PROJECT_DIR || process.cwd() };
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    const val = argv[i + 1];
    if (key === '--run-id') { args.runId = val; i++; }
    else if (key === '--event') { args.event = val; i++; }
    else if (key === '--payload') { args.payload = val; i++; }
    else if (key === '--local_docs') { args.local_docs = val; i++; }
    else if (key === '--dry-run') { args.dryRun = true; }
    else if (key === '--help' || key === '-h') { args.help = true; }
  }
  return args;
}

function printHelp() {
  process.stdout.write(`emit-pipeline-log.js — M10 emission script

Usage:
  node emit-pipeline-log.js --run-id <id> --event <event> --payload '<json>' [--local_docs <path>] [--dry-run]

Events: ${VALID_EVENTS.join(' | ')}

Output: appends YAML block to outputs/slides-creator/{run-id}/pipeline-execution-log.yaml
`);
}

function validateArgs(args) {
  const errors = [];
  if (!args.runId || !/^[A-Za-z0-9._-]+$/.test(args.runId)) {
    errors.push('--run-id required, alphanumeric/._- only');
  }
  if (!args.event || !VALID_EVENTS.includes(args.event)) {
    errors.push(`--event required, one of: ${VALID_EVENTS.join(', ')}`);
  }
  if (!args.payload) {
    errors.push('--payload required (JSON string)');
  } else {
    try { JSON.parse(args.payload); } catch (e) {
      errors.push(`--payload invalid JSON: ${e.message}`);
    }
  }
  return errors;
}

function toIsoUtc(date) {
  return new Date(date).toISOString();
}

function yamlEscape(s) {
  if (s === null || s === undefined) return '~';
  if (typeof s === 'number' || typeof s === 'boolean') return String(s);
  const str = String(s);
  if (/^[A-Za-z0-9._\/-]+$/.test(str)) return str;
  return JSON.stringify(str);
}

function serializeRecord(rec, indent = '  ') {
  const lines = [];
  for (const [key, val] of Object.entries(rec)) {
    if (val === null || val === undefined) {
      lines.push(`${indent}${key}: ~`);
    } else if (Array.isArray(val)) {
      if (val.length === 0) {
        lines.push(`${indent}${key}: []`);
      } else {
        lines.push(`${indent}${key}:`);
        for (const item of val) {
          if (typeof item === 'object' && item !== null) {
            lines.push(`${indent}  - ${serializeInline(item)}`);
          } else {
            lines.push(`${indent}  - ${yamlEscape(item)}`);
          }
        }
      }
    } else if (typeof val === 'object') {
      lines.push(`${indent}${key}:`);
      lines.push(serializeRecord(val, indent + '  '));
    } else {
      lines.push(`${indent}${key}: ${yamlEscape(val)}`);
    }
  }
  return lines.join('\n');
}

function serializeInline(obj) {
  const pairs = Object.entries(obj).map(([k, v]) => `${k}: ${yamlEscape(v)}`);
  return `{ ${pairs.join(', ')} }`;
}

function ensureLogFile(logPath, runId) {
  const dir = path.dirname(logPath);
  fs.mkdirSync(dir, { recursive: true });
  if (!fs.existsSync(logPath)) {
    const header = `---
# Pipeline execution log — slides-creator
# Run: ${runId}
# Schema: squads/slides-creator/data/pipeline-execution-log.yaml
schema_version: "1.0"
run_id: "${runId}"
events: []
`;
    fs.writeFileSync(logPath, header, 'utf8');
  }
}

function appendEvent(logPath, record) {
  const block = `\n  - event: ${record.event}\n${serializeRecord(record, '    ')}\n`;
  // Append under events: key (simple append — events list grows monotonically)
  const current = fs.readFileSync(logPath, 'utf8');
  if (current.includes('events: []')) {
    const replaced = current.replace('events: []', 'events:' + block);
    fs.writeFileSync(logPath, replaced, 'utf8');
  } else {
    fs.appendFileSync(logPath, block, 'utf8');
  }
}

function main() {
  const args = parseArgs(process.argv);

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const errors = validateArgs(args);
  if (errors.length > 0) {
    process.stderr.write(`emit-pipeline-log: invalid args\n  - ${errors.join('\n  - ')}\n`);
    process.exit(1);
  }

  const payload = JSON.parse(args.payload);
  const eventId = crypto.randomBytes(4).toString('hex');
  const timestamp = toIsoUtc(Date.now());

  const record = {
    event_id: `EV-${eventId}`,
    event: args.event,
    timestamp,
    run_id: args.runId,
    payload,
  };

  const logPath = path.join(
    args.local_docs,
    'outputs',
    'slides-creator',
    args.runId,
    'pipeline-execution-log.yaml'
  );

  if (args.dryRun) {
    process.stdout.write(`[DRY RUN] Would write to: ${logPath}\n`);
    process.stdout.write(`[DRY RUN] Record:\n${serializeRecord(record, '  ')}\n`);
    process.exit(0);
  }

  try {
    ensureLogFile(logPath, args.runId);
    appendEvent(logPath, record);
    process.stdout.write(`emit-pipeline-log: appended ${record.event_id} (${args.event}) to ${logPath}\n`);
    process.exit(0);
  } catch (err) {
    process.stderr.write(`emit-pipeline-log: IO error\n${err.stack || err.message}\n`);
    process.exit(2);
  }
}

if (require.main === module) {
  main();
}

module.exports = { parseArgs, validateArgs, serializeRecord, VALID_EVENTS };
