# Task: Optimize Claude Code Context Surface

## Metadata

| Campo | Valor |
|-------|-------|
| **Task ID** | `optimize-context` |
| **Squad** | `claude-code-mastery` |
| **Entry Agent** | `claude-mastery-chief` |
| **Atomic Layer** | Organism (8-phase pipeline composed of 8 Atoms/Molecules) |
| **Domain** | Operational |
| **Duration** | 45-90 min per cycle |
| **Checkpoint** | `task_anatomy_validation` (Phase 5) |
| **Pipeline** | `sinkra-pipeline-context-optimizer-2026` |
| **Workflow** | `wf-context-optimizer` (scaffolded in Phase 7) |

Previous task stub (CCM-CONFIG-004) is superseded by this definition.

---

## Purpose

Recurring optimization process for the Claude Code always-loaded context surface. Measures token budget, audits rules/skills/agents/CLAUDE.md/MCPs/config, remediates bloat via hard-gate-approved proposals, and re-measures the delta. Owned by `claude-code-mastery` squad, invoked via `/context-optimizer` OR auto-triggered when `scripts/doctor.js` detects threshold breach.

---

## SINKRA Task Anatomy (Organism-level)

### 1. task
```yaml
task: optimize-context
atomic_layer: Atom
executor: skill-craftsman
Domain: Operational
accountability_token: TK-CCM-ACC-001
Input:
- contexto do projeto
- objetivo da task
- artefatos de referência
Output:
- optimize-context-report
- recomendação executável
output_schema: context-optimization-yaml
Pre-Conditions:
- Contexto do projeto disponível e legível
- Artefatos de referência acessíveis ao executor
- Critério de sucesso entendido antes da execução
Post-Conditions:
- Output publicado em formato auditável
- Próximo passo explícito ou handoff emitido
- Decisões relevantes registradas no artefato final
Performance:
- Execução em uma sessão sem falha silenciosa
- Thresholds e veto conditions respeitados
- Resultado acionável para o próximo executor
Completion Criteria:
- Context budget reduced with measured token savings
- Unnecessary files flagged for removal
- CLAUDE.md trimmed or split into rules/imports

Error_handling:
  strategy: per_phase_rollback_with_commit_barriers
  max_retries: 1_per_phase
  fallback:
    - "phase fails soft gate → git revert <phase-sha>; pipeline continues"
    - "phase fails hard gate (operator NO) → skip operation; pipeline continues"
    - "phase fails anchor check (sp3) → auto git revert HEAD + abort phase; pipeline continues with other branches"
    - "pipeline preconditions fail → exit 1 BEFORE any mutation; operator fixes and re-runs"
  alert_on_failure: true
  rollback_boundary: "commit barrier per phase = single-phase blast radius"
```

---

## Execution Protocol (claude-mastery-chief orchestration)

### Phase Execution Sequence

1. **phase_01_sp7_baseline** (inline_bash by chief)
   - Chief runs `scripts/context-budget-audit.js --json` via Bash tool
   - Captures `baseline.json` in session state for final delta
   - Zero sub-agent spawn (pure worker)

2. **phase_02_sp6_collapse** (skill invocation)
   - Chief invokes `/update-config` skill with settings.json target + env block spec
   - Soft gate: `validate-yaml.js --changed`
   - Commit barrier: `chore(context-optimizer): sp6 collapse env vars applied`

3. **phase_03_sp1_rules** (subagent_task)
   - Pre-spawn: chief runs `audit-rule-items.js` for each candidate rule → inventory YAML
   - Pre-spawn: chief runs `validate-rule-frontmatter.js` for each target
   - Spawn `hooks-architect` (fork) with inventory + baseline as context
   - Sub-agent emits `sp1-rules-proposal.yaml` — NO direct file writes on hard-gate ops
   - Post-spawn: chief reads proposal, PAUSES for operator YES per hard-gate op
   - Pre-apply: `sinkra:rename-artifact --dry-run` for every rename
   - Apply approved ops via Edit + commit barrier

4. **phase_04_sp3_claudemd** (subagent_task)
   - Pre-spawn: `validate-claudemd-anchors.js --mode=pre-edit` captures anchor graph
   - Spawn `config-engineer` (fork)
   - Post-spawn: apply approved edits → `validate-claudemd-anchors.js --mode=post-edit`
   - On failure: auto `git revert HEAD` + abort phase (AP-CO-1 prevention)
   - Commit barrier

