---
name: full-sdc
description: "Full Story Development Cycle — orchestrates validate → develop → review (QG loop) → deploy → close via Agent Teams with sequential handoffs, durable per-phase checkpoints, re-entry protocol, worktree lifecycle auto-management (WL-1..WL-7: auto-spawn, auto-merge-back via @devops, auto-teardown, failure-path, GC), teardown ordering contract, and auto-ACK emission (Story 115A.8b)"
version: "8.0.0"
owner_squad: "sinkra-squad"
sinkra_tier: Tier2
context: conversation
agent: general-purpose
activation_type: pipeline
user-invocable: true
argument-hint: "[story-path] [mode: yolo|interactive]"
depends_on: ["/validate-story-draft", "/develop-story", "/review-story", "/apply-qa-fixes", "/deploy-story", "/verify-deploy", "/close-story"]
invokes: []
---

# Full SDC — Complete Story Development Cycle

Orchestrates the entire story lifecycle from validation through closure using Agent Teams.
Each phase is executed by the correct agent persona with full skill protocol.
QG loop is real — separate agents conversing until PASS or circuit breaker.

## Skill Agnosticism (Story 115A.S7 AC7 + Round 1 FIX-4)

**Canonical SOT:** [`.claude/rules/skill-agnosticism.md`](../../rules/skill-agnosticism.md) —
Compatibility Matrix (7 modes), anti-patterns (AP1–AP6), enforcement levels, regression test
requirements, and path-naming dual convention. Read it for the full matrix. This `SKILL.md`
keeps **only** the Phase 0c routing-decision algorithm to avoid SOT drift (Codex Round 1
FIX-4 — duplicate matrices drifted on day 1).

**Mandate:** Pedro Valério (2026-05-23) — toda skill deve poder ser usada SEPARADAMENTE,
sem dependência do orquestrador. Modificações em `/full-sdc` NUNCA podem destruir o uso
unitário das skills atômicas que ele compõe.

### Mode-Detection Algorithm (canonical for Phase 0c.1 — MUST match the rule SOT)

```
WT_PROVISIONED_TTL_HOURS = 24  # FIX-3 — stale ACK rejection

def detect_phase_0c_mode():
    cwd = os.getcwd()
    # Tier 1 — STRUCTURAL (Invariant 2 of worktree-isolation.md) — immune to staleness
    if cwd.contains("/.claude/worktrees/") or cwd.contains("\\.claude\\worktrees\\"):
        return NESTED_SKIP   # SKIP 0c.2-0c.5; emit ACK with provisioned_by:external

    # Tier 2 — STORY-SCOPED ACK with TTL guard
    if exists(f".sdc-ack/{story_id}/dispatch.ack"):
        ack = read(f".sdc-ack/{story_id}/dispatch.ack")
        if ack.contains("wt_provisioned: true"):
            age_hours = (now - parse_timestamp(ack)) / 3600
            if age_hours <= WT_PROVISIONED_TTL_HOURS:
                return SCOPED_ACK_SKIP    # SKIP 0c.2-0c.5
            # else: stale ACK → fall through

    # Tier 3 — LEGACY non-scoped ACK (deprecated, TTL applies)
    if exists(".sdc-ack/dispatch.ack"):
        ack = read(".sdc-ack/dispatch.ack")
        if ack.contains("wt_provisioned: true"):
            age_hours = (now - parse_timestamp(ack)) / 3600
            if age_hours <= WT_PROVISIONED_TTL_HOURS:
                return LEGACY_NON_SCOPED_SKIP  # SKIP, with deprecation warning
            # else: stale → fall through

    # Tier 4 — STANDALONE: no nesting, no fresh ACK → run Phase 0c.2 onward
    return STANDALONE_CREATE  # RUN 0c.2 → 0c.3 → 0c.5 → 0c.5b
```

**Reference test:** `.claude/skills/wave-execute/__tests__/full-sdc-standalone-mode1.test.js`
executes this algorithm against synthetic environments. Any drift between this block and the
test = test failure = PR rejected (AP5).

**See the rule SOT for:**
- The 7-mode Compatibility Matrix (Modes 1–7 entry conditions + expected behavior)
- Path naming dual convention (`wt-{story_id}` from standalone vs `story-{story_id}` from wave-launch)
- Anti-Patterns AP1–AP6 (BLOQUEANTES em PR review)
- Decision Tree (modificando uma skill)
- Enforcement levels (advisory → story-AC → CI regression future)

---

## Execution Context — Worktree Isolation (Story 115.S2.O2, 2026-05-16)

When run standalone against MAIN, callers with a dirty MAIN worktree should invoke via
`claude --worktree <story-id>` to obtain a clean baseline from `origin/main`.

The internal PO/dev/QG spawns within a `/full-sdc` session do NOT carry `isolation: worktree`
— they must share context to review each other's work. Isolation is at the `/full-sdc` session
(outermost) level only; `/full-sdc` is the pipeline that runs INSIDE a worktree.

Do NOT add a `WorktreeRemove` blocking gate — this hook does not support decision-control
(payload = `worktree_path` only; no allow/block mechanism exists in Claude Code).

Roundtable sign-off: RT-1 (7.4/10, 2026-05-16) + RT-2 (8.0/10, 2026-05-16).
Full report: `docs/stories/epic-115/ROUNDTABLE-DECISION-115.S2.O2-20260516.md`.

## Usage

```
/full-sdc docs/stories/epic-N/STORY-N.M-TITLE.md
/full-sdc docs/stories/epic-N/STORY-N.M-TITLE.md yolo
/full-sdc docs/stories/epic-N/STORY-N.M-TITLE.md interactive
```

## Architecture: Agent Teams + Tasks + Sequential Handoffs

Flow for team `sdc-{story-id}`: Task 1 Phase 0 Analysis runs inline; Task 2 Phase 1 Validate uses `@po`; Task 3 Phase 2 Develop uses `{executor}`; Task 4 Phase 3 Review/QG uses `{quality_gate}` and on FAIL sends fixes to `{executor}`, asks `{quality_gate}` to re-review, and loops max 3x; Task 5 Phase 4 Deploy plus Phase 4b Verify uses `{deploy_agent}` when `deploy_type != none`; Task 6 Phase 5 Close reuses `@po`.

## MANDATORY EXECUTION RULES

1. **Sequential execution** — each phase completes before the next starts
2. **Agents persist** — spawned teammates stay alive across phases (PO is reused for close)
3. **QG loop is real** — QG and Executor communicate via SendMessage, not re-spawned
4. **Tasks track progress** — TaskCreate for visual tracking, TaskUpdate on completion
5. **Deploy is conditional** — only spawn deploy agent if `deploy_type != none`
6. **Circuit breaker** — QG loop max 3 iterations, then escalate to user
7. **Post-phase verification (NON-NEGOTIABLE)** — after each agent reports completion, team-lead MUST verify the artifacts that the invoked skill's SKILL.md promises to produce, BEFORE marking the phase completed. If any expected artifact is missing, dispatch a fix-message to the agent (max 2 retries). See "Post-Phase Verification Gate" below.
8. **Action-prefixed handoffs are dispatch tokens, not parse hints** — every `SendMessage` that invokes a skill MUST begin with `[ACTION REQUIRED: {skill-name}]`. The prefix is the team-lead's authorization to start that phase, issued ONLY after the Sequence Lock conditions are met. It is NOT a cue for a subagent to "treat this as a new task" on its own initiative. See "Sequence Lock" below — the lock, not the prefix, is what governs phase progression.

---

## Sequence Lock (NON-NEGOTIABLE — FIX-1b, Story 115.S2.O4)

The pipeline is **strictly sequential and team-lead-gated**. This section is
**prohibitive**, not advisory.

### The lock

> **No phase may be dispatched until the team-lead has verified, on disk, the
> artifacts of the immediately-preceding phase (per the Post-Phase Verification
> Gate). The team-lead is the SOLE authorizer of every phase transition.**

- A subagent **MUST NOT** start, request, propose, anticipate, or "skip ahead"
  to any phase it was not explicitly dispatched into via an
  `[ACTION REQUIRED: {skill}]` message from the team-lead.
- A subagent **MUST NOT** infer that a later phase is due because it "knows the
  pipeline shape". Forward knowledge of the pipeline is deliberately withheld
  (see Phase-1-only spawn) precisely so it cannot be acted on prematurely.
- The team-lead **MUST NOT** dispatch phase N+1 while phase N's on-disk
  artifacts are unverified, missing, or empty — even if a subagent reports
  completion. Self-report is not authorization; on-disk verification is.
- A phase **MUST NOT** be reordered, merged, or skipped by anyone other than
  the team-lead, and only for a phase's *declared* skip condition (e.g.
  `deploy_type: none` skips Phase 4). Any other skip is a
  `phase_skipped_unexpected` orchestration event.

### Prohibited (this is the construct the 2026-05-16 audit traced to friction)

- ❌ Pre-announcing future phases at spawn time ("you will later run close-story").
- ❌ "Treat each `[ACTION REQUIRED]` prefix as a NEW task" framing that lets a
  reused agent self-advance the pipeline.
- ❌ Acting on a stale task-channel (e.g. a pre-created Phase-5 task surviving a
  task-list wipe) as if it were a live dispatch.
- ❌ Closing / setting `status: Done` outside Phase 5 under any circumstance
  (enforced mechanically by close-story CHK-0 and the Post-Phase Verification
  Gate `integrity-violation` HALT).

### Enforcement reality (honest scope — D-RT-2)

This Sequence Lock is **LLM-read protocol text**. Its correctness is therefore
*probabilistic*, not mechanically guaranteed. The verifiable test of this AC is
**external diff inspection**: a reviewer confirms that prohibitive (not advisory)
language is present on disk. True mechanical enforcement (durable per-phase
state, re-entry, `runtime_state_loss` HALT) is the residual C3 risk and is
delivered by **Story 115.S2.O6** (durable orchestration state layer — existing
stub, Draft). O4 reduces the probability of failure on a fragile substrate; O6
removes the substrate fragility. The two are complementary.

## Agent Resolution Notes

- `subagent_type: "{agent_id}"` resolves to `.claude/agents/{agent_id}.md` **automatically by the harness**. The persona is injected as the subagent's system prompt at spawn time. **Do NOT instruct the agent to "read your persona from .claude/agents/..."** — that is redundant and wastes tools/context.
- **Skills are filesystem protocols, not agent-bound tools.** Any agent can execute any skill by reading its `SKILL.md`. The `skills:` field in agent frontmatter declares "native" skills (those the agent is designed for), but other skills may be invoked as needed when the story domain calls for it. Example: an `@po` may execute `review-story` (typically `@architect`/`@qa`) if the story's `quality_gate: @po`.
- **Story drives executor/QG selection.** The story's `executor:` and `quality_gate:` fields determine who runs which phase, regardless of skills declared in the agent. The orchestrator obeys the story.

---

## Phase 0: Story Analysis (team-lead, inline)

**Execute BEFORE creating the team.** This is lightweight analysis by the orchestrator.

### 0.1 — Read Story File

```
Read {story_path}
Extract:
  - story_id (from filename, e.g., "101.46")
  - title (from H1)
  - status (must be Ready or Draft — validate will fix Draft)
  - executor (e.g., "@dev", "@architect", "@db-sage")
  - quality_gate (e.g., "@qa", "@po", "@architect")
  - deploy_type (e.g., "none", "hetzner_docker", "vercel", "supabase_migration", "railway", "multi")
  - accountable (e.g., "pedro-valerio")
  - depends_on (list of dependency story IDs)
```

### 0.2 — Resolve Agent IDs

Map story fields to agent file paths:

| Field | Agent ID | Persona File |
|-------|----------|-------------|
| executor: @dev | dev | .claude/agents/dev.md |
| executor: @architect | architect | .claude/agents/architect.md |
| executor: @db-sage | db-sage | .claude/agents/db-sage.md |
| executor: @devops | devops | .claude/agents/devops.md |
| quality_gate: @qa | qa | .claude/agents/qa.md |
| quality_gate: @po | po | .claude/agents/po.md |
| quality_gate: @architect | architect | .claude/agents/architect.md |

### 0.3 — Resolve Deploy Agent

| deploy_type | Deploy Agent | Verify Agent |
|-------------|-------------|-------------|
| none | — (skip Phase 4) | — |
| hetzner_docker | @infra-chief | @infra-chief |
| supabase_migration | @db-sage | @db-sage |
| railway | @devops | @devops |
| vercel | @devops | @devops |
| multi | @devops (primary) | @devops |

### 0.4 — Determine Execution Mode

```
mode = argument[1] || "interactive"
Valid: "yolo" | "interactive" | "preflight"
```

### 0.5 — Dependency Check

For each story in `depends_on`:
- Read the dependency story file
- Check status is `Done`
- If any dependency is NOT Done → HALT with clear message listing blockers

### 0.6 — Display Analysis Summary

```
╔══════════════════════════════════════════════════════════╗
║  Full SDC — Story {story_id}: {title}                    ║
╠══════════════════════════════════════════════════════════╣
║  Executor:     @{executor} ({persona_name})              ║
║  Quality Gate: @{quality_gate} ({persona_name})          ║
║  Deploy Type:  {deploy_type}                             ║
║  Deploy Agent: @{deploy_agent} (or "none — skip deploy") ║
║  Mode:         {mode}                                    ║
║  Accountable:  {accountable}                             ║
╠══════════════════════════════════════════════════════════╣
║  Pipeline:                                               ║
║    1. Validate (@po)                                     ║
║    2. Develop (@{executor})                              ║
║    3. Review (@{quality_gate}) + QG Loop                 ║
║    4. {Deploy (@{deploy_agent}) | SKIP}                  ║
║    5. Close (@po)                                        ║
╚══════════════════════════════════════════════════════════╝
Proceed? [y/n]
```

