#!/usr/bin/env node
/**
 * check-bootstrap.cjs
 *
 * Gate determinístico do COO. Verifica se o workspace tem os 5 itens obrigatórios.
 * Roda ANTES de qualquer task de workspace governance do squad c-level.
 *
 * Usage:
 *   node squads/c-level/scripts/check-bootstrap.cjs
 *
 * Exit code 0 = PASS, exit code 1 = FAIL
 * Output: JSON { status, missing, found }
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');

const REQUIRED = [
  { id: 'system_config', path: 'workspace/_system/config.yaml', type: 'file' },
  { id: 'businesses_dir', path: 'workspace/businesses', type: 'dir' },
  { id: 'business_template_dir', path: 'workspace/_templates/business-template', type: 'dir' },
  { id: 'workspace_scripts_dir', path: 'workspace/scripts', type: 'dir' },
  { id: 'workspace_health_dir', path: 'docs/qa/workspace-health', type: 'dir' },
];

function check() {
  const found = [];
  const missing = [];

  for (const item of REQUIRED) {
    const fullPath = path.join(ROOT, item.path);
    const exists = item.type === 'dir'
      ? fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory()
      : fs.existsSync(fullPath) && fs.statSync(fullPath).isFile();

    if (exists) {
      found.push(item.id);
    } else {
      missing.push({ id: item.id, path: item.path, type: item.type });
    }
  }

  const status = missing.length === 0 ? 'PASS' : 'FAIL';

  return { status, found, missing };
}

const result = check();

console.log(JSON.stringify(result, null, 2));

process.exit(result.status === 'PASS' ? 0 : 1);
