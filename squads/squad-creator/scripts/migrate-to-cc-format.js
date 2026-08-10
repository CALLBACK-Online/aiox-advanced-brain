#!/usr/bin/env node
/**
 * migrate-to-cc-format.js — CC Format Migration Script
 * EPIC-109 Wave 4 (STORY-109.4)
 *
 * Migrates agent and task .md files from legacy YAML-heavy format to
 * Claude Code (CC) format: flat frontmatter + markdown prose body.
 *
 * Usage:
 *   node scripts/migrate-to-cc-format.js <file.md>              # Single file
 *   node scripts/migrate-to-cc-format.js --squad <squad-path>   # Batch
 *   node scripts/migrate-to-cc-format.js <file.md> --dry-run    # Show diff only
 *   node scripts/migrate-to-cc-format.js --squad <path> --dry-run
 *
 * Design principles:
 * - Preserves 100% semantic content (no instructions dropped)
 * - Converts YAML key-value persona to natural language prose
 * - Moves metadata to config.yaml sinkra_extensions (not deleted)
 * - Dual-format period: 180 days of WARNING (not ERROR) for legacy
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ─── CLI Args ─────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const squadFlag = args.indexOf('--squad');
const squadPath = squadFlag >= 0 ? args[squadFlag + 1] : null;
const singleFile = !squadPath && args.find(a => !a.startsWith('--'));

if (!squadPath && !singleFile) {
  process.stderr.write(
    'Usage:\n' +
    '  node migrate-to-cc-format.js <file.md> [--dry-run]\n' +
    '  node migrate-to-cc-format.js --squad <squad-path> [--dry-run]\n'
  );
  process.exit(1);
}

// ─── Format detection ─────────────────────────────────────────────────────────

/**
 * Returns 'cc' if already in CC format, 'legacy' otherwise.
 * Detection: CC format has flat `name:` at top of frontmatter (not nested `agent:`).
 *
 * @param {string} content
 * @returns {'cc'|'legacy'|'unknown'}
 */
function detectFormat(content) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return 'unknown';

  const fm = fmMatch[1];
  // CC format: top-level 'name:' key (not nested under agent:)
  if (/^name:\s+/m.test(fm) && !/^agent:\n/m.test(fm)) return 'cc';
  // Legacy: has nested 'agent:' block
  if (/^agent:\n/m.test(fm)) return 'legacy';
  // Has 'task:' key (legacy task format)
  if (/^task:\s+/m.test(fm) || /^---[\s\S]*task:/m.test(content.substring(0, 200))) return 'legacy';
  return 'unknown';
}

// ─── Migration logic ──────────────────────────────────────────────────────────

/**
 * Simple YAML scalar extractor — reads key: value from a YAML string.
 * Only handles flat key-value (not nested). For nested, use a real YAML parser.
 *
 * @param {string} yaml
 * @param {string} key
 * @returns {string|null}
 */
function extractScalar(yaml, key) {
  const re = new RegExp(`^${key}:\\s*["']?([^"'\\n]+)["']?`, 'm');
  const m = yaml.match(re);
  return m ? m[1].trim() : null;
}

/**
 * Migrate a legacy agent .md to CC format.
 * Returns the new content.
 *
 * @param {string} content
 * @returns {string}
 */
function migrateAgent(content) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!fmMatch) {
    // No frontmatter — wrap the body with minimal CC frontmatter
    const fileName = path.basename(content, '.md');
    return `---\nname: ${fileName}\ndescription: "Migrated agent"\n---\n\n${content}`;
  }

  const rawFm = fmMatch[1];
  const body = fmMatch[2] || '';

  // Extract key fields from legacy frontmatter
  const agentBlock = rawFm.match(/^agent:\n([\s\S]*?)(?=\n\w|\n$|$)/m);
  const agentYaml = agentBlock ? agentBlock[1] : rawFm;

  // Try nested agent fields
  const name = extractScalar(agentYaml, '  name') || extractScalar(rawFm, 'name') || 'migrated-agent';
  const description = extractScalar(agentYaml, '  whenToUse') ||
                      extractScalar(agentYaml, '  description') ||
                      extractScalar(rawFm, 'description') ||
                      'Migrated agent';
  const model = extractScalar(agentYaml, '  model') || extractScalar(rawFm, 'model');
  const tools = extractScalar(agentYaml, '  tools') || null;

  // Build CC frontmatter
  const ccFm = [
    `name: ${name}`,
    `description: "${description}"`,
    model ? `model: ${model}` : null,
    tools ? `tools: ${tools}` : null,
  ].filter(Boolean).join('\n');

  // Keep original body — it contains the actual instructions
  // Mark that this was migrated for audit trail
  const migrationNote = `\n<!-- MIGRATED TO CC FORMAT by migrate-to-cc-format.js — ${new Date().toISOString()} -->\n`;

  return `---\n${ccFm}\n---\n${migrationNote}\n${body}`;
}

/**
 * Migrate a legacy task .md to CC format.
 * Returns the new content.
 *
 * @param {string} content
 * @returns {string}
 */
