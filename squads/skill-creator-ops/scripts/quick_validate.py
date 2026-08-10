#!/usr/bin/env python3
"""
Quick validation script for skills — AllFluence extended version.
Based on SynkraAI/upstream monorepo quick_validate.py, extended with AllFluence fields.
"""

import sys
import re
from pathlib import Path

# AllFluence required frontmatter fields
REQUIRED_FIELDS = ['name', 'description']
# CC-native fields only — AIOX fields (owner_squad, aiox_tier) belong in tasks, not skills
CC_NATIVE_FIELDS = ['version', 'user-invocable']
VALID_CONTEXTS = ['inline', 'fork', 'conversation']


def validate_skill(skill_path, strict=True):
    """
    Validate a skill against AllFluence standards.

    Args:
        skill_path: Path to skill directory
        strict: If True, check AllFluence-specific fields too

    Returns:
        (bool, str, list) — valid, message, warnings
    """
    skill_path = Path(skill_path)
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", warnings

    # Read and validate frontmatter
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", warnings

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", warnings

    frontmatter = match.group(1)

    # Check required fields (base)
    for field in REQUIRED_FIELDS:
        if f'{field}:' not in frontmatter:
            return False, f"Missing required field: '{field}'", warnings

    # Extract and validate name
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip().strip('"').strip("'")
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' must be kebab-case (lowercase, digits, hyphens)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or have consecutive hyphens"
        if len(name) > 40:
            return False, f"Name '{name}' exceeds 40 characters"

        # Check name matches directory
        if name != skill_path.name:
            warnings.append(f"Name '{name}' does not match directory '{skill_path.name}'")

    # Validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"

    # CC-native field checks (strict mode)
    if strict:
        for field in CC_NATIVE_FIELDS:
            if f'{field}:' not in frontmatter:
                warnings.append(f"Missing CC-native field: '{field}' (recommended)")

        # Validate context if present
        ctx_match = re.search(r'context:\s*(.+)', frontmatter)
        if ctx_match:
            ctx = ctx_match.group(1).strip().strip('"').strip("'")
            if ctx not in VALID_CONTEXTS:
                warnings.append(f"context '{ctx}' not in {VALID_CONTEXTS}")

        # Check version is semver
        ver_match = re.search(r'version:\s*["\']?(\S+)', frontmatter)
        if ver_match:
            ver = ver_match.group(1).strip('"').strip("'")
            if not re.match(r'^\d+\.\d+\.\d+$', ver):
                warnings.append(f"version '{ver}' is not valid semver (X.Y.Z)")

    # Structure checks based on tier
    tier_match = re.search(r'aiox_tier:\s*(.+)', frontmatter)
    if tier_match:
        tier = tier_match.group(1).strip().strip('"').strip("'")
        if tier == 'Tier2' and not (skill_path / 'config.yaml').exists():
            warnings.append("Tier2 requires config.yaml")
        if tier == 'Tier3':
            for req_dir in ['templates', 'checklists', 'data']:
                if not (skill_path / req_dir).exists():
                    warnings.append(f"Tier3 requires {req_dir}/ directory")

    if warnings:
        return True, f"Valid with {len(warnings)} warning(s)", warnings
    return True, "Skill is valid!", warnings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory> [--strict|--basic]")
        sys.exit(1)

    strict = '--basic' not in sys.argv
    valid, message, warnings = validate_skill(sys.argv[1], strict=strict)

    print(f"{'PASS' if valid else 'FAIL'}: {message}")
    for w in warnings:
        print(f"  WARNING: {w}")

    sys.exit(0 if valid else 1)
