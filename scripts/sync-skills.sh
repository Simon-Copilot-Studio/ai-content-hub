#!/bin/bash
set -e

REPO_DIR="$HOME/projects/OpenClawSkills"
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
RESEARCH_DIR="$HOME/.openclaw/workspace/research"
LEARNINGS_DIR="$HOME/.openclaw/workspace/.learnings"

# Clone if not exists
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone https://github.com/Simon-Copilot-Studio/OpenClawSkills.git "$REPO_DIR"
fi

cd "$REPO_DIR"
git pull --rebase origin main 2>/dev/null || true

# Sync skills (exclude __pycache__ and .git)
rsync -av --delete --exclude='__pycache__' --exclude='.git' --exclude='research' --exclude='.learnings' "$SKILLS_DIR/" ./

# Sync research
mkdir -p research
cp "$RESEARCH_DIR"/*.md research/ 2>/dev/null || true
cp -r "$RESEARCH_DIR"/daily-radar research/ 2>/dev/null || true

# Sync learnings
mkdir -p .learnings
cp "$LEARNINGS_DIR"/*.md .learnings/ 2>/dev/null || true

# Commit and push if changes
git add -A
if ! git diff --cached --quiet; then
  git commit -m "sync: auto-sync skills + research $(date +%Y-%m-%d)"
  git push origin main
  echo "SYNCED"
else
  echo "NO_CHANGES: already up to date"
fi
