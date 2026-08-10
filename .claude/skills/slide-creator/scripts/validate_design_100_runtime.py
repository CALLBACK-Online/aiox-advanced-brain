#!/usr/bin/env python3
"""
validate_design_100_runtime.py — Design 100 executable gate.

Bridges the runtime artifacts produced by slides-renderer (`deck.ir.json`,
`editability-report.json`) with the canonical design contracts shipped in this
skill (`templates/visual/design-mastery-contract.yaml`,
`templates/visual/brand-template-manifest.yaml`,
`templates/visual/key-slide-render-review.yaml`,
`templates/visual/visual-regression-checklist.yaml`).

Verdict policy
--------------
A deck is allowed to claim Design 100 only when ALL of the following hold:
  - editability_score >= 95 AND editability_report.verdict == PASS
  - 5 key slides present in the IR: cover, reframe, mechanism, proof (or demo),
    cta (these are the canonical decision slides from key-slide-render-review).
  - brand-template-manifest.yaml exists alongside the run artifacts.
  - design-mastery-report.yaml emitted by this script does NOT report blockers.
  - visual-regression checklist passes (overflow, contrast, density, palette
    consistency, native overlays).

The script is intentionally conservative — it refuses Design 100 when any signal
is missing, per .claude/rules/extraction-no-fallbacks.md (no universal defaults).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - import guard
    print("ERROR: PyYAML not available. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(3)


CANONICAL_KEY_FUNCTIONS = ("cover", "reframe", "mechanism", "proof", "cta")
DENSITY_WORD_LIMIT = 45

# ── Cross-fit bench absorption (impeccable + tasteskill) ────────────────────
# Authority: .claude/rules/design-absolute-bans.md
# Bench source: docs/bench/2026-05-18-impeccable-vs-sinkra-design-stack/

# Font canon (mirror of squads/design-ops/data/font-allowlist.yaml)
FONT_BLOCKLIST_BRAND_REGISTER = {"Inter", "Inter Tight", "Mona Sans", "Plus Jakarta Sans", "Space Grotesk", "Instrument Sans"}
FONT_BLOCKLIST_ALL_REGISTERS = {"Fraunces", "Recoleta"}  # italic-serif hero AI fingerprint
FONT_ALLOWLIST_SANS = {"Geist", "Outfit", "Cabinet Grotesk", "Satoshi"}
FONT_ALLOWLIST_MONO = {"Geist Mono", "JetBrains Mono", "IBM Plex Mono"}

# Jane Doe Effect content patterns
import re
JANE_DOE_REGEX = re.compile(r"\b(John|Jane)\s+Doe\b|\bSarah\s+(Chen|Chan)\b|\bJack\s+Su\b|\b(Test|Demo|Example|Lorem)\s+(User|Person)\b", re.IGNORECASE)
STARTUP_SLOP_REGEX = re.compile(r"\b(Acme(\s+(Corp|Inc))?|Nexus|SmartFlow|FlowSync|DataSync|ExampleCo|TestCo|StartupCo|TechFlow|CloudSync|AISync|TechCorp|GenericCo)\b")
FILLER_WORD_REGEX = re.compile(r"\b(elevate|unlock|unleash|empower|streamline|seamless|next[\s-]gen|best[\s-]in[\s-]class|world[\s-]class|industry[\s-]leading|revolutionary|disruptive|cutting[\s-]edge|state[\s-]of[\s-]the[\s-]art|game[\s-]chang(er|ing)|innovative)\b", re.IGNORECASE)
FAKE_NUMBER_PCT_REGEX = re.compile(r"\b(99\.99|99,99|50|100)\s*%")
EM_DASH_REGEX = re.compile(r"—|–|--")
LOREM_IPSUM_REGEX = re.compile(r"\bLorem\s+ipsum\b|\bdolor\s+sit\s+amet\b", re.IGNORECASE)

# 8 absolute bans — visual / CSS-level (best-effort detection in deck IR)
SIDE_STRIPE_REGEX = re.compile(r"border-(left|right):\s*[2-9][\d]?px\s+(solid|dashed|dotted)", re.IGNORECASE)
GRADIENT_TEXT_REGEX = re.compile(r"background-clip:\s*text|-webkit-background-clip:\s*text", re.IGNORECASE)
PURE_BLACK_WHITE_REGEX = re.compile(r"#000000?\b|#FFF(FFF)?\b", re.IGNORECASE)


@dataclass
class Finding:
    code: str
    severity: str  # "BLOCKER" | "OBSERVATION"
    message: str


@dataclass
class Report:
    run_id: str
    evaluated_at: str
    editability_score: int
    findings: list[Finding] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)
    verdict: str = "UNKNOWN"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def find_run_dir(arg: str) -> Path:
    p = Path(arg).expanduser().resolve()
    if not p.exists():
        raise SystemExit(f"run dir not found: {p}")
    return p


def collect_text(slide: dict[str, Any]) -> str:
    """Flatten all text in a slide for density/coverage analysis."""
    chunks: list[str] = [slide.get("action_title", "")]

    def walk(node: dict[str, Any]) -> None:
        if not isinstance(node, dict):
            return
        if node.get("type") == "text":
            for run in node.get("runs", []) or []:
                chunks.append(str(run.get("text", "")))
        elif node.get("type") == "shape" and node.get("text"):
            walk(node["text"])
        elif node.get("type") == "group":
            for child in node.get("children", []) or []:
                walk(child)
        elif node.get("type") == "table":
            for row in node.get("rows", []) or []:
                for cell in row.get("cells", []) or []:
                    chunks.append(str(cell.get("text", "")))

    for node in slide.get("nodes", []) or []:
        walk(node)
    return "\n".join(chunks)


def score_key_slides(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Verify the 5 decisive slides are present and well-formed."""
    present = {s.get("function") for s in ir.get("slides", [])}
    missing = [f for f in CANONICAL_KEY_FUNCTIONS if f not in present and f != "proof"]
    # proof OR demo OR demo_setup counts as the proof slot
    proof_alt = {"proof", "demo", "demo_setup"} & present
    if not proof_alt:
        missing.append("proof|demo|demo_setup")
    if missing:
        findings.append(
            Finding(
                code="KEY_SLIDES_MISSING",
                severity="BLOCKER",
                message=f"Missing key slide functions: {sorted(missing)}.",
            )
        )
        return 0
    return 100


