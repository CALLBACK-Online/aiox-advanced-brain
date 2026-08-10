# Changelog

## 2026-07-06 — skills/full-sdc/SKILL.md

Movido para fora do contexto carregado.

## Changelog

### v8.0.0 — 2026-05-23

**Source:** Story 115A.S7 — Worktree Nesting Root Cause Fix + Dashboard Ink ADAPT. Roundtable RT-20260523-WAVEv9 (5 agents, 7.34/10, APROVA_WITH_CONDITIONS). Codex deep-dive `agentId a95c4c21b9563a32a` identified 4 structural defects in Phase 0c.1.

**Changes (BREAKING — guard semantics changed):**

1. **Phase 0c.1 — Nesting Detection Guard (Invariant 2, structural primary):**
   - **PRIMARY check is now cwd-structural** (`cwd.contains("/.claude/worktrees/")` or `\\.claude\\worktrees\\`), not ACK-file presence.
   - When cwd is nested, SKIP Phase 0c AND write a story-scoped `dispatch.ack` with `provisioned_by: "external"`.
   - Secondary check: `.sdc-ack/{story_id}/dispatch.ack` (story-scoped — the canonical wave-execute path).
   - Tertiary check: `.sdc-ack/dispatch.ack` (legacy non-scoped — deprecated, kept for backward-compat with explicit log).
   - Resolves 4 defects:
     - **Defect #1 (path mismatch):** old guard read `.sdc-ack/dispatch.ack`, writer wrote `.sdc-ack/{story_id}/dispatch.ack` → infinite re-creation. Fixed by reading both paths + structural fallback.
     - **Defect #2 (naming mismatch):** Phase 0c fallback expected `wt-{story_id}` but wave-launch.js created `story-{storyId}`. Fixed by making cwd check structural (any path inside `.claude/worktrees/` is recognized).
     - **Defect #3 (logical race):** child decided routing BEFORE wave-launch wrote ACK → ACK couldn't be relied upon. Fixed by removing dependency on ACK timing (cwd is always available at decision time).
     - **Defect #4 (indirect Invariant-2 check):** ACK presence was a proxy. Fixed by checking the invariant directly.
2. **Phase 5b.1 — Skip Guard mirror:** Same 3-tier structural-first detection. If cwd is inside a pre-provisioned worktree, merge-back/teardown is delegated to the spawning orchestrator (wave-execute Stage 6 OR human-external). full-sdc must NOT tear down a worktree it did not create.
3. **New section "Skill Agnosticism" (AC7, Pedro mandate 2026-05-23; renamed Round 2 from "Skill Agnosticism Matrix" — orphan ref fix per Codex Round 2 finding):** Documents 7 execution modes (5 standalone + 2 orchestrated) with canonical mode-detection algorithm, 6 BLOQUEANTE anti-patterns, and 3-tier enforcement model (advisory → story-AC → CI regression). References canonical SOT `.claude/rules/skill-agnosticism.md`.