In YOLO mode: skip confirmation, proceed directly.

---

## Phase 0b: Create Team + Tasks

### Create Team

```
TeamCreate(
  team_name: "sdc-{story_id}",
  description: "Full SDC for Story {story_id}: {title}"
)
```

### Create Tasks (visual tracking) — FIX-4: Deferred Phase-4/5 (Story 115.S2.O4)

Create ONLY the tasks for phases that execute up-front and in immediate sequence
(Phase 1 → 2 → 3). **Phase 4 and Phase 5 tasks are NOT created here.**

```
TaskCreate(title: "Phase 1: Validate Story Draft (@po)", description: "PO validates story completeness, ACs, executor assignment, deploy_type")
TaskCreate(title: "Phase 2: Develop Story (@{executor})", description: "Executor implements all tasks, writes tests, updates File List")
TaskCreate(title: "Phase 3: Review + QG Loop (@{quality_gate})", description: "QG reviews code, CodeRabbit self-healing, AC validation. Loop with executor if FAIL.")
```

**FIX-4 — Defer Phase-4/5 TaskCreate (NON-NEGOTIABLE):**
The Phase 4 (Deploy+Verify) and Phase 5 (Close) tracking tasks are created
**immediately before the phase is dispatched**, inside the Phase 4 / Phase 5
sections — never here in the init block. Rationale: a Phase-5 task created
up-front is a *stale task channel* (audit event E5) that can survive a
runtime task-list wipe and induce a premature close even though the
sequence-locked pipeline never legitimately reached Phase 5. Deferring
TaskCreate to the dispatch boundary eliminates that stale channel entirely.

---

## Phase 0c: Auto-Spawn Worktree (WL-1 — Story 115.S2.O7; nesting-fix Story 115A.S7)

**Execute AFTER Phase 0b (team + tasks created) and BEFORE Phase 1.**
**Provisions a dedicated worktree for this story off `origin/main` (fresh fetch).**
**Skip if already running inside ANY pre-provisioned worktree** — detection is primarily structural (cwd check, Invariant 2), with story-scoped ACK as secondary.

### 0c.1 — Nesting Detection Guard (Invariant 2, structural — Story 115A.S7 fix)

The guard checks the cwd structurally FIRST (Invariant 2 of `.claude/rules/worktree-isolation.md`), then falls back to the story-scoped ACK file. This eliminates the 4 defects identified by Codex deep-dive (path mismatch, naming mismatch, logical race, indirect Invariant-2 check).

**Constants:**
- `WT_PROVISIONED_TTL_HOURS = 24` — Story 115A.S7 Round 1 FIX-3. Any `wt_provisioned: true` ACK older than 24 hours is treated as **expired**; the guard falls through to Phase 0c.2 and creates a fresh worktree. This prevents stale ACK files left over from prior aborted runs from incorrectly suppressing worktree creation for a brand-new story session. The cwd-structural check (Tier 1) is **immune** to staleness because it inspects the live cwd state, not a persisted file.

```
# Primary (structural — Invariant 2): cwd inside any worktree → SKIP, regardless of ACK presence
IF cwd contains "/.claude/worktrees/" OR cwd contains "\\.claude\\worktrees\\":
  LOG: "[WL-1] Invariant 2: already inside pre-provisioned worktree at {cwd}. Skipping Phase 0c (nesting prevention)."
  # Emit auto-ACK so downstream phases (and any sibling tools) can detect dispatch
  mkdir -p .sdc-ack/{story_id}
  Write(
    path: ".sdc-ack/{story_id}/dispatch.ack",
    content: "phase: \"dispatch\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: passed\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\nwt_provisioned: true\nprovisioned_by: \"external\"\nevent_schema_version: \"1.0\"\n"
  )
  → Proceed to Phase 1 (no-op in pre-provisioned context)

# Secondary (story-scoped ACK — wave-execute pre-provisioning legacy path)
ELSE IF exists(".sdc-ack/{story_id}/dispatch.ack") AND file contains "wt_provisioned: true":
  # FIX-3: TTL guard — stale ACK must not suppress fresh worktree creation
  # Round 2 Codex finding: clock skew (future timestamp → negative age) was silently
  # treated as "fresh". Now: negative age (future timestamp) is treated as expired.
  ack_timestamp = parse timestamp field from .sdc-ack/{story_id}/dispatch.ack
  age_hours_raw = (now - ack_timestamp) / 3600
  IF age_hours_raw < 0:
    LOG: "[WL-1 FIX-3 CLOCK-SKEW] Scoped ACK timestamp is in the future (clock skew: {age_hours_raw}h). Treating as expired — falling through to Phase 0c.2."
    → Proceed to 0c.2 (create-new path, fresh worktree)
  age_hours = age_hours_raw
  IF age_hours > WT_PROVISIONED_TTL_HOURS:
    LOG: "[WL-1 FIX-3] Scoped ACK is stale (age {age_hours}h > TTL {WT_PROVISIONED_TTL_HOURS}h). Treating as expired — falling through to Phase 0c.2."
    → Proceed to 0c.2 (create-new path, fresh worktree)
  ELSE:
    LOG: "[WL-1] Worktree pre-provisioned by wave-execute (story-scoped ACK present, age {age_hours}h within TTL). Skipping Phase 0c."
    → Proceed to Phase 1 (no-op in wave-execute context)

# Tertiary (legacy non-scoped ACK — deprecated, kept for backward-compat)
ELSE IF exists(".sdc-ack/dispatch.ack") AND file contains "wt_provisioned: true":
  # FIX-3: TTL guard applies to legacy path too (Round 2: clock-skew guard added)
  ack_timestamp = parse timestamp field from .sdc-ack/dispatch.ack
  age_hours_raw = (now - ack_timestamp) / 3600
  IF age_hours_raw < 0:
    LOG: "[WL-1 FIX-3 CLOCK-SKEW DEPRECATED] Legacy ACK timestamp is in the future (clock skew: {age_hours_raw}h). Treating as expired — falling through to Phase 0c.2."
    → Proceed to 0c.2
  age_hours = age_hours_raw
  IF age_hours > WT_PROVISIONED_TTL_HOURS:
    LOG: "[WL-1 FIX-3 DEPRECATED] Legacy non-scoped ACK is stale (age {age_hours}h). Falling through to Phase 0c.2."
    → Proceed to 0c.2
  ELSE:
    LOG: "[WL-1 DEPRECATED] Non-scoped dispatch.ack found at .sdc-ack/dispatch.ack. Path is deprecated — wave-execute should write .sdc-ack/{story_id}/dispatch.ack. Skipping Phase 0c for backward-compat."
    → Proceed to Phase 1

ELSE:
  → Proceed to 0c.2 (standalone full-sdc path, will create wt-{story_id} below)
```

**Why structural (cwd) FIRST:**

The previous version only consulted `.sdc-ack/dispatch.ack`, which produced 4 defects observed in production (Wave W7/W1, 2026-05-23):

| # | Defect | Effect |
|---|--------|--------|
| 1 | Path mismatch | guard read `.sdc-ack/dispatch.ack` but writer wrote `.sdc-ack/{story_id}/dispatch.ack` → guard never matched → infinite re-creation |
| 2 | Naming mismatch | fallback expected `wt-{story_id}` but wave-launch.js created `story-{storyId}` → idempotency check missed |
| 3 | Logical race (not temporal) | child decided routing BEFORE wave-launch wrote ACK → ACK presence couldn't be relied upon |
| 4 | Indirect Invariant-2 check | ACK presence is a proxy for "already provisioned"; the real invariant is "cwd inside `.claude/worktrees/`" → check the invariant directly |

The cwd check fixes #3 and #4 at the source (structural detection, no ACK needed) and makes #1/#2 harmless (we no longer depend on path/naming agreement). The ACK fallbacks remain for explicit wave-execute hand-off compatibility.

**Canonical reference:** Roundtable RT-20260523-WAVEv9 (5 agents, 7.34/10, APROVA_WITH_CONDITIONS) — `docs/architecture/roundtable-wave-execute-v9-20260523.md`.

### 0c.2 — Fetch and idempotency check

```bash
git fetch origin

# Idempotent: if worktree wt-{story_id} already exists, re-use it
wt_path=".claude/worktrees/wt-{story_id}"
branch="feat/{story_id}-{short_title}"
# short_title = first 3 kebab-case words of story title, max 40 chars total
```

IF `git worktree list` output includes `{wt_path}`:
  LOG: `[WL-1] Worktree {wt_path} already exists — re-using (idempotent).`
  → Skip to 0c.4

ELSE:
  # Story file availability check (Story 115G.W1.3 — fallback contract)
  IF `git show origin/<default_branch>:{story_path}` exits 0:
    # origin has story → normal path
    → Proceed to 0c.3 (existing behavior, UNCHANGED)

  ELSE IF `git show HEAD:{story_path}` exits 0:
    # local HEAD has story but origin does not → FALLBACK (local-commits-ahead scenario)
    local_head_sha = `git rev-parse HEAD`
    LOG (stderr + stdout — machine-parseable):
      `[full-sdc] WARN provisioned_by=local-ahead story={story_id} local_sha={local_head_sha} note="story not on origin; baseRef still fresh"`
    LOG (human-readable):
      `[full-sdc Phase 0c.2] FALLBACK: story {story_id} not on origin/<branch>; using local HEAD {local_head_sha}. Invariant 3 NOT violated — baseRef remains fresh from origin/<branch>; story file overlay only. Push story to origin before Phase 5 to clear annotation.`
    SET fallback_local_ahead = true
    SET fallback_local_sha = local_head_sha
    → Proceed to 0c.3 (UNCHANGED — `git worktree add` uses origin/main, Invariant 3 preserved)
    AFTER 0c.3 completes successfully:
      # Overlay story file from local HEAD onto the fresh worktree
      Bash: `git show HEAD:{story_path} > {wt_path}/{story_path}`
      LOG: `[WL-1 FALLBACK] Story file overlay written: {wt_path}/{story_path} from local HEAD {local_head_sha}`

  ELSE:
    # Neither origin nor local HEAD has story → HARD ERROR (Mandamento 8)
    LOG LOUD (stderr): `[full-sdc Phase 0c.2] HARD ERROR: story {story_id} not found on origin/<branch> nor local HEAD <sha>. Cannot proceed. Push the story file to origin or ensure it exists locally before invoking /full-sdc.`
    HALT with exit non-zero

### 0c.3 — Create worktree

```bash
git worktree add ".claude/worktrees/wt-{story_id}" -b "feat/{story_id}-{short_title}" origin/main
```

LOG: `[WL-1] Worktree created: .claude/worktrees/wt-{story_id} on branch feat/{story_id}-{short_title}`

**On failure (e.g., name collision or dirty state):**
- LOG LOUD: `[WL-1 FAIL] git worktree add failed: {error}`
- HALT. Notify user. Do NOT proceed to Phase 1 without a valid worktree.

### 0c.4 — Check TK-SDC-MAX-PARALLEL-WORKTREES

Count entries with `state: "active"` in `.aiox/worktrees/registry.json` (if file exists):

IF count >= `TK-SDC-MAX-PARALLEL-WORKTREES` (default: 3):
  LOG LOUD: `[WL-1 WARNING] MAX_PARALLEL_WORKTREES limit reached ({TK-SDC-MAX-PARALLEL-WORKTREES}). Queuing story {story_id} — free a slot or increase the token to proceed.`
  HALT (do not proceed). User must resolve.

### 0c.5 — Register in worktree registry (O6b write primitive)

```
READ .aiox/worktrees/registry.json
  (if absent: initialize with {"schema_version": "worktree-registry-v1", "worktrees": [], "last_updated": "<ISO8601>"})
UPSERT entry by story_id:
  story_id: "{story_id}"
  branch: "feat/{story_id}-{short_title}"
  wt_path: ".claude/worktrees/wt-{story_id}"
  state: "active"
  halt_reason: null
  created_at: "<current ISO8601>"
  last_seen: "<current ISO8601>"
  age_days: 0
SET last_updated = <current ISO8601>
WRITE back JSON
```

### 0c.5b — Write dispatch.ack (Auto-ACK Protocol — Story 115A.8b)

```bash
mkdir -p .sdc-ack/{story_id}
commit_sha=$(git rev-parse HEAD)
```

```
IF fallback_local_ahead = true:
  Write(
    path: ".sdc-ack/{story_id}/dispatch.ack",
    content: "phase: \"dispatch\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<commit_sha>\"\nstatus: passed\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\nwt_provisioned: true\nprovisioned_by: \"local-ahead\"\nlocal_head_sha: \"{fallback_local_sha}\"\norigin_lacks_story: true\nevent_schema_version: \"1.0\"\n"
  )
ELSE:
  Write(
    path: ".sdc-ack/{story_id}/dispatch.ack",
    content: "phase: \"dispatch\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<commit_sha>\"\nstatus: passed\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\nwt_provisioned: true\nprovisioned_by: \"self\"\nevent_schema_version: \"1.0\"\n"
  )
```

LOG: `[AUTO-ACK] dispatch.ack written for story {story_id}`

### 0c.6 — Write Phase 0c checkpoint

