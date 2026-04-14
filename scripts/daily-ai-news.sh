#!/usr/bin/env bash
# 每日 AI 新聞整理 → 通知 TG + 寫 Blog
# Cron: 0 0 * * * (每天午夜 12 點)
# 透過 OpenClaw system event 觸發，讓 AI agent 執行升級版流程
# 詳細流程見 blog-enhanced-pipeline.md

set -euo pipefail

# Cron environment fixes
export PATH="$HOME/.npm-global/bin:$HOME/.local/share/pnpm:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

LOG="/tmp/daily-ai-news.log"
DATE=$(date '+%Y-%m-%d')

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

log "Starting daily AI news job for $DATE"

# Use openclaw system event to trigger agent
if command -v openclaw &>/dev/null; then
  openclaw system event \
    --text "每日 AI 新聞升級版任務 ($DATE)，請讀取 ~/.openclaw/workspace/scripts/blog-enhanced-pipeline.md 了解完整流程後執行：

Stage 1 - 多源蒐集：
- web_search 搜尋過去 24 小時 AI/科技新聞（英文主流媒體 + AI 專業 + 中文科技媒體 + OpenClaw 生態）
- 額外搜尋 site:x.com 抓科技 KOL 公開推文觀點（Karpathy, LeCun, Sam Altman 等）

Stage 2 - 深度研究：
- 對 Top 3-5 主題，用 notebooklm skill（mcporter）建臨時 notebook 加入相關 URL，生成深度交叉分析，完成後清理 notebook

Stage 3 - 撰寫 3-5 篇 SEO 優化繁體中文文章到 ~/blog/content/tech/：
- 格式參考既有文章（title < 60 字元, description 150-160 字元, tags 5-8 個, FAQ 3-5 個, 正文 800-1500 字）
- 加入內部連結到既有相關文章

Stage 4 - 產圖：
- 用 meta-ai-imagine skill 為每篇產生配圖，存到 ~/blog/static/images/，更新 frontmatter

Stage 5 - 發布：
- cd ~/blog && git add -A && git commit -m 'daily: $DATE AI news' && git push
- 發送 Telegram 摘要通知 Simon（Top 5 新聞 + 已發布文章列表）" \
    --mode now >> "$LOG" 2>&1
  log "System event triggered successfully"
else
  log "ERROR: openclaw command not found"
  exit 1
fi
