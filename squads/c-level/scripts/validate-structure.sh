#!/bin/bash
# Workspace Structure Validation Script (5-Layer Model)
# COO runs this before activating governance
#
# Usage: ./squads/c-level/scripts/validate-structure.sh
# Exit codes: 0 = pass, 1 = fail
#
# Author: @architect (The Architect), @coo
# Updated: 2026-02-24

set -u

WORKSPACE_ROOT="workspace"
SPOKE_ROOT="$WORKSPACE_ROOT/{spoke}"
PASS=0
FAIL=0

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Workspace Structure Validation (5-Layer Model)"
echo "================================================"
echo ""

run_check() {
    local description="$1"
    shift

    if "$@"; then
        echo -e "${GREEN}✅${NC} $description"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}❌${NC} $description"
        FAIL=$((FAIL + 1))
    fi
}

count_lines() {
    wc -l | tr -d ' '
}

collect_layers() {
    find "$SPOKE_ROOT" -mindepth 1 -maxdepth 1 -type d -name "l*" 2>/dev/null | sort
}

# 1. Foundation checks
echo "1. Foundation"
echo "---"
run_check "workspace/ exists" test -d "$WORKSPACE_ROOT"
run_check "workspace/{spoke}/ exists" test -d "$SPOKE_ROOT"
run_check "document-registry.yaml exists" test -f "$SPOKE_ROOT/document-registry.yaml"
layer_count=$(collect_layers | count_lines)
run_check "At least one layer exists" test "$layer_count" -gt 0
echo ""

# 2. 5-Layer structure checks
echo "2. 5-Layer Structure (workspace/{spoke}/l{N}-*)"
echo "---"
if [ "$layer_count" -eq 0 ]; then
    echo -e "${YELLOW}⚠️${NC} No layer directories found, skipping layer checks"
else
    # L0 — Identity
    run_check "L0-identity/ exists" test -d "$SPOKE_ROOT/L0-identity"
    run_check "L0-identity/company-dna.yaml exists" test -f "$SPOKE_ROOT/L0-identity/company-dna.yaml"
    run_check "L0-identity/founder-dna.yaml exists" test -f "$SPOKE_ROOT/L0-identity/founder-dna.yaml"

    # L1 — Strategy
    run_check "L1-strategy/ exists" test -d "$SPOKE_ROOT/L1-strategy"
    run_check "L1-strategy/icp.yaml exists" test -f "$SPOKE_ROOT/L1-strategy/icp.yaml"
    run_check "L1-strategy/pricing-strategy.yaml exists" test -f "$SPOKE_ROOT/L1-strategy/pricing-strategy.yaml"

    # L2 — Tactical
    run_check "L2-tactical/ exists" test -d "$SPOKE_ROOT/L2-tactical"

    # L3 — Product
    if test -d "$SPOKE_ROOT/L3-product"; then
        echo -e "${GREEN}✅${NC} L3-product/ exists"
        PASS=$((PASS + 1))
    else
        echo -e "${YELLOW}⚠️${NC} L3-product/ missing (created when products are added)"
    fi

    # L4 — Operational
    if test -d "$SPOKE_ROOT/L4-operational"; then
        echo -e "${GREEN}✅${NC} L4-operational/ exists"
        PASS=$((PASS + 1))
    else
        echo -e "${YELLOW}⚠️${NC} L4-operational/ missing (recommended)"
    fi
    echo ""
fi

# 3. YAML syntax validation
echo "3. YAML Syntax"
echo "---"
if command -v yq >/dev/null 2>&1; then
    invalid_yaml_tmp="$(mktemp)"
    yaml_files_checked=0

    while IFS= read -r -d '' yaml_file; do
        yaml_files_checked=$((yaml_files_checked + 1))
        if ! yq e "." "$yaml_file" >/dev/null 2>&1; then
            echo "$yaml_file" >> "$invalid_yaml_tmp"
        fi
    done < <(find "$WORKSPACE_ROOT" -type f \( -name "*.yaml" -o -name "*.yml" \) -print0)

    invalid_yaml_count=$(cat "$invalid_yaml_tmp" | count_lines)

    if [ "$yaml_files_checked" -eq 0 ]; then
        echo -e "${YELLOW}⚠️${NC} No YAML files found under $WORKSPACE_ROOT"
    fi

    run_check "All YAML files parse correctly" test "$invalid_yaml_count" -eq 0

    if [ "$invalid_yaml_count" -gt 0 ]; then
        echo -e "${RED}Invalid YAML files (first 20):${NC}"
        sed -n '1,20p' "$invalid_yaml_tmp"
    fi

    rm -f "$invalid_yaml_tmp"