```json
// .aiox/checkpoints/{story_id}/phase-0c.json
{
  "story_id": "{story_id}",
  "phase": "0c",
  "phase_status": "completed",
  "wt_path": ".claude/worktrees/wt-{story_id}",
  "branch": "feat/{story_id}-{short_title}",
  "timestamp_start": "<ISO8601>",
  "timestamp_end": "<ISO8601>",
  "checkpoint_schema_version": "1.0",
  "expected_tasks": []
}
```

LOG: `[WL-1] Phase 0c complete. Worktree: .claude/worktrees/wt-{story_id} | Branch: feat/{story_id}-{short_title}`

---

## Phase 1: Validate Story Draft

### Spawn PO Teammate — Phase-1-ONLY spawn (FIX-1a, Story 115.S2.O4)

The PO teammate is spawned here for **Phase 1 (validate-story-draft) ONLY**.
The spawn prompt MUST scope the agent to validate-story-draft and **MUST NOT**
pre-announce, hint at, or reference any later phase (review, close), any
`status=Done` transition, or "Phase 5".

**Why de-pre-announced (audit-confirmed, Story 115.S2.O4):** Pre-announcing all
3 phases at spawn time made a premature close the *path of least resistance*
once coordination state degraded — the agent already "knew" close was coming and
could skip ahead on a stale signal. Each later phase is communicated to the PO
**only after** the team-lead has verified the prior phase's artifacts on disk
(see "Sequence Lock" below). The PO persists (idle) and is re-commanded later
via SendMessage; it does not need — and must not be given — forward knowledge of
phases it has not been authorized to start.

```
Agent(
  subagent_type: "po",       # harness loads .claude/agents/po.md as persona
  name: "po",
  team_name: "sdc-{story_id}",
  model: "sonnet",
  description: "SDC PO: validate-story-draft (Phase 1)",
  prompt: "[ACTION REQUIRED: validate-story-draft]

    You are spawned for Phase 1 of the Full SDC pipeline of Story {story_id}.
    Your task this turn is exactly one skill protocol: validate-story-draft.
    Do not anticipate or act on any later phase — the team-lead is the sole
    authorizer of every phase transition and will send a separate, explicitly
    action-prefixed message if and when a further phase is authorized.

    ---

    CURRENT TASK — Phase 1: validate-story-draft

    Read .claude/skills/validate-story-draft/SKILL.md and execute the
    COMPLETE protocol for:

    Story: {story_path}

    Follow ALL phases (Phase 0 Epic Context, Phase 0.5 D10, Steps 1-10,
    Report, Auto-Fix). Do NOT skip steps.

    When done, SendMessage to 'team-lead' with:
    - Verdict: GO | GO with Auto-Fix | GO Condicional | NO-GO
    - Score: X/10
    - Summary of findings and auto-fixes applied
    - Any conditions the executor must address
    - **Artifacts produced** (list paths created/modified — used by team-lead for verification gate)

    Then STOP and wait. Do not request, propose, or begin any further phase."
)
```

### Wait for PO Result

PO sends verdict via SendMessage. Team-lead processes:

- **GO / GO with Auto-Fix:** TaskUpdate(task1, completed). Write `validate.ack` (status: passed). Proceed to Phase 2.
- **GO Condicional:** TaskUpdate(task1, completed). Write `validate.ack` (status: passed). Note conditions for executor. Proceed.
- **NO-GO:** TaskUpdate(task1, completed). Write `validate.ack` (status: failed). **HALT pipeline.** Show NO-GO reasons to user. Ask user to fix story and retry.

