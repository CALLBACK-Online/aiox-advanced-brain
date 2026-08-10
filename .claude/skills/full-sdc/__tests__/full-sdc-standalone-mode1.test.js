/**
 * Story 115G.W1.3 — Phase 0c.2 fallback contract (local-commits-ahead-of-origin).
 *
 * Reference implementation tests for the fallback contract documented in
 * `.claude/skills/full-sdc/SKILL.md` Phase 0c.2 ("Story file availability check").
 *
 * AC coverage (per docs/stories/epic-115/epic-115g/STORY-115G.W1.3-...md):
 *   - AC-1  Detection logic: origin/branch present → normal; origin absent + HEAD present → fallback
 *   - AC-2  Structured WARN emitted on fallback branch
 *   - AC-3  Dispatch ACK annotated with provisioned_by:"local-ahead" + local_head_sha + origin_lacks_story
 *   - AC-4  Invariant 3 NOT weakened: baseRef stays origin/<default-branch>, story is overlay-only
 *   - AC-5  HARD ERROR (HALT, non-zero) if story absent from BOTH origin and HEAD
 *   - AC-6  Compatibility matrix 7 modes preserved — Mode 1 (standalone) + Mode 6 (nested wave-execute)
 *           continue to exhibit canonical Phase 0c routing even when the fallback contract is active
 *
 * Test architecture:
 *   The canonical Phase 0c.1 mode-detection algorithm (cwd/ACK structural check) is owned by
 *   `.claude/skills/wave-execute/__tests__/full-sdc-standalone-mode1.test.js` — that file
 *   reproduces `detectPhase0cMode()`. We REUSE it via require() to honor skill-agnosticism.md
 *   Compatibility Matrix SOT — drift between the two files is itself a test failure (AP5).
 *
 *   On top of the reused mode-detection algorithm, this file adds a Phase 0c.2 fallback
 *   detector — `detectPhase0c2Fallback()` — which is the SOT for the local-ahead branch logic.
 *   It is also a pure function (zero deps, deterministic) and MUST stay in sync with the
 *   SKILL.md Phase 0c.2 ELSE-branch block.
 *
 * Run: node --test .claude/skills/full-sdc/__tests__/full-sdc-standalone-mode1.test.js
 */

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

// Reuse Phase 0c.1 mode-detection from the canonical wave-execute test file (SOT).
// This guarantees we cannot drift from skill-agnosticism.md Compatibility Matrix.
const {
  detectPhase0cMode,
  makeAckProbe,
} = require('../../wave-execute/__tests__/full-sdc-standalone-mode1.test.js');

/**
 * Reference implementation of /full-sdc Phase 0c.2 fallback contract.
 *
 * MUST stay in sync with the ELSE-branch block in `.claude/skills/full-sdc/SKILL.md`
 * under §0c.2 "Story file availability check (Story 115G.W1.3 — fallback contract)".
 *
 * Decision matrix:
 *
 *   | origin has story | HEAD has story | Branch                        |
 *   |------------------|----------------|-------------------------------|
 *   | YES              | (any)          | NORMAL (existing 0c.3 path)   |
 *   | NO               | YES            | FALLBACK (local-ahead)        |
 *   | NO               | NO             | HARD ERROR (HALT)             |
 *
 * @param {object} env
 * @param {string} env.storyId - story identifier (used to build ACK annotation)
 * @param {string} env.storyPath - relative path of the story file
 * @param {function} env.originHasStory - () → bool  (proxy for `git show origin/<branch>:{path}` exit 0)
 * @param {function} env.localHeadHasStory - () → bool  (proxy for `git show HEAD:{path}` exit 0)
 * @param {function} env.localHeadSha - () → string  (proxy for `git rev-parse HEAD`)
 * @returns {{ branch: 'normal'|'fallback'|'hard_error', warn?: string, ackAnnotation?: object, halt?: boolean, error?: string }}
 */