else
    echo -e "${YELLOW}⚠️${NC} yq not found - YAML syntax check skipped"
    run_check "yq available for YAML validation" false
fi
echo ""

# 4. Forbidden patterns
echo "4. Forbidden Patterns"
echo "---"
forbidden_count=$(
    find "$WORKSPACE_ROOT" -type f \
        \( -name "*_backup" -o -name "*_old" -o -name "*_v2" -o -name "*_v3" -o -name "test_*" -o -name "temp_*" -o -name "TODO_*" -o -name "*~" \) \
        2>/dev/null | count_lines
)
run_check "No forbidden file patterns found" test "$forbidden_count" -eq 0
echo ""

# 5. Orphaned files in workspace root
echo "5. Orphaned Files (workspace root)"
echo "---"
allowed_root_files=(
    "structure.yaml"
    "relationships.yaml"
    "synapse-integration.yaml"
    "index.json"
    "PRODUCT_OFFERBOOK_SYSTEM.md"
)

orphaned=0
while IFS= read -r file_path; do
    file_name="$(basename "$file_path")"
    allowed=false
    for allowed_file in "${allowed_root_files[@]}"; do
        if [ "$file_name" = "$allowed_file" ]; then
            allowed=true
            break
        fi
    done
    if [ "$allowed" = false ]; then
        orphaned=$((orphaned + 1))
        echo -e "${YELLOW}⚠️${NC} Potential orphaned file: $file_name"
    fi
done < <(find "$WORKSPACE_ROOT" -maxdepth 1 -type f ! -name ".*" 2>/dev/null)

run_check "No orphaned files in workspace root" test "$orphaned" -eq 0
echo ""

# 6. Product naming checks (root + businesses)
echo "6. Product Naming (snake_case)"
echo "---"
product_count=0
bad_products=0

while IFS= read -r product_path; do
    [ -z "$product_path" ] && continue
    product_name="$(basename "$product_path")"
    product_count=$((product_count + 1))

    if [[ ! "$product_name" =~ ^[a-z0-9]+(_[a-z0-9]+)*$ ]]; then
        echo -e "${RED}❌${NC} Product not snake_case: $product_name ($product_path)"
        bad_products=$((bad_products + 1))
    fi
done < <(
    {
        find "$SPOKE_ROOT/L3-product" -mindepth 1 -maxdepth 1 -type d 2>/dev/null
    } | sort
)

if [ "$product_count" -eq 0 ]; then
    echo -e "${GREEN}✅${NC} No products yet (OK)"
    PASS=$((PASS + 1))
else
    run_check "All $product_count products are snake_case" test "$bad_products" -eq 0
fi
echo ""

# 7. Core workspace docs
echo "7. Core Workspace Docs"
echo "---"
run_check ".aiox-core/core-config.yaml exists" test -f ".aiox-core/core-config.yaml"
run_check ".user/user.md exists" test -f ".user/user.md"
run_check "_templates/ exists (canonical BU templates)" test -d "$WORKSPACE_ROOT/_templates"
run_check "_templates/README.md exists" test -f "$WORKSPACE_ROOT/_templates/README.md"
run_check "_templates/TEMPLATE_SYSTEM.md exists" test -f "$WORKSPACE_ROOT/_templates/TEMPLATE_SYSTEM.md"
if [ -d "$WORKSPACE_ROOT/templates" ]; then
    echo -e "${YELLOW}⚠️${NC} workspace/templates/ is operational-only. Canonical BU templates live in workspace/_templates/"
fi
echo ""

# Summary
echo "================================================"
echo -e "Summary:"
echo -e "  ${GREEN}Passed: $PASS${NC}"
if [ "$FAIL" -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAIL${NC}"
fi
echo ""

# Final result
if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✅ Workspace structure is valid and ready for governance activation${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Please fix the errors above before activating governance${NC}"
    echo ""
    echo "For help, see: workspace/_templates/TEMPLATE_SYSTEM.md"
    echo ""
    exit 1
fi
