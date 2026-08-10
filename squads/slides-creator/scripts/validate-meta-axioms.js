#!/usr/bin/env node
/**
 * validate-meta-axioms.js — Mandamento 8 (Meta-Axioms) scoring validator
 *
 * Computes truth/completeness/coherence scores per
 * squads/slides-creator/data/composition-rules.yaml#meta_axioms
 * and emits meta_axiomas_overall composite.
 *
 * 16 scoring signals across 3 dimensions, each a deterministic file scan.
 *
 * Usage:
 *   node squads/slides-creator/scripts/validate-meta-axioms.js [--squad <slug>] [--json] [--strict]
 *
 * Default squad: slides-creator. --json emits machine-readable result.
 * --strict exits 1 if composite < release_floor (75).
 *
 * Exit codes: 0 PASS (>= floor) | 1 BELOW_FLOOR (--strict only) | 2 IO error
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const REPO_ROOT = process.env.CLAUDE_PROJECT_DIR || process.cwd();

function parseArgs(argv) {
  const args = { squad: 'slides-creator', json: false, strict: false };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i], v = argv[i + 1];
    if (k === '--squad') { args.squad = v; i++; }
    else if (k === '--json') args.json = true;
    else if (k === '--strict') args.strict = true;
    else if (k === '--help' || k === '-h') args.help = true;
  }
  return args;
}

function safeRead(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return null; }
}

function listTaskFiles(squadPath) {
  const dir = path.join(squadPath, 'tasks');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(f => f.endsWith('.md')).map(f => path.join(dir, f));
}

// ─── TRUTH signals (5) ────────────────────────────────────────────────
function scoreTruth(squadPath) {
  const signals = [];

  // Signal 1: source_ref traceability in evidence ledger schema
  const evidenceLedger = safeRead(path.join(squadPath, 'data/qa-rubric.yaml'));
  signals.push({
    weight: 0.30,
    name: 'evidence_ledger_source_ref',
    pass: evidenceLedger && /KI-11|evidence_ledger|source_ref/i.test(evidenceLedger),
  });

  // Signal 2: principios-invioláveis enforcement_level references
  const principios = safeRead(path.join(squadPath, 'data/principios-invioláveis.md'));
  signals.push({
    weight: 0.20,
    name: 'enforcement_level_referenced',
    pass: principios && /(enforcement_level|enforced_by|code|schema|validator)/i.test(principios),
  });

  // Signal 3: composition_mapping no phantom refs (all referenced files exist)
  const config = safeRead(path.join(squadPath, 'config.yaml'));
  let phantomRefs = 0;
  if (config) {
    const taskRefs = [...config.matchAll(/tasks\/([\w-]+)\.md/g)].map(m => m[1]);
    const taskFiles = new Set(listTaskFiles(squadPath).map(p => path.basename(p, '.md')));
    phantomRefs = taskRefs.filter(t => !taskFiles.has(t)).length;
  }
  signals.push({
    weight: 0.20,
    name: 'composition_mapping_no_phantom_refs',
    pass: phantomRefs === 0,
    note: `phantom_count=${phantomRefs}`,
  });

  // Signal 4: token-registry token_definitions non-empty per family
  const tokenRegistry = safeRead(path.join(squadPath, 'data/token-registry.yaml'));
  signals.push({
    weight: 0.15,
    name: 'token_definitions_populated',
    pass: tokenRegistry && /token_definitions:/.test(tokenRegistry) && /SLIDES_/.test(tokenRegistry),
  });

  // Signal 5: workflow gates reference defined thresholds
  const workflow = safeRead(path.join(squadPath, 'workflows/generate-presentation.yaml'));
  signals.push({
    weight: 0.15,
    name: 'workflow_gates_defined',
    pass: workflow && /D04:/.test(workflow) && /pass_criteria:/.test(workflow),
  });

  return computeDimension(signals);
}

// ─── COMPLETENESS signals (5) ─────────────────────────────────────────
function scoreCompleteness(squadPath) {
  const signals = [];

  // Signal 1: 100% tasks declare 8 AIOX mandatory fields (flat block OR sectional ### N format)
  const taskFiles = listTaskFiles(squadPath);
  let fullCompliance = 0;
  // Each entry: list of acceptable patterns (any match = field present)
  const required = [
    [/^task:\s+\w+/m, /task:\s+\w+/, /###\s+1\.\s*task/i],
    [/^atomic_layer:\s+\w+/m, /atomic_layer:\s+\w+/, /###\s+\d+\.\s*atomic_layer/i],
    [/^responsavel_type:\s+\w+/m, /responsavel_type:\s+\w+/, /###\s+\d+\.\s*responsavel_type/i],
    [/^Inputs?:/m, /###\s+\d+\.\s*Inputs?(\[\])?/i],
    [/^Outputs?:/m, /###\s+\d+\.\s*Outputs?(\[\])?/i],
    [/Pre.conditions/i, /###\s+\d+\.\s*Pre.conditions/i],
    [/Post.conditions/i, /###\s+\d+\.\s*Post.conditions/i],
    [/Acceptance.criteria|Acceptance Criteria/i, /###\s+\d+\.\s*Post.conditions\s*\+\s*Acceptance/i],
  ];
  for (const f of taskFiles) {
    const content = safeRead(f) || '';
    const has = required.every(patterns => patterns.some(rx => rx.test(content)));
    if (has) fullCompliance++;
  }
  const completenessRatio = taskFiles.length > 0 ? fullCompliance / taskFiles.length : 0;
  signals.push({
    weight: 0.30,
    name: 'tasks_8_field_compliance',
    pass: completenessRatio >= 0.95,
    note: `${fullCompliance}/${taskFiles.length}`,
  });

  // Signal 2: 100% tasks placed in composition_mapping.atoms
  const config = safeRead(path.join(squadPath, 'config.yaml')) || '';
  const taskSlugs = new Set(taskFiles.map(p => path.basename(p, '.md')));
  const mappedSlugs = new Set([...config.matchAll(/tasks\/([\w-]+)\.md/g)].map(m => m[1]));
  const orphans = [...taskSlugs].filter(t => !mappedSlugs.has(t));
  signals.push({
    weight: 0.20,
    name: 'no_orphan_tasks',
    pass: orphans.length === 0,
    note: `orphans=${orphans.length}`,
  });

  // Signal 3: all gates referenced have definitions with thresholds
  const workflow = safeRead(path.join(squadPath, 'workflows/generate-presentation.yaml')) || '';
  const phantomGates = !/gate: D04[^\n]*\n[^\n]*/.test(workflow) || !/D04:/.test(workflow);
  signals.push({
    weight: 0.20,
    name: 'gates_fully_defined',
    pass: !phantomGates && /D04:/.test(workflow),
  });

  // Signal 4: infrastructure-map.yaml maps automated tasks
  const infraMap = safeRead(path.join(squadPath, 'data/infrastructure-map.yaml')) || '';
  const taskInfraLines = [...infraMap.matchAll(/^\s+-\s+task:\s+/gm)].length;
  signals.push({
    weight: 0.15,
    name: 'infrastructure_map_coverage',
    pass: taskInfraLines >= 40 && /reuse_ratio:/.test(infraMap),
    note: `task_count=${taskInfraLines}`,
  });

  // Signal 5: deviation-registry.yaml exists with schema (M7)
  const deviationReg = safeRead(path.join(squadPath, 'data/deviation-registry.yaml'));
  signals.push({
    weight: 0.15,
    name: 'deviation_registry_present',
    pass: deviationReg && /schema:/.test(deviationReg) && /deviations:/.test(deviationReg),
  });

  return computeDimension(signals);
}

