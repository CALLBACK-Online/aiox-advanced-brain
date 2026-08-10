#!/usr/bin/env python3
"""Offline intent→squad smoke test (mirrors validate-agent-routing.mjs scorer)."""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

# Maintainer tooling in dev/; router remains under the course package.
ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "cursos/AIOX-Advanced-Squads"
TOOLS = Path(__file__).resolve().parent
ROUTER = COURSE / "agent-router.json"
EVALS = TOOLS / "routing-evals.json"
LEGACY_CASES = TOOLS / "routing-cases.json"

router = json.loads(ROUTER.read_text(encoding="utf-8"))
evals = json.loads(EVALS.read_text(encoding="utf-8")) if EVALS.exists() else {"cases": []}
legacy = json.loads(LEGACY_CASES.read_text(encoding="utf-8")) if LEGACY_CASES.exists() else {"cases": []}
routes = router.get("routes") or []


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.lower()


def score_route(prompt: str, route: dict) -> float:
    normalized = normalize(prompt)
    score = 0.0
    for signal in route.get("signals") or []:
        candidate = normalize(str(signal))
        if candidate and candidate in normalized:
            score += 10 + len(candidate.split())
    for alias in route.get("aliases") or []:
        candidate = normalize(str(alias))
        if candidate and candidate in normalized:
            score += 8 + len(candidate.split())
    for signal in route.get("anti_signals") or []:
        candidate = normalize(str(signal))
        if candidate and candidate in normalized:
            score -= 12 + len(candidate.split())
    return score


def route_prompt(prompt: str) -> str:
    ranked = sorted(
        ((score_route(prompt, r), r["id"]) for r in routes),
        key=lambda item: (-item[0], item[1]),
    )
    return ranked[0][1] if ranked else ""


failed = 0
cases = list(evals.get("cases") or [])
# keep three classic prompts from the verdict if not already covered
for legacy_case in legacy.get("cases") or []:
    if not any(c.get("prompt") == legacy_case.get("prompt") for c in cases):
        cases.append(
            {
                "id": legacy_case["id"],
                "prompt": legacy_case["prompt"],
                "expected": legacy_case["expect_squad"],
                "forbidden": legacy_case.get("reject_squads") or [],
            }
        )

for case in cases:
    got = route_prompt(case["prompt"])
    exp = case["expected"]
    ok = got == exp
    if not ok:
        failed += 1
        print(f"FAIL {case['id']}: expected {exp}, got {got}")
    else:
        print(f"OK   {case['id']}: {got}")
    for bad in case.get("forbidden") or []:
        if got == bad:
            failed += 1
            print(f"FAIL {case['id']}: rejected squad selected {bad}")

print(f"Result: {len(cases) - failed}/{len(cases)} primary matches; failures={failed}")
sys.exit(1 if failed else 0)