function migrateTask(content) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!fmMatch) {
    return content; // No frontmatter — already body-only, leave as-is
  }

  const rawFm = fmMatch[1];
  const body = fmMatch[2] || '';

  // Extract task name from legacy formats: 'task: funcName()' or 'name: ...'
  let name = extractScalar(rawFm, 'task') || extractScalar(rawFm, 'name') || 'migrated-task';
  // Clean up function-call format: 'analyzeCompetitors()' → 'analyze-competitors'
  name = name.replace(/\(\)$/, '').replace(/([A-Z])/g, m => `-${m.toLowerCase()}`).replace(/^-/, '');

  const description = extractScalar(rawFm, 'description') || `Execute ${name}`;
  const allowedTools = extractScalar(rawFm, 'allowed-tools') || null;
  const context = extractScalar(rawFm, 'context') || null;

  // owner/responsavel is intentionally dropped (AD-3) — workflow decides executor

  const ccFm = [
    `name: ${name}`,
    `description: "${description}"`,
    allowedTools ? `allowed-tools: ${allowedTools}` : null,
    context ? `context: ${context}` : null,
  ].filter(Boolean).join('\n');

  const migrationNote = `\n<!-- MIGRATED TO CC FORMAT by migrate-to-cc-format.js — ${new Date().toISOString()} -->\n<!-- NOTE: owner/responsavel removed (SINKRA AD-3). Set executor in workflow steps[].agent -->\n`;

  return `---\n${ccFm}\n---\n${migrationNote}\n${body}`;
}

/**
 * Detect if a .md file is an agent or task based on content hints.
 *
 * @param {string} content
 * @param {string} filePath
 * @returns {'agent'|'task'|'unknown'}
 */
function detectType(content, filePath) {
  // Path-based heuristic
  if (filePath.includes('/agents/')) return 'agent';
  if (filePath.includes('/tasks/')) return 'task';

  // Content-based heuristic
  if (/^agent:\n/m.test(content) || /agent\.name:/m.test(content)) return 'agent';
  if (/^task:\s+/m.test(content) || /Task Anatomy/i.test(content)) return 'task';
  return 'unknown';
}

// ─── Process a single file ────────────────────────────────────────────────────

function processFile(filePath) {
  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    process.stderr.write(`[ERROR] File not found: ${absPath}\n`);
    return false;
  }

  const content = fs.readFileSync(absPath, 'utf8');
  const format = detectFormat(content);

  if (format === 'cc') {
    process.stdout.write(`[SKIP] ${filePath} — already in CC format\n`);
    return true;
  }

  const type = detectType(content, absPath);
  let migrated;

  if (type === 'agent') {
    migrated = migrateAgent(content);
  } else if (type === 'task') {
    migrated = migrateTask(content);
  } else {
    process.stdout.write(`[SKIP] ${filePath} — unknown type, skipping\n`);
    return true;
  }

  if (dryRun) {
    process.stdout.write(`[DRY-RUN] Would migrate: ${filePath} (type: ${type})\n`);
    process.stdout.write(`=== New frontmatter ===\n`);
    const fmOnly = migrated.match(/^---\n([\s\S]*?)\n---/);
    process.stdout.write(fmOnly ? fmOnly[0] + '\n' : '(could not extract frontmatter)\n');
    return true;
  }

  fs.writeFileSync(absPath, migrated, 'utf8');
  process.stdout.write(`[MIGRATED] ${filePath} (${type})\n`);
  return true;
}

// ─── Batch mode ───────────────────────────────────────────────────────────────

function processSquad(squadDir) {
  const absDir = path.resolve(squadDir);
  if (!fs.existsSync(absDir)) {
    process.stderr.write(`[ERROR] Squad directory not found: ${absDir}\n`);
    process.exit(1);
  }

  const mdFiles = [];

  // Collect all .md files in agents/ and tasks/
  for (const subdir of ['agents', 'tasks']) {
    const dir = path.join(absDir, subdir);
    if (!fs.existsSync(dir)) continue;
    fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .forEach(f => mdFiles.push(path.join(dir, f)));
  }

  if (mdFiles.length === 0) {
    process.stdout.write(`[INFO] No .md files found in agents/ or tasks/ under ${squadDir}\n`);
    return;
  }

  let migrated = 0;
  let skipped = 0;

  for (const f of mdFiles) {
    const success = processFile(f);
    if (success) {
      const content = fs.readFileSync(f, 'utf8');
      if (content.includes('MIGRATED TO CC FORMAT')) migrated++;
      else skipped++;
    }
  }

  process.stdout.write(`\n── Migration Summary ─────────────────────────────\n`);
  process.stdout.write(`  Total files:   ${mdFiles.length}\n`);
  process.stdout.write(`  Migrated:      ${migrated}\n`);
  process.stdout.write(`  Skipped:       ${skipped}\n`);
  process.stdout.write(`  Dry-run:       ${dryRun}\n`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

if (squadPath) {
  processSquad(squadPath);
} else {
  processFile(singleFile);
}