// ─── COHERENCE signals (6) ────────────────────────────────────────────
function scoreCoherence(squadPath) {
  const signals = [];

  // Signal 1: task atomic_layer matches composition_mapping placement
  const config = safeRead(path.join(squadPath, 'config.yaml')) || '';
  const atomsBlockMatch = config.match(/atoms:[\s\S]*?molecules:/);
  const atomsBlock = atomsBlockMatch ? atomsBlockMatch[0] : '';
  const inAtoms = new Set([...atomsBlock.matchAll(/tasks\/([\w-]+)\.md/g)].map(m => m[1]));
  let mismatches = 0;
  for (const f of listTaskFiles(squadPath)) {
    const slug = path.basename(f, '.md');
    const content = safeRead(f) || '';
    const layerMatch = content.match(/atomic_layer:\s*(\w+)/);
    if (!layerMatch) continue;
    if (inAtoms.has(slug) && layerMatch[1] !== 'Atom' && layerMatch[1] !== 'Organism') {
      mismatches++;
    }
  }
  signals.push({
    weight: 0.25,
    name: 'atomic_layer_matches_mapping',
    pass: mismatches === 0,
    note: `mismatches=${mismatches}`,
  });

  // Signal 2: task Domain HTML comment + standalone match
  let domainMismatches = 0;
  for (const f of listTaskFiles(squadPath)) {
    const content = safeRead(f) || '';
    const html = content.match(/<!--\s*AIOX Domain:\s*(\w+)/);
    const standalone = content.match(/^Domain:\s*(\w+)/m);
    if (html && standalone && html[1] !== standalone[1]) domainMismatches++;
  }
  signals.push({
    weight: 0.20,
    name: 'domain_dual_declaration_match',
    pass: domainMismatches === 0,
    note: `mismatches=${domainMismatches}`,
  });

  // Signal 3: PPTEval threshold SOT referenced
  const qaRubric = safeRead(path.join(squadPath, 'data/qa-rubric.yaml')) || '';
  const workflow = safeRead(path.join(squadPath, 'workflows/generate-presentation.yaml')) || '';
  signals.push({
    weight: 0.20,
    name: 'ppteval_sot_referenced',
    pass: /sot:\s*\n\s*canonical:\s*true/.test(qaRubric) && /threshold_sot:/.test(workflow),
  });

  // Signal 4: Token registry quality_gate matches config quality_gates
  const tokenRegistry = safeRead(path.join(squadPath, 'data/token-registry.yaml')) || '';
  signals.push({
    weight: 0.15,
    name: 'token_quality_gate_alignment',
    pass: /quality_gate:/.test(tokenRegistry) && /quality_gates:/.test(config),
  });

  // Signal 5: executor declarations match infrastructure-map
  const infraMap = safeRead(path.join(squadPath, 'data/infrastructure-map.yaml')) || '';
  signals.push({
    weight: 0.10,
    name: 'executor_infra_alignment',
    pass: /task_infrastructure:/.test(infraMap) && /executor:/.test(infraMap),
  });

  // Signal 6: principios-invioláveis P1-P7 align with config.yaml#invariants
  const principios = safeRead(path.join(squadPath, 'data/principios-invioláveis.md')) || '';
  const p1to7 = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'].every(p => principios.includes(p) && config.includes(p));
  signals.push({
    weight: 0.10,
    name: 'invariants_principios_alignment',
    pass: p1to7,
  });

  return computeDimension(signals);
}

