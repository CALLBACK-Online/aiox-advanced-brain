import { readFileSync } from 'node:fs';
import yaml from 'js-yaml';

const WORKFLOW_FILES = [
  'squads/c-level/workflows/workspace-governance.yaml',
  'squads/c-level/workflows/business-profile-pipeline.yaml'
];

const BUILTIN_REFS = new Set(['input', 'system', 'item', 'event', 'now']);

function loadWorkflowDoc(filePath) {
  const raw = readFileSync(filePath, 'utf8');
  return yaml.load(raw);
}

function collectStepIds(workflow) {
  return new Set((workflow.steps || []).map((step) => step.id).filter(Boolean));
}

function collectTemplateRefs(workflow) {
  const raw = JSON.stringify(workflow);
  return [...raw.matchAll(/\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\./g)].map((m) => m[1]);
}

describe('workspace workflow integrity', () => {
  test.each(WORKFLOW_FILES)('parses YAML: %s', (filePath) => {
    expect(() => loadWorkflowDoc(filePath)).not.toThrow();
  });

  test.each(WORKFLOW_FILES)('has no unresolved step references: %s', (filePath) => {
    const doc = loadWorkflowDoc(filePath);
    const workflows = doc.workflows || {};

    for (const [workflowName, workflow] of Object.entries(workflows)) {
      const stepIds = collectStepIds(workflow);
      const refs = collectTemplateRefs(workflow);
      const unknown = [...new Set(refs.filter((ref) => !stepIds.has(ref) && !BUILTIN_REFS.has(ref)))];

      if (unknown.length > 0) {
        throw new Error(`${filePath} -> ${workflowName} unresolved refs: ${unknown.join(', ')}`);
      }

      expect(unknown).toEqual([]);
    }
  });

  test('workspace-governance workflow has no nested template expressions in rules', () => {
    const raw = readFileSync('squads/c-level/workflows/workspace-governance.yaml', 'utf8');
    const nestedInRule = /rule:\s*".*\{\{[^"\n]*\{\{/.test(raw);

    expect(nestedInRule).toBe(false);
  });
});
