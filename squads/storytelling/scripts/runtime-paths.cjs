#!/usr/bin/env node

const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..', '..', '..');
const DEFAULT_RUNTIME_ROOT = path.join(PROJECT_ROOT, '.aiox', 'squad-runtime');

function toPosix(value) {
  return value.split(path.sep).join('/');
}

function toProjectRelative(targetPath) {
  const relative = path.relative(PROJECT_ROOT, targetPath);
  if (!relative) return '.';
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    return toPosix(path.resolve(targetPath));
  }
  return toPosix(relative);
}

function resolveRuntimeRoot() {
  const override = (process.env.AIOX_RUNTIME_ROOT || '').trim();
  if (!override) return DEFAULT_RUNTIME_ROOT;
  if (path.isAbsolute(override)) return override;
  return path.resolve(PROJECT_ROOT, override);
}

function getStorytellingRuntimeRoot() {
  return path.join(resolveRuntimeRoot(), 'storytelling', 'story-chief');
}

function getStorytellingSessionContextPath() {
  return path.join(getStorytellingRuntimeRoot(), 'session-context.yaml');
}

module.exports = {
  DEFAULT_RUNTIME_ROOT,
  PROJECT_ROOT,
  getStorytellingRuntimeRoot,
  getStorytellingSessionContextPath,
  resolveRuntimeRoot,
  toPosix,
  toProjectRelative,
};
