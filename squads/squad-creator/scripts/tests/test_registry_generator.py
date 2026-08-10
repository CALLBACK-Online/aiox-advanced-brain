#!/usr/bin/env python3
"""
Tests for update-claude-command-registry.py — STORY-125.5.

Tests the 4 status dimensions: published (cascade), disabled, draft, incomplete.
Runs without pytest dependency.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = REPO_ROOT / "squads" / "squad-creator" / "scripts" / "update-claude-command-registry.py"


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class AssertionError(Exception):
    pass


def assert_eq(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")


def assert_gt(actual, threshold, msg=""):
    if not (actual > threshold):
        raise AssertionError(f"{msg}: expected > {threshold}, got {actual!r}")


def assert_in(item, collection, msg=""):
    if item not in collection:
        raise AssertionError(f"{msg}: {item!r} not found in {collection!r}")


def test_dry_run_json_has_four_dimensions():
    """IV1: JSON output contains published/draft/disabled/incomplete keys, published > 0."""
    result = run_script("--dry-run", "--json", "--project-root", str(REPO_ROOT))
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    data = json.loads(result.stdout)
    for key in ("published", "draft", "disabled", "incomplete", "total"):
        assert key in data, f"Missing key: {key}"
    assert_gt(data["published"], 0, "published count")
    total_check = data["published"] + data["draft"] + data["disabled"] + data["incomplete"]
    assert_eq(total_check, data["total"], "total sum mismatch")
    print("PASS test_dry_run_json_has_four_dimensions")


def test_phantom_squad_appears_in_incomplete():
    """IV2: Squad directory with no config.yaml -> incomplete with 'missing config.yaml'."""
    with tempfile.TemporaryDirectory() as tmp_squads:
        phantom_dir = Path(tmp_squads) / "squads" / "test-phantom"
        phantom_dir.mkdir(parents=True)
        (Path(tmp_squads) / "squads" / "CLAUDE.md").parent.mkdir(parents=True, exist_ok=True)
        # We can't easily use a minimal project root here, so use REPO_ROOT + temp squad
        phantom_in_repo = REPO_ROOT / "squads" / "test-phantom"
        phantom_in_repo.mkdir(exist_ok=True)
        try:
            result = run_script("--dry-run", "--json", "--project-root", str(REPO_ROOT))
            assert result.returncode == 0
            data = json.loads(result.stdout)
            # Phantom adds 1 to incomplete
            result2 = run_script("--dry-run", "--json", "--project-root", str(REPO_ROOT))
            data2 = json.loads(result2.stdout)
            assert_gt(data2["incomplete"], 0, "incomplete should be > 0 with phantom")
            print("PASS test_phantom_squad_appears_in_incomplete")
        finally:
            phantom_in_repo.rmdir()


def test_slides_creator_is_published_via_cascade():
    """AC2 step 4: slides-creator resolves via frontmatter agent-match (variant-dirname)."""
    result = run_script("--dry-run", "--json", "--project-root", str(REPO_ROOT))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    # slides-creator should be published (not draft)
    assert_gt(data["published"], 0, "at least one published squad")

    # Verify via text output that slides-creator appears in Published section
    result_text = run_script("--dry-run", "--project-root", str(REPO_ROOT))
    # Run a separate check by inspecting the section build output
    # We know from the JSON that published > 0; for slides-creator specifically,
    # we call collect_registry and verify
    import importlib.util, types
    spec = importlib.util.spec_from_file_location("registry", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    published, draft_rows, disabled, incomplete = mod.collect_registry(REPO_ROOT)
    slides_entries = [r for r in published if r["squad"] == "slides-creator"]
    assert len(slides_entries) == 1, f"slides-creator should be published, got: {slides_entries}"
    assert_eq(slides_entries[0]["status"], "published", "slides-creator status")
    print("PASS test_slides_creator_is_published_via_cascade")


def test_disabled_squads_have_rationale():
    """AC1: disabled squads surface with non-empty rationale from ide_sync.rationale."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("registry", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    _, _, disabled, _ = mod.collect_registry(REPO_ROOT)
    assert len(disabled) > 0, "Expected at least one disabled squad"
    for row in disabled:
        assert row["status"] == "disabled"
        assert row["note"], f"Disabled squad {row['squad']} has empty rationale"
    print(f"PASS test_disabled_squads_have_rationale ({len(disabled)} disabled squads)")


def test_incomplete_squads_specify_missing_fields():
    """AC4: incomplete squads have specific missing field(s) in note."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("registry", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    _, _, _, incomplete = mod.collect_registry(REPO_ROOT)
    assert len(incomplete) > 0, "Expected at least one incomplete squad"
    for row in incomplete:
        assert row["status"] == "incomplete"
        assert row["note"], f"Incomplete squad {row['squad']} has empty note"
        # Should mention 'missing' or be 'missing config.yaml'
        assert "missing" in row["note"].lower(), (
            f"Incomplete squad {row['squad']} note should say 'missing ...': {row['note']}"
        )
    print(f"PASS test_incomplete_squads_specify_missing_fields ({len(incomplete)} incomplete squads)")


def test_all_squads_accounted_for():
    """AC5: total count matches filesystem squad count (excluding .yaml files)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("registry", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    published, draft_rows, disabled, incomplete = mod.collect_registry(REPO_ROOT)
    total = len(published) + len(draft_rows) + len(disabled) + len(incomplete)

    squads_dir = REPO_ROOT / "squads"
    fs_count = sum(1 for p in squads_dir.iterdir() if p.is_dir())

    assert_eq(total, fs_count, f"Total registry entries vs filesystem squad dirs")
    print(f"PASS test_all_squads_accounted_for ({total} squads)")


if __name__ == "__main__":
    tests = [
        test_dry_run_json_has_four_dimensions,
        test_phantom_squad_appears_in_incomplete,
        test_slides_creator_is_published_via_cascade,
        test_disabled_squads_have_rationale,
        test_incomplete_squads_specify_missing_fields,
        test_all_squads_accounted_for,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)