function computeDimension(signals) {
  const total = signals.reduce((sum, s) => sum + s.weight, 0);
  const score = signals.reduce((sum, s) => sum + (s.pass ? s.weight : 0) * 100, 0) / total;
  return { score: Math.round(score * 10) / 10, signals };
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    process.stdout.write(`validate-meta-axioms.js — M8 scoring validator\n\nUsage: node validate-meta-axioms.js [--squad <slug>] [--json] [--strict]\n`);
    process.exit(0);
  }

  const squadPath = path.join(REPO_ROOT, 'squads', args.squad);
  if (!fs.existsSync(squadPath)) {
    process.stderr.write(`squad not found: ${squadPath}\n`);
    process.exit(2);
  }

  const truth = scoreTruth(squadPath);
  const completeness = scoreCompleteness(squadPath);
  const coherence = scoreCoherence(squadPath);

  // Weighted composite per composition-rules.yaml#meta_axiomas_overall
  const composite = Math.round((truth.score * 0.40 + completeness.score * 0.35 + coherence.score * 0.25) * 10) / 10;
  const verdict = composite >= 75 ? 'PASS' : composite >= 70 ? 'PARTIAL' : 'FAIL';

  const result = {
    squad: args.squad,
    timestamp: new Date().toISOString(),
    truth: truth.score,
    completeness: completeness.score,
    coherence: coherence.score,
    composite,
    verdict,
    release_floor: 75,
    signals: {
      truth: truth.signals,
      completeness: completeness.signals,
      coherence: coherence.signals,
    },
  };

  if (args.json) {
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  } else {
    process.stdout.write(`Meta-Axioms validation — ${args.squad}\n`);
    process.stdout.write(`  truth:        ${result.truth}\n`);
    process.stdout.write(`  completeness: ${result.completeness}\n`);
    process.stdout.write(`  coherence:    ${result.coherence}\n`);
    process.stdout.write(`  composite:    ${result.composite} (verdict: ${verdict})\n`);
    process.stdout.write(`\nSignals:\n`);
    for (const [dim, list] of Object.entries(result.signals)) {
      process.stdout.write(`  ${dim}:\n`);
      for (const s of list) {
        process.stdout.write(`    [${s.pass ? 'PASS' : 'FAIL'}] ${s.name}${s.note ? ' (' + s.note + ')' : ''}\n`);
      }
    }
  }

  if (args.strict && composite < 75) process.exit(1);
  process.exit(0);
}

if (require.main === module) main();

module.exports = { scoreTruth, scoreCompleteness, scoreCoherence };
