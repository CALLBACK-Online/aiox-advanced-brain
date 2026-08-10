#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DEFAULT_PROFILE_PATH = '.aiox/advisory-board/alan-nicolas-profile.yaml';
const DEFAULT_SESSIONS_ROOT = 'docs/advisory';

function toRepoRelative(repoRoot, absolutePath) {
  return path.relative(repoRoot, absolutePath).split(path.sep).join('/');
}

function parseArgs(argv) {
  const options = {
    format: 'json',
    profilePath: DEFAULT_PROFILE_PATH,
    sessionsRoot: DEFAULT_SESSIONS_ROOT,
    sessionFile: null,
    repoRoot: process.cwd(),
  };

  for (const arg of argv) {
    if (arg.startsWith('--format=')) {
      options.format = arg.slice('--format='.length);
      continue;
    }
    if (arg.startsWith('--profile-path=')) {
      options.profilePath = arg.slice('--profile-path='.length);
      continue;
    }
    if (arg.startsWith('--sessions-root=')) {
      options.sessionsRoot = arg.slice('--sessions-root='.length);
      continue;
    }
    if (arg.startsWith('--session-file=')) {
      options.sessionFile = arg.slice('--session-file='.length);
      continue;
    }
    if (arg.startsWith('--repo-root=')) {
      options.repoRoot = path.resolve(arg.slice('--repo-root='.length));
    }
  }

  return options;
}

function listSessionFiles(sessionsRootAbsolute) {
  if (!fs.existsSync(sessionsRootAbsolute) || !fs.statSync(sessionsRootAbsolute).isDirectory()) {
    return [];
  }

  return fs
    .readdirSync(sessionsRootAbsolute, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md'))
    .map((entry) => entry.name)
    .sort((left, right) => right.localeCompare(left));
}

function resolveSelectedSession(options) {
  const sessionsRootAbsolute = path.join(options.repoRoot, options.sessionsRoot);
  const sessionFiles = listSessionFiles(sessionsRootAbsolute);

  if (options.sessionFile) {
    const explicitAbsolute = path.join(options.repoRoot, options.sessionFile);
    if (fs.existsSync(explicitAbsolute) && fs.statSync(explicitAbsolute).isFile()) {
      return {
        latestSessionPath: toRepoRelative(options.repoRoot, explicitAbsolute),
        sessionSelectionStrategy: 'explicit',
        sessionCandidates: sessionFiles.map((file) => `${options.sessionsRoot}/${file}`),
      };
    }

    return {
      latestSessionPath: null,
      sessionSelectionStrategy: 'explicit_missing',
      sessionCandidates: sessionFiles.map((file) => `${options.sessionsRoot}/${file}`),
      missingPaths: [options.sessionFile],
    };
  }

  if (sessionFiles.length === 0) {
    return {
      latestSessionPath: null,
      sessionSelectionStrategy: 'latest_by_filename_desc',
      sessionCandidates: [],
      missingPaths: [`${options.sessionsRoot}/*.md`],
    };
  }

  return {
    latestSessionPath: `${options.sessionsRoot}/${sessionFiles[0]}`,
    sessionSelectionStrategy: 'latest_by_filename_desc',
    sessionCandidates: sessionFiles.map((file) => `${options.sessionsRoot}/${file}`),
  };
}

function resolveAdvisoryContext(rawOptions = {}) {
  const options = {
    ...parseArgs([]),
    ...rawOptions,
  };

  const profileAbsolute = path.join(options.repoRoot, options.profilePath);
  const missingPaths = [];
  const availableSources = [];

  let profilePath = null;
  if (fs.existsSync(profileAbsolute) && fs.statSync(profileAbsolute).isFile()) {
    profilePath = toRepoRelative(options.repoRoot, profileAbsolute);
    availableSources.push('founder_profile');
  } else {
    missingPaths.push(options.profilePath);
  }

  const sessionResolution = resolveSelectedSession(options);
  if (sessionResolution.latestSessionPath) {
    availableSources.push('latest_session');
  }
  if (Array.isArray(sessionResolution.missingPaths)) {
    missingPaths.push(...sessionResolution.missingPaths);
  }

  let status = 'missing';
  if (availableSources.length === 2) {
    status = 'ready';
  } else if (availableSources.length > 0) {
    status = 'partial';
  }

  return {
    advisory_context: {
      status,
      profile_path: profilePath,
      latest_session_path: sessionResolution.latestSessionPath,
      sessions_root: options.sessionsRoot,
      session_selection_strategy: sessionResolution.sessionSelectionStrategy,
      available_sources: availableSources,
      missing_paths: missingPaths,
      session_candidates: sessionResolution.sessionCandidates,
      continuity_mode: sessionResolution.latestSessionPath ? 'resume_available' : 'fresh_session_only',
      privacy_contract: 'local_gitignored_only',
    },
  };
}

function renderText(result) {
  const context = result.advisory_context;
  const lines = [
    `status: ${context.status}`,
    `profile_path: ${context.profile_path || '-'}`,
    `latest_session_path: ${context.latest_session_path || '-'}`,
    `continuity_mode: ${context.continuity_mode}`,
  ];

  if (context.missing_paths.length > 0) {
    lines.push(`missing_paths: ${context.missing_paths.join(', ')}`);
  }

  return `${lines.join('\n')}\n`;
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const result = resolveAdvisoryContext(options);

  if (options.format === 'text') {
    process.stdout.write(renderText(result));
    return;
  }

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (require.main === module) {
  main();
}

module.exports = {
  DEFAULT_PROFILE_PATH,
  DEFAULT_SESSIONS_ROOT,
  listSessionFiles,
  parseArgs,
  resolveAdvisoryContext,
};
