/**
 * Doom Loop Detector — EPIC-109 Wave 1 (C1)
 *
 * Detects when an agent is repeating the same output in consecutive steps,
 * indicating a doom loop (stuck state). Uses SHA-256 hashing with a circular
 * buffer of 10 entries per step ID.
 *
 * Design intent:
 * - Stateful in-memory (Map). Does NOT persist between restarts.
 * - Each pipeline run starts clean via resetAll().
 * - Fail-open: if hashing fails for any reason, returns { detected: false }.
 * - Max buffer size: 10 entries per step (prevents memory leak in long runs).
 *
 * Condition PV_BS_001: model_strategy MUST NOT use gemini-flash.
 */

'use strict';

const crypto = require('crypto');

// Internal state: Map<stepId, string[]> — circular buffer of output hashes
const _state = new Map();
const BUFFER_SIZE = 10;
const DEFAULT_CONSECUTIVE_THRESHOLD = 3;

/**
 * Compute SHA-256 hash of a string output.
 * Returns null on error (fail-open behavior).
 *
 * @param {string} output
 * @returns {string|null}
 */
function _hash(output) {
  try {
    return crypto.createHash('sha256').update(String(output)).digest('hex');
  } catch (_err) {
    return null;
  }
}

/**
 * Get or initialize the circular buffer for a given stepId.
 *
 * @param {string} stepId
 * @returns {string[]}
 */
function _getBuffer(stepId) {
  if (!_state.has(stepId)) {
    _state.set(stepId, []);
  }
  return _state.get(stepId);
}

/**
 * Check if the current output triggers a doom loop for the given step.
 *
 * @param {string} stepId       — Unique identifier for the pipeline step
 * @param {string} output       — The output produced by the step (will be hashed)
 * @param {object} [options]    — Optional configuration
 * @param {number} [options.threshold=3] — How many consecutive identical outputs = doom loop
 * @returns {{ detected: boolean, consecutive_count: number, action: string }}
 */
function checkDoomLoop(stepId, output, options = {}) {
  // Fail-open: invalid stepId or output → not detected
  if (!stepId || output === undefined || output === null) {
    return { detected: false, consecutive_count: 0, action: 'none' };
  }

  const threshold = options.threshold || DEFAULT_CONSECUTIVE_THRESHOLD;
  const hash = _hash(output);

  // Fail-open: hash computation failed
  if (hash === null) {
    return { detected: false, consecutive_count: 0, action: 'none' };
  }

  const buffer = _getBuffer(stepId);

  // Push hash into circular buffer
  buffer.push(hash);
  if (buffer.length > BUFFER_SIZE) {
    buffer.shift(); // remove oldest entry
  }

  // Count consecutive identical hashes at the END of the buffer
  let consecutiveCount = 0;
  for (let i = buffer.length - 1; i >= 0; i--) {
    if (buffer[i] === hash) {
      consecutiveCount++;
    } else {
      break;
    }
  }

  const detected = consecutiveCount >= threshold;
  let action = 'none';

  if (detected) {
    // Never recommend fresh_context_retry when doom loop detected
    // (ralph-loop-manager.js respects this contract)
    action = 'escalate';
  } else if (consecutiveCount >= Math.floor(threshold / 2)) {
    action = 'warn';
  }

  return {
    detected,
    consecutive_count: consecutiveCount,
    action,
  };
}

/**
 * Reset the circular buffer for a specific step.
 * Useful when a step recovers and should start fresh.
 *
 * @param {string} stepId
 */
function resetStep(stepId) {
  _state.delete(stepId);
}

/**
 * Clear ALL step buffers.
 * Call at the start of each pipeline run to avoid cross-run contamination.
 */
function resetAll() {
  _state.clear();
}

module.exports = { checkDoomLoop, resetStep, resetAll };