**validate.ack write (Auto-ACK Protocol):**
```
Write(
  path: ".sdc-ack/{story_id}/validate.ack",
  content: "phase: \"validate\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: <passed|failed>\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

---

## Phase 2: Develop Story

### Spawn Executor Teammate

```
Agent(
  subagent_type: "{executor_id}",   # harness loads .claude/agents/{executor_id}.md
  name: "{executor_id}",
  team_name: "sdc-{story_id}",
  model: "sonnet",
  description: "SDC Executor: develop story",
  prompt: "[ACTION REQUIRED: develop-story]

    You are spawned for Phase 2 of the Full SDC pipeline. You will execute
    UP TO 2 distinct skills across this pipeline:

      Phase 2 (NOW): develop-story
      Phase 3 QG loop (if FAIL): apply-qa-fixes — arrives as SendMessage with
        prefix `[ACTION REQUIRED: apply-qa-fixes]`

    ---

    CURRENT TASK — Phase 2: develop-story

    Read .claude/skills/develop-story/SKILL.md and execute the COMPLETE
    development protocol for:

    Story: {story_path}
    Mode: {mode}

    {IF conditions from PO validation:}
    PO Conditions to address (from Phase 1):
    {conditions_list}
    {ENDIF}

    Follow ALL phases: Constitutional Gates, Code Intelligence, Implementation,
    Tests, CodeRabbit Self-Healing, DOD Checklist.

    When done, SendMessage to 'team-lead' with:
    - Status: completed | halted | failed
    - Tasks completed: N/N
    - Tests passing: yes/no
    - CodeRabbit iterations: N
    - **Artifacts produced** (list paths created/modified — used by verification gate)
    - Any blockers encountered"
)
```

### Wait for Executor Result

- **completed:** TaskUpdate(task2, completed). Write `develop.ack` (status: passed). Proceed to Phase 3.
- **halted:** Show blocker to user. Wait for user input. SendMessage to executor with guidance. Resume.
- **failed:** TaskUpdate(task2, completed with note). Write `develop.ack` (status: failed). **HALT pipeline.** Ask user.

**develop.ack write (Auto-ACK Protocol):**
```
Write(
  path: ".sdc-ack/{story_id}/develop.ack",
  content: "phase: \"develop\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: <passed|failed>\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

---

## Phase 3: Review + QG Loop

### Spawn or Reuse QG Teammate

**Reuse rule:** if `quality_gate == "@po"` AND PO was already spawned in Phase 1, **reuse the same teammate via SendMessage** (do NOT spawn a duplicate). Otherwise, spawn a new teammate.

**Branch A — Reuse PO (quality_gate=@po):**

```
SendMessage(
  to: "po",
  summary: "Phase 3 review",
  message: "[ACTION REQUIRED: review-story]

    Phase 1 validate completed. Phase 2 develop completed.
    NOW you switch to Quality Gate role and execute review-story.

    Read .claude/skills/review-story/SKILL.md and execute the COMPLETE
    review protocol for:

    Story: {story_path}

    Implementation by @{executor_id} produced these artifacts:
    {artifacts_from_phase_2}

    Follow ALL phases: CodeRabbit Self-Healing, Code Intelligence, Risk Assessment,
    Comprehensive Analysis, Deploy Readiness, Active Refactoring, Standards,
    AC Validation, Gate File Creation.

    When done, SendMessage to 'team-lead' with:
    - Gate: PASS | CONCERNS | FAIL | WAIVED
    - Quality Score: N/100
    - Top issues (if any)
    - **Gate file path** (mandatory — used by verification gate)
    - **Artifacts produced/modified** (list paths)"
)
```

**Branch B — Spawn new QG (quality_gate != @po):**

```
Agent(
  subagent_type: "{qg_id}",      # harness loads .claude/agents/{qg_id}.md
  name: "{qg_id}",
  team_name: "sdc-{story_id}",
  model: "sonnet",
  description: "SDC QG: review story",
  prompt: "[ACTION REQUIRED: review-story]

    You are spawned for Phase 3 of the Full SDC pipeline. You may also be
    asked to re-review in QG loop iterations (each arrives as a SendMessage
    with `[ACTION REQUIRED: review-story]` prefix — treat each as new task).

    ---

    CURRENT TASK — Phase 3: review-story

    Read .claude/skills/review-story/SKILL.md and execute the COMPLETE
    review protocol for:

    Story: {story_path}

    Implementation by @{executor_id} produced these artifacts:
    {artifacts_from_phase_2}

    Follow ALL phases: CodeRabbit Self-Healing, Code Intelligence, Risk Assessment,
    Comprehensive Analysis, Deploy Readiness, Active Refactoring, Standards,
    AC Validation, Gate File Creation.

    When done, SendMessage to 'team-lead' with:
    - Gate: PASS | CONCERNS | FAIL | WAIVED
    - Quality Score: N/100
    - Top issues (if any)
    - **Gate file path** (mandatory — used by verification gate)
    - **Artifacts produced/modified** (list paths)"
)
```

### Process QG Result

**PASS or WAIVED:**
- TaskUpdate(task3, completed). Proceed to Phase 4.

**CONCERNS:**
- Show concerns to user. Ask: "Accept concerns and proceed? [y/n]"
- If yes → TaskUpdate(task3, completed). Proceed.
- If no → enter QG Loop (treat as FAIL).

**FAIL → QG Loop:**

```
qg_iteration = 1
max_qg_iterations = 3

WHILE qg_iteration <= max_qg_iterations AND gate == FAIL:

  # 1. Send fix request to Executor (STILL ALIVE from Phase 2)
  SendMessage(
    to: "{executor_id}",
    summary: "QG Fix Round {qg_iteration}",
    message: "[ACTION REQUIRED: apply-qa-fixes]

      Quality gate Round {qg_iteration} returned FAIL. Fix these issues:

      {top_issues from QG}

      Read the gate file at {gate_path} for full details.
      Read the QA Results section in the story file.

      Read .claude/skills/apply-qa-fixes/SKILL.md and execute the protocol:
      - Fix each issue
      - Run tests to confirm no regressions
      - Update story File List if new files created

      When done, SendMessage to 'team-lead' with:
      - Fixes applied: list
      - Tests passing: yes/no
      - **Artifacts modified** (paths — used by verification gate)"
  )

  # 2. Wait for Executor fix confirmation

  # 3. Send re-review request to QG (STILL ALIVE from Phase 3)
  SendMessage(
    to: "{qg_id}",
    summary: "Re-review Round {qg_iteration}",
    message: "[ACTION REQUIRED: review-story]

      DO NOT report on prior gate decisions — this is a NEW re-review task.

      Executor applied fixes for Round {qg_iteration}. Re-execute the
      review-story protocol for:
      Story: {story_path}

      Focus on the previously-failed items but do a full re-review.

      SendMessage to 'team-lead' with:
      - Updated gate verdict (PASS | CONCERNS | FAIL | WAIVED)
      - Quality Score
      - Gate file path (if updated)
      - Top remaining issues (if any)"
  )

  # 4. Wait for QG re-verdict
  qg_iteration++

END WHILE
```

**After loop:**
- If PASS → Proceed to **Post-Phase 3 Verification Gate L2** (below). If L2 PASS → TaskUpdate(task3, completed). Write `review.ack` (status: passed). Proceed.
- If still FAIL after 3 rounds → Write `review.ack` (status: failed). **ESCALATE to user.** Show all 3 rounds of issues. HALT.

**review.ack write (Auto-ACK Protocol):**
```
Write(
  path: ".sdc-ack/{story_id}/review.ack",
  content: "phase: \"review\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: <passed|failed>\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

### Post-Phase 3 Verification Gate — Layer 2: Status Diff-Check (NON-NEGOTIABLE — Story 115.S2.O11, AC-5)

> **Defense-in-depth Layer 2** (L1 = Role Boundary in-skill; **L2 = this gate**; L3 = close-story CHK-0; L4 = registry-governance mapping #16)
>
> **Bootstrapping note:** `.claude/skills/full-sdc/SKILL.md` is self-modified by AC-5 of Story 115.S2.O11. NÃO invocar `/full-sdc` recursivamente para desenvolver O11. Verificar on-disk diretamente. Precedente: O6b CG-8.

Após Phase 3 (review-story) reportar conclusão, e **ANTES** de marcar task3 completed ou avançar para Phase 4 ou 5, o team-lead DEVE executar este status diff-check:

```
1. Ler o frontmatter da story file on disk: Read {story_path}
   Extrair o valor do campo `status`.

2. Verificar se `status` foi mutado por review-story:
   IF status == "Done" OR status == "Ready for Review":
     # review-story NUNCA deve setar status — apenas close-story pode
     EMIT integrity-violation event (ver §Integrity Violation acima):
       subtype: "review-story-status-mutation"
       detected_status: {value}
       detected_at: "phase 3 post-phase L2 gate"
     HALT — NÃO prosseguir para Phase 4 ou 5.
     Surface ao usuário: "L2 Gate FAIL — review-story mutou `status` para '{value}'.
     Este é o defect F2/E3 premature-close. Revert manualmente o campo `status`
     para o valor pré-Phase-3, depois reiniciar a partir de Phase 3."
   ELSE:
     # status não foi mutado — L2 PASS
     Continuar para verificação normal de artefatos (gate file, QA Results).
```

**Expected status values após Phase 3 (L2 PASS):**
- `InProgress` — correto (dev ainda não fez push; close ainda não executou)
- `InReview` — correto (equivalente; PR criado)
- `Ready` — aceitável (edge case de re-review)
- Qualquer valor que **não seja `Done`** — L2 PASS

**`status: Done` detectado em Phase 3 = L2 FAIL imediato.** Sem override, sem waiver.

---

## Phase 4: Deploy + Verify (CONDITIONAL)

**IF `deploy_type == "none"` or absent:** Skip Phase 4 entirely. Write `deploy.ack` (status: skipped). **No Phase-4 task is created** (FIX-4 — deferred TaskCreate; nothing to skip-mark). Proceed to Phase 5.

**deploy.ack write when skipped (Auto-ACK Protocol):**
```
Write(
  path: ".sdc-ack/{story_id}/deploy.ack",
  content: "phase: \"deploy\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: skipped\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

**IF `deploy_type != "none"`:**

**FIX-4 — Deferred TaskCreate (Story 115.S2.O4):** create the Phase-4 tracking
task NOW, immediately before dispatching the deploy teammate — not in the init block.

```
TaskCreate(title: "Phase 4: Deploy + Verify (@{deploy_agent})", description: "Deploy to {deploy_type} target, verify E2E.")
```

### Spawn Deploy Teammate

```
Agent(
  subagent_type: "{deploy_agent_id}",   # harness loads agent persona
  name: "{deploy_agent_id}",
  team_name: "sdc-{story_id}",
  model: "sonnet",
  description: "SDC Deploy: {deploy_type}",
  prompt: "[ACTION REQUIRED: deploy-story → verify-deploy]

    You are spawned for Phase 4 of the Full SDC pipeline. You will execute
    TWO skill protocols sequentially in this turn:

    ---

    SKILL 1 — deploy-story

    Read .claude/skills/deploy-story/SKILL.md and execute the deploy protocol for:
    Story: {story_path}
    deploy_type: {deploy_type}

    ---

    SKILL 2 — verify-deploy (only if SKILL 1 succeeds)

    Read .claude/skills/verify-deploy/SKILL.md and execute the verify protocol
    for the same story.

    ---

    When BOTH skills are complete, SendMessage to 'team-lead' with:
    - Deploy status: success | failed
    - Verify status: PASS | FAIL | PARTIAL
    - e2e_verification summary
    - **Artifacts produced** (e2e_verification section in story, deploy logs path)
    - Any issues"
)
```

### Process Deploy Result

- **Deploy success + Verify PASS:** TaskUpdate(task4, completed). Write `deploy.ack` (status: passed). Proceed to Phase 5.
- **Deploy failed:** Write `deploy.ack` (status: failed). HALT. Show error. Ask user.
- **Verify FAIL/PARTIAL:** Write `deploy.ack` (status: failed). HALT. Show failing checks. Ask user to resolve and retry.

**deploy.ack write when deployed (Auto-ACK Protocol):**
```
Write(
  path: ".sdc-ack/{story_id}/deploy.ack",
  content: "phase: \"deploy\"\ntimestamp: \"<ISO-8601>\"\ncommit_sha: \"<git rev-parse HEAD>\"\nstatus: <passed|failed>\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

---

## Phase 5: Close Story

**Sequence Lock precondition (NON-NEGOTIABLE):** Phase 5 may begin ONLY after
the team-lead has verified on disk the artifacts of Phase 3 (and Phase 4 if
`deploy_type != none`) per the Post-Phase Verification Gate. If those artifacts
are unverified, missing, or empty, the team-lead MUST NOT enter Phase 5.

### 5.0 — Deferred Phase-5 TaskCreate (FIX-4, Story 115.S2.O4)

Create the Phase-5 tracking task NOW — immediately before writing the dispatch
lockfile and dispatching close — never in the init block.

```
TaskCreate(title: "Phase 5: Close Story (@po)", description: "PO closure: CHK-0/8/9/10 gates, status→Done, Epic update")
```

### 5.1 — Write the Phase-5 dispatch lockfile (orchestrator-exclusive — FIX-1c / D-RT-1)

Before dispatching close-story, the team-lead (full-sdc Phase-5 orchestrator)
MUST write a dedicated dispatch lockfile. This is the **on-disk authorization
artifact** that close-story's CHK-0 reads to confirm it was dispatched by the
orchestrator (not invoked out-of-sequence on a stale/fabricated signal — the
E3 catastrophic-close failure mode, 115.S2.O2).

```
ts = <ISO-8601 timestamp, e.g. 2026-05-16T14:32:07Z>
Write(
  path:    ".aiox/dispatch/{story_id}-phase5-{ts}.lock",
  content: "story_id: {story_id}\nphase: 5\ndispatched_by: full-sdc-team-lead\nts: {ts}\n"
)
```

**Artifact contract — declared orchestrator-exclusive:** `.aiox/dispatch/*.lock`
files are written **exclusively** by this Phase-5 orchestrator step. No other
skill, agent, or phase may create them.

**Barrier scope (honest — D-RT-1, NON-NEGOTIABLE to state):** This is a
**protocol barrier, not a cryptographic control**. A subagent holding Write/Edit
tools can technically forge this lockfile; the lock relies on the
orchestrator-exclusive convention plus the Post-Phase Verification Gate
`integrity-violation` HALT, not on unforgeable proof. True cryptographic
hardening is deferred to **Story 115.S2.O6** (durable orchestration state layer
— existing stub, Draft). This limit is stated here and in
`.claude/skills/close-story/SKILL.md` CHK-0 deliberately.

### 5.2 — Dispatch close to the PO teammate

PO was spawned in Phase 1 (Phase-1-only) and is **still alive** (idle). The
message below is the team-lead's **Sequence-Lock authorization** to begin
Phase 5 — issued ONLY after 5.0 + 5.1 and the Phase 3/4 on-disk verification.
It is not a "parse this as a new task" hint; it is the gated dispatch token.

```
SendMessage(
  to: "po",
  summary: "Phase 5 close",
  message: "[ACTION REQUIRED: close-story]

    This message is the team-lead's Sequence-Lock authorization to begin
    Phase 5 (close-story). It was issued only after on-disk verification of
    the prior phases.

    Read .claude/skills/close-story/SKILL.md and execute the COMPLETE
    closure protocol for:

    Story: {story_path}

    Concrete actions you MUST perform (per the SKILL.md):
    - Run CHK-0 FIRST: read the orchestrator dispatch lockfile at
      .aiox/dispatch/{story_id}-phase5-*.lock — it exists because the
      team-lead wrote it in step 5.1 before this dispatch. CHK-0 validates
      story_id + timestamp freshness. (Absent lockfile → human-direct path.)
    - Verify CHK-8: Deploy verification gate (deploy_type: {deploy_type})
      → if {deploy_type}=='none': CHK-8 is SKIP (no e2e_verification required)
      → else: CHK-8 must find a PASS e2e_verification record
    - Verify CHK-9: Registry governance (advisory)
    - Verify CHK-10: IDS post-check (advisory)
    - **Mutate story frontmatter: status → Done** (via Edit tool)
    - **Update Epic file** ({epic_path}) — mark this story as completed
      in Development Log section
    - **Create learning log** at:
      .aiox/learning/logs/close-story/close-story-{story_id}-{YYYYMMDD}-{HHmmss}.yaml
      (this is REQUIRED by close-story SKILL.md — do not skip)
    - Append entry to story Change Log

    When done, SendMessage to 'team-lead' with:
    - Closure status: completed | blocked
    - CHK results (CHK-8, CHK-9, CHK-10 each with verdict)
    - Epic progress (X/Y stories Done)
    - Next story recommendation
    - **Artifacts produced** (list paths created/modified, INCLUDING the
      learning log path — used by verification gate)"
)
```

### Process Close Result

- **completed:** TaskUpdate(task5, completed). Write `phase-5.ack` AND `sdc-complete.ack` (status: passed). Proceed to **Phase 5b (merge-back)**.
- **blocked:** Write `phase-5.ack` (status: failed). Show CHK block reason. Ask user. (Most likely CHK-8 if deploy verify failed.)

**phase-5.ack + sdc-complete.ack write (Auto-ACK Protocol):**
```
commit_sha=$(git rev-parse HEAD)
ts=<ISO-8601>

Write(
  path: ".sdc-ack/{story_id}/phase-5.ack",
  content: "phase: \"phase-5\"\ntimestamp: \"{ts}\"\ncommit_sha: \"{commit_sha}\"\nstatus: passed\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)

Write(
  path: ".sdc-ack/{story_id}/sdc-complete.ack",
  content: "phase: \"sdc-complete\"\ntimestamp: \"{ts}\"\ncommit_sha: \"{commit_sha}\"\nstatus: passed\nstory_id: \"{story_id}\"\nskill: \"full-sdc\"\n"
)
```

LOG: `[AUTO-ACK] phase-5.ack + sdc-complete.ack written for story {story_id} — wave-execute orquestrador pode detectar conclusão via polling`

---

## Phase 5 §merge-back (Phase 5b) — Auto-Merge-Back + WL-3 Teardown (WL-2/WL-3 — Story 115.S2.O7)

**Execute AFTER Phase 5 (close-story) completes with status `completed`.**
**Skip if Phase 0c was skipped (wave-execute context — `wt_provisioned: true`). In that case, wave-execute Stage 6 HANDOFF-TEARDOWN handles merge-back.**
**O6b AC-5 teardown ordering contract is the sole ordering owner. WL-3 is the executor of Step 3 in that contract.**

### 5b.1 — Check if standalone context (skip guard — story-scoped, Story 115A.S7 fix)

The skip guard mirrors Phase 0c.1: structural cwd check primary, story-scoped ACK secondary, legacy non-scoped ACK tertiary. Uses the same `WT_PROVISIONED_TTL_HOURS = 24` constant for ACK staleness (FIX-3).

```
# Primary (structural): if we were spawned into an external worktree (cwd inside .claude/worktrees/),
# merge-back is owned by the spawning orchestrator (wave-execute Stage 6 OR human external)
IF cwd contains "/.claude/worktrees/" OR cwd contains "\\.claude\\worktrees\\":
  # In this context, full-sdc did NOT create the worktree (Phase 0c.1 SKIPPED). Therefore
  # full-sdc MUST NOT tear it down. The spawning context owns lifecycle.
  LOG: "[WL-2] Pre-provisioned worktree context detected (cwd: {cwd}). Merge-back/teardown delegated to spawning orchestrator. Skipping Phase 5b."
  → Proceed to Phase 6 (Shutdown)

# Secondary (story-scoped ACK)
ELSE IF exists(".sdc-ack/{story_id}/dispatch.ack") AND file contains "wt_provisioned: true":
  # FIX-3: TTL guard — stale ACK is treated as expired here too. If expired, we proceed
  # with merge-back (assume the worktree we are about to tear down is ours, not pre-provisioned).
  # Round 2: clock-skew guard added (future timestamp → treated as expired).
  ack_timestamp = parse timestamp field from .sdc-ack/{story_id}/dispatch.ack
  age_hours_raw = (now - ack_timestamp) / 3600
  IF age_hours_raw < 0:
    LOG: "[WL-2 FIX-3 CLOCK-SKEW] Scoped ACK timestamp in future (clock skew: {age_hours_raw}h). Falling through to merge-back."
    → Continue to 5b.2
  age_hours = age_hours_raw
  IF age_hours > WT_PROVISIONED_TTL_HOURS:
    LOG: "[WL-2 FIX-3] Scoped ACK is stale (age {age_hours}h). Falling through to merge-back (assume not pre-provisioned)."
    → Continue to 5b.2
  ELSE:
    LOG: "[WL-2] wave-execute context (story-scoped ACK, age {age_hours}h within TTL) — merge-back delegated to Stage 6 HANDOFF-TEARDOWN. Skipping Phase 5b."
    → Proceed to Phase 6 (Shutdown)

# Tertiary (legacy non-scoped — deprecated)
ELSE IF exists(".sdc-ack/dispatch.ack") AND file contains "wt_provisioned: true":
  # FIX-3: TTL guard for legacy path (Round 2: clock-skew guard added)
  ack_timestamp = parse timestamp field from .sdc-ack/dispatch.ack
  age_hours_raw = (now - ack_timestamp) / 3600
  IF age_hours_raw < 0:
    LOG: "[WL-2 FIX-3 CLOCK-SKEW DEPRECATED] Legacy ACK in future (clock skew). Falling through to merge-back."
    → Continue to 5b.2
  age_hours = age_hours_raw
  IF age_hours > WT_PROVISIONED_TTL_HOURS:
    LOG: "[WL-2 FIX-3 DEPRECATED] Legacy ACK stale — falling through to merge-back."
    → Continue to 5b.2
  ELSE:
    LOG: "[WL-2 DEPRECATED] Non-scoped dispatch.ack — skipping merge-back for backward-compat."
    → Proceed to Phase 6 (Shutdown)
```

### 5b.2 — WL-2: Prepare merge-back (git fetch + diff + rebase/ff local)

```bash
# Step 1: fresh fetch
git fetch origin

# Step 2: diff vs origin/main — check for conflicts
git diff "feat/{story_id}-{short_title}..origin/main" --name-only
```

IF diff is non-empty (changes in origin/main not in branch):
  ```bash
  # Step 3: rebase/ff onto origin/main (TK-SDC-MERGE-BACK-STRATEGY = "rebase-ff" default)
  git rebase origin/main
  ```
  IF rebase fails (conflict):
    LOG LOUD: `[WL-2 CONFLICT] Rebase failed on: {conflicting_files}. Emitting handoff to @devops with conflict details.`
    SET merge_back_has_conflict = true
    (continue to 5b.3 — @devops resolves conflict)
  ELSE:
    SET merge_back_has_conflict = false

ELSE (no diff, branch already up-to-date):
  LOG: `[WL-2] Branch feat/{story_id}-{short_title} is up-to-date with origin/main. No rebase needed.`
  SET merge_back_has_conflict = false

### 5b.3 — WL-2: Emit structured handoff to @devops

**@devops has EXCLUSIVE push authority (agent-authority.md). WL-2 PREPARES the merge-back; @devops materializes it.**

```yaml
# .aiox/handoffs/handoff-full-sdc-{story_id}-merge-back-{date}.yaml
handoff:
  from: "full-sdc (Phase 5b)"
  to: "@devops"
  date: "{YYYY-MM-DD}"
  story_id: "{story_id}"
  scope: intra_bu
  lifecycle_state: created

context:
  branch: "feat/{story_id}-{short_title}"
  wt_path: ".claude/worktrees/wt-{story_id}"
  merge_strategy: "{TK-SDC-MERGE-BACK-STRATEGY}"   # default: rebase-ff
  has_conflict: {merge_back_has_conflict}
  pass_evidence: "Phase 3 gate file at docs/qa/gates/{story_id}-*.yml"
  story_path: "{story_path}"

what_remains:
  - "Push branch feat/{story_id}-{short_title} to origin"
  - "Create PR and merge to main"
  - "{IF merge_back_has_conflict}: Resolve rebase conflicts before push"
  - "After confirmed merge in origin/main: signal team-lead to execute WL-3 teardown"

instructions: |
  1. IF has_conflict=true: resolve conflicts in {wt_path}, then git rebase --continue
  2. git push origin feat/{story_id}-{short_title}
  3. Create PR (or direct merge per project policy)
  4. After merge confirmed: SendMessage to team-lead "[WL-3 TRIGGER] Branch feat/{story_id}-{short_title} merged in origin/main — proceed with teardown"
```

```
SendMessage(
  to: "@devops",
  summary: "WL-2 merge-back handoff for story {story_id}",
  message: {
    type: "worktree_merge_back_handoff",
    story_id: "{story_id}",
    branch: "feat/{story_id}-{short_title}",
    wt_path: ".claude/worktrees/wt-{story_id}",
    handoff_file: ".aiox/handoffs/handoff-full-sdc-{story_id}-merge-back-{date}.yaml",
    has_conflict: {merge_back_has_conflict},
    action_required: "Push branch, create PR/merge, then signal WL-3 teardown"
  }
)
```

LOG: `[WL-2] Merge-back handoff emitted to @devops. Branch: feat/{story_id}-{short_title}. Conflict: {merge_back_has_conflict}.`

### 5b.4 — WL-3: Wait for @devops merge confirmation + teardown

**WL-3 respects O6b AC-5 teardown-ordering contract (O6b = owner; WL-3 = executor of Step 3).**

**Wait for @devops signal:** `[WL-3 TRIGGER]` message confirming branch merged in origin/main.

IF signal NOT received (team-lead is wrapping up session):
  LOG: `[WL-3] No merge confirmation received in this session. Teardown deferred to next session or manual trigger.`
  UPDATE registry entry: state = "active" (remains until teardown confirmed)
  → Proceed to Phase 6 (teardown deferred)

WHEN `[WL-3 TRIGGER]` received:

**Execute O6b AC-5 teardown sequence (Step 3 — WL-3 is executor):**

```bash
# Verify merged (NEVER git branch --merged — use remote ref: CG-O7O9-5)
git fetch origin
git branch -r --merged origin/main | grep "feat/{story_id}-{short_title}"
```

IF branch NOT found in remote merged list:
  LOG LOUD: `[WL-3 FAIL] Branch feat/{story_id}-{short_title} not confirmed merged in origin/main. Aborting teardown. Will re-check on next GC run (WL-7).`
  → Proceed to Phase 6 (teardown deferred — safe)

ELSE (confirmed merged):

  **O6b AC-5 Step 1 — O1 flush (per O6b degradation rules):**
  (already executed by O6b as part of Phase 5. If not: emit LOUD WARNING per O6b DEC-O6b-6.)

  **O6b AC-5 Step 2 — Checkpoint cleanup:**
  (executed by O6b — deferred if O1 not implemented)

  **O6b AC-5 Step 3 — WL-3 executes worktree teardown:**
  ```bash
  git worktree remove ".claude/worktrees/wt-{story_id}"
  git branch -d "feat/{story_id}-{short_title}"
  git worktree prune
  ```

  **Post-teardown assertion (WL-3 gate):**
  ```bash
  git worktree list | grep "wt-{story_id}"
  git branch --list "feat/{story_id}-{short_title}"
  ```
  IF either command returns output:
    LOG LOUD: `[WL-3 FAIL] Teardown incomplete — residue detected: {output}. Zero-accumulation invariant VIOLATED. Human intervention required.`
    HALT. Do NOT mark teardown complete.
  ELSE:
    LOG: `[WL-3] Teardown verified. Zero residue confirmed.`

  **O1-absent degradation (CG-O7O9-7):**
  IF O1 aggregator absent when WL-3 executes:
    SendMessage(to: "team-lead", message: "[WL-3 LOUD WARNING] O1 aggregator absent. Skipping removal of .aiox/ contents. Story marked 'pending integration validation'. DO NOT remove .aiox/checkpoints/{story_id}/ until O1 flush completes.")
    SET registry state = "halted" with halt_reason = "O1-aggregator-absent"
    SKIP .aiox/ cleanup (preserve state)
    Continue worktree/branch removal only.

  **O6b AC-5 Step 4 — Registry update:**
  ```
  UPDATE .aiox/worktrees/registry.json entry:
    state: "merged"
    last_seen: "<current ISO8601>"
  ```

  LOG: `[WL-3] Complete. Worktree .claude/worktrees/wt-{story_id} removed. Registry updated: state=merged.`

---

## Phase 6: Shutdown + Summary

### Shutdown All Teammates

```
SendMessage(to: "po", message: {type: "shutdown_request", reason: "SDC complete"})
SendMessage(to: "{executor_id}", message: {type: "shutdown_request", reason: "SDC complete"})
SendMessage(to: "{qg_id}", message: {type: "shutdown_request", reason: "SDC complete"})
IF deploy_agent spawned:
  SendMessage(to: "{deploy_agent_id}", message: {type: "shutdown_request", reason: "SDC complete"})
TeamDelete()
```

### Display Final Summary

```
╔══════════════════════════════════════════════════════════╗
║  Full SDC Complete — Story {story_id}: {title}           ║
╠══════════════════════════════════════════════════════════╣
║  Phase 1: Validate  ✅ {verdict} ({score}/10)            ║
║  Phase 2: Develop   ✅ {tasks_completed} tasks           ║
║  Phase 3: Review    ✅ Gate: {gate} ({quality_score}/100) ║
║           QG Loops: {qg_iterations}                      ║
║  Phase 4: Deploy    ✅ {deploy_status} | ⏭ Skipped       ║
║  Phase 5: Close     ✅ Status → Done                     ║
╠══════════════════════════════════════════════════════════╣
║  Epic Progress: {done}/{total} ({percentage}%)           ║
║  Next: Story {next_id} — {next_title}                    ║
║  Command: /full-sdc {next_story_path}                    ║
╚══════════════════════════════════════════════════════════╝
```

---

## Post-Phase Verification Gate (NON-NEGOTIABLE)

After every agent reports completion via SendMessage, the team-lead MUST verify on disk that the artifacts promised by the invoked SKILL.md were actually produced — BEFORE marking the phase task as completed.

### Why this exists

Empirically observed (Story 115.S0.3, 2026-05-14): an agent may report a step as "done" and even list the artifact path in its summary, while in fact never having created the file. The fidelity gap is invisible without on-disk verification. The team-lead is the only entity that can close this gap.

### Integrity Violation — premature `status: Done` outside Phase 5 (auto-HALT, NON-NEGOTIABLE — FIX-1c, Story 115.S2.O4)

After **every** phase verification (Phases 1–4, and any QG-loop iteration), the
team-lead MUST read the story frontmatter on disk and check `status`.

> **If `status: Done` is detected at ANY point OUTSIDE Phase 5, the team-lead
> MUST auto-HALT immediately and emit a structured `integrity-violation`
> event. This is not a warning — it is a hard stop.**

```yaml
- type: integrity-violation
  subtype: premature-done-outside-phase5
  story_id: {story_id}
  detected_at: <phase number where Done was observed, e.g. "phase 3">
  action: HALT
  ts: <ISO-8601>
```

Procedure:
1. HALT the pipeline (do not dispatch any further phase).
2. Append the event above to the full-sdc learning log `orchestration_events[]`
   (write a partial log immediately — friction data is never discarded on HALT).
3. Surface to the user: a `status: Done` outside Phase 5 means a subagent (or a
   direct edit) bypassed the close-story gate — exactly the F2 failure mode
   proven in 115.S1.D1 where the catastrophic close occurred *outside*
   close-story. CHK-0 alone does NOT close this (CHK-0 governs only the
   close-story internal path); this gate closes the direct-edit bypass.
4. Do not auto-recover. Human triage required.

This mechanism + close-story CHK-0 are complementary: CHK-0 verifies the
*provenance* of a close-story invocation; this gate detects a `Done`
transition that never went through close-story at all.

### Per-skill verification checklist

| Skill | Required artifacts to verify on disk |
|-------|---------------------------------------|
| validate-story-draft | Story frontmatter `status` advanced (Draft → Ready); story Change Log has new entry from @po; if auto-fixes applied, file has those edits |
| develop-story | All files in agent's reported artifact list exist; story Tasks `- [x]` checked; story File List populated; story Change Log has new entry from executor |
| review-story | **Gate file** at `docs/qa/gates/{story_id}-{slug}.yml` exists and is non-empty; story has `## QA Results` section populated; story Change Log has new entry from QG |
| apply-qa-fixes | Files in fix list show modifications (git diff or mtime check); story File List updated if new files |
| deploy-story | Story has `## Deploy Log` section populated; deploy artifacts (e.g., commit hash, image tag) recorded |
| verify-deploy | Story has `## e2e_verification` section with verdict PASS/FAIL/PARTIAL; check timestamps |
| close-story | Story frontmatter `status: Done`; Epic file has Development Log entry for this story; **learning log exists** at `.aiox/learning/logs/close-story/close-story-{story_id}-{YYYYMMDD}-{HHmmss}.yaml` |

### Post-Phase-2 Branch Guard (NON-NEGOTIABLE — AC-2b, Story 115.S2.O12)

> **Defense-in-depth — Layer 2.** L1 = the in-skill instruction `develop-story/SKILL.md §Pre-Execution Branch Setup` (AC-2a) that creates the feature branch before the first commit. **L2 = this post-Phase-2 check** in full-sdc — a backstop that catches the case where develop-story (or a non-conformant executor) committed to a protected branch anyway.

After the Phase 2 (develop-story) Post-Phase Verification Gate confirms artifacts, and **BEFORE dispatching Phase 3**, the team-lead MUST run this branch guard:

```
# L2 BRANCH GUARD — defense-in-depth Layer 2 (L1 = develop-story AC-2a Pre-Execution Branch Setup)
current_branch = `git branch --show-current`

IF current_branch == "main" OR current_branch == "master":
  FAIL with explicit message:
    "BRANCH GUARD VIOLATION: Phase 2 (develop-story) committed to main.
     Expected: feat/{story_id}-*. Dispatch fix-message to executor before Phase 3."
  # Treat as a verification-gate retry (NOT an integrity-violation HALT):
  # the executor is still alive; remediation is to create the feature branch
  # and re-point the commits, then re-verify.
  retry_count++
  IF retry_count <= 2:
    SendMessage(
      to: "{executor_id}",
      summary: "Branch guard violation",
      message: "[ACTION REQUIRED: complete-missing-artifacts]

        L2 Branch Guard FAILED after Phase 2: current branch is '{current_branch}'.
        develop-story §Pre-Execution Branch Setup (AC-2a) requires a
        feat/{story_id}-* branch BEFORE the first commit. Create the feature
        branch, move the Phase-2 commits onto it (so `main`/`master` is clean),
        and confirm `git branch --show-current` begins with feat/{story_id}.

        When done, SendMessage to 'team-lead' confirming the branch."
    )
    wait for executor → re-run this guard
  ELSE:
    ESCALATE to user (branch guard unrecoverable after 2 retries)
ELSE IF current_branch begins with "feat/":
  PASS — proceed to dispatch Phase 3
ELSE:
  # Non-protected but also non-feature branch (e.g., a detached or ad-hoc branch).
  # Surface as a verification-gate retry with the same remediation message.
```

Emit a `verification_gate_retry` orchestration event (closed enum — §Orchestration Telemetry) on any FAIL, with `detail` naming the observed branch. This guard is additive and non-breaking: a conformant develop-story run (post-AC-2a) always lands on `feat/{story_id}-*`, so the guard is a no-op PASS on the happy path.

### Verification procedure (team-lead inline)

```
FOR each artifact_path in expected_artifacts:
  IF NOT exists(artifact_path):
    missing.append(artifact_path)
  ELIF empty(artifact_path):
    missing.append(artifact_path + " (empty)")

IF missing is empty:
  TaskUpdate(task_for_this_phase, completed)
  proceed to next phase
ELSE:
  retry_count++
  IF retry_count <= 2:
    SendMessage(
      to: "{agent_name}",
      summary: "Verification gate failed",
      message: "[ACTION REQUIRED: complete-missing-artifacts]

        Post-phase verification found these expected artifacts missing
        or empty after your previous turn:

        {missing list}

        These are REQUIRED by .claude/skills/{skill_name}/SKILL.md.
        Create them now (do not re-execute the full skill protocol —
        just produce the missing artifacts).

        When done, SendMessage to 'team-lead' confirming each path now exists."
    )
    wait for agent → re-verify
  ELSE:
    ESCALATE to user with the missing artifact list
```

### Task-List Wipe Detection (O6a — NON-NEGOTIABLE)

After writing the per-phase checkpoint seed (see below) and before marking a phase completed, the team-lead MUST check whether the active task-list has been wiped.

#### Minimal Checkpoint Seed (Gate Ownership Contract — O6a owns write; O6b owns full cycle)

At the **START** of each phase (Phases 1–5), before dispatching the agent, the team-lead writes a minimal checkpoint seed:

```json
// .aiox/checkpoints/{story_id}/phase-{N}.json
{
  "story_id": "<string>",
  "phase": <int>,
  "phase_status": "started",
  "expected_tasks": ["<task-id-or-title-1>", "<task-id-or-title-2>"]
}
```

This seed is the source of truth for wipe detection. O6b expands it to a full checkpoint (adding `artifacts_on_disk[]`, `timestamp_end`, `phase_status: "completed"`). O6a only writes the seed — do NOT attempt to implement re-entry or full checkpoint expansion here.

**`expected_tasks[]`** is populated from the TaskCreate calls made for this phase (Phase 1 → Phase 2 → Phase 3, and deferred Phase 4/5 when applicable). Use the task title strings as stable identifiers until O1 delivers canonical task IDs.

#### Wipe Detection Heuristic (c) — adjudicated DEC-O6a-1

**Any expected task absent from the active task-list without `Done` status = wipe detected.**

Tokens governing this gate:
- `TK-SDC-WIPE-THRESHOLD` — default 0: any single absent task triggers detection
- `TK-SDC-WIPE-GRACE-WINDOW` — grace/retry interval (seconds) before declaring HALT; re-verify after this window to absorb TaskList propagation latency
- `TK-SDC-CHECKPOINT-TTL` — TTL for checkpoint files on disk (managed by O6b)

#### Wipe Detection Procedure

```
FOR each phase N (at post-phase verification time):
  expected = read .aiox/checkpoints/{story_id}/phase-{N}.json → expected_tasks[]
  active   = list current TaskList entries with status != "Done"
  missing  = expected_tasks[] items not present in active

  # Exclusion: legitimately completed phase
  IF all expected_tasks are present with status "Done":
    → phase completed normally, proceed (NOT a wipe)

  IF count(missing) > TK-SDC-WIPE-THRESHOLD:
    # Apply grace/retry window before HALT
    WAIT TK-SDC-WIPE-GRACE-WINDOW seconds
    Re-verify: missing = expected_tasks[] items not present in active task-list
    IF missing still > TK-SDC-WIPE-THRESHOLD:
      EMIT runtime_state_loss event (see below)
      HALT pipeline
```

#### Structured HALT — `runtime_state_loss` Event (O1-canonical schema)

On wipe detection, emit this event into `orchestration_events[]` in the learning log:

```json
{
  "type": "runtime_state_loss",
  "phase": <int>,
  "severity": "high",
  "skill": "full-sdc",
  "run_id": "<story_id>-<ISO8601-start-ts>",
  "timestamp": "<ISO8601>",
  "detail": {
    "subtype": "task-list-wipe",
    "tasks_expected": <int>,
    "tasks_found": <int>,
    "story_id": "<string>",
    "action": "HALT"
  },
  "resolution": "Pipeline HALTed. Await O6b for re-entry or re-execute manually from phase N.",
  "event_schema_version": "1.0"
}
```

**Fields `subtype`, `tasks_expected`, `tasks_found`, `story_id`, `action` MUST be inside `detail` — NEVER top-level.**

Schema fixture: `.aiox/fixtures/o1-event-schema-v1.0.json` (AC-3, Story 115.S2.O6a).

#### HALT procedure on wipe detection

1. Write the partial learning log immediately with `orchestration_events[]` containing the `runtime_state_loss` event — friction data is never discarded on HALT.
2. SendMessage to team-lead (self, for audit trail) AND send the following structured message to the team-lead channel:

```
SendMessage(
  to: "team-lead",
  message: "[WIPE-HALT] runtime_state_loss detected.
    Phase: {N}
    tasks_expected: {count}
    tasks_found: {count_active_not_done}
    story_id: {story_id}
    Recomendação: aguardar O6b para re-entry seguro, ou re-executar manualmente a partir da fase {N}. NÃO continue execução sem confirmar estado."
)
```

3. **Do NOT continue pipeline execution.** Returning `action: "HALT"` is the ONLY valid outcome after wipe detection. Silent fallback (continuing as if tasks exist) is explicitly forbidden (anti-pattern per `.claude/rules/epistemic-standards.md`).

#### HALT scope — wave-execute callers (T1.3 adjudication — CG-11)

**Adjudicated decision:** The O6a HALT is **isolated to the affected story's `/full-sdc` session**. It does NOT HALT the whole wave.

Rationale: wave-execute v5.0 (ATM-WE-005) already handles per-story failures by marking the story `Blocked` and continuing with other stories in the batch. A wipe HALT in one story's `/full-sdc` session produces a `Blocked` result for that story; the wave orchestrator cascade-blocks dependent stories only (per DAG), not all stories. This is consistent with the timeout/circuit-breaker handling pattern already in wave-execute. The team-lead of the affected `/full-sdc` session emits the structured event and halts; wave-execute detects the missing sdc-complete.ack and reports `Blocked` to the orchestrator.

#### When NOT to apply wipe detection

- If the phase legitimately has zero tasks (no TaskCreate was called for this phase, e.g., Phase 4 with `deploy_type: none`): the expected_tasks[] is empty → wipe detection is vacuously satisfied (no tasks to be missing). Do NOT HALT.
- If the SKILL.md for the invoked skill explicitly marks artifacts as conditional: the artifact verification gate (above) governs; wipe detection is a separate, task-list-level check.

### When NOT to enforce (artifact gate)

If the SKILL.md being invoked explicitly states that an artifact is conditional (e.g., gate file only if review actually ran, learning log skipped in `--dry-run` mode), the gate respects those conditions. Read the relevant SKILL.md to know what's truly required.

---

## Durable State Checkpoint Layer (O6b — NON-NEGOTIABLE)

> **Story 115.S2.O6b** — Durable State Checkpoint Layer: per-phase on-disk checkpoints + re-entry protocol + worktree registry + epic-state sync + teardown ordering contract.
> **DEC-O6b-1 CLOSED → JSON** (R40: machine-consumed → JSON). All checkpoint/registry files are JSON.

### AC-1 — Full Checkpoint on-disk per Phase

O6a writes a minimal seed (`phase_status: "started"`, `expected_tasks[]`) at the START of each phase. O6b expands that seed to a full checkpoint at the END of each phase (after Post-Phase Verification Gate PASS).

**Full checkpoint schema `checkpoint-schema-version: "1.0"` (JSON — R40):**

```json
// .aiox/checkpoints/{story_id}/phase-{N}.json
{
  "story_id": "<string>",
  "phase": <int>,
  "phase_status": "started | completed | halted",
  "artifacts_on_disk": ["<path1>", "<path2>"],
  "timestamp_start": "<ISO8601>",
  "timestamp_end": "<ISO8601 | null>",
  "checkpoint_schema_version": "1.0",
  "expected_tasks": ["<task-id-or-title>"]
}
```

**O6b expansion procedure (after Post-Phase Verification Gate PASS, before marking phase Done):**

```
READ existing .aiox/checkpoints/{story_id}/phase-{N}.json (written by O6a seed)
SET phase_status = "completed"
SET timestamp_end = <current ISO8601>
SET artifacts_on_disk = [list of artifact paths verified by Post-Phase Gate]
WRITE back the expanded JSON to same path
```

**Gate dependency:** O6b expansion runs ONLY after Post-Phase Verification Gate PASS (inherited from AC-1/O6a). Never before.

**Token:** `TK-SDC-CHECKPOINT-TTL` — TTL/cleanup managed at teardown (Phase 5, after O1 flush).

### AC-2 — Re-entry Protocol with Triple Validation

The pipeline can resume from any phase with checkpoint `phase_status: "completed"` without re-executing earlier phases.

**Invocation:** the team-lead can be instructed to re-enter at phase N by the user or by a wave-execute recovery mechanism after a wipe-HALT.

**Re-entry procedure:**

```
INPUT: story_id, resume_from_phase (e.g., 3)

FOR N = 1 .. (resume_from_phase - 1):
  APPLY TRIPLE VALIDATION on .aiox/checkpoints/{story_id}/phase-{N}.json:
    (1) File exists at .aiox/checkpoints/{story_id}/phase-{N}.json
    (2) phase_status == "completed"  (NOT "started" or "halted")
    (3) timestamp_end is non-null
    (4) EACH path in artifacts_on_disk[] EXISTS on disk
  IF any check fails:
    HALT with explicit list of failed items (file path + which check failed)
    Message format: "Re-entry HALT: phase {N} validation failed — {item}: {reason}"

IF all phases 1..(N-1) pass triple validation:
  LOG: "Re-entry PASS for phases 1..{resume_from_phase-1} — resuming from phase {resume_from_phase}"
  PROCEED: execute phase {resume_from_phase} with full normal protocol (including O6a seed write + O6b expansion)
```

**5 negative scenarios — mandatory behavior (CG-9/C-c):**

| Scenario | O6b behavior |
|----------|-------------|
| **(a)** Checkpoint with `phase_status: "started"` (not "completed") | **HALT** with message: `"partial-phase execution detected — re-entry not safe without human confirmation"`. Never re-execute automatically. |
| **(b)** Artifact in `artifacts_on_disk[]` absent on disk | **HALT** with explicit list of missing artifacts. |
| **(c)** Wipe during phase execution (mid-phase wipe) | O6a detects and HALTs. O6b re-entry available for the immediately preceding phase with `completed`. |
| **(d)** Wipe across multiple consecutive phases | HALT with inventory of ALL affected phases. Re-entry only from most recent phase with `completed`. |
| **(e)** Re-entry without `epic-{N}-state.json` present | **WARNING LOUD** via SendMessage to team-lead. Does NOT fail re-entry (see AC-4 degradation rules). |

**Test scenario (documented):** Simulate task-list wipe after Phase 2 completed → run re-entry at Phase 3 → verify Phases 1 and 2 pass triple validation → Phase 3 executes without re-running Phases 1/2.

### AC-3 — Worktree Registry (`worktree-registry-v1`)

> **Ownership seam (single-writer):** O6b owns the file and JSON write mechanism. O7 WL-6/WL-7 own reconciliation and GC logic — they REUSE O6b primitives, never copy code (@architect F4). No split-brain.

**File:** `.aiox/worktrees/registry.json` — JSON (R40: machine-consumed). Gitignored.

**Schema `worktree-registry-v1`:**

```json
{
  "schema_version": "worktree-registry-v1",
  "last_updated": "<ISO8601>",
  "worktrees": [
    {
      "story_id": "<str>",
      "branch": "<str>",
      "wt_path": "<str>",
      "state": "active|merged|halted|orphan|orphan-no-wt|stale",
      "halt_reason": "<str|null>",
      "last_seen": "<ISO8601>",
      "created_at": "<ISO8601>",
      "age_days": "<int>"
    }
  ]
}
```

**Write primitive (O6b owns — called by O6b at worktree creation/state transitions):**

```
READ .aiox/worktrees/registry.json (or initialize with schema_version + empty worktrees[] if absent — M4 reconstruction)
UPSERT entry by story_id: set fields as provided
SET last_updated = <current ISO8601>
WRITE back JSON
```

**M4 Reconstruction:** if registry absent → O7 WL-7 GC reconstructs from `git worktree list --porcelain` without state loss. O6b re-creates the file on next write primitive call.

**Reconciliation (executed by O7 WL-6 at start of each execution — uses O6b write primitive):**

Parse `git worktree list --porcelain` + **`git branch -r --merged origin/main`** (NEVER `git branch --merged` — prevents false-merged data loss, @qa C1) → diff vs registry → flag:
- `orphan`: present in registry, absent from `git worktree list`
- `orphan-no-wt`: branch unmerged, worktree absent
- `stale`: age_days > `TK-SDC-WORKTREE-STALE-DAYS`

**Orphan housekeeping (NON-NEGOTIABLE):** NEVER auto-delete unmerged worktree without explicit team-lead confirmation. Protocol:
1. SendMessage to team-lead with list of orphans
2. Set `pending_confirmation: true` note in registry entry
3. Re-notify per TTL on every execution until confirmation

**3 negative test-cases (@qa C4):**
- **(a)** Worktree disk-only, absent from registry → detect and register as `orphan`.
- **(b)** Registry entry with state `active` but absent from `git worktree list` → flag as `orphan` (do NOT remove).
- **(c)** `git worktree add` manual outside registry → detected at reconciliation → register as `orphan` with `halt_reason: "manually added outside registry"`.

**INDEX.json registration (R39 — NON-DEFERRABLE):** `.aiox/worktrees/registry.json` MUST be registered in `.sinkra/registries/INDEX.json` (schema `sinkra-index-v1`) when the file is first created. See §INDEX.json Registration below.

### AC-4 — Epic-state.json Sync (Degradation-Safe — Gated on O9 ES-2)

> **CG-O7O9-10 gate:** O9 ES-2 (`epic-state-v1` schema freeze, Done) is a SEQUENTIAL prerequisite of full AC-4 implementation. O9 status = **Ready** (not Done) as of 2026-05-17. Implementation below is degradation-safe: WARNING + HALT rules implemented; schema-coupled parts (crash-recovery, drift sentinel) are gated-pending-O9-ES2.

**O6b owns the UPDATE mechanism. O9 defines the schema.** O6b writes ONLY a minimal node: `{story_id, status, last_updated}`. NEVER defines schema — uses `epic-state-v1` as external contract.

**Step added to §Phase 5 (close) — after Post-Phase Gate PASS:**

```
IF epic-{N}-state.json absent:
  SendMessage(to: "team-lead", message: "[O6b WARNING] epic-{epic_N}-state.json absent — story state sync skipped. File may not exist if epic was created before O8/O9. No action required but state drift will accumulate.")
  # Do NOT fail the phase — degradation-safe

ELSE:
  READ docs/stories/epic-{N}/epic-{N}-state.json
  CHECK schema_version field:
    IF schema_version != "epic-state-v1":
      SendMessage(to: "team-lead", message: "[O6b HALT LOUD] epic-state.json schema_version is '{actual}', expected 'epic-state-v1'. Refusing to write to unknown schema. Pipeline HALTed — human triage required.")
      HALT pipeline (do NOT update the file)

  # [GATED-PENDING-O9-ES2] Parts below require epic-state-v1 schema freeze (O9 ES-2 Done)
  # When O9 ES-2 is Done: implement crash-recovery idempotence + drift sentinel here.
  # Until then: proceed with best-effort minimal node write:
  UPDATE story node in file: {story_id: story_id, status: "Done", last_updated: <current ISO8601>}
  WRITE back JSON
  # Note: idempotent crash-recovery and drift sentinel (last_updated staleness check)
  # are NOT implemented until O9 ES-2 Done — gated-pending-O9-ES2
```

**Drift sentinel [GATED-PENDING-O9-ES2]:** once O9 ES-2 Done — `last_updated` MUST change in the same operation as `status`. If diff between `last_updated` and current timestamp > `TK-SDC-CHECKPOINT-TTL` → LOUD WARNING via SendMessage.

**Crash-recovery [GATED-PENDING-O9-ES2]:** once O9 ES-2 Done — detect incomplete write (e.g., `last_updated` older than status transition) and overwrite with clean write.

### AC-5 — Pre-teardown Ordering Contract (Phase 5 — O1 Coordination)

> **O6b owns the teardown ordering contract.** O1 (aggregator) MUST run BEFORE any worktree/checkpoint cleanup.

**Teardown sequence (mandatory order) — added to §Phase 5 (Close), after close-story completes:**

```
TEARDOWN SEQUENCE (O6b §Phase 5 contract):

STEP 1 — O1 aggregator flush:
  IF O1 aggregator available (.aiox/ or O1 implementation exists):
    INVOKE O1 flush: orchestration_events[] → .synapse/metrics/orchestration-friction.json
    IF O1 flush fails:
      SendMessage(to: "team-lead", message: "[O6b HALT LOUD] O1 aggregator flush failed. Leaving ALL state intact (checkpoints, registry, worktree). Human triage required before cleanup.")
      HALT — do NOT proceed to steps 2-4. Leave state intact.
  ELSE (O1 not yet implemented):
    SendMessage(to: "team-lead", message: "[O6b WARNING] O1 aggregator not yet available. Deferring checkpoint cleanup — .aiox/checkpoints/{story_id}/ will NOT be cleaned until O1 is implemented. Worktree teardown continues.")
    # Skip to step 3 (worktree remove) — checkpoint cleanup deferred until O1 available

STEP 2 — Checkpoint cleanup (only after O1 flush succeeds, respecting TTL TK-SDC-CHECKPOINT-TTL):
  REMOVE .aiox/checkpoints/{story_id}/
  # Respect TTL: if run timestamp < TTL expiry, defer removal

STEP 3 — Worktree teardown:
  RUN git worktree remove {wt_path} (only if wt_path is valid and not dirty)
  RUN git branch -d {branch} (only if merged — confirmed via git branch -r --merged origin/main)

STEP 4 — Worktree registry update:
  UPDATE .aiox/worktrees/registry.json entry: state = "merged", last_seen = <current ISO8601>
  (Using O6b write primitive from AC-3)
```

**DEC-O6b-6 degradation rules:**
- O1 not implemented → LOUD WARNING via SendMessage + **defer checkpoint cleanup** (never silent skip). Worktree teardown continues.
- O1 flush fail → **HALT LOUD, leave ALL state intact** (no partial cleanup). Explicit message to team-lead.

This teardown ordering contract is referenced in `STORY-115.S2.O1` AC-3 as "teardown-ordering contract owned by O6b."

---

## INDEX.json Registration (R39 — NON-DEFERRABLE)

When `.aiox/worktrees/registry.json` is first created (AC-3), register it in `.sinkra/registries/INDEX.json` using schema `sinkra-index-v1`:

```json
{
  "id": "worktree-registry",
  "path": ".aiox/worktrees/registry.json",
  "schema_version": "worktree-registry-v1",
  "description": "Durable worktree registry — tracks active/merged/orphan worktrees per story. Written by O6b, reconciled by O7 WL-6/WL-7.",
  "owner": "sinkra-squad",
  "story": "115.S2.O6b",
  "created_at": "<ISO8601>"
}
```

This registration is NON-DEFERRABLE (R39 mandate, @sm CG-7).

---

## Error Handling

### HALT Conditions (pipeline stops, user decides)

| Condition | Phase | Action |
|-----------|-------|--------|
| Dependency not Done | 0 | HALT before team creation |
| WL-1: worktree add failed | 0c | HALT, notify user |
| WL-1: MAX_PARALLEL_WORKTREES reached | 0c | HALT, free a slot |
| PO verdict: NO-GO | 1 | HALT, show issues |
| Executor halted (blocker) | 2 | HALT, show blocker, wait for user |
| QG FAIL after 3 loops | 3 | ESCALATE to user |
| Deploy failed | 4 | HALT, show error |
| Verify FAIL/PARTIAL | 4 | HALT, show checks |
| CHK-8 blocked | 5 | HALT, run verify-deploy first |
| WL-3 teardown incomplete | 5b | HALT LOUD, human intervention |

### WL-4 — Failure Path: Preserve + Register Halted Worktree

When the pipeline HALTs for ANY reason after Phase 0c has created a worktree, the worktree MUST be preserved (NOT destroyed) and registered with `state: "halted"`:

```
ON HALT after Phase 0c (any phase 1..5b):

  halt_reason = "<concise description of what caused the HALT>"

  UPDATE .aiox/worktrees/registry.json entry for story_id:
    state: "halted"
    halt_reason: "{halt_reason}"
    last_seen: "<current ISO8601>"

  LOG LOUD: "[WL-4] Pipeline HALT. Worktree .claude/worktrees/wt-{story_id} PRESERVED for debug.
    Branch: feat/{story_id}-{short_title} | Reason: {halt_reason}
    Use WL-7 GC to review and clean up when resolved."
```

**Stale detection (TK-SDC-WORKTREE-STALE-DAYS):**
At the START of each full-sdc execution, after Phase 0c registry check:

```
FOR each entry in .aiox/worktrees/registry.json WHERE state IN ("halted", "active"):
  age_days = (current_date - created_at) in days
  IF age_days > TK-SDC-WORKTREE-STALE-DAYS (default: 7):
    UPDATE entry: state = "stale"
    LOG LOUD: "[WL-4 STALE] Worktree wt-{entry.story_id} is {age_days} days old (limit: {TK-SDC-WORKTREE-STALE-DAYS}).
      Branch: {entry.branch} | Last halt: {entry.halt_reason}
      Review and clean up via WL-7 GC."
```

**Invariant:** No orphan silent worktree. Every worktree in the registry has an explicit state and reason. Unknown worktrees detected at reconciliation are flagged `orphan` (WL-6).

### Recovery

On any HALT:
1. Tasks show partial progress (completed phases visible)
2. Team stays alive — user can SendMessage to any agent
3. User resolves issue → SendMessage to team-lead → pipeline resumes
4. If user wants to abort → team-lead shuts down all agents

### Circuit Breakers

| Breaker | Limit | Action |
|---------|-------|--------|
| QG loop | 3 iterations | Escalate to user |
| CodeRabbit (in develop) | 2 iterations | Continue with warning |
| CodeRabbit (in review) | 3 iterations | Gate FAIL |
| Executor consecutive failures | 3 | HALT develop phase |

---

## Agent Spawn Specifications

### Model Selection

| Agent | Default Model | YOLO Mode | Rationale |
|-------|-------------|-----------|-----------|
| PO (validate) | sonnet | sonnet | Needs judgment for D10 analysis |
| Executor | sonnet | sonnet | Code generation quality |
| QG (review) | sonnet | sonnet | Needs judgment for risk assessment |
| Deploy agent | sonnet | haiku | Deploy is deterministic |
| PO (close) | — (reused) | — | Same instance from Phase 1 |

### Agent Persistence Map

```
Phase 1:  [PO spawned] ────────────────────────────────── [PO reused Phase 5]
Phase 2:  [Executor spawned] ──── [Executor fixes Phase 3 QG loop] ── [shutdown]
Phase 3:  [QG spawned] ─────────── [QG re-reviews Phase 3 loop] ──── [shutdown]
Phase 4:  [Deploy spawned if needed] ──────────────────────────────── [shutdown]
```

Key: PO lives from Phase 1 to Phase 5. Executor lives from Phase 2 through QG loop. QG lives for Phase 3 only. Deploy lives for Phase 4 only.

---

## Comparison with Existing Skills

| Existing Skill | What It Does | What /full-sdc Adds |
|---------------|-------------|-------------------|
| /story-executor *(deleted 115A.8b)* | PO + Executor + QG via Agent Teams | Absorbed by /full-sdc (+ validate-story-draft, + deploy, + verify, + close) |
| /validate-story-draft | PO validates story | Embedded as Phase 1 |
| /develop-story | Executor implements | Embedded as Phase 2 |
| /review-story | QG reviews | Embedded as Phase 3 |
| /apply-qa-fixes | Fix QG findings | Embedded in QG loop |
| /deploy-story | Deploy artifacts | Embedded as Phase 4a |
| /verify-deploy | Verify deployment | Embedded as Phase 4b |
| /close-story | PO closes | Embedded as Phase 5 |

**/full-sdc is the composition of all 7 skills into a single orchestrated pipeline.**

---

## Blocking Conditions

HALT and surface to user when:

1. **Story file not found** — Cannot start pipeline. Resolution: provide correct path.
2. **Dependencies not Done** — Upstream stories incomplete. Resolution: complete dependencies first.
3. **PO verdict NO-GO** — Story has blocking issues. Resolution: fix story, retry.
4. **Executor halted** — Implementation blocker. Resolution: user provides guidance.
5. **QG FAIL after 3 loops** — Quality issues unresolvable by agents. Resolution: human intervention.
6. **Deploy failed** — Deployment error. Resolution: fix and retry deploy.
7. **User cancellation** — User types "abort" or denies any confirmation. Resolution: graceful shutdown of all agents.

---

## Auto-ACK Emission Protocol (NON-NEGOTIABLE — Story 115A.8b)

`/full-sdc` is now the sole writer of `.sdc-ack/{story-id}/*.ack` files. This replaces the
discontinued `/story-executor` wrapper that previously owned this responsibility.

**ACK files are the on-disk coordination channel** used by `wave-execute --spawn-external`
to monitor progress without a SendMessage channel back to the orchestrator. They are also
used by Phase 0c to detect a pre-provisioned worktree (`wt_provisioned: true` in dispatch.ack).

### When to write each ACK file

| ACK file | Written at | Notes |
|----------|-----------|-------|
| `.sdc-ack/{story-id}/dispatch.ack` | Start of Phase 0c (after team created) | Includes `wt_provisioned` flag |
| `.sdc-ack/{story-id}/validate.ack` | Phase 1 complete (PO verdict GO/GO-with-fix) | |
| `.sdc-ack/{story-id}/develop.ack` | Phase 2 complete (executor reports completed) | |
| `.sdc-ack/{story-id}/review.ack` | Phase 3 complete (QG gate PASS or WAIVED) | |
| `.sdc-ack/{story-id}/deploy.ack` | Phase 4 complete OR skipped (deploy_type=none) | `status: skipped` when deploy skipped |
| `.sdc-ack/{story-id}/phase-5.ack` | Phase 5 complete (close-story reports completed) | |
| `.sdc-ack/{story-id}/sdc-complete.ack` | Phase 5 complete (same moment as phase-5.ack) | Signals wave-execute orquestrador |

### ACK file format (YAML — exact field names required)

```yaml
phase: "{phase-name}"          # dispatch | validate | develop | review | deploy | phase-5 | sdc-complete
timestamp: "{ISO-8601}"        # e.g. 2026-05-22T14:32:07Z
commit_sha: "{git-HEAD-sha}"   # run: git rev-parse HEAD
status: passed                 # MUST be exactly: passed | skipped | failed  (lowercase, no quotes)
story_id: "{story-id}"
skill: "full-sdc"
```

### Idempotence contract

If a `.sdc-ack/{story-id}/*.ack` file already exists when the phase completes, **overwrite it**
without error. ACK writes are unconditional — no check-before-write gate.

### Mode independence

ACK files are written in **both execution modes**:
- Default (Agent Teams in-process via `wave-execute`)
- `--spawn-external` (pane externa via psmux/wezterm)

The ACK write step is NOT conditional on the execution mode.

### Write procedure (per ACK point)

```bash
# 1. Ensure directory exists
mkdir -p .sdc-ack/{story-id}

# 2. Get current HEAD sha
commit_sha=$(git rev-parse HEAD)

# 3. Write ACK file (overwrite if exists — idempotent)
Write(
  path: ".sdc-ack/{story-id}/{phase}.ack",
  content: "phase: \"{phase-name}\"\ntimestamp: \"{ISO-8601}\"\ncommit_sha: \"{commit_sha}\"\nstatus: {status}\nstory_id: \"{story-id}\"\nskill: \"full-sdc\"\n"
)
```

### Insertion points in the pipeline

The ACK writes are inserted at the following locations (each phase section calls this protocol):

- **Phase 0c.5** (after worktree registered): write `dispatch.ack` with `wt_provisioned: true`
- **Phase 1** (after PO result GO): write `validate.ack` with `status: passed`
- **Phase 2** (after executor completed): write `develop.ack` with `status: passed`
- **Phase 3** (after QG PASS/WAIVED + L2 gate passed): write `review.ack` with `status: passed`
- **Phase 4** (after deploy+verify OR when skipped): write `deploy.ack` with `status: passed|skipped`
- **Phase 5** (after close-story completed): write `phase-5.ack` AND `sdc-complete.ack` with `status: passed`

On **HALT or FAIL** at any phase, write that phase's ACK with `status: failed` before halting —
friction data is never lost (mirrors the learning log partial-write rule).

---

## Orchestration Telemetry (NON-NEGOTIABLE)

### Why this exists

The pipeline has **three telemetry planes**, and historically only two were recorded:

| Plane | Captures | Lives in | Aggregable |
|-------|----------|----------|------------|
| Development | What was built (artifacts, tech debt) | Epic Development Log | ✅ |
| Skill execution | Each skill from its own point of view | `.aiox/learning/logs/{skill}/` | ✅ |
| **Orchestration** | Coordination friction between team-lead and spawned agents | **nowhere structured** (was free-text prose) | ❌ |

The orchestration plane is structurally invisible: spawned agents are blind to it (a reused @po never knows it was re-commanded — from its side it just received a message; a runtime task-list wipe is never surfaced to a sub-agent). **Only the team-lead sees the seams between agents.** Free-text `what_failed` prose cannot be counted, so "this happened 4× → fix it" never surfaces. This section makes the team-lead emit **typed, countable events** so coordination overhead becomes a first-class, aggregable signal.

### Closed event vocabulary

The team-lead MUST classify every coordination-layer friction into exactly ONE of these types (closed enum — do not invent types):

| `type` | Emit when |
|--------|-----------|
| `handoff_misparse` | Recipient agent treated a new-task `[ACTION REQUIRED]` message as a status report (or vice-versa); a re-send was required |
| `verification_gate_retry` | Post-Phase Verification Gate found a promised artifact missing/empty; a fix-message was dispatched |
| `runtime_state_loss` | TaskList/TaskUpdate/team state desynced or wiped mid-pipeline (e.g., "Task not found", "No tasks found") |
| `agent_respawn` | A teammate had to be re-spawned (crash, unresponsive, lost context) |
| `circuit_breaker_trip` | A loop hit its max (QG loop ≥3, CodeRabbit, executor consecutive failures) |
| `escalation` | Pipeline HALTed and was surfaced to the user for a decision |
| `sendmessage_failure` | A `SendMessage` routing failed / recipient unreachable |
| `phase_skipped_unexpected` | A phase was skipped for a reason other than its declared conditions |

### Event shape

```yaml
- type: <one of the closed enum>
  phase: <1-6 | "0">
  agent: <recipient/affected agent name, or "team-lead">
  severity: low | medium | high
  detail: <one-line factual description — what was observed>
  resolution: <what the team-lead did about it>
  retry_count: <int — how many re-sends/retries this friction caused>
  ts: <ISO-8601>
```

### Emission rule

1. The team-lead emits an event **the moment friction is detected**, accumulating them in working memory across phases.
2. The complete `orchestration_events[]` array is written into the full-sdc learning log at Phase 6 (Shutdown + Summary).
3. If the pipeline HALTs before Phase 6, the team-lead MUST still write a **partial** learning log containing the events captured so far — friction data is never discarded on HALT.
4. Record **only directly observed** events (Epistemic Standards: ALTA confidence). Never infer or pad. Zero events is a valid, healthy run — record `orchestration_events: []`.

### Aggregation (cross-skill — tracked by formal story)

The cross-skill rule `.claude/rules/orchestration-telemetry.md` (inherited by ALL Agent-Teams orchestrators: full-sdc, full-tec, wave-execute, roundtable) and the roll-up aggregator `.synapse/metrics/orchestration-friction.json` (same pattern as `.synapse/metrics/registry-coverage.json`) are delivered by **Story 115.S2.O1**. Until that lands, full-sdc emits events locally per this section so **no data is lost from any run**.

---

## Post-Execution Learning (MANDATORY)

Create learning log at: `.aiox/learning/logs/full-sdc/full-sdc-{story-id}-{YYYYMMDD}-{HHmmss}.yaml`

```yaml
schema_version: "1.1"
skill_id: "full-sdc"
timestamp: "{ISO-8601}"
story_id: "{story-id}"
executor_agent: "{executor from story}"
quality_gate_agent: "{qg from story}"
deploy_agent: "{deploy agent or null}"
deploy_type: "{deploy_type}"
duration_minutes: {estimate}
mode: "{yolo|interactive}"
phases:
  validate: {verdict: "GO", score: 8}
  develop: {status: "completed", tasks: "8/8"}
  review: {gate: "PASS", score: 85, qg_loops: 0}
  deploy: {status: "completed|skipped", verify: "PASS|skipped"}
  close: {status: "completed", chk8: "PASS|SKIP", chk9: "advisory", chk10: "advisory"}
files_modified: []
# Orchestration plane (schema v1.1+) — typed, countable coordination-friction
# events observed by team-lead. Closed enum. [] is a valid healthy run.
orchestration_events: []
#  - type: runtime_state_loss
#    phase: 5
#    agent: team-lead
#    severity: low
#    detail: ""
#    resolution: ""
#    retry_count: 0
#    ts: "{ISO-8601}"
errors: []
outcome: "{completed|halted|failed|escalated}"
epilogue:
  what_worked: ""
  what_failed: ""
  qg_loop_count: 0
  orchestration_event_count: 0
  total_agents_spawned: 0
  confidence: "HIGH|MEDIUM|LOW"
  source_type: "skill_execution"
```

---

## WL-6 — Worktree Registry Reconciliation

**Execute at the START of Phase 0c (before provisioning).** Also invocable standalone.

> **Seam:** O6b AC-3 owns the schema (`worktree-registry-v1`) and write primitive. WL-6 USES those primitives for reconciliation. WL-6 never copies the write code — it calls the O6b primitive.

### WL-6.1 — Parse git worktree list

```bash
git worktree list --porcelain
```

Extract: `worktree` (path), `HEAD` (sha), `branch` (refs/heads/...) for each entry.

### WL-6.2 — Parse merged branches

```bash
git fetch origin
git branch -r --merged origin/main
```

**NEVER `git branch --merged`** — prevents false-merged data loss (CG-O7O9-5).

### WL-6.3 — Reconcile registry vs git state

```
FOR each entry in .aiox/worktrees/registry.json (if file exists):
  wt_exists = (entry.wt_path is in git worktree list output)
  branch_merged = (entry.branch is in git branch -r --merged origin/main output)

  IF wt_exists AND NOT branch_merged:
    → state remains "active" or "halted" (no change)

  IF NOT wt_exists AND NOT branch_merged:
    → flag "orphan" with note "worktree absent but branch unmerged"
    → NEVER auto-remove

  IF NOT wt_exists AND branch_merged:
    → flag "orphan-no-wt" (registry entry exists, branch merged, no worktree)
    → safe to clean up registry entry (not the branch)

  IF wt_exists AND branch_merged:
    → flag for teardown (WL-7 GC will handle)

FOR each worktree in git worktree list NOT in registry:
  IF it is NOT the main worktree:
    → register as "orphan" with halt_reason: "detected at reconciliation — not in registry"
    → LOG LOUD: "[WL-6 ORPHAN] Unregistered worktree detected: {path}"
```

### WL-6.4 — Report orphans to team-lead

```
IF any orphans detected:
  SendMessage(to: "team-lead", message: "[WL-6 ORPHAN REPORT] {N} orphan worktree(s) detected before starting story {story_id}:
    {list of orphan entries with path, branch, state}
    These are preserved. Run WL-7 GC to review and clean up.
    O7 story will proceed normally — orphan detection does not block execution.")
```

**CG-DEFER-2 / O9 compatibility:** registry.json schema `worktree-registry-v1` is compatible with O9 `epic-state-v1` (no schema conflict — separate files, separate fields).

---

## WL-7 — GC Idempotente

**Invocable standalone (at start of any full-sdc execution, or manually).**
**GC is idempotent: running multiple times produces the same result.**
**Invariant: NEVER destroy unmerged work without explicit team-lead confirmation.**

### WL-7.0 — Concurrent GC lock

```bash
# Lock file prevents concurrent GC runs
IF exists(".aiox/worktrees/gc.lock"):
  LOG LOUD: "[WL-7 ABORTED] Concurrent GC detected — .aiox/worktrees/gc.lock exists. Aborting. Another GC instance is running or a previous run did not clean up."
  → HALT WL-7 (do NOT proceed). User must remove stale lock manually.

ELSE:
  WRITE ".aiox/worktrees/gc.lock" with content: "gc_started: <ISO8601>\npid: <current process>\nstory_id: {story_id}"
```

### WL-7.1 — Fetch + gather state

```bash
git fetch origin
git worktree list --porcelain         # → active worktrees
git branch -r --merged origin/main    # → branches confirmed merged in origin (NEVER git branch --merged)
```

### WL-7.2 — M4 Reconstruction (registry absent)

```
IF .aiox/worktrees/registry.json absent:
  LOG: "[WL-7] Registry absent — reconstructing from git worktree list --porcelain (M4)."
  FOR each worktree (non-main):
    REGISTER as "orphan" with halt_reason: "reconstructed by WL-7 M4 — state unknown"
  WRITE .aiox/worktrees/registry.json
```

### WL-7.3 — Process each registry entry

```
FOR each entry in registry:

  branch_merged_remote = (entry.branch in `git branch -r --merged origin/main`)
  wt_exists = (entry.wt_path in `git worktree list --porcelain`)

  CASE: branch_merged_remote AND wt_exists
    → Safe to teardown (confirmed merged in origin — not just local)
    → Execute: git worktree remove {entry.wt_path}
               git branch -d {entry.branch}
               git worktree prune
    → UPDATE registry: state = "merged", last_seen = <ISO8601>
    → LOG: "[WL-7 GC] Removed merged worktree: {entry.wt_path} (branch: {entry.branch})"

  CASE: branch_merged_remote AND NOT wt_exists
    → Registry stale entry (worktree already removed, branch merged)
    → UPDATE registry: state = "merged", last_seen = <ISO8601>
    → LOG: "[WL-7 GC] Stale registry entry cleaned: {entry.story_id}"

  CASE: NOT branch_merged_remote AND wt_exists
    → Work NOT merged — preserve. Flag orphan if unregistered.
    → IF state == "active": no change (legitimate in-progress)
    → IF state == "halted": no change (preserved for debug per WL-4)
    → IF age_days > TK-SDC-WORKTREE-STALE-DAYS: flag "stale" + report
    → NEVER auto-remove

  CASE: NOT branch_merged_remote AND NOT wt_exists
    → Branch exists locally but no worktree → "orphan-no-wt"
    → UPDATE registry: state = "orphan-no-wt"
    → LOG: "[WL-7] Orphan-no-wt: {entry.branch} (branch exists, no worktree, not merged)"
    → PRESERVE branch (do not delete)
```

### WL-7.4 — 3 Negative Test Cases (CG-O7O9-5 — NON-NEGOTIABLE)

**(a) Local-merged-not-origin:** Branch merged locally (via `git merge`) but NOT in `git branch -r --merged origin/main`.
→ WL-7 MUST NOT flag as merged. `branch_merged_remote` check uses `-r` flag — local merge is NOT sufficient.
→ Behavior: state remains "active" or "halted". No teardown.

**(b) HEAD detached:** Worktree in detached HEAD state (no branch reference).
→ `git worktree list --porcelain` returns `detached` for HEAD.
→ WL-7 flags as `orphan` with `halt_reason: "detached HEAD"` and reports — NEVER removes automatically.

**(c) Concurrent GC lock:** Second GC invocation while first is running.
→ WL-7.0 detects `.aiox/worktrees/gc.lock` → LOUD WARNING → ABORT.
→ Never execute two GC instances simultaneously. Never silent skip.

### WL-7.5 — Release lock + summary

```bash
REMOVE ".aiox/worktrees/gc.lock"

LOG: "[WL-7 GC Complete] Removed: {merged_count} | Preserved: {active_count} | Orphans: {orphan_count} | Stale: {stale_count}"
```

IF any orphans or stale entries:
  ```
  SendMessage(to: "team-lead", message: "[WL-7 GC REPORT] {N} worktrees require attention:
    Orphans: {list}
    Stale (>{TK-SDC-WORKTREE-STALE-DAYS}d): {list}
    These are PRESERVED. Confirm removal before next GC run.")
  ```

---
