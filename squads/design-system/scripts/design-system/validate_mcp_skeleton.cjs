#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const requiredFiles = [
  'docs/design-system/domains/mcp/server.ts',
  'docs/design-system/domains/mcp/types.ts',
  'docs/design-system/domains/mcp/config.json',
  'docs/design-system/domains/mcp/handlers/components.ts',
  'docs/design-system/domains/mcp/handlers/registry.ts',
  'docs/design-system/domains/mcp/handlers/tokens.ts',
  'docs/design-system/domains/mcp/handlers/guidelines.ts'
];

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function main() {
  for (const rel of requiredFiles) {
    const full = path.join(ROOT, rel);
    if (!fs.existsSync(full)) {
      fail(`Missing required MCP file: ${rel}`);
    }

    const content = fs.readFileSync(full, 'utf8');
    if (!content.trim()) {
      fail(`MCP file is empty: ${rel}`);
    }
  }

  console.log('PASS: MCP skeleton files are present');
}

main();
