#!/usr/bin/env node

/**
 * Phase Gate Validator (deterministic worker)
 * Implementa enforcement rule E9
 * SINKRA Execution Type: Worker
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

if (process.argv.length < 3) {
  console.error('FAIL: Missing phase_dir argument.');
  process.exit(1);
}

const phaseDirArg = process.argv[2];
const phaseDir = path.resolve(process.cwd(), phaseDirArg);

// Step 1: Ensure directory exists and is not empty
if (!fs.existsSync(phaseDir)) {
  console.error(`FAIL: phase directory does not exist: ${phaseDirArg}`);
  process.exit(1);
}

const files = fs.readdirSync(phaseDir).filter(f => fs.lstatSync(path.join(phaseDir, f)).isFile());
if (files.length === 0) {
  console.error(`FAIL: phase directory is empty: ${phaseDirArg}`);
  process.exit(1);
}

// Step 2: Check each .md file size directly (equivalent to wc -c)
const mdFiles = files.filter(f => f.endsWith('.md'));
for (const file of mdFiles) {
  const filePath = path.join(phaseDir, file);
  const stats = fs.statSync(filePath);
  if (stats.size < 500) {
    console.error(`FAIL: ${file} below 500 bytes (${stats.size} bytes)`);
    process.exit(1);
  }
}

// Step 3: Check for VETO, BLOCKED, FAILED (equivalent to grep -rl)
let blockedFiles = [];
for (const file of files) {
  const filePath = path.join(phaseDir, file);
  const content = fs.readFileSync(filePath, 'utf8');
  if (/(VETO|BLOCKED|FAILED)/.test(content)) {
    blockedFiles.push(file);
  }
}

if (blockedFiles.length > 0) {
  console.error(`FAIL: blocking keywords found in ${blockedFiles.join(', ')}`);
  process.exit(1);
}

// All checks passed
console.log('PASS: phase gate validated');
process.exit(0);
