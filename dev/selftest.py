#!/usr/bin/env python3
"""Self-test do harness (contrato operacional). Exit 0 = verde."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DEV = Path(__file__).resolve().parent
ROOT = DEV.parent


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def main() -> int:
    fails = 0
    if run([sys.executable, str(DEV / "validate.py")]) != 0:
        fails += 1
    if run([sys.executable, str(DEV / "validate.py"), "--only-courses"]) != 0:
        fails += 1
    if run([sys.executable, str(DEV / "validate.py"), "--course", "aiox-design", "--only-courses"]) != 0:
        fails += 1
    # no-yaml path: frontmatter typed
    sys.path.insert(0, str(DEV))
    sys.modules.pop("yaml", None)
    import builtins
    real = builtins.__import__

    def blocked(name, *a, **k):
        if name == "yaml" or (isinstance(name, str) and name.startswith("yaml.")):
            raise ImportError("blocked")
        return real(name, *a, **k)

    builtins.__import__ = blocked
    for m in list(sys.modules):
        if m == "yaml" or m.startswith("lib."):
            sys.modules.pop(m, None)
    from lib.frontmatter import parse_frontmatter_yaml
    from lib.manifest import load_manifest

    fm, _ = parse_frontmatter_yaml(
        ROOT / "cursos/AIOX Advanced/aulas/01-token-economy-mindset.md"
    )
    assert fm.get("manual") is True, fm
    man = load_manifest(DEV / "courses/aiox-design/manifest.yaml")
    assert man.get("required_root"), man
    print("OK no-yaml frontmatter + manifest", flush=True)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
