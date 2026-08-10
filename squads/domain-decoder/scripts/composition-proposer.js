const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

if (process.argv.length < 4) {
  console.error("Usage: node composition-proposer.js <path-to-decision-model.yaml> <path-to-aiox-token-map.yaml>");
  process.exit(1);
}

const decisionModelPath = path.resolve(process.cwd(), process.argv[2]);
const tokenMapPath = path.resolve(process.cwd(), process.argv[3]);
const outputDir = path.dirname(decisionModelPath);
const outputPath = path.join(outputDir, 'aiox-composition-proposal.yaml');

if (!fs.existsSync(decisionModelPath) || !fs.existsSync(tokenMapPath)) {
  console.error("FAIL: Input files not found.");
  process.exit(1);
}

const dm = yaml.load(fs.readFileSync(decisionModelPath, 'utf8'));
const tm = yaml.load(fs.readFileSync(tokenMapPath, 'utf8'));

const proposal = {
  version: "1.0.0",
  pipeline_id: `DD-INST-${Date.now()}`,
  proposed_composition: {
    molecules: [],
    atoms: []
  },
  validation: {
    dag_is_acyclic: true,
    single_executor_per_atom: true,
    accountability_assigned: true
  }
};

let atomCounter = 1;
let molCounter = 1;

// Group rules by decision family in DM
if (dm.decisions) {
  for (const decision of dm.decisions) {
    const molId = `MOL-PROP-${String(molCounter).padStart(3, '0')}`;
    molCounter++;
    
    const molAtoms = [];
    
    for (const rule of decision.rules) {
      const atomId = `ATM-PROP-${String(atomCounter).padStart(3, '0')}`;
      atomCounter++;
      
      molAtoms.push(atomId);
      
      // Determine executor based on rule nature
      let executor_type = 'Agent';
      let executor_id = 'ronald-ross';
      
      const mappedToken = tm.mapped_tokens.find(t => t.rule_source === rule.rule_id);
      let tokensBound = [];
      if (mappedToken) {
        tokensBound.push(mappedToken.token_id);
        // If it mapped to threshold or capacity or time, it's deterministic
        if (['Threshold', 'Capacity', 'Time', 'Behavior'].includes(mappedToken.family)) {
           executor_type = 'Worker';
           executor_id = 'phase-gate-validator';
        }
      }
      
      proposal.proposed_composition.atoms.push({
        atom_id: atomId,
        name: `Evaluate ${rule.rule_id}`,
        executor_type: executor_type,
        executor_id: executor_id,
        inputs: [{ name: "rule_data", type: "yaml", source: rule.rule_id }],
        outputs: [{ name: "evaluation_result", type: "yaml", artifact: true }],
        completion_criteria: [`${rule.rule_id} evaluated with verdict PASS/FAIL`],
        accountable_human: "Human:process_owner",
        depends_on: [],
        tokens_bound: tokensBound
      });
    }
    
    // Create sequential dependencies to ensure DAG is acyclic within the molecule
    for (let i = 1; i < molAtoms.length; i++) {
        const currentAtom = proposal.proposed_composition.atoms.find(a => a.atom_id === molAtoms[i]);
        currentAtom.depends_on.push(molAtoms[i-1]);
    }
    
    proposal.proposed_composition.molecules.push({
      molecule_id: molId,
      name: decision.decision_name,
      atoms: molAtoms
    });
  }
}

fs.writeFileSync(outputPath, yaml.dump(proposal));
console.log(`PASS: Generated ${outputPath}`);
process.exit(0);