**Why MAJOR:** The cwd-structural primary check is a semantic break for any caller that depended on the old "ACK-only" routing path. Specifically, callers that wrote `.sdc-ack/dispatch.ack` (legacy non-scoped) outside a worktree expecting the guard to SKIP Phase 0c will now find the guard PROCEEDS to 0c.2 (because the cwd check fails). This is intentional — the old behavior was buggy (Defect #4). Wave-execute writes the story-scoped path, so its callers are unaffected.

**Migration:** No change required for the `/full-sdc {story}` invocation contract. Wave-execute and external pane spawners that put cwd inside `.claude/worktrees/` continue to work (now via the structural check, which is more robust). The deprecated `.sdc-ack/dispatch.ack` non-scoped path is supported with a one-time log; remove that write path in callers.

**Tests:** 3/3 `wave-launch-nesting-guard.test.js` pass; 3/3 `parse-agents-json-stream.test.js` pass; 5 vitest cases in `services/mux-adapter/__tests__/telemetry.test.ts` written (pending worktree `npm install`).

### v7.0.0 — 2026-05-22

**Source:** Story 115A.8b — Deleção `/story-executor` + Retrofit `/full-sdc` Auto-ACK.

**MAJOR — Auto-ACK Emission Protocol (additive, backward-compatible):**
1. `/full-sdc` agora é o único writer de `.sdc-ack/{story-id}/*.ack` files. O wrapper `/story-executor` (descontinuado em 115A.8b) era o owner anterior.
2. Nova seção `## Auto-ACK Emission Protocol` documenta: 7 ACK files, formato YAML exato, idempotência (overwrite OK), independência de modo (default + --spawn-external).
3. Insertion points adicionados em cada fase: `dispatch.ack` (Phase 0c.5b), `validate.ack` (Phase 1), `develop.ack` (Phase 2), `review.ack` (Phase 3 pós L2-gate), `deploy.ack` (Phase 4 PASS ou SKIPPED), `phase-5.ack` + `sdc-complete.ack` (Phase 5).
4. Em HALT/FAIL, o ACK da fase corrente é escrito com `status: failed` antes do halt — mirrors a partial learning log rule.
5. Phase 0c texto atualizado: referência a story-executor removida (era "story-executor sets `wt_provisioned: true`"); agora é `/full-sdc` quem escreve o dispatch.ack.

**Backward-compat:** Callers que não lêem ACK files são 100% não afetados. Callers que lêem ACK files (wave-execute polling) passam a recebê-los com campos adicionais (`story_id`, `skill`) que são additive.

### v6.0.0 — 2026-05-18

**Source:** Story 115.S2.O7 — Worktree Lifecycle Auto-Management (RT-20260517-O7O9, APPROVE_WITH_CONDITIONS 7.33/10, 6/6 unânime).

**MAJOR — Worktree Lifecycle Auto-Management (WL-1..WL-7):**

1. **Phase 0c — Auto-Spawn (WL-1):** Provisiona worktree dedicado por story off `origin/main` (fetch fresco). Idempotente. Naming canônico `wt-{story_id}`. Skippado se wave-execute pre-provisionou (`wt_provisioned: true`). Verifica TK-SDC-MAX-PARALLEL-WORKTREES. Registra em `.aiox/worktrees/registry.json` via O6b write primitive. Escreve checkpoint `phase-0c.json`.
2. **Phase 5 §merge-back (Phase 5b) — Auto-Merge-Back + Teardown (WL-2/WL-3):** Sub-step de Phase 5 (pós close-story PASS). WL-2 prepara merge-back (git fetch + diff + rebase/ff local per TK-SDC-MERGE-BACK-STRATEGY=rebase-ff) e emite handoff estruturado ao @devops (autoridade exclusiva de push — agent-authority.md). WL-3 executa teardown após confirmação de merge em origin/main (via `git branch -r --merged origin/main`). Respeita O6b AC-5 teardown-ordering (O6b=owner, WL-3=executor do Step 3). Gate pós-teardown: assert zero resíduo. O1-absent degradation: LOUD WARNING + skip .aiox/ cleanup + registry state=halted.
3. **WL-4 — Failure Path:** Em qualquer HALT após Phase 0c, worktree é PRESERVADO (nunca destruído). Registry atualizado: state=halted, halt_reason preenchido. Detecção de stale por TK-SDC-WORKTREE-STALE-DAYS.
4. **WL-6 — Reconciliação Registry:** Executada no start de Phase 0c. Reconcilia `.aiox/worktrees/registry.json` vs `git worktree list --porcelain`. Usa `git branch -r --merged origin/main` (NUNCA `git branch --merged`). Detecta e reporta orphans antes de iniciar nova execução.
5. **WL-7 — GC Idempotente:** Comando standalone de reconciliação completa. Lock file (gc.lock) previne GC concorrente. M4 reconstruction se registry ausente. 3 negative test-cases: (a) local-merged-not-origin, (b) detached HEAD, (c) concurrent GC lock.

**Why MAJOR:** Adds Phase 0c (new phase before Phase 1), Phase 5b (new sub-phase after Phase 5), WL-4 failure protocol, WL-6 reconciliation, WL-7 GC — all of which change orchestrator behavior for any caller. Pipeline now self-manages worktree lifecycle end-to-end.

**Rollback:** Revert O7 full-sdc commits → state O6b-end v5.1.0 (stable). Each WL commit is independently revertible.

**Preserves:** O11 L2 gate (§Post-Phase 3 Verification Gate), O6a/O6b content, O12 Branch Guard — none removed or regressed.

### v5.2.0 — 2026-05-18

**Source:** Story 115.S2.O12 — develop-story lifecycle hygiene (FINDING 2, AC-2b). Empirical defect origin: full SDC run of Story 115.S2.O10 (2026-05-18) — 3 commits (`2138af5a3`, `0257ca9c9`, `f484d27ac`) landed on `main` with no feature branch, making PR-based review structurally impossible. `roundtable_required: false` (additive gate, non-breaking — per `skill-standards.md §Versioning`, Minor bumps require owner-squad approval, not a roundtable). QG: @architect.

**Changes (MINOR — additive gate, non-breaking):**
1. **Post-Phase-2 Branch Guard (new NON-NEGOTIABLE subsection in §Post-Phase Verification Gate).** After Phase 2 artifact verification and BEFORE dispatching Phase 3, the team-lead runs `git branch --show-current`; if `main`/`master`, emits an explicit `BRANCH GUARD VIOLATION` FAIL, dispatches a fix-message to the still-alive executor (verification-gate-retry semantics, max 2 retries → escalate), and emits a `verification_gate_retry` orchestration event. This is **defense-in-depth Layer 2** (L1 = `develop-story/SKILL.md §Pre-Execution Branch Setup`, AC-2a). The guard is a no-op PASS on the conformant happy path (post-AC-2a develop-story always lands on `feat/{story_id}-*`).

**Why MINOR:** Purely additive — adds a new gate check with retry/escalate semantics already used elsewhere in the Post-Phase Verification Gate. No existing API, output format, pipeline contract, or phase ordering changed. No breaking change for callers; `/full-sdc {story}` invocation contract unchanged.

**Migration:** None — additive. A conformant run is unaffected (guard PASSes silently).

> **Reconciliation note:** the on-disk frontmatter was at `version: "5.1.0"` with no corresponding `### v5.1.0` changelog entry (a pre-existing discrepancy outside this story's scope — same class as the v2.0.0 reconciliation recorded above for Story 115.S2.O2). This v5.2.0 entry bumps from the on-disk `5.1.0` baseline and does not retroactively author the missing 5.1.0 entry (out of scope for 115.S2.O12).

### v5.0.0 — 2026-05-17

**Source:** Story 115.S2.O6b — Durable State Checkpoint Layer. Roundtable RT-20260517-O6aO6b (APPROVE_WITH_CONDITIONS 7.33/10, 6/6 unanimous) + RT-20260517-O7O9 (CG-DEFER-1/2 CLOSED). Sequenciado após O6a v4.0.0.

**Changes (BREAKING — durable persistence layer added):**
1. **AC-1 — Full Checkpoint on-disk per phase (schema `checkpoint-schema-version: "1.0"`, JSON).** O6b expands the O6a seed (which has `phase_status: "started"`) to a full checkpoint after Post-Phase Verification Gate PASS: adds `artifacts_on_disk[]`, `timestamp_end`, updates `phase_status: "completed"`. Token `TK-SDC-CHECKPOINT-TTL` governs TTL/cleanup.
2. **AC-2 — Re-entry Protocol with Triple Validation + 5 negative scenarios.** Pipeline can resume from any phase with `completed` checkpoint without re-executing prior phases. Triple validation: (1) file exists, (2) `phase_status == "completed"`, (3) `timestamp_end` non-null, (4) all `artifacts_on_disk[]` paths exist. 5 negative scenarios (a–e) with defined HALT/WARNING behavior.
3. **AC-3 — Worktree Registry (`worktree-registry-v1`, JSON).** `.aiox/worktrees/registry.json` managed by O6b write primitive. Ownership seam: O6b=write, O7 WL-6/WL-7=reconciliation+GC. Reconciliation uses `git branch -r --merged origin/main` (NEVER `git branch --merged`). Orphan housekeeping: NEVER auto-delete without team-lead confirmation. Registered in `.aiox/registries/INDEX.json` (R39, NON-DEFERRABLE).
4. **AC-4 — Epic-state.json sync (degradation-safe, gated on O9 ES-2).** Step added to Phase 5: update minimal node `{story_id, status, last_updated}`. HALT LOUD if `schema_version != "epic-state-v1"`. WARNING LOUD via SendMessage if file absent. Crash-recovery + drift sentinel gated-pending-O9-ES2 (schema freeze prerequisite per CG-O7O9-10).
5. **AC-5 — Pre-teardown ordering contract (Phase 5, O1 coordination).** Teardown sequence: O1 flush → checkpoint cleanup → git worktree remove → registry update. DEC-O6b-6: O1 not-impl → LOUD WARNING + defer checkpoint cleanup; O1 flush fail → HALT LOUD + state intact.
6. **New section "Durable State Checkpoint Layer (O6b)"** with all ACs + "INDEX.json Registration" section.

**Rollback procedure:** Reverting O6b → v4.0.0 (O6a-end) is a valid rollback state. The O6a v4.0.0 commit is the rollback checkpoint. Granular commits: O6b is NOT squashed with O6a. To rollback: `git revert` the O6b commit(s) back to the last O6a commit on the `full-sdc/SKILL.md` file.

**Why MAJOR:** Adds new behavioral obligation (checkpoint expansion, re-entry, registry write, teardown ordering) that callers and sub-implementations must account for. Removes implicit "no durable state" assumption. Breaking for any implementation that assumed ephemeral-only execution state.

**Migration:** Non-breaking for `/full-sdc {story}` invocation contract. BREAKING for implementations that assumed no on-disk state between phases. O7 WL-6/WL-7 must implement using O6b write primitives (not a new format).

### v4.0.0 — 2026-05-17

**Source:** Story 115.S2.O6a — Interim Runtime State HALT. Roundtable RT-20260517-O6aO6b (APPROVE_WITH_CONDITIONS 7.33/10, 6/6 unanimous). DEC-O6a-1 CLOSED→heurística (c)+snapshot+grace window. DEC-O6a-2 CLOSED→MAJOR. DEC-O6a-3 CLOSED→granular commits.

**Changes (BREAKING — HALT behavior added to Post-Phase Verification Gate):**
1. **Task-List Wipe Detection (new NON-NEGOTIABLE subsection in Post-Phase Verification Gate).** The team-lead now writes a minimal checkpoint seed (`.aiox/checkpoints/{story_id}/phase-{N}.json`) at the START of each phase, then checks the active task-list against `expected_tasks[]` after the grace window (`TK-SDC-WIPE-GRACE-WINDOW`). Any expected task absent without `Done` status triggers wipe detection per heurística (c) adjudicada (DEC-O6a-1). Legitimately-completed phases (all tasks Done) are an explicit exclusion.
2. **Structured HALT — `runtime_state_loss` event (O1-canonical schema).** On wipe, the team-lead emits a typed event with `event_schema_version: "1.0"`, O6a-specific fields (`subtype`, `tasks_expected`, `tasks_found`, `story_id`, `action`) inside `detail` (never top-level), writes the partial learning log, and sends a structured SendMessage to team-lead with the verbatim recommendation text. Execution STOPS — silent fallback is explicitly forbidden.
3. **HALT scope adjudication (T1.3/CG-11).** HALT is isolated to the affected story's `/full-sdc` session; it does NOT HALT the whole wave. wave-execute v5.0 handles per-story Blocked results via the existing per-story failure pattern (cascade-blocks dependents per DAG only).
4. **Gate Ownership Contract documented.** O6a owns: gate detection + minimal checkpoint seed write. O6b owns: full checkpoint cycle (expand seed, `artifacts_on_disk[]`, `timestamp_end`) + re-entry protocol + worktree registry.

**Why MAJOR:** The HALT removes the implicit behavior "continue after wipe" — any caller (especially wave-execute) that assumed the pipeline continues after a task-list desync now gets a hard stop instead. This is a removed feature per `skill-standards.md §Versioning`. Precedent: O3/wave-execute was also MAJOR for an orchestration behavioral change.

**Migration:** BREAKING for pipeline callers that assumed continuation after wipe. No change to the `/full-sdc {story}` invocation contract. O6b will add re-entry on top of this HALT foundation.

### v3.0.0 — 2026-05-16

**Source:** Story 115.S2.O4 — forensic friction audit (`docs/research/2026-05-16-full-sdc-friction-audit/00-SYNTHESIS.md`, 3 parallel audits, 43 logs same schema; DiD experiment `06-did-experiment.md` refuted the Epic-115-complexity confounder as primary driver). Idle-events/run rose monotonically 0.09 → 1.00 → 1.60 across v1.0→v1.1→v1.2, culminating in a catastrophic out-of-sequence fabricated-authorization close (event E3, 115.S2.O2). Roundtable RT-2026-05-16-O4 (APPROVE_WITH_CONDITIONS 7.7/10, 5/5; decisions D-RT-1..D-RT-7).

**Changes (BREAKING — orchestration protocol):**
1. **FIX-1a — De-pre-announce.** The @po teammate is now spawned **Phase-1-only**. The spawn prompt no longer pre-announces review/close, `status=Done`, or "Phase 5". Pre-announcing all 3 phases made a premature close the path of least resistance once coordination state degraded.
2. **FIX-1b — Sequence Lock (new NON-NEGOTIABLE section).** Prohibitive (not advisory) phase-progression lock: the team-lead is the SOLE authorizer of every transition; no phase dispatched until the prior phase's on-disk artifacts are verified; the permissive "treat each `[ACTION REQUIRED]` prefix as a NEW task" framing is removed; rule #8 reframed (prefix = gated dispatch token, not a self-advance parse hint). Honest scope (D-RT-2): LLM-read protocol text, diff-verifiable; true mechanical enforcement → Story 115.S2.O6.
3. **FIX-1c — Post-Phase Verification Gate auto-HALT.** Any `status: Done` detected OUTSIDE Phase 5 now emits a structured `integrity-violation` (`subtype: premature-done-outside-phase5`) and hard-HALTs (closes the F2 direct-edit bypass proven in 115.S1.D1; complementary to close-story CHK-0). Phase 5 now writes an orchestrator-exclusive dispatch lockfile `.aiox/dispatch/{story-id}-phase5-{ISO8601}.lock` (D-RT-1) — a protocol barrier (not cryptographic; true hardening → O6) that close-story CHK-0 reads to verify invocation provenance.
4. **FIX-4 — Defer Phase-4/5 TaskCreate.** Phase 4 and Phase 5 tracking tasks are no longer created in the init block; each is created immediately before its phase is dispatched. Eliminates the stale Phase-5 task channel (audit event E5) that could survive a task-list wipe and induce a premature close.

**Scoping constraint (AC-6 item 7, NON-NEGOTIABLE):** the rewrite targets the pre-announce-all-phases + trust-the-prefix construct ONLY. The Post-Phase Verification Gate (load-bearing mitigation confirmed by audits 01–05) is **preserved and hardened**, not reverted. A blanket revert of all v1.1.0 text was explicitly out of scope.

**Migration:** BREAKING for orchestration semantics (phase progression is now team-lead-gated, not subagent-self-advanced) but NOT for callers — the `/full-sdc {story}` invocation contract is unchanged. Sibling fixes FIX-2 (ACK handshake) and FIX-3 (Recipient Contract) are delegated to Stories 115.S2.O3 / 115.S2.O1 and intentionally NOT in this version.

### v2.0.0 — 2026-05-16

**Source:** Story 115.S2.O2 (Worktree Isolation), FA-7. Reconciliation entry — the frontmatter `version` was set to `2.0.0` by 115.S2.O2 but no corresponding changelog entry was recorded (Roundtable D-RT-4: frontmatter is authoritative; this entry closes the discrepancy noted in Story 115.S2.O4 Nota 3).

**Changes:**
1. **"Execution Context — Worktree Isolation" (new section)** — standalone runs against a dirty MAIN invoke via `claude --worktree <story-id>` for a clean `origin/main` baseline; internal PO/dev/QG spawns do NOT carry `isolation: worktree` (they share context to review each other's work); isolation is at the story-executor outermost level only. Explicit guidance not to add a `WorktreeRemove` blocking gate (hook payload has no allow/block mechanism). Roundtable sign-off RT-1 (7.4/10) + RT-2 (8.0/10), report `docs/stories/epic-115/ROUNDTABLE-DECISION-115.S2.O2-20260516.md`.

**Migration:** No breaking changes for callers — additive guidance for worktree-isolated execution.

### v1.2.0 — 2026-05-15

**Source:** Live execution of Story 115.S1.E3 + founder (Pedro Valério) observation: coordination-layer friction between the team-lead and spawned agents (runtime task-list wipe, handoff misparse forcing re-commands, verification-gate retries) is observed in the main thread but recorded **nowhere structured** — neither Development Log nor per-skill Learning Logs nor (as countable data) the full-sdc log. A meta-analysis can aggregate tech debt and what-was-built, but is blind to the architecture/infrastructure of inter-agent communication (SendMessage / Agent Teams), so recurring friction never surfaces as volume ("happened 4× → fix").

**Changes:**
1. **Orchestration Telemetry (new NON-NEGOTIABLE section)** — names the third (orchestration) telemetry plane, gives a **closed event vocabulary** (`handoff_misparse`, `verification_gate_retry`, `runtime_state_loss`, `agent_respawn`, `circuit_breaker_trip`, `escalation`, `sendmessage_failure`, `phase_skipped_unexpected`), a typed event shape, and an emission rule (team-lead emits at detection; written at Phase 6; partial log on HALT; observed-only per Epistemic Standards).
2. **Learning log schema → v1.1** — added `orchestration_events: []` block + `epilogue.orchestration_event_count`. Free-text `what_failed` remains as human summary; the structured array is now the canonical, aggregable record.
3. **Aggregation handoff** — cross-skill rule `.claude/rules/orchestration-telemetry.md` (inherited by full-sdc, full-tec, wave-execute, roundtable) + `.synapse/metrics/orchestration-friction.json` roll-up are scoped to **Story 115.S2.O1** (roundtable-gated, since it is a major change across 5 Tier-2/3 orchestrator skills). full-sdc emits locally in the interim so no run's data is lost.

**Migration:** No breaking changes for callers. Learning logs jump schema_version 1.0 → 1.1 (additive only — consumers ignoring `orchestration_events` keep working).

### v1.1.0 — 2026-05-14

**Source:** Live execution of Story 115.S0.3 surfaced 1 reproducible gap (handoff ambiguity) + 1 audit-process failure (orchestrator's own verification used a flawed shell command and reported a false-positive missing artifact). Together they motivate stricter verification.

**Changes:**
1. **Post-Phase Verification Gate (new MANDATORY section)** — team-lead now verifies on disk that artifacts promised by the invoked SKILL.md were actually produced, before marking a phase completed. Includes per-skill artifact checklist + retry policy (max 2). Rationale: even when agents are honest, a downstream auditor needs deterministic verification. The Story 115.S0.3 audit itself surfaced this — the orchestrator's `ls | tail -10` truncated the actually-existing learning log and produced a false negative. A formal verification gate (with explicit file paths, not ad-hoc shell) prevents both classes of failure (agent fidelity AND auditor methodology).
2. **`[ACTION REQUIRED: {skill}]` prefix mandatory on all SendMessage that invokes a skill** — eliminates the ambiguity where a reused agent (e.g., @po reused for close after review) parses a follow-up message as a status report rather than a new task. Observed empirically on Story 115.S0.3: Phase 5 needed a retry because the first message led with phase narration ("Phase 3 review completed... now execute close-story") and the @po responded with a Phase 3 status summary instead of executing close-story.
3. **Pre-announce sequential actions at spawn time** — the initial Agent spawn prompt for PO now lists all 3 potential phases (validate, review-if-qg, close) so the agent has full context from turn 1 about future SendMessage handoffs.
4. **Removed redundant "Read your persona from .claude/agents/{id}.md" instruction** — the persona is already injected by the harness via `subagent_type`. Asking the agent to re-read its own definition wastes tools/context.
5. **Added "Agent Resolution Notes" section** — documents that (a) `subagent_type` resolves to `.claude/agents/{id}.md` automatically, (b) skills are filesystem protocols (any agent can execute any skill), (c) the story's `executor:`/`quality_gate:` fields drive selection regardless of an agent's declared native skills.
6. **Phase 3 spawn split into Branch A (reuse PO) and Branch B (spawn new QG)** — when `quality_gate=@po`, do NOT spawn a duplicate; reuse the existing PO teammate via SendMessage.
7. **All Agent spawn blocks now include `subagent_type:` explicitly** — was implicit in v1.0.0, making the harness mechanism opaque.
8. **Agents now report `Artifacts produced` in all SendMessage completions** — list of paths created/modified, used by the verification gate.

**Migration:** No breaking changes for callers. v1.1.0 is a stricter execution of the same pipeline.

### v1.0.0 — initial release

