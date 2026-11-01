#!/usr/bin/env bash
# Removes a GAME STUDIO install (user level by default, or --project <dir>).
# Only removes the directory if it is really a game-studio install. A backup is kept.
set -euo pipefail
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BASE="$CONFIG_DIR/skills"
if [[ "${1:-}" == "--project" ]]; then BASE="$(cd "${2:?--project needs a directory}" && pwd)/.claude/skills"; fi
TARGET="$BASE/game-studio"
AGENTS_DIR="$(dirname "$BASE")/agents/game-studio"
if [[ "${1:-}" == "--project" && -d "$AGENTS_DIR" ]]; then
  rm -rf "$AGENTS_DIR"; echo "Removed project agents $AGENTS_DIR"
fi

if [[ -L "$TARGET" ]]; then
  rm "$TARGET"; echo "Removed symlink $TARGET"; exit 0
fi
if [[ ! -d "$TARGET" ]]; then echo "Nothing installed at $TARGET"; exit 0; fi
if ! grep -q '"name": *"game-studio"' "$TARGET/.claude-plugin/plugin.json" 2>/dev/null; then
  echo "ERROR: $TARGET is not a game-studio install; not removing." >&2; exit 1
fi
BACKUP="$CONFIG_DIR/backups/game-studio-removed-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CONFIG_DIR/backups"
mv "$TARGET" "$BACKUP"
echo "Removed $TARGET (backup kept at $BACKUP). Start a new session to unload it."
