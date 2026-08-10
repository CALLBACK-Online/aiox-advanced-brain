/**
 * AJV In-Process Validator — EPIC-109 Wave 3 (C6)
 *
 * Validates a data file (JSON or YAML) against a JSON Schema Draft-07 file
 * using AJV with ajv-formats.
 *
 * Configuration:
 *   - allErrors: true   → report ALL errors, not just the first
 *   - strict: false     → allow additional properties by default
 *   - formats: enabled via ajv-formats (date-time, email, uri, etc.)
 *
 * Exit codes (for CLI usage via validate-schemas.js):
 *   0 = valid
 *   1 = invalid (validation errors)
 *   2 = schema not found
 *   3 = data not found
 *   4 = invalid schema (AJV cannot compile it)
 *
 * Graceful degradation:
 *   If AJV or ajv-formats is not installed, logs a WARNING and returns
 *   { valid: true, errors: [], degraded: true } — does NOT crash.
 *
 * Override rule (NON-NEGOTIABLE):
 *   If AJV says invalid → result is FAIL, regardless of any LLM result.
 *   If AJV says valid   → LLM evaluation still runs (AJV valid ≠ semantically good).
 */

'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Try to load AJV and ajv-formats. Returns null if not available.
 */
function _tryLoadAjv() {
  try {
    const Ajv = require('ajv');
    const addFormats = require('ajv-formats');
    const ajv = new Ajv({ allErrors: true, strict: false });
    addFormats(ajv);
    return ajv;
  } catch (_err) {
    return null;
  }
}

/**
 * Auto-detect file format from extension and parse to JS object.
 *
 * @param {string} filePath
 * @returns {object} parsed data
 * @throws {Error} if parse fails
 */
function _parseDataFile(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const ext = path.extname(filePath).toLowerCase();

  if (ext === '.json') {
    return JSON.parse(raw);
  } else if (ext === '.yaml' || ext === '.yml') {
    // Lazy load js-yaml — it's a peer dependency already in the hub
    const yaml = require('js-yaml');
    return yaml.load(raw);
  } else {
    // Attempt JSON first, then YAML
    try {
      return JSON.parse(raw);
    } catch (_jsonErr) {
      const yaml = require('js-yaml');
      return yaml.load(raw);
    }
  }
}

/**
 * Validate a data file against a JSON Schema.
 *
 * @param {string} schemaPath — Absolute or relative path to the .schema.json file
 * @param {string} dataPath   — Absolute or relative path to the data file (JSON or YAML)
 * @returns {{
 *   valid: boolean,
 *   errors: Array<object>,
 *   schemaId: string,
 *   dataFile: string,
 *   degraded?: boolean,
 *   exitCode: number
 * }}
 */
function validate(schemaPath, dataPath) {
  const schemaFile = path.resolve(schemaPath);
  const dataFile = path.resolve(dataPath);

  // Graceful degradation — AJV not available
  const ajv = _tryLoadAjv();
  if (!ajv) {
    process.stderr.write(
      '[ajv-validate] WARNING: AJV or ajv-formats not available. ' +
      'Skipping schema validation (graceful degradation).\n'
    );
    return {
      valid: true,
      errors: [],
      schemaId: schemaFile,
      dataFile,
      degraded: true,
      exitCode: 0,
    };
  }

  // Check schema exists
  if (!fs.existsSync(schemaFile)) {
    return {
      valid: false,
      errors: [{ message: `Schema not found: ${schemaFile}` }],
      schemaId: schemaFile,
      dataFile,
      exitCode: 2,
    };
  }

  // Check data exists
  if (!fs.existsSync(dataFile)) {
    return {
      valid: false,
      errors: [{ message: `Data file not found: ${dataFile}` }],
      schemaId: schemaFile,
      dataFile,
      exitCode: 3,
    };
  }

  // Load and compile schema
  let schema;
  try {
    const rawSchema = fs.readFileSync(schemaFile, 'utf8');
    schema = JSON.parse(rawSchema);
  } catch (err) {
    return {
      valid: false,
      errors: [{ message: `Invalid schema JSON: ${err.message}` }],
      schemaId: schemaFile,
      dataFile,
      exitCode: 4,
    };
  }

  let compiledValidator;
  try {
    compiledValidator = ajv.compile(schema);
  } catch (err) {
    return {
      valid: false,
      errors: [{ message: `AJV cannot compile schema: ${err.message}` }],
      schemaId: schemaFile,
      dataFile,
      exitCode: 4,
    };
  }

  // Load and parse data
  let data;
  try {
    data = _parseDataFile(dataFile);
  } catch (err) {
    return {
      valid: false,
      errors: [{ message: `Data parse error: ${err.message}` }],
      schemaId: schemaFile,
      dataFile,
      exitCode: 3,
    };
  }

  // Run validation
  const isValid = compiledValidator(data);
  const errors = compiledValidator.errors || [];

  return {
    valid: isValid,
    errors,
    schemaId: schema.$id || schemaFile,
    dataFile,
    exitCode: isValid ? 0 : 1,
  };
}

module.exports = { validate };