5. **phase_05_sp2_skills** (subagent_task)
   - Pre-spawn: `validate-skill-entry-agent-binding.js --mode=pre-delete` for every delete candidate
   - Pre-spawn: create pre-delete snapshots
   - Spawn `skill-craftsman` (fork), invokes `/validate-skill` per skill post-edit
   - Apply approved ops + commit barrier

6. **phase_06_sp4_agents** (subagent_task)
   - Pre-spawn: chief reads deletion-allowlist.yaml
   - Spawn `project-integrator` (fork)
   - Post-spawn: `ide-sync sync --deletion-allowlist=<path>` (ADAPTED tool — AS-02)
   - Commit barrier (v1: report-only for verbose-name renames; v2 handles renames)

7. **phase_07_sp5_mcps** (subagent_task — advisory)
   - Spawn `mcp-integrator` (fork) — NO mutations
   - Chief writes handoff `.aiox/handoffs/handoff-mcp-integrator-to-devops-{date}.yaml` (scope: intra_bu, lifecycle: created)
   - `@devops` executes any actual MCP add/remove per `.claude/rules/agent-authority.md`

8. **phase_08_sp7_final** (inline_bash)
   - Chief runs `context-budget-audit.js --strict`
   - Sentinel verifies all 24 tokens (see `.aiox/squad-runtime/sinkra-squad/context-optimizer/phase-05-task-definitions/token-assignments.yaml`)
   - Chief writes `delta-report.md` + moves proposals from `.aiox/` to `outputs/qa/context-budget/proposals/{date}/`
   - Commit barrier

---

## Hard-Gate Presentation Protocol

When a sub-agent emits a proposal with hard-gate operations, the chief MUST:

1. Read the proposal YAML
2. For each `operation.gate == 'hard'`:
   - Print operation ID, type (merge/delete/condense), target path, rationale, diff preview, and `preservation_map` (what items go where)
   - Emit prompt: `Apply proposal <proposal-id>? Reply 'YES <proposal-id>' to approve, 'NO' to skip.`
3. WAIT for operator response
4. On `YES <id>`: apply via Edit; log approval in proposal
5. On `NO`: skip operation; log rejection
6. Never execute a hard-gate op without explicit YES

**Exception:** `approval_mode: ci_strict` → exit 1 on any hard gate (CI contexts). `approval_mode: advisory` → log-only, no mutations. `dry_run: true` overrides all to proposal-only.

---

## Heuristics

### H1 — Infer from Context First (inherited from sinkra-chief; prevents AP-CO-5)

> Before asking the operator for a parameter, INFER from session context. Prompt only when inference fails.

Examples:
- `scope` parameter omitted → infer from session: is operator currently editing `.claude/rules/`? Default to `scope: rules`.
- `yolo_soft` omitted → infer from current branch: `main` → interactive; feature branch → yolo_soft.
- Operator slug missing → cascade fallback (.aiox/active-operator.yaml → git config → env) before asking.

### H2 — Commit Barriers = Single Blast Radius

Every phase has `commit_barrier_after: true`. Rationale: a failure in phase N must only roll back phase N — not contaminate N-1 baselines or N+1 state. `git revert <phase-sha>` is the ONLY rollback primitive. Never use `git stash` across phases.

### H3 — Source of Truth is squads/*/agents/

`.claude/agents/*.md` is a projection. ALL agent edits target `squads/*/agents/`. ide-sync regenerates the projection. Writing directly to `.claude/agents/` is FORBIDDEN (pre_step check in phase_06).

### H4 — Destructive Ops Require Operator YES

Merge rule, delete rule, delete skill, delete agent, condense > 10 lines, remove referenced anchor — ALL require hard-gate YES. Hooks-architect, skill-craftsman, project-integrator, config-engineer: emit proposals, never execute destructive ops directly.

### H5 — MCP Authority Belongs to @devops

MCP add/remove is EXCLUSIVE to `@devops` per `.claude/rules/agent-authority.md`. `mcp-integrator` writes recommendations; handoff delivers them to @devops via `.aiox/handoffs/`. Zero `.mcp.json` mutations in phase_07.

### H6 — Tokens are Binary

Every completion token in `token-assignments.yaml` is binary (done | not done). Roadmap-sentinel verifies during phase_08 exit gate. No partial credit.

---

## Anti-Patterns with Mechanical Prevention

### AP-CO-1 — Anchor Break / Content Loss on Merge
**Symptom:** CLAUDE.md anchor removed or rule merge drops items silently; downstream references break.
**Prevention:**
- Phase_03 MANDATES `audit-rule-items.js` pre-step + `preservation_map` in proposal
- Phase_04 MANDATES `validate-claudemd-anchors.js --mode=pre-edit/post-edit`; auto `git revert` on fail
- Mechanism: scripts block phase on missing inventory OR broken anchor post-edit

