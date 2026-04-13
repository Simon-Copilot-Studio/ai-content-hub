#!/bin/bash
# Sync OpenClaw workspace to GitHub (openclaw-workspace repo)
set -e

cd ~/.openclaw/workspace

# Remove stale lock
rm -f .git/index.lock

# Ensure correct remote
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null)
EXPECTED_REMOTE="https://github.com/Simon-Copilot-Studio/openclaw-workspace.git"
if [ "$CURRENT_REMOTE" != "$EXPECTED_REMOTE" ]; then
  git remote set-url origin "$EXPECTED_REMOTE"
  echo "Fixed remote → $EXPECTED_REMOTE"
fi

# Ensure on workspace-clean branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "workspace-clean" ]; then
  git checkout workspace-clean 2>/dev/null || git checkout -b workspace-clean
fi

# Stage only tracked workspace files
git add -A \
  .gitignore \
  ACTIVE_TASKS.md \
  AGENTS.md \
  SOUL.md \
  TOOLS.md \
  IDENTITY.md \
  USER.md \
  HEARTBEAT.md \
  BOOTSTRAP.md \
  .learnings/ \
  memory/ \
  research/ \
  scripts/ \
  2>/dev/null

# Commit if changes exist
if git diff --cached --quiet; then
  echo "No changes to sync"
else
  git commit -m "auto: workspace sync $(date +%Y-%m-%d_%H:%M)"
  git push origin workspace-clean
  echo "✅ Synced to GitHub"
fi
