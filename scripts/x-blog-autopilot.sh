#!/bin/bash
# X → Blog Autopilot
# 每 3 小時自動執行：搜尋熱門話題 → 撰寫 Blog → 產圖 → git push → 發 X 貼文
# 由 cron 觸發，透過 OpenClaw system event 讓 AI agent 執行完整流程

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$BLOG_DIR/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
LOG_FILE="$LOG_DIR/autopilot_${TIMESTAMP}.log"

echo "[$(date)] Starting X-Blog Autopilot..." | tee -a "$LOG_FILE"

# Send system event to OpenClaw to trigger the AI agent
openclaw event send --type "x-blog-autopilot" \
  --message "執行 X → Blog 自動發佈流程：
1. 用 web_search 搜尋 AI 科技、經濟財金、科技產業的最新熱門話題（過去 3 小時）
2. 選擇最有價值的 1 個主題，撰寫一篇 SEO 優化繁體中文 Blog 文章
3. 文章格式：title, date, description, categories, tags, image, readingTime, FAQ section
4. 儲存到 ~/blog/content/ 對應分類目錄
5. 產生封面圖存到 ~/blog/static/images/ 對應目錄
6. cd ~/blog && git add -A && git commit && git push
7. 完成後在 Telegram 通知 Simon 文章標題和連結
主題範圍：AI/LLM/chips/robotics、Fed/台股/美股/crypto、Apple/Google/Meta/TSMC/Nvidia、地緣政治對科技影響
注意：避免重複最近已發佈的主題（先檢查 ~/blog/content/ 最近文章）" \
  2>&1 | tee -a "$LOG_FILE"

echo "[$(date)] Event sent." | tee -a "$LOG_FILE"

# Clean up old logs (keep 7 days)
find "$LOG_DIR" -name "autopilot_*.log" -mtime +7 -delete 2>/dev/null || true