### AP-CO-2 — Rename Ref-Count Drift
**Symptom:** File rename touches 2x more refs than estimated; silent corruption.
**Prevention:**
- `sinkra:rename-artifact --dry-run` BEFORE every rename
- Block if ref-count deviates > 2x OR > 10 absolute
- Mechanism: chief's during_step_checks in phase_03 enforce this gate

### AP-CO-3 — Dirty Tree Contaminates Baseline
**Symptom:** Uncommitted changes present at phase entry; rollback ambiguous; baseline JSON reflects mixed state.
**Prevention:**
- Pipeline precondition: `git status --porcelain` empty
- Every phase (except phase_01) declares `mandatory_commit_or_empty_tree` barrier_before
- Mechanism: skill runner exits 1 with explicit rollback guidance

### AP-CO-4 — Auto-Gen Stub Deleted as Duplicate
**Symptom:** Skill deleted that is referenced as `entry_agent` in an active squad config; routing breaks.
**Prevention:**
- `validate-skill-entry-agent-binding.js --mode=pre-delete` BLOCKS phase_05 deletion
- Agent allowlist requires operator YES with reason + approved_by + approved_at
- Mechanism: binding check exit code 1 → skill-craftsman CANNOT include op in proposal

### AP-CO-5 — Operator Prompt Spam (Inference Fatigue)
**Symptom:** Chief asks operator for parameters it could infer from context; operator disengages.
**Prevention:**
- Claude-mastery-chief persona inherits `infer_from_context_first` rule from sinkra-chief
- Phase 5 acceptance: "prompt only when inference fails"
- Mechanism: checklist item in persona; reviewed at phase_06 handoff

---

## Dependencies (Scripts + Skills + Rules)

### Scripts (must exist before pipeline runs)
- `scripts/context-budget-audit.js` (ADAPT AS-01 — `--strict` + segment_breakdown)
- `scripts/audit-rule-items.js` (CREATE AS-06)
- `scripts/validate-rule-frontmatter.js` (CREATE AS-03)
- `scripts/validate-claudemd-anchors.js` (CREATE AS-04)
- `scripts/validate-skill-entry-agent-binding.js` (CREATE AS-05)
- `scripts/sinkra/rename-artifact.js` (REUSE)
- `scripts/validate-yaml.js` (REUSE)
- `.aiox-core/infrastructure/scripts/ide-sync/index.js` (ADAPT AS-02 — `--deletion-allowlist`)

### Skills invoked
- `/update-config` (phase_02 — REUSE)
- `/validate-skill` (phase_05 — REUSE per-skill post-edit)

---

## Checkpoint Hooks (Phase 5 task_anatomy_validation)

```yaml
validation:
  - rule_1_eight_fields_populated_per_phase:
      expectation: "Each of 8 phase tasks in task-definitions.yaml has all 8 anatomy fields"
      method: "YAML schema validator on task-definitions.yaml"
      result: PASS (score 1.0)

  - rule_2_single_executor_per_task:
      expectation: "Every task has exactly 1 responsavel_id"
      method: "count distinct responsavel_id per task_id == 1"
      result: PASS

  - rule_3_dag_validity:
      expectation: "dependency-graph.yaml is acyclic, has exactly 1 root and 1 leaf"
      method: "topological sort + orphan scan"
      result: PASS

  - rule_4_data_flow_connectivity:
      expectation: "Every saida is consumed by >= 1 downstream task OR is final output"
      method: "graph traversal from each saida"
      result: PASS
```

---

## Handoff to Phase 6 (QA Gates)

Phase 6 (`design-qa-gates`) consumes:
- `task-definitions.yaml` (8 tasks with pre/post conditions)
- `dependency-graph.yaml` (DAG structure)
- `token-assignments.yaml` (24 tokens for sentinel verification)

Phase 6 MUST design:
- PV-PA-001 Authority Coherence gate (Accountable vs Responsible alignment)
- PV-PB-001 Threshold Compliance gate (context-budget limits)
- Quality gate matrix linking tokens to gate decisions

Phase 7 (Implementation) consumes all Phase 5 + Phase 6 deliverables and scaffolds scripts, SKILL.md body, config.yaml process_id binding, and registry updates.

---

*Task Definition v1.0 — claude-code-mastery squad*
*Pipeline: sinkra-pipeline-context-optimizer-2026 | Phase 5: Task Definitions*
*Produced by: composition-engineer (sinkra-squad)*
