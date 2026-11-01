#!/usr/bin/env bash
# GAME STUDIO installer.
# Installs this directory as a Claude Code "skills-dir" plugin:
#   user level (default): ~/.claude/skills/game-studio   -> available in every project
#   project level:        <dir>/.claude/skills/game-studio
# It never touches other skills/agents. An existing game-studio install is backed up first;
# a foreign directory with the same name is never overwritten.
#
# Usage: scripts/install.sh [--project <dir>] [--link] [--dry-run]
#   --project <dir>  install into <dir>/.claude/skills instead of the user config dir
#   --link           symlink instead of copy (for developing the skill itself)
#   --dry-run        show what would happen
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="game-studio"
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BASE="$CONFIG_DIR/skills"
MODE=copy
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) BASE="$(cd "${2:?--project needs a directory}" && pwd)/.claude/skills"; shift 2 ;;
    --link) MODE=link; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

TARGET="$BASE/$NAME"
run() { if [[ $DRY -eq 1 ]]; then echo "[dry-run] $*"; else "$@"; fi; }

is_ours() {  # $1 = dir; true if it is a game-studio install
  [[ -f "$1/.claude-plugin/plugin.json" ]] && grep -q '"name": *"game-studio"' "$1/.claude-plugin/plugin.json"
}

echo "GAME STUDIO installer"
echo "  source : $SRC"
echo "  target : $TARGET ($MODE)"

if [[ "$(cd "$SRC" && pwd -P)" == "$( [[ -e "$TARGET" ]] && cd "$TARGET" && pwd -P )" ]]; then
  echo "Source and target are the same directory — already installed in place."
  python3 "$SRC/scripts/validate.py" "$TARGET" || exit 1
  exit 0
fi

if [[ -e "$TARGET" || -L "$TARGET" ]]; then
  if [[ -L "$TARGET" ]] || is_ours "$TARGET"; then
    BACKUP="$CONFIG_DIR/backups/${NAME}-$(date +%Y%m%d-%H%M%S)"
    echo "  existing game-studio install found -> backup to $BACKUP"
    run mkdir -p "$CONFIG_DIR/backups"
    run mv "$TARGET" "$BACKUP"
  else
    echo "ERROR: $TARGET exists and is not a game-studio install. Refusing to overwrite it." >&2
    echo "Move it away manually or install with --project <dir>." >&2
    exit 1
  fi
fi

run mkdir -p "$BASE"
if [[ $MODE == link ]]; then
  run ln -s "$SRC" "$TARGET"
else
  run mkdir -p "$TARGET"
  if command -v rsync >/dev/null 2>&1; then
    run rsync -a --exclude '.git' --exclude '.github' --exclude '__pycache__' "$SRC/" "$TARGET/"
  else
    run bash -c "cd '$SRC' && tar --exclude=.git --exclude=.github --exclude=__pycache__ -cf - . | (cd '$TARGET' && tar -xf -)"
  fi
  [[ $DRY -eq 1 ]] || chmod +x "$TARGET"/scripts/*.sh 2>/dev/null || true
fi

if [[ $DRY -eq 0 ]]; then
  python3 "$TARGET/scripts/validate.py" "$TARGET"
  echo
  echo "Installed. Start a NEW Claude Code session (or run /reload-plugins) and use:"
  echo "  /game-studio <oyun fikri veya görev>"
  echo "Specialists appear as subagents named game-studio:<role> (see /agents)."
fi
