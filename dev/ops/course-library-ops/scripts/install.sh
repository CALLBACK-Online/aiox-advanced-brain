#!/usr/bin/env bash
# Project course-library-ops into local agent runtimes (.claude / .agents).
# Maintainer-only. Does not touch student skills/ catalog.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="course-library-ops"

TARGET="both"
SOURCE="$PACK_DIR"
REPO_ROOT=""

usage() {
  cat <<'EOF'
Usage: install.sh [--target claude|agents|both] [--source DIR] [--repo ROOT]

  --target   Where to install (default: both)
  --source   Pack directory with SKILL.md (default: parent of scripts/)
  --repo     Acervo root for project-local .claude/.agents
             (default: cwd if it has catalog.json+package.json, else pack parent climb)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --source) SOURCE="$(cd "${2:-}" && pwd)"; shift 2 ;;
    --repo) REPO_ROOT="$(cd "${2:-}" && pwd)"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ ! -f "$SOURCE/SKILL.md" ]]; then
  echo "SKILL.md not found in source: $SOURCE" >&2
  exit 1
fi

find_repo_root() {
  local cur
  cur="$(pwd)"
  while [[ "$cur" != "/" ]]; do
    if [[ -f "$cur/catalog.json" && -f "$cur/package.json" ]]; then
      echo "$cur"
      return 0
    fi
    cur="$(dirname "$cur")"
  done
  return 1
}

if [[ -z "$REPO_ROOT" ]]; then
  if REPO_ROOT="$(find_repo_root)"; then
    :
  else
    REPO_ROOT="$(pwd)"
    echo "warn: acervo root not found (catalog.json+package.json); installing under $REPO_ROOT" >&2
  fi
fi

install_one() {
  local dest_parent="$1"
  local dest="$dest_parent/skills/$SKILL_NAME"
  # Backups NUNCA dentro de skills/: o runtime carrega qualquer dir com
  # SKILL.md, e um backup ali vira skill fantasma no namespace.
  local backup_root="$dest_parent/skills-backups"
  local stage
  local backup=""
  local legacy
  mkdir -p "$dest_parent/skills"
  stage="$(mktemp -d "$dest_parent/.${SKILL_NAME}.stage.XXXXXX")"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
      --exclude 'dist' "$SOURCE/" "$stage/"
  else
    (cd "$SOURCE" && tar -cf - --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='dist' .) \
      | (cd "$stage" && tar -xf -)
  fi
  if [[ -e "$dest" ]]; then
    mkdir -p "$backup_root"
    backup="$backup_root/${SKILL_NAME}.$(date +%Y%m%d%H%M%S)"
    mv "$dest" "$backup"
  fi
  mv "$stage" "$dest"
  echo "installed → $dest"
  if [[ -n "$backup" ]]; then
    echo "previous version → $backup"
  fi
  # Backups legados são movidos, não apagados, para sair da descoberta de skills.
  for ghost in "$dest_parent/skills/$SKILL_NAME".backup.*; do
    [[ -e "$ghost" ]] || continue
    mkdir -p "$backup_root"
    legacy="$backup_root/legacy.$(basename "$ghost")"
    mv "$ghost" "$legacy"
    echo "legacy backup moved outside discovery → $legacy"
  done
}

case "$TARGET" in
  claude)
    install_one "$REPO_ROOT/.claude"
    ;;
  agents)
    install_one "$REPO_ROOT/.agents"
    ;;
  both)
    install_one "$REPO_ROOT/.claude"
    install_one "$REPO_ROOT/.agents"
    ;;
  *)
    echo "invalid --target: $TARGET (use claude|agents|both)" >&2
    exit 1
    ;;
esac

echo "OK course-library-ops ($TARGET) @ $REPO_ROOT"
echo "Note: .claude/ and .agents/ are gitignored — share via scripts/package.sh"