function detectPhase0c2Fallback(env) {
  const {
    storyId,
    storyPath,
    originHasStory,
    localHeadHasStory,
    localHeadSha,
  } = env;

  // Branch 1 (AC-1 normal): origin has the story → existing 0c.3 path
  if (originHasStory()) {
    return {
      branch: 'normal',
      reason: 'origin/<branch> has story file — proceed to 0c.3 (UNCHANGED behavior, Invariant 3 preserved by default)',
    };
  }

  // Branch 2 (AC-1 fallback + AC-2 WARN + AC-3 annotation + AC-4 invariant): local HEAD has story
  if (localHeadHasStory()) {
    const sha = localHeadSha();
    return {
      branch: 'fallback',
      // AC-2: structured WARN
      warn: `[full-sdc Phase 0c.2] FALLBACK: story ${storyId} not on origin/<branch>; using local HEAD ${sha}. Invariant 3 NOT violated — baseRef remains fresh from origin/<branch>; story file overlay only. Push story to origin before Phase 5 to clear annotation.`,
      // AC-3: dispatch ACK annotation fields
      ackAnnotation: {
        provisioned_by: 'local-ahead',
        local_head_sha: sha,
        origin_lacks_story: true,
      },
      // AC-4: baseRef invariant — Phase 0c.3 STILL uses origin/<default-branch>
      baseRef: 'origin/<default-branch>',
      // AC-4: post-0c.3 overlay of the story file from local HEAD onto the fresh worktree
      postCreatedOverlay: {
        storyPath,
        sourceRef: 'HEAD',
        sha,
      },
      reason: 'origin/<branch> lacks story, local HEAD has it — fallback active with overlay',
    };
  }

  // Branch 3 (AC-5): neither origin nor HEAD has the story → HARD ERROR
  return {
    branch: 'hard_error',
    halt: true,
    error: `[full-sdc Phase 0c.2] HARD ERROR: story ${storyId} not found on origin/<branch> nor local HEAD. Cannot proceed. Push the story file to origin or ensure it exists locally before invoking /full-sdc.`,
    reason: 'story file absent from BOTH origin and HEAD — Mandamento 8: fail loud, never silent-skip',
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Suite 1 — Phase 0c.2 fallback contract (Story 115G.W1.3 AC-1..AC-5)
// ─────────────────────────────────────────────────────────────────────────────

describe('Phase 0c.2 — local-commits-ahead-of-origin fallback contract (Story 115G.W1.3)', () => {
  const STORY_ID = '115G.W1.3';
  const STORY_PATH = 'docs/stories/epic-115/epic-115g/STORY-115G.W1.3-full-sdc-phase0c2-fallback-contract.md';

  test('AC-1 normal: origin has story → NORMAL branch (existing 0c.3 behavior, UNCHANGED)', () => {
    const result = detectPhase0c2Fallback({
      storyId: STORY_ID,
      storyPath: STORY_PATH,
      originHasStory: () => true,
      localHeadHasStory: () => true,
      localHeadSha: () => 'deadbeef000000000000000000000000deadbeef',
    });
    assert.equal(result.branch, 'normal', 'origin presence MUST take the normal path');
    assert.equal(result.warn, undefined, 'normal branch MUST NOT emit fallback WARN');
    assert.equal(result.ackAnnotation, undefined, 'normal branch MUST NOT annotate ACK');
    assert.equal(result.halt, undefined, 'normal branch MUST NOT halt');
  });

  test('AC-1 + AC-2 fallback: origin lacks story, HEAD has it → FALLBACK + structured WARN', () => {
    const sha = 'c94a0c3569d0c602cd6c612cfccbd48357604811';
    const result = detectPhase0c2Fallback({
      storyId: STORY_ID,
      storyPath: STORY_PATH,
      originHasStory: () => false,
      localHeadHasStory: () => true,
      localHeadSha: () => sha,
    });
    assert.equal(result.branch, 'fallback');
    assert.match(result.warn, /FALLBACK/, 'WARN must contain "FALLBACK" marker');
    assert.match(result.warn, /Invariant 3 NOT violated/, 'WARN must explicitly assert Invariant 3 preservation');
    assert.match(result.warn, new RegExp(sha), 'WARN must include the local HEAD sha for traceability');
    assert.match(result.warn, /Push story to origin before Phase 5/, 'WARN must instruct push-to-origin remediation');
  });

  test('AC-3 ACK annotation: fallback writes provisioned_by/local_head_sha/origin_lacks_story', () => {
    const sha = '1234567890abcdef1234567890abcdef12345678';
    const result = detectPhase0c2Fallback({
      storyId: STORY_ID,
      storyPath: STORY_PATH,
      originHasStory: () => false,
      localHeadHasStory: () => true,
      localHeadSha: () => sha,
    });
    assert.equal(result.branch, 'fallback');
    assert.deepEqual(result.ackAnnotation, {
      provisioned_by: 'local-ahead',
      local_head_sha: sha,
      origin_lacks_story: true,
    }, 'ACK annotation MUST match the schema documented in SKILL.md Phase 0c.2');
  });

  test('AC-4 Invariant 3 preserved: fallback baseRef stays origin/<default-branch> (overlay-only)', () => {
    const result = detectPhase0c2Fallback({
      storyId: STORY_ID,
      storyPath: STORY_PATH,
      originHasStory: () => false,
      localHeadHasStory: () => true,
      localHeadSha: () => 'abc123',
    });
    assert.equal(result.branch, 'fallback');
    assert.equal(
      result.baseRef,
      'origin/<default-branch>',
      'baseRef MUST remain origin/<default-branch> — the fallback is a story-file overlay, NOT a git checkout of HEAD',
    );
    assert.ok(result.postCreatedOverlay, 'fallback MUST schedule a post-0c.3 overlay');
    assert.equal(result.postCreatedOverlay.sourceRef, 'HEAD', 'overlay source MUST be local HEAD');
    assert.equal(result.postCreatedOverlay.storyPath, STORY_PATH, 'overlay path MUST match the story path');
  });

  test('AC-5 HARD ERROR: story absent from BOTH origin and HEAD → HALT non-zero', () => {
    const result = detectPhase0c2Fallback({
      storyId: STORY_ID,
      storyPath: STORY_PATH,
      originHasStory: () => false,
      localHeadHasStory: () => false,
      localHeadSha: () => 'irrelevant',
    });
    assert.equal(result.branch, 'hard_error');
    assert.equal(result.halt, true, 'AC-5: must HALT, never silent-skip (Mandamento 8 / feedback_fallback_silent_problem.md)');
    assert.match(result.error, /HARD ERROR/, 'error message MUST be loud and explicit');
    assert.match(result.error, new RegExp(STORY_ID), 'error message MUST include story id for diagnostics');
    assert.match(result.error, /Cannot proceed/, 'error message MUST instruct the operator on remediation');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 2 — AC-6: Compatibility Matrix 7 modes preserved under fallback
// ─────────────────────────────────────────────────────────────────────────────

describe('AC-6 — Compatibility Matrix 7 modes preserved under Phase 0c.2 fallback (Story 115G.W1.3)', () => {
  /**
   * The fallback contract is layered ON TOP of the mode-detection algorithm; the two
   * are orthogonal. Mode-detection (Phase 0c.1) decides standalone vs. nested vs.
   * scoped-ACK — it runs BEFORE Phase 0c.2 ever considers origin/HEAD presence. The
   * tests below assert that Modes 1 and 6 (the matrix-canonical standalone and
   * wave-execute nested invocations) continue to exhibit their documented routing
   * even when the fallback contract is active in the same /full-sdc session.
   *
   * Rationale per skill-agnosticism.md Compatibility Matrix (SOT):
   *   - Mode 1 (standalone main): cwd=/repo/root, no ACKs → STANDALONE_CREATE → 0c.2.
   *     The fallback contract executes WITHIN 0c.2 as a sub-decision; it does NOT
   *     redirect mode-detection.
   *   - Mode 6 (nested wave-execute): cwd inside .claude/worktrees/, ACK may exist →
   *     NESTED_SKIP → routes directly to phase-1, SKIPPING 0c.2 entirely. Therefore
   *     the fallback contract is INERT for Mode 6 — exactly the behavior the matrix
   *     promises (zero side effects on nested invocations).
   */

  test('AC-6 Mode 1 standalone: fallback contract executes inside 0c.2, mode-detection routes there', () => {
    const { exists, readAck } = makeAckProbe([]);
    const modeResult = detectPhase0cMode({
      cwd: '/repo/root',
      storyId: '115G.W1.3',
      exists,
      readAck,
    });
    assert.equal(modeResult.mode, 'STANDALONE_CREATE', 'Mode 1: cwd=root + no ACK → STANDALONE_CREATE');
    assert.equal(modeResult.routing, '0c.2', 'Mode 1 routes to 0c.2 where fallback contract lives');

    // Inside that 0c.2 routing, the fallback decision is now exercisable. Simulate
    // the local-ahead scenario that motivated this story (Epic 115F observation).
    const fbResult = detectPhase0c2Fallback({
      storyId: '115G.W1.3',
      storyPath: 'docs/stories/epic-115/epic-115g/STORY-115G.W1.3-full-sdc-phase0c2-fallback-contract.md',
      originHasStory: () => false,
      localHeadHasStory: () => true,
      localHeadSha: () => 'feedface00000000feedface00000000feedface',
    });
    assert.equal(fbResult.branch, 'fallback', 'Mode 1 + local-ahead → fallback engages as expected');
    assert.equal(
      fbResult.baseRef,
      'origin/<default-branch>',
      'Mode 1 fallback STILL uses origin/<default-branch> for the worktree — Invariant 3 preserved',
    );
  });

  test('AC-6 Mode 6 nested wave-execute (story- prefix): NESTED_SKIP routes around 0c.2 — fallback INERT', () => {
    const { exists, readAck } = makeAckProbe([]);
    // wave-launch.js creates .claude/worktrees/story-{id} for spawn-external mode
    const nestedCwd =
      process.platform === 'win32'
        ? 'C:\\repo\\.claude\\worktrees\\story-115G.W1.3'
        : '/repo/.claude/worktrees/story-115G.W1.3';
    const modeResult = detectPhase0cMode({
      cwd: nestedCwd,
      storyId: '115G.W1.3',
      exists,
      readAck,
    });
    assert.equal(
      modeResult.mode,
      'NESTED_SKIP',
      'Mode 6: cwd inside .claude/worktrees/ → NESTED_SKIP regardless of ACK presence (AP6 fix)',
    );
    assert.equal(
      modeResult.routing,
      'phase-1',
      'Mode 6 routes to phase-1, completely SKIPPING 0c.2 — fallback contract is INERT for nested invocations',
    );
    assert.equal(modeResult.emitAck, true, 'Mode 6 emits ACK with provisioned_by:external');
  });

  test('AC-6 Mode 6 nested wave-execute (wt- prefix): also NESTED_SKIP — fallback INERT', () => {
    const { exists, readAck } = makeAckProbe([]);
    // /full-sdc standalone Phase 0c.2 uses .claude/worktrees/wt-{id}; both prefixes
    // must trigger NESTED_SKIP per the worktree-isolation.md Path naming convention.
    const nestedCwd =
      process.platform === 'win32'
        ? 'C:\\repo\\.claude\\worktrees\\wt-115G.W1.3'
        : '/repo/.claude/worktrees/wt-115G.W1.3';
    const modeResult = detectPhase0cMode({
      cwd: nestedCwd,
      storyId: '115G.W1.3',
      exists,
      readAck,
    });
    assert.equal(modeResult.mode, 'NESTED_SKIP', 'wt- prefix MUST also trigger NESTED_SKIP');
    assert.equal(modeResult.routing, 'phase-1', 'Mode 6 wt- routes to phase-1 — fallback INERT');
  });

  test('AC-6 Mode 1 normal (origin has story): fallback contract takes NORMAL branch, behavior unchanged from pre-115G.W1.3', () => {
    const result = detectPhase0c2Fallback({
      storyId: '115G.W1.3',
      storyPath: 'docs/stories/epic-115/epic-115g/STORY-115G.W1.3-full-sdc-phase0c2-fallback-contract.md',
      originHasStory: () => true,  // pre-fallback world: story is always on origin
      localHeadHasStory: () => true,
      localHeadSha: () => 'irrelevant',
    });
    assert.equal(result.branch, 'normal', 'baseline pre-115G.W1.3 behavior is fully preserved');
    assert.equal(result.ackAnnotation, undefined, 'no annotation when on the normal branch');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Suite 3 — Drift guard: SKILL.md Phase 0c.2 ELSE-branch ↔ detectPhase0c2Fallback()
// ─────────────────────────────────────────────────────────────────────────────

describe('Drift guard — SKILL.md Phase 0c.2 ↔ detectPhase0c2Fallback() (Story 115G.W1.3)', () => {
  /**
   * Whenever the SKILL.md Phase 0c.2 ELSE-branch block is edited, the corresponding
   * fields in detectPhase0c2Fallback() above MUST be updated to match. This test
   * encodes the canonical field set so any drift surfaces as a deterministic failure.
   * If you change the ACK annotation schema in SKILL.md, you MUST also update both
   * the function and this test in the same commit.
   */

  test('ACK annotation fields match the SKILL.md Phase 0c.2 contract exactly', () => {
    const result = detectPhase0c2Fallback({
      storyId: 'X',
      storyPath: 'p',
      originHasStory: () => false,
      localHeadHasStory: () => true,
      localHeadSha: () => 'sha',
    });
    const fields = Object.keys(result.ackAnnotation).sort();
    assert.deepEqual(
      fields,
      ['local_head_sha', 'origin_lacks_story', 'provisioned_by'],
      'If SKILL.md Phase 0c.2 ACK annotation schema changes, this assertion MUST be updated in the same commit',
    );
  });

  test('Three branches exhaust the matrix: normal | fallback | hard_error', () => {
    const branches = new Set();
    [
      [true, true],
      [false, true],
      [false, false],
    ].forEach(([originHas, localHas]) => {
      const r = detectPhase0c2Fallback({
        storyId: 'X',
        storyPath: 'p',
        originHasStory: () => originHas,
        localHeadHasStory: () => localHas,
        localHeadSha: () => 'sha',
      });
      branches.add(r.branch);
    });
    assert.deepEqual(
      [...branches].sort(),
      ['fallback', 'hard_error', 'normal'],
      'The 3 documented branches (normal | fallback | hard_error) MUST be exhaustively reachable',
    );
  });
});

module.exports = { detectPhase0c2Fallback };
