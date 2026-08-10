#!/usr/bin/env node
// Rule Lint - Scans markdown for forbidden qualifiers in rule statements.
// Usage: node squads/code-anatomist/scripts/rule-lint.js <file> [file2 ...]
// Exit code: 1 if violations found, 0 if clean.

import { readFileSync } from 'fs';

const FORBIDDEN = [
  // Palavras existentes (10)
  'adequate', 'appropriate', 'timely', 'reasonable',
  'proper', 'valid', 'applicable', 'authorized',
  'current', 'recent',
  // Palavras a adicionar (7 simples)
  'sufficient', 'significant', 'usually', 'generally',
  'normally', 'often', 'sometimes'
];

const FORBIDDEN_PHRASES = [
  'may impact', 'could affect', 'etc.', 'and/or', 'as needed', 'up to'
];

const pattern = new RegExp(`\\b(${FORBIDDEN.join('|')})\\b`, 'gi');

// Mapeia frases escapando caracteres especiais
const escapedPhrases = FORBIDDEN_PHRASES.map(p => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
const phrasePattern = new RegExp(`(?:\\b|\\s|^)(${escapedPhrases.join('|')})(?:\\b|\\s|$)`, 'gi');

const files = process.argv.slice(2);
if (!files.length) {
  console.error('Usage: node squads/code-anatomist/scripts/rule-lint.js <file> [file2 ...]');
  process.exit(2);
}

let violations = 0;

for (const file of files) {
  let content;
  try {
    content = readFileSync(file, 'utf8');
  } catch (err) {
    console.error(`Error reading ${file}: ${err.message}`);
    process.exit(2);
  }
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    let match;
    while ((match = pattern.exec(lines[i])) !== null) {
      violations++;
      console.log(`${file}:${i + 1}: FORBIDDEN_QUALIFIER "${match[1]}" found in rule statement`);
    }
    while ((match = phrasePattern.exec(lines[i])) !== null) {
      violations++;
      console.log(`${file}:${i + 1}: FORBIDDEN_QUALIFIER "${match[1]}" found in rule statement`);
    }
  }
}

process.exit(violations > 0 ? 1 : 0);
