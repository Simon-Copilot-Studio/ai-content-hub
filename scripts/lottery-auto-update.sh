#!/usr/bin/env bash
# 台灣樂透 AI 資料自動更新
# 1) 抓最新開獎資料 (pilio scraper)
# 2) Seed 到 Supabase
# 3) Git push
# Cron: 每天 22:30 (開獎後執行)

set -euo pipefail

export PATH="$HOME/.npm-global/bin:$HOME/.local/share/pnpm:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

PROJECT_DIR="$HOME/projects/tw-lottery-ai"
LOG="/tmp/lottery-auto-update.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

log() {
  echo "[$DATE] $*" >> "$LOG"
}

log "=== Starting lottery auto-update ==="

cd "$PROJECT_DIR"

# Step 1: Scrape latest data
log "Step 1: Scraping lottery data..."
SCRAPE_OUTPUT=$(node scripts/scrape-pilio.mjs 2>&1) || {
  log "ERROR: Scraper failed"
  log "$SCRAPE_OUTPUT"
  exit 1
}

# Extract new record count
NEW_COUNT=$(echo "$SCRAPE_OUTPUT" | grep "Total new records" | grep -o '[0-9]*' || echo "0")
log "Scraper done: $NEW_COUNT new records"

if [ "$NEW_COUNT" = "0" ]; then
  log "No new records, skipping push and seed"
  exit 0
fi

# Step 2: Git commit & push
log "Step 2: Git push..."
git add -A
if git diff --cached --quiet; then
  log "No git changes to push"
else
  git commit -m "data: auto-update lottery draws $(date '+%Y-%m-%d') (+$NEW_COUNT records)" --quiet
  git push --quiet 2>&1 || log "WARN: git push failed"
  log "Git push done"
fi

# Step 3: Seed Supabase
log "Step 3: Seeding Supabase..."
SEED_OUTPUT=$(node scripts/seed-supabase.mjs 2>&1) || {
  log "WARN: Supabase seed failed"
  log "$SEED_OUTPUT"
}
log "Supabase seed done"

log "=== Lottery auto-update complete ==="
