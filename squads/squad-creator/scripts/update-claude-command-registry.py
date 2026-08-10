#!/usr/bin/env python3
"""
Update the generated squad activation appendix inside root CLAUDE.md.

Scans all squads/*/config.yaml files, derives honest status for each squad
(published / draft / disabled / incomplete), and writes a 4-section registry
block delimited by sentinel markers so surrounding CLAUDE.md content is preserved.

Status dimension logic:
  disabled   — ide_sync.enabled: false in config (intentional, surfaced with rationale)
  incomplete — config missing entry_agent OR slash_prefix (and not disabled)
  published  — SKILL.md resolved via 4-step cascade (see AC2)
  draft      — chief .md exists, config complete, but no SKILL.md candidate found
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


BEGIN_MARKER = "<!-- BEGIN GENERATED SQUAD ACTIVATION REGISTRY -->"
END_MARKER = "<!-- END GENERATED SQUAD ACTIVATION REGISTRY -->"
SECTION_TITLE = "## Generated Squad Activation Registry"


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "squads").exists():
            return candidate
    raise FileNotFoundError("Could not find project root containing squads/")


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def extract_field(config: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = config.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    for parent in ("squad", "pack"):
        nested = config.get(parent)
        if not isinstance(nested, dict):
            continue
        for key in keys:
            value = nested.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def extract_ide_sync(config: Dict[str, Any]) -> Tuple[bool, str]:
    """Return (enabled, rationale). Defaults to (True, '')."""
    for key in ("ide_sync",):
        val = config.get(key)
        if not isinstance(val, dict):
            for parent in ("squad", "pack"):
                nested = config.get(parent)
                if isinstance(nested, dict):
                    val = nested.get(key)
                    if isinstance(val, dict):
                        break
        if isinstance(val, dict):
            enabled = val.get("enabled", True)
            rationale = val.get("rationale", "") or ""
            return bool(enabled), str(rationale).strip()
    return True, ""


def parse_frontmatter_agent(skill_path: Path) -> Optional[str]:
    """Return the 'agent:' value from a SKILL.md YAML frontmatter block, or None."""
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception:
        return None
    if isinstance(fm, dict):
        agent = fm.get("agent")
        if isinstance(agent, str) and agent.strip():
            return agent.strip()
    return None


def build_frontmatter_index(skills_root: Path) -> Dict[str, Path]:
    """Build index: agent_field_value -> skill_path for all depth-2 SKILL.md files."""
    index: Dict[str, Path] = {}
    for skill_path in skills_root.glob("*/SKILL.md"):
        agent_val = parse_frontmatter_agent(skill_path)
        if agent_val:
            index[agent_val] = skill_path
    return index


def resolve_skill_path(
    project_root: Path,
    entry_agent: str,
    slash_prefix: str,
    frontmatter_index: Dict[str, Path],
) -> Optional[Path]:
    """
    4-step cascade per AC2:
    1. skills/{entry_agent}/SKILL.md
    2. skills/{slash_prefix}/{entry_agent}/SKILL.md
    3. skills/{slash_prefix}/SKILL.md
    4. Frontmatter agent-match (variant-dirname)
    """
    skills_root = project_root / ".claude" / "skills"

    # Step 1: canonical depth-2 flat
    candidate = skills_root / entry_agent / "SKILL.md"
    if candidate.exists():
        return candidate

    # Step 2: depth-3 legacy (prefix/entry_agent)
    if slash_prefix:
        candidate = skills_root / slash_prefix / entry_agent / "SKILL.md"
        if candidate.exists():
            return candidate

        # Step 3: rare single-file variant (prefix/SKILL.md)
        candidate = skills_root / slash_prefix / "SKILL.md"
        if candidate.exists():
            return candidate

    # Step 4: frontmatter agent-match
    match = frontmatter_index.get(entry_agent)
    if match and match.exists():
        return match

    return None


def collect_registry(project_root: Path) -> List[Dict[str, str]]:
    squads_dir = project_root / "squads"
    skills_root = project_root / ".claude" / "skills"

    # Build frontmatter index once (expensive-ish, done once at startup)
    frontmatter_index = build_frontmatter_index(skills_root)

    published: List[Dict[str, str]] = []
    draft: List[Dict[str, str]] = []
    disabled: List[Dict[str, str]] = []
    incomplete: List[Dict[str, str]] = []

    for squad_dir in sorted(p for p in squads_dir.iterdir() if p.is_dir()):
        squad_name = squad_dir.name

        # AC5: squads without config.yaml → incomplete with reason
        config_path = squad_dir / "config.yaml"
        if not config_path.exists():
            incomplete.append({
                "squad": squad_name,
                "prefix": "",
                "entry_agent": "",
                "command_surface": "",
                "status": "incomplete",
                "note": "missing config.yaml",
            })
            continue

        config = load_yaml(config_path)

        # AC1: disabled squads
        ide_enabled, ide_rationale = extract_ide_sync(config)
        if not ide_enabled:
            entry_agent = extract_field(config, "entry_agent")
            slash_prefix = extract_field(config, "slashPrefix", "slash_prefix")
            rationale = ide_rationale if ide_rationale else "not specified"
            disabled.append({
                "squad": squad_name,
                "prefix": slash_prefix,
                "entry_agent": entry_agent,
                "command_surface": f"/{slash_prefix}:{entry_agent}" if entry_agent and slash_prefix else "",
                "status": "disabled",
                "note": rationale,
            })
            continue

        entry_agent = extract_field(config, "entry_agent")
        slash_prefix = extract_field(config, "slashPrefix", "slash_prefix")

        # AC4: incomplete config
        if not entry_agent or not slash_prefix:
            missing = []
            if not entry_agent:
                missing.append("entry_agent")
            if not slash_prefix:
                missing.append("slash_prefix")
            incomplete.append({
                "squad": squad_name,
                "prefix": slash_prefix,
                "entry_agent": entry_agent,
                "command_surface": "",
                "status": "incomplete",
                "note": f"missing: {', '.join(missing)}",
            })
            continue

        # AC2: cascade skill path resolution
        skill_path = resolve_skill_path(project_root, entry_agent, slash_prefix, frontmatter_index)

        command_surface = f"/{slash_prefix}:{entry_agent}"

        if skill_path is not None:
            # published
            published.append({
                "squad": squad_name,
                "prefix": slash_prefix,
                "entry_agent": entry_agent,
                "command_surface": command_surface,
                "status": "published",
                "note": str(skill_path.relative_to(project_root)),
            })
        else:
            # AC3: draft — chief .md must exist
            chief_path = squad_dir / "agents" / f"{entry_agent}.md"
            note = "publishable via create-squad-publish"
            if not chief_path.exists():
                note = "publishable via create-squad-publish (chief .md not found)"
            draft.append({
                "squad": squad_name,
                "prefix": slash_prefix,
                "entry_agent": entry_agent,
                "command_surface": command_surface,
                "status": "draft",
                "note": note,
            })

    return published, draft, disabled, incomplete


def build_section(
    published: List[Dict[str, str]],
    draft: List[Dict[str, str]],
    disabled: List[Dict[str, str]],
    incomplete: List[Dict[str, str]],
) -> str:
    lines = [
        SECTION_TITLE,
        "",
        BEGIN_MARKER,
    ]

    def table_header():
        return [
            "| Squad | Prefix | Entry Agent | Command Surface | Status |",
            "|---|---|---|---|---|",
        ]

    # Section: Published
    lines += ["", "### Published", ""]
    if published:
        lines += table_header()
        for r in published:
            lines.append(
                f"| `{r['squad']}` | `/{r['prefix']}` | `{r['entry_agent']}` | "
                f"`{r['command_surface']}` | `{r['status']}` |"
            )
    else:
        lines.append("_No published squads._")

    # Section: Draft (publish pending)
    lines += ["", "### Draft (publish pending)", ""]
    if draft:
        lines += table_header()
        for r in draft:
            lines.append(
                f"| `{r['squad']}` | `/{r['prefix']}` | `{r['entry_agent']}` | "
                f"`{r['command_surface']}` | `{r['status']}` |"
            )
    else:
        lines.append("_No draft squads._")

    # Section: Disabled (intentional)
    lines += ["", "### Disabled (intentional)", ""]
    if disabled:
        lines += [
            "| Squad | Entry Agent | Rationale |",
            "|---|---|---|",
        ]
        for r in disabled:
            lines.append(
                f"| `{r['squad']}` | `{r['entry_agent']}` | {r['note']} |"
            )
    else:
        lines.append("_No disabled squads._")

    # Section: Incomplete (needs config)
    lines += ["", "### Incomplete (needs config)", ""]
    if incomplete:
        lines += [
            "| Squad | Note |",
            "|---|---|",
        ]
        for r in incomplete:
            lines.append(f"| `{r['squad']}` | {r['note']} |")
    else:
        lines.append("_No incomplete squads._")

    lines.append("")
    lines.append(END_MARKER)
    return "\n".join(lines)


def replace_or_append(content: str, section: str) -> str:
    if BEGIN_MARKER in content and END_MARKER in content:
        start = content.index(BEGIN_MARKER)
        section_start = content.rfind(SECTION_TITLE, 0, start)
        end = content.index(END_MARKER) + len(END_MARKER)
        prefix = content[:section_start].rstrip() if section_start != -1 else content[:start].rstrip()
        suffix = content[end:].lstrip()
        parts = [prefix, section]
        if suffix:
            parts.append(suffix)
        return "\n\n".join(part for part in parts if part)

    return content.rstrip() + "\n\n" + section + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update generated squad activation registry in root CLAUDE.md"
    )
    parser.add_argument("--project-root", default=".", help="Project root or any nested path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    project_root = find_project_root(Path(args.project_root))
    claude_path = project_root / "CLAUDE.md"
    if not claude_path.exists():
        raise SystemExit(f"CLAUDE.md not found at project root: {claude_path}")

    published, draft_rows, disabled, incomplete = collect_registry(project_root)
    section = build_section(published, draft_rows, disabled, incomplete)
    updated = replace_or_append(claude_path.read_text(encoding="utf-8"), section)

    if not args.dry_run:
        claude_path.write_text(updated, encoding="utf-8")

    total = len(published) + len(draft_rows) + len(disabled) + len(incomplete)
    payload = {
        "project_root": str(project_root),
        "claude_path": str(claude_path),
        "total": total,
        "written": not args.dry_run,
        "published": len(published),
        "draft": len(draft_rows),
        "disabled": len(disabled),
        "incomplete": len(incomplete),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        action = "updated" if not args.dry_run else "preview"
        print(
            f"OK: {action} CLAUDE.md registry — "
            f"{len(published)} published / {len(draft_rows)} draft / "
            f"{len(disabled)} disabled / {len(incomplete)} incomplete "
            f"({total} total)"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
