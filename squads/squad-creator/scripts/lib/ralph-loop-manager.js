/**
 * Ralph Loop Manager — EPIC-109 Wave 2 (C2)
 *
 * Manages fresh-context retry logic for pipeline steps. Prevents error
 * compounding by detecting doom loops before recommending retry strategies.
 *
 * Design intent:
 * - Integrates with doom-loop-detector.js: reads doom_loop_check from the
 *   retry state YAML, never recommends retry_fresh when doom loop detected.
 * - Persists retry state to .aiox/squad-runtime/ (creates dir if missing).
 * - Max iterations: default 5, configurable.
 * - Aborting conditions:
 *   (a) max_iterations exceeded
 *   (b) structural error persists after attempt > 2
 *
 * Error taxonomy (PV_BS_001):
 *   transient: ETIMEDOUT, ECONNRESET, rate_limit, 503, 429, context_length_exceeded
 *   structural: schema_validation_failed, missing_required_field, type_mismatch,
 *               ENOENT, SyntaxError
 *   unknown: everything else
 */

'use strict';

const fs = require('fs');
const path = require('path');

const DEFAULT_MAX_ITERATIONS = 5;
const STATE_ROOT = '.aiox/squad-runtime';

/** Transient error patterns — safe to retry */
const TRANSIENT_PATTERNS = [
  'ETIMEDOUT',
  'ECONNRESET',
  'rate_limit',
  'context_length_exceeded',
  '503',
  '429',
];

/** Structural error patterns — retry unlikely to help */
const STRUCTURAL_PATTERNS = [
  'schema_validation_failed',
  'missing_required_field',
  'type_mismatch',
  'ENOENT',
  'SyntaxError',
];

/**
 * Classify an error string into transient / structural / unknown.
 *
 * @param {string} errorMessage
 * @returns {'transient'|'structural'|'unknown'}
 */
function classifyError(errorMessage) {
  if (!errorMessage) return 'unknown';
  const msg = String(errorMessage);

  for (const pattern of TRANSIENT_PATTERNS) {
    if (msg.includes(pattern)) return 'transient';
  }
  for (const pattern of STRUCTURAL_PATTERNS) {
    if (msg.includes(pattern)) return 'structural';
  }
  return 'unknown';
}

/**
 * Resolve the state file path for a given squad and step.
 *
 * @param {string} stepId
 * @param {string} [squadName]
 * @returns {string}
 */
function _stateFilePath(stepId, squadName) {
  const safeStep = stepId.replace(/[^a-zA-Z0-9-_]/g, '_');
  const baseDir = squadName
    ? path.join(STATE_ROOT, squadName, 'retry-states')
    : path.join(STATE_ROOT, 'retry-states');
  return path.join(baseDir, `${safeStep}.json`);
}

/**
 * Load retry state from disk. Returns null if file doesn't exist.
 *
 * @param {string} stateFile
 * @returns {object|null}
 */
function _loadState(stateFile) {
  try {
    if (!fs.existsSync(stateFile)) return null;
    const raw = fs.readFileSync(stateFile, 'utf8');
    return JSON.parse(raw);
  } catch (_err) {
    return null;
  }
}

/**
 * Save retry state to disk. Creates directories as needed.
 *
 * @param {string} stateFile
 * @param {object} state
 */
function _saveState(stateFile, state) {
  const dir = path.dirname(stateFile);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2), 'utf8');
}

/**
 * Manage retry strategy for a pipeline step.
 *
 * @param {string} stepId       — Unique step identifier
 * @param {object} [options]    — Configuration options
 * @param {number} [options.maxIterations=5]   — Max retry attempts before abort
 * @param {string} [options.errorMessage]      — Last error message (for classification)
 * @param {string} [options.squadName]         — Squad name (for state path namespacing)
 * @param {object} [options.doomLoopCheck]     — Injected doom_loop_check from state
 *
 * @returns {{
 *   action: 'retry_fresh'|'retry_resume'|'abort',
 *   attempt: number,
 *   stateFile: string,
 *   reason: string,
 *   errorClass: string
 * }}
 */
function manageRetry(stepId, options = {}) {
  const maxIterations = options.maxIterations || DEFAULT_MAX_ITERATIONS;
  const errorMessage = options.errorMessage || '';
  const squadName = options.squadName || null;
  const doomLoopCheck = options.doomLoopCheck || null;

  const stateFile = _stateFilePath(stepId, squadName);
  const existingState = _loadState(stateFile);

  const attempt = existingState ? existingState.attempt + 1 : 1;
  const errorClass = classifyError(errorMessage);

  // Doom loop guard: NEVER recommend retry_fresh when doom loop is active
  const doomLoopDetected = doomLoopCheck && doomLoopCheck.detected === true;

  let action;
  let reason;

  if (attempt > maxIterations) {
    action = 'abort';
    reason = `Max iterations (${maxIterations}) exceeded`;
  } else if (doomLoopDetected) {
    // Doom loop detected: escalate, not retry
    action = 'abort';
    reason = `Doom loop detected (consecutive_count=${doomLoopCheck.consecutive_count}). Retry suppressed.`;
  } else if (errorClass === 'structural' && attempt > 2) {
    // Structural errors after 2 attempts won't resolve with retry
    action = 'abort';
    reason = `Structural error (${errorMessage}) persists after ${attempt} attempts`;
  } else if (errorClass === 'transient') {
    action = 'retry_fresh';
    reason = `Transient error (${errorClass}) — fresh context retry`;
  } else if (errorClass === 'structural' && attempt <= 2) {
    action = 'retry_fresh';
    reason = `Structural error on attempt ${attempt} — one more fresh try before abort`;
  } else {
    // unknown error class
    action = 'retry_resume';
    reason = `Unknown error class — resume from last checkpoint`;
  }

  const state = {
    stepId,
    attempt,
    errorClass,
    errorMessage,
    action,
    reason,
    doomLoopCheck: doomLoopCheck || null,
    updatedAt: new Date().toISOString(),
  };

  _saveState(stateFile, state);

  return {
    action,
    attempt,
    stateFile,
    reason,
    errorClass,
  };
}

module.exports = { manageRetry, classifyError };