def score_density(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Detect overflow / wall-of-text per slide."""
    violations: list[str] = []
    for slide in ir.get("slides", []) or []:
        if slide.get("function") in ("appendix", "summary"):
            continue
        text = collect_text(slide)
        words = len([w for w in text.split() if w.strip()])
        if words > DENSITY_WORD_LIMIT:
            violations.append(f"{slide.get('id')} ({words} words)")
    if violations:
        findings.append(
            Finding(
                code="DENSITY_OVER_LIMIT",
                severity="OBSERVATION",
                message=f"Slides exceeding {DENSITY_WORD_LIMIT}-word density: {violations}.",
            )
        )
        return max(0, 100 - 8 * len(violations))
    return 100


def score_palette(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Brand fidelity heuristic — every color used in the IR must come from the theme palette."""
    theme = ir.get("theme", {}) or {}
    palette = theme.get("palette", {}) or {}
    allowed = set()
    for key, value in palette.items():
        if isinstance(value, str):
            allowed.add(value.lower())
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, str):
                    allowed.add(v.lower())
    allowed.add("#ffffff")
    allowed.add("#000000")

    leaks: list[tuple[str, str]] = []

    def visit(slide_id: str, node: dict[str, Any]) -> None:
        if not isinstance(node, dict):
            return
        for color_key in ("fill", "stroke"):
            color = node.get(color_key)
            if isinstance(color, str) and color.lower() not in allowed:
                leaks.append((slide_id, color))
        if node.get("type") == "text":
            for run in node.get("runs", []) or []:
                color = run.get("color")
                if isinstance(color, str) and color.lower() not in allowed:
                    leaks.append((slide_id, color))
        if node.get("type") == "shape" and node.get("text"):
            visit(slide_id, node["text"])
        if node.get("type") == "group":
            for child in node.get("children", []) or []:
                visit(slide_id, child)

    for slide in ir.get("slides", []) or []:
        for node in slide.get("nodes", []) or []:
            visit(slide.get("id", "?"), node)

    if leaks:
        sample = leaks[:5]
        findings.append(
            Finding(
                code="PALETTE_DRIFT",
                severity="OBSERVATION",
                message=f"{len(leaks)} non-theme colors used (sample: {sample}).",
            )
        )
        return max(0, 100 - 6 * len(leaks))
    return 100


