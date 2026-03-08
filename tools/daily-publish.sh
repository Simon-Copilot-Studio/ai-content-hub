#!/bin/bash
# daily-publish.sh — Build and deploy AI Content Hub
# Run by cron or manually: bash tools/daily-publish.sh
#
# This script:
# 1. Builds the Hugo site with minification
# 2. Commits any new/changed content
# 3. Pushes to GitHub (triggers GitHub Pages deploy)

set -euo pipefail

REPO_DIR="/home/simon/.openclaw/workspace/projects/ai-content-hub"
LOG_FILE="${REPO_DIR}/tools/publish.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

cd "$REPO_DIR"

echo "[$DATE] Starting daily publish..." >> "$LOG_FILE"

# Build
if hugo --minify >> "$LOG_FILE" 2>&1; then
    PAGES=$(hugo --minify 2>&1 | grep "Pages" | awk '{print $NF}')
    echo "[$DATE] Build OK — $PAGES pages" >> "$LOG_FILE"
else
    echo "[$DATE] ERROR: Hugo build failed!" >> "$LOG_FILE"
    exit 1
fi

# Check for changes
if git diff --quiet && git diff --staged --quiet; then
    echo "[$DATE] No changes to deploy" >> "$LOG_FILE"
    exit 0
fi

# Commit and push
ARTICLE_COUNT=$(find content -name "*.md" -not -name "_index.md" -not -path "*/about/*" -not -path "*/privacy/*" -not -path "*/contact/*" | wc -l)
git add -A
git commit -m "daily: publish update ($ARTICLE_COUNT articles)" --quiet
git push --quiet

echo "[$DATE] Deployed successfully — $ARTICLE_COUNT articles total" >> "$LOG_FILE"
