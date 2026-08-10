#!/usr/bin/env bash
# Build a team-shareable zip of course-library-ops (not student npm pack).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
NAME="course-library-ops"

usage() {
  echo "Usage: package.sh [OUT_DIR]"
  echo "Build a team-only archive. Default: $PACK_DIR/dist"
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -gt 1 || "${1:-}" == -* ]]; then
  usage >&2
  exit 2
fi

VERSION="$(python3 - "$PACK_DIR/package.json" <<'PY'
import json
import re
import sys

version = json.load(open(sys.argv[1], encoding="utf-8")).get("version", "")
if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
    raise SystemExit("package.json: version SemVer inválida")
print(version)
PY
)"
OUT_DIR="${1:-$PACK_DIR/dist}"
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT

# Gate funcional: só empacotar fluxos que provam o contrato fail-closed.
if python3 "$SCRIPT_DIR/selftest.py" >/dev/null 2>&1; then
  echo "selftest bootstrap+create+improve+upgrade: PASS"
else
  echo "ERRO: selftest funcional do pack falhou." >&2
  echo "Execute python3 scripts/selftest.py para diagnosticar." >&2
  exit 1
fi

mkdir -p "$OUT_DIR" "$STAGING/$NAME"

if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude 'dist' \
    --exclude '.DS_Store' \
    "$PACK_DIR/" "$STAGING/$NAME/"
else
  (cd "$PACK_DIR" && tar -cf - --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='dist' --exclude='.DS_Store' .) \
    | (cd "$STAGING/$NAME" && tar -xf -)
fi

# Ensure install is executable in the zip
chmod +x "$STAGING/$NAME/scripts/"*.sh 2>/dev/null || true
chmod +x "$STAGING/$NAME/scripts/"*.py 2>/dev/null || true

ZIP_PATH="$OUT_DIR/${NAME}-${VERSION}.zip"
if command -v zip >/dev/null 2>&1; then
  if [[ -e "$ZIP_PATH" ]]; then
    mv "$ZIP_PATH" "${ZIP_PATH}.backup.$(date +%Y%m%d%H%M%S)"
  fi
  (
    cd "$STAGING"
    zip -qr "$ZIP_PATH" "$NAME"
  )
else
  ZIP_PATH="$OUT_DIR/${NAME}-${VERSION}.tgz"
  if [[ -e "$ZIP_PATH" ]]; then
    mv "$ZIP_PATH" "${ZIP_PATH}.backup.$(date +%Y%m%d%H%M%S)"
  fi
  (
    cd "$STAGING"
    tar -czf "$ZIP_PATH" "$NAME"
  )
fi

echo "packed → $ZIP_PATH"
echo "Team install: unzip && bash scripts/install.sh --target both --repo /path/to/acervo"
