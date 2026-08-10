#!/usr/bin/env node

/**
 * Input Validator (deterministic worker)
 * Implementa IV-1, IV-2, IV-3
 * SINKRA Execution Type: Worker
 */

const fs = require('fs');
const path = require('path');

if (process.argv.length < 3) {
  console.error('FAIL: Missing input JSON string argument.');
  process.exit(1);
}

let inputs;
try {
  inputs = JSON.parse(process.argv[2]);
} catch (e) {
  console.error('FAIL: Invalid JSON input.');
  process.exit(1);
}

const vetos = [];

// IV-1: rules_source
if (!inputs.rules_source) {
  vetos.push('IV-1 VETO: rules_source é obrigatório. Forneça path para regras existentes.');
} else {
  // Try to resolve path and see if it exists
  const sourcePath = path.resolve(process.cwd(), inputs.rules_source);
  if (!fs.existsSync(sourcePath)) {
    vetos.push(`IV-1 VETO: rules_source path does not exist: ${inputs.rules_source}`);
  }
}

// IV-2: source_format
const validFormats = ['spreadsheet', 'document', 'wiki', 'pdf', 'email', 'mixed'];
if (!inputs.source_format || !validFormats.includes(inputs.source_format)) {
  vetos.push('IV-2 VETO: source_format deve ser um de: spreadsheet, document, wiki, pdf, email, mixed.');
}

// IV-3: domain
if (!inputs.domain || inputs.domain.trim() === '') {
  vetos.push("IV-3 VETO: domain é obrigatório. Forneça o domínio de negócio (ex: 'Credit Approval', 'Order Processing').");
}

if (vetos.length > 0) {
  // Output all vetos at once
  vetos.forEach(v => console.error(v));
  process.exit(1);
}

// All valid
console.log('PASS: all inputs valid');
process.exit(0);
