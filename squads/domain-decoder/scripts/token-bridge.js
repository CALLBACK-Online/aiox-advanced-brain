const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

if (process.argv.length < 3) {
  console.error("Usage: node token-bridge.js <path-to-rule-catalog.md>");
  process.exit(1);
}

const catalogPath = path.resolve(process.cwd(), process.argv[2]);
const outputDir = path.dirname(catalogPath);
const outputPath = path.join(outputDir, 'sinkra-token-map.yaml');

if (!fs.existsSync(catalogPath)) {
  console.error(`File not found: ${catalogPath}`);
  process.exit(1);
}

const content = fs.readFileSync(catalogPath, 'utf8');

// A simple regex to parse a markdown table or list representing rules.
// Looking for something like: | RE-001 | CONSTRAINT | "Pedido DEVE ter valor minimo de R$50" |
const rules = [];
const ruleLines = content.split('\n');

ruleLines.forEach(line => {
  // Try matching markdown table rows
  const match = line.match(/\|\s*(RE-[A-Z0-9\-]+)\s*\|\s*([A-Z_]+)\s*\|\s*([^|]+)\s*\|/);
  if (match) {
    rules.push({
      rule_id: match[1].trim(),
      rule_type: match[2].trim(),
      statement: match[3].replace(/['"]/g, '').trim()
    });
  }
});

const tokens = [];
const unmappable_rules = [];

rules.forEach((rule, idx) => {
  const { rule_id, rule_type, statement } = rule;
  let family = null;
  let token_value = null;
  let recommendation = null;
  let reason = null;

  const st = statement.toLowerCase();

  if (rule_type === 'CONSTRAINT' && /\d+/.test(st) && !(st.includes('mais de') || st.includes('limite') || st.includes('sessões'))) {
    if (st.includes('dia') || st.includes('hora') || st.includes('mes') || st.includes('prazo') || st.includes('até')) {
      family = 'Time';
      token_value = st.match(/\d+\s*(?:dias|horas?|h|mês|meses)/i)?.[0] || 'unknown_time';
    } else {
      family = 'Threshold';
      token_value = st.match(/(?:R\$|usd|\$)?\s*\d+(?:[\.,]\d+)?/i)?.[0] || 'numeric_value';
    }
  } else if (rule_type === 'CONSTRAINT' && (st.includes('mais de') || st.includes('máximo') || st.includes('limite') || st.includes('sessões') || st.includes('tentativas'))) {
    family = 'Capacity';
    token_value = st.match(/\d+/)?.[0] || 'capacity_value';
  } else if (rule_type === 'COMPUTATION' || rule_type === 'DERIVATION') {
    family = 'Behavior';
    token_value = 'computation_formula';
  } else if (rule_type === 'INFERENCE' && (st.includes('status') || st.includes('classifica') || st.includes('tipo'))) {
    family = 'Taxonomy';
    token_value = 'enum_inference';
  } else if (rule_type === 'ACTION_ENABLER' && (st.includes('pode') || st.includes('permitido'))) {
    family = 'Permission';  // Permission family exists in SINKRA token-registry
    token_value = 'role_access';
  }

  if (family) {
    tokens.push({
      token_id: `TK-DD-BR-${String(idx + 1).padStart(3, '0')}`,
      family: family,
      rule_source: rule_id,
      rule_statement: statement,
      token_value: token_value,
      domain: "Tactical",
      produced_by: "token-bridge",
      consumed_by: []
    });
  } else {
    unmappable_rules.push({
      rule_id: rule_id,
      reason: "Could not infer appropriate SINKRA family from statement logic.",
      recommendation: "atom"
    });
  }
});

const outputData = {
  version: "1.0.0",
  metadata: {
    generated_by: "token-bridge",
    source: catalogPath
  },
  mapped_tokens: tokens,
  unmappable_rules: unmappable_rules
};

fs.writeFileSync(outputPath, yaml.dump(outputData));
console.log(`PASS: Generated ${outputPath}`);
process.exit(0);
