#!/usr/bin/env node
/**
 * Runner-Ops Squad Greeting Generator
 *
 * Generates contextual greetings for runner-ops agents.
 * Adapted from squads/squad-creator/scripts/generate-squad-greeting.js pattern.
 *
 * Usage:
 *   node generate-squad-greeting.js [agent-name]
 *
 * Examples:
 *   node generate-squad-greeting.js
 *   node generate-squad-greeting.js runner-chief
 *   node generate-squad-greeting.js runner-architect
 *
 * @module generate-squad-greeting
 * @version 1.0.0
 * @location squads/runner-ops/scripts/
 * @owner runner-ops
 */

'use strict';

const fs = require('fs').promises;
const path = require('path');

const SQUAD_NAME = 'runner-ops';
const DEFAULT_AGENT = 'runner-chief';
const TIMEOUT_MS = 5000;

const AGENTS = {
  'runner-chief': {
    title: 'Runner Lifecycle Orchestrator',
    commands: ['*create-runner', '*validate-runner', '*integrate-runner', '*monitor', '*registry', '*evolve-module', '*gateway-status', '*gap-matrix', '*help', '*exit'],
  },
  'runner-architect': {
    title: 'Runner Design & Framework Evolution Specialist',
    commands: ['*design-runner', '*propose-module', '*review-integration', '*adr', '*help', '*exit'],
  },
  'runner-integrator': {
    title: 'Runner-Lib Migration & Brownfield Upgrade Specialist',
    commands: ['*integrate', '*diff-from-golden', '*brownfield-audit', '*help', '*exit'],
  },
  'runner-validator': {
    title: 'Runner Compliance & Standards Enforcement Specialist',
    commands: ['*validate', '*validate-all', '*compliance-report', '*headless-check', '*help', '*exit'],
  },
  'runner-monitor': {
    title: 'Runner Metrics & Health Monitoring Specialist',
    commands: ['*dashboard', '*cost-report', '*health-check', '*alert-config', '*runner-stats', '*help', '*exit'],
  },
};

/**
 * Load runner-registry snapshot from data/
 *
 * @returns {Promise<Object|null>} Registry data or null
 */
async function loadRunnerRegistry() {
  const registryPath = path.join(process.cwd(), 'squads', SQUAD_NAME, 'data', 'runner-registry.yaml');
  try {
    const content = await fs.readFile(registryPath, 'utf8');
    // Parse basic YAML fields without full yaml library dependency
    const totalMatch = content.match(/total_runners:\s*(\d+)/);
    const goldenMatch = content.match(/golden_master:\s*"?(\w+)"?/);
    return {
      total_runners: totalMatch ? parseInt(totalMatch[1], 10) : 8,
      golden_master: goldenMatch ? goldenMatch[1] : 'mmos',
    };
  } catch {
    return null;
  }
}

/**
 * Generate greeting for runner-ops agent
 *
 * @param {string} agentName - Agent name
 * @returns {Promise<string>} Formatted greeting
 */
async function generateRunnerOpsGreeting(agentName) {
  const agentInfo = AGENTS[agentName] || AGENTS[DEFAULT_AGENT];
  const registry = await loadRunnerRegistry();

  const runnerCount = registry ? registry.total_runners : 8;
  const goldenMaster = registry ? registry.golden_master : 'mmos';

  const commandList = agentInfo.commands
    .map((cmd) => `- \`${cmd}\``)
    .join('\n');

  return `**${agentName}** — ${agentInfo.title} | runner-ops squad

**Runner Ecosystem:** ${runnerCount} runners | Golden Master: \`${goldenMaster}.sh\` | Framework: \`infrastructure/scripts/runner-lib/\`

**Available Commands:**
${commandList}

Type \`*help\` for full command documentation or \`*registry\` to view the runner ecosystem.`;
}

/**
 * Generate fallback greeting
 *
 * @param {string} agentName - Agent name
 * @returns {string} Simple fallback
 */
function generateFallbackGreeting(agentName) {
  return `**${agentName}** — runner-ops squad ready\n\nType \`*help\` for available commands.`;
}

// CLI interface
if (require.main === module) {
  const agentName = process.argv[2] || DEFAULT_AGENT;

  if (!AGENTS[agentName]) {
    console.error(`Unknown agent: ${agentName}`);
    console.error(`Available agents: ${Object.keys(AGENTS).join(', ')}`);
    process.exit(1);
  }

  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Greeting timeout')), TIMEOUT_MS),
  );

  Promise.race([generateRunnerOpsGreeting(agentName), timeoutPromise])
    .then((greeting) => {
      console.log(greeting);
      process.exit(0);
    })
    .catch((error) => {
      if (error.message === 'Greeting timeout') {
        console.log(generateFallbackGreeting(agentName));
        process.exit(0);
      }
      console.error('Error:', error.message);
      console.log(generateFallbackGreeting(agentName));
      process.exit(1);
    });
}

module.exports = { generateRunnerOpsGreeting };
