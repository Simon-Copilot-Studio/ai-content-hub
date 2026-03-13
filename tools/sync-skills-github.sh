#!/usr/bin/env bash
# Sync local skills to Simon-Copilot-Studio/OpenClawSkills
# Cron: 0 3 * * *
set -euo pipefail

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
LOG_PREFIX="[sync-skills]"

cd "$SKILLS_DIR"

# Ensure remote is set
if ! git remote get-url origin &>/dev/null; then
  echo "$LOG_PREFIX ERROR: no git remote 'origin'" >&2
  exit 1
fi

# Pull any remote changes first (rebase to keep linear history)
git pull --rebase --quiet origin main 2>/dev/null || true

# Stage all changes (new, modified, deleted)
git add -A

# Check if there's anything to commit
if git diff --cached --quiet; then
  echo "$LOG_PREFIX $(date '+%F %T') — nothing to sync"
  exit 0
fi

# Count changed files
CHANGED=$(git diff --cached --name-only | wc -l)

# Commit and push
git commit -m "sync: update $CHANGED skill file(s) — $(date '+%F %H:%M')" --quiet
git push --quiet origin main

echo "$LOG_PREFIX $(date '+%F %T') — pushed $CHANGED file(s)"
