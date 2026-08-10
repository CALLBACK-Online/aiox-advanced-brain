#!/usr/bin/env python3
"""Bench-mode semantic tests for unified tech-research extractors.

Origin: STORY-153.6 follow-up. These tests verify that --mode=bench changes
extractor behavior, not only detection/logging.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from action_assets_extractor import build_assets  # noqa: E402
from dashboard_manifest import build_manifest  # noqa: E402
from research_graph import build_graph  # noqa: E402


def write_fixture(folder: Path) -> None:
    (folder / "executive-report.md").write_text(
        """# Relatório Executivo — Fixture Bench

## Decisão

**GO para absorção parcial.**

## Roadmap Recomendado

| Wave | Nome | Itens |
| --- | --- | --- |
| 1 | contract | Criar contrato de traceabilidade |
| 2 | runtime | Integrar runner de pesquisa |
""",
        encoding="utf-8",
    )
    (folder / "gap-analysis.md").write_text(
        """# Gap Analysis

## Gaps

- Falta traceabilidade por claim.
- Falta custo por wave.
""",
        encoding="utf-8",
    )
    (folder / "bench-output-dash.json").write_text(
        json.dumps(
            {
                "players": [
                    {"key": "aiox_research", "name": "AIOX Research", "category": "internal"},
                    {"key": "drbench", "name": "DRBench", "category": "framework"},
                ],
                "matrix": {
                    "dimensions": [
                        {
                            "id": "trace__claim_provenance",
                            "label": "Claim provenance",
                            "group": "Evidence Fidelity",
                            "weight": 2,
                        }
                    ]
                },
                "duels": [
                    {
                        "id": "aiox_research-vs-drbench",
                        "a": "aiox_research",
                        "b": "drbench",
                        "verdict": "AIOX vence por rastreabilidade",
                        "winsA": ["trace__claim_provenance"],
                        "winsB": [],
                    }
                ],
                "personas": [
                    {
                        "id": "operator",
                        "label": "Operator",
                        "ranking": [
                            {"rank": 1, "player": "aiox_research", "score": 91},
                            {"rank": 2, "player": "drbench", "score": 78},
                        ],
                    }
                ],
                "gaps": [{"id": "claim_provenance", "title": "Claim provenance", "priority": "P1"}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (folder / "bench-contract.json").write_text(
        json.dumps(
            {
                "schema": "bench-contract.v1",
                "type": "absorption-benchmark",
                "decision_improved": "Decidir padrões de absorção.",
                "anchor": {"id": "aiox_research"},
                "taxonomy": {"groups": ["Evidence Fidelity"]},
                "scoring_model": {"scale": "0-100"},
                "completeness_criteria": ["matrix", "duels"],
            }
        ),
        encoding="utf-8",
    )
    (folder / "comparison-matrix.json").write_text("{}", encoding="utf-8")
    (folder / "comparison-matrix.md").write_text("# Matrix\n", encoding="utf-8")
    (folder / "scorecard.json").write_text("{}", encoding="utf-8")
    (folder / "scorecard.md").write_text("# Scorecard\n", encoding="utf-8")
    (folder / "decision-rubric.yaml").write_text(
        "status: applicable\nmodel:\n  dimension_pack: bench\nplayers: {}\n",
        encoding="utf-8",
    )
    (folder / "research-profile.yaml").write_text(
        "profile:\n  type: bench\n",
        encoding="utf-8",
    )
    (folder / "metrics.yaml").write_text("coverage_score: 95\nintegrity_score: 94\n", encoding="utf-8")
    (folder / "README.md").write_text("# Fixture\n", encoding="utf-8")
    (folder / "INDEX.md").write_text("# Index\n", encoding="utf-8")
    (folder / "MANIFEST.json").write_text("{}", encoding="utf-8")
    (folder / "sources.yaml").write_text("sources: []\n", encoding="utf-8")
    (folder / "claims.yaml").write_text("claims: []\n", encoding="utf-8")
    (folder / "risk-register.yaml").write_text("risks: []\n", encoding="utf-8")
    (folder / "action-plan.yaml").write_text("actions: []\n", encoding="utf-8")
    (folder / "decision-ledger.yaml").write_text("decisions: []\n", encoding="utf-8")


class TestBenchModeSemantics(unittest.TestCase):
    def test_action_assets_read_executive_report_in_bench_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_fixture(folder)
            assets = build_assets(folder, mode="bench")
            self.assertIn("executive-report.md", assets["action-plan.yaml"]["decision"]["evidence"])
            roadmap_titles = [row["title"] for row in assets["action-plan.yaml"]["roadmap"]]
            self.assertIn("contract", roadmap_titles)

    def test_research_graph_adds_bench_nodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_fixture(folder)
            graph = build_graph(folder, mode="bench")
            node_types = graph["node_type_counts"]
            self.assertEqual(graph["mode"], "bench")
            self.assertEqual(node_types["player"], 2)
            self.assertEqual(node_types["dimension"], 1)
            self.assertEqual(node_types["duel"], 1)
            self.assertEqual(node_types["persona"], 1)
            self.assertEqual(node_types["gap"], 1)
            relations = {edge["relation"] for edge in graph["edges"]}
            self.assertIn("contains_microdim", relations)
            self.assertIn("competes_with", relations)
            self.assertIn("declares_persona", relations)

    def test_dashboard_manifest_uses_bench_tabs_and_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_fixture(folder)
            graph = build_graph(folder, mode="bench")
            (folder / "research-graph.json").write_text(json.dumps(graph), encoding="utf-8")
            manifest = build_manifest(folder, mode="bench")
            self.assertEqual(manifest["mode"], "bench")
            self.assertEqual(manifest["tier_per_tab"]["matrix"], "required")
            self.assertEqual(manifest["tier_per_tab"]["duel"], "gold")
            self.assertIn("score", manifest["tabs"])
            self.assertIn("decision", manifest["tabs"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
