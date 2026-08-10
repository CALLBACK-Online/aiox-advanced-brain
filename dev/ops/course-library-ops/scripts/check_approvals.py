#!/usr/bin/env python3
"""Valida os dois gates humanos registrados nos artefatos de bastidor."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from course_common import find_root, validate_approval_artifacts
from scaffold_course import validate_spec


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida brief e outline aprovados")
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    root = find_root(args.repo_root or Path.cwd())
    spec_path = args.spec if args.spec.is_absolute() else root / args.spec
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    validate_spec(spec)
    approvals = validate_approval_artifacts(root, spec)
    for gate, path in approvals.items():
        print(f"{gate}: approved → {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