def score_overlap(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Trivial rectangle overlap detector inside each slide (heuristic, not authoritative)."""
    issues = 0
    for slide in ir.get("slides", []) or []:
        boxes: list[tuple[int, int, int, int, str]] = []

        def collect(node: dict[str, Any]) -> None:
            if not isinstance(node, dict):
                return
            box = node.get("box")
            if isinstance(box, dict) and node.get("type") in ("text", "shape", "image", "table", "chart"):
                boxes.append(
                    (
                        int(box.get("x", 0)),
                        int(box.get("y", 0)),
                        int(box.get("x", 0)) + int(box.get("w", 0)),
                        int(box.get("y", 0)) + int(box.get("h", 0)),
                        str(node.get("id", "")),
                    )
                )
            if node.get("type") == "group":
                for child in node.get("children", []) or []:
                    collect(child)

        for node in slide.get("nodes", []) or []:
            collect(node)
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]:
                    continue
                # Allow fully-contained children (group/parent semantics).
                contained = (
                    (a[0] <= b[0] and a[1] <= b[1] and a[2] >= b[2] and a[3] >= b[3])
                    or (b[0] <= a[0] and b[1] <= a[1] and b[2] >= a[2] and b[3] >= a[3])
                )
                if contained:
                    continue
                issues += 1
    if issues > 0:
        findings.append(
            Finding(
                code="OVERLAP_DETECTED",
                severity="OBSERVATION",
                message=f"{issues} potential overlapping rectangles (heuristic).",
            )
        )
    return max(0, 100 - 5 * issues)


# ── Cross-fit absorption scorers (font allowlist, 8 bans, Jane Doe) ────────

def score_font_monoculture(run_dir: Path, ir: dict[str, Any], findings: list[Finding]) -> int:
    """Validate render-lock fonts against canonical allowlist.

    Returns 0-100 score. P0/P1 hits become BLOCKER/OBSERVATION findings.
    Authority: .claude/rules/design-absolute-bans.md §1
    """
    render_lock_path = run_dir / "render-lock.yaml"
    if not render_lock_path.exists():
        findings.append(Finding(
            code="MISSING_RENDER_LOCK",
            severity="OBSERVATION",
            message=f"render-lock.yaml not found at {render_lock_path}; font monoculture cannot be enforced.",
        ))
        return 50

    try:
        lock = load_yaml(render_lock_path) or {}
    except Exception as exc:
        findings.append(Finding(
            code="RENDER_LOCK_PARSE_ERROR",
            severity="BLOCKER",
            message=f"failed to parse render-lock.yaml: {exc}",
        ))
        return 0

    typo = lock.get("typography", {}) or {}
    register = (ir.get("briefing", {}) or {}).get("register", "unknown")

    heading = typo.get("heading_family", "")
    body = typo.get("body_family", "")
    mono = typo.get("mono_family", "")

    score = 100
    for slot, font in (("heading", heading), ("body", body)):
        if not font:
            continue
        if font in FONT_BLOCKLIST_ALL_REGISTERS:
            findings.append(Finding(
                code="FONT_BLOCKLIST_ITALIC_SERIF",
                severity="BLOCKER",
                message=f"render-lock.{slot}_family={font!r} is on the italic-serif hero blocklist (AI fingerprint). Replace with brand-extracted serif or sans from allowlist.",
            ))
            score -= 40
        elif register in {"brand", "pitch", "marketing", "creative"} and font in FONT_BLOCKLIST_BRAND_REGISTER:
            findings.append(Finding(
                code=f"FONT_BLOCKLIST_BRAND_REGISTER_{slot.upper()}",
                severity="BLOCKER",
                message=f"render-lock.{slot}_family={font!r} is banned in {register} register (AI monoculture). Use Geist|Outfit|Cabinet Grotesk|Satoshi.",
            ))
            score -= 30
        elif font not in FONT_ALLOWLIST_SANS:
            findings.append(Finding(
                code=f"FONT_OFF_ALLOWLIST_{slot.upper()}",
                severity="OBSERVATION",
                message=f"render-lock.{slot}_family={font!r} not in canonical allowlist (Geist|Outfit|Cabinet Grotesk|Satoshi). May still be valid if from extracted brand DNA.",
            ))
            score -= 5

    if mono and mono not in FONT_ALLOWLIST_MONO:
        findings.append(Finding(
            code="FONT_MONO_OFF_ALLOWLIST",
            severity="OBSERVATION",
            message=f"render-lock.mono_family={mono!r} not in canonical mono allowlist (Geist Mono|JetBrains Mono|IBM Plex Mono).",
        ))
        score -= 5

    return max(0, score)


def score_eight_bans(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Detect 8 absolute design bans in deck IR.

    Authority: .claude/rules/design-absolute-bans.md §2 (ban_01-ban_08)
    """
    slides = ir.get("slides", []) or []
    score = 100

    for slide in slides:
        sid = slide.get("id", "?")
        text = collect_text(slide)
        css = json.dumps(slide.get("styles", {})) + " " + json.dumps(slide.get("css", {}))

        # ban_01 — side-stripe borders >1px colored
        if SIDE_STRIPE_REGEX.search(css):
            findings.append(Finding(
                code=f"BAN_01_SIDE_STRIPE_BORDERS:{sid}",
                severity="BLOCKER",
                message=f"slide {sid}: side-stripe border >1px detected (ban_01). Replace with full border or background tint.",
            ))
            score -= 12

        # ban_02 — gradient text
        if GRADIENT_TEXT_REGEX.search(css):
            findings.append(Finding(
                code=f"BAN_02_GRADIENT_TEXT:{sid}",
                severity="BLOCKER",
                message=f"slide {sid}: background-clip:text + gradient detected (ban_02). Use single solid color + weight/size emphasis.",
            ))
            score -= 12

        # ban_07 — em dashes
        if EM_DASH_REGEX.search(text):
            findings.append(Finding(
                code=f"BAN_07_EM_DASHES:{sid}",
                severity="OBSERVATION",
                message=f"slide {sid}: em-dash or '--' detected in copy (ban_07). Use commas, colons, semicolons, periods, or parentheses.",
            ))
            score -= 6

        # ban_08 — pure #000 / #fff
        if PURE_BLACK_WHITE_REGEX.search(css):
            findings.append(Finding(
                code=f"BAN_08_PURE_BW:{sid}",
                severity="OBSERVATION",
                message=f"slide {sid}: pure #000 or #fff detected (ban_08). Tint neutrals to brand hue (min_chroma 0.005).",
            ))
            score -= 4

    return max(0, score)


def score_jane_doe(ir: dict[str, Any], findings: list[Finding]) -> int:
    """Detect Jane Doe Effect content patterns in deck IR.

    Authority: .claude/rules/design-absolute-bans.md §5
    """
    slides = ir.get("slides", []) or []
    score = 100

    for slide in slides:
        sid = slide.get("id", "?")
        text = collect_text(slide)

        if JANE_DOE_REGEX.search(text):
            m = JANE_DOE_REGEX.search(text)
            findings.append(Finding(
                code=f"JANE_DOE_GENERIC_NAME:{sid}",
                severity="BLOCKER",
                message=f"slide {sid}: generic AI placeholder name detected ({m.group(0)!r}). Use real or [TESTIMONIAL_PENDING — collect from {{source}}].",
            ))
            score -= 15

        if STARTUP_SLOP_REGEX.search(text):
            m = STARTUP_SLOP_REGEX.search(text)
            findings.append(Finding(
                code=f"JANE_DOE_STARTUP_SLOP:{sid}",
                severity="BLOCKER",
                message=f"slide {sid}: startup-slop company name detected ({m.group(0)!r}). Replace with real customer name or [CASE_STUDY_PENDING].",
            ))
            score -= 15

        if FAKE_NUMBER_PCT_REGEX.search(text):
            m = FAKE_NUMBER_PCT_REGEX.search(text)
            findings.append(Finding(
                code=f"JANE_DOE_FAKE_NUMBER:{sid}",
                severity="OBSERVATION",
                message=f"slide {sid}: round/lazy percentage detected ({m.group(0)!r}). Use organic figure (e.g. 47.2% with source).",
            ))
            score -= 6

        if LOREM_IPSUM_REGEX.search(text):
            findings.append(Finding(
                code=f"JANE_DOE_LOREM_IPSUM:{sid}",
                severity="BLOCKER",
                message=f"slide {sid}: Lorem ipsum placeholder detected. Replace with real copy or [TODO: copy from {{source}}].",
            ))
            score -= 20

        # Filler words: only OBSERVATION (depends on context)
        filler_hits = FILLER_WORD_REGEX.findall(text)
        if len(filler_hits) >= 3:
            findings.append(Finding(
                code=f"JANE_DOE_FILLER_HEAVY:{sid}",
                severity="OBSERVATION",
                message=f"slide {sid}: {len(filler_hits)} filler word hits detected (Elevate/Unleash/Seamless/etc). Replace with concrete verb + number.",
            ))
            score -= 4

    return max(0, score)


def score_persona_walkthrough(run_dir: Path, findings: list[Finding]) -> int:
    """Read qa/persona-walkthrough-report.yaml if present and bubble up its verdict."""
    report_path = run_dir / "qa" / "persona-walkthrough-report.yaml"
    if not report_path.exists():
        findings.append(Finding(
            code="MISSING_PERSONA_WALKTHROUGH",
            severity="OBSERVATION",
            message=f"persona-walkthrough-report.yaml not found at {report_path}; persona red-flag review not run.",
        ))
        return 60

    try:
        report = load_yaml(report_path) or {}
    except Exception as exc:
        findings.append(Finding(
            code="PERSONA_WALKTHROUGH_PARSE_ERROR",
            severity="OBSERVATION",
            message=f"failed to parse persona-walkthrough-report.yaml: {exc}",
        ))
        return 50

    body = report.get("persona_walkthrough", report)
    p0 = int(body.get("p0_count", 0))
    p1 = int(body.get("p1_count", 0))
    if body.get("blocking"):
        findings.append(Finding(
            code="PERSONA_WALKTHROUGH_BLOCKING",
            severity="BLOCKER",
            message=f"persona walkthrough blocked: {p0} P0 + {p1} P1 red flags.",
        ))
        return max(0, 100 - p0 * 20 - p1 * 5)
    return max(0, 100 - p0 * 15 - p1 * 4)


def evaluate(run_dir: Path) -> Report:
    ir_path = run_dir / "deck.ir.json"
    edit_path = run_dir / "editability-report.json"
    manifest_path = run_dir / "brand-template-manifest.yaml"

    if not ir_path.exists():
        raise SystemExit(f"missing artifact: {ir_path}")
    ir = load_json(ir_path)

    findings: list[Finding] = []

    editability_score = 0
    if edit_path.exists():
        edit = load_json(edit_path)
        editability_score = int(edit.get("editability_score", 0))
        if edit.get("verdict") != "PASS":
            findings.append(
                Finding(
                    code="EDITABILITY_NOT_PASS",
                    severity="BLOCKER",
                    message=f"Editability verdict {edit.get('verdict')!r}; required PASS for Design 100.",
                )
            )
    else:
        findings.append(
            Finding(
                code="MISSING_EDITABILITY_REPORT",
                severity="BLOCKER",
                message=f"editability-report.json not found at {edit_path}.",
            )
        )

    if not manifest_path.exists():
        findings.append(
            Finding(
                code="MISSING_BRAND_MANIFEST",
                severity="OBSERVATION",
                message=f"brand-template-manifest.yaml not found at {manifest_path}; brand fidelity unproven.",
            )
        )

    scores = {
        "editability": editability_score,
        "key_slides": score_key_slides(ir, findings),
        "density": score_density(ir, findings),
        "palette": score_palette(ir, findings),
        "overlap": score_overlap(ir, findings),
        # Cross-fit absorption (bench: impeccable + tasteskill)
        "font_monoculture": score_font_monoculture(run_dir, ir, findings),
        "eight_bans": score_eight_bans(ir, findings),
        "jane_doe": score_jane_doe(ir, findings),
        "persona_walkthrough": score_persona_walkthrough(run_dir, findings),
    }
    overall = round(sum(scores.values()) / len(scores))
    blockers = [f for f in findings if f.severity == "BLOCKER"]

    if blockers or overall < 95:
        verdict = "DESIGN_LT_100"
    else:
        verdict = "DESIGN_100"

    return Report(
        run_id=str(run_dir.name),
        evaluated_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z"),
        editability_score=editability_score,
        findings=findings,
        scores=scores | {"overall": overall},
        verdict=verdict,
    )


def write_report(run_dir: Path, report: Report) -> Path:
    out_path = run_dir / "design-mastery-report.yaml"
    payload = {
        "schema_version": "1.0.0",
        "run_id": report.run_id,
        "evaluated_at": report.evaluated_at,
        "editability_score": report.editability_score,
        "scores": report.scores,
        "findings": [
            {"code": f.code, "severity": f.severity, "message": f.message}
            for f in report.findings
        ],
        "verdict": report.verdict,
    }
    with out_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, sort_keys=False)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="SINKRA Design 100 runtime gate.")
    parser.add_argument(
        "run_dir",
        help="Path to the run workspace, e.g. outputs/slides-creator/{run_id}/",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when verdict != DESIGN_100.",
    )
    args = parser.parse_args()

    run_dir = find_run_dir(args.run_dir)
    report = evaluate(run_dir)
    out_path = write_report(run_dir, report)
    print(
        json.dumps(
            {
                "verdict": report.verdict,
                "overall": report.scores.get("overall"),
                "editability_score": report.editability_score,
                "report_path": str(out_path),
                "blockers": [f.message for f in report.findings if f.severity == "BLOCKER"],
            },
            indent=2,
        )
    )
    if args.strict and report.verdict != "DESIGN_100":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
