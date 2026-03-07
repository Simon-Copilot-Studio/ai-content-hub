#!/bin/bash
# publish-article.sh — 發佈 Hugo 文章並推送到 GitHub
#
# 使用方式：
#   bash publish-article.sh --category tech --title "文章標題" --content /tmp/article.md
#   bash publish-article.sh -c economy -t "財經分析" -f /tmp/content.md
#
# 參數：
#   --category / -c   分類 (tech|economy|entertainment|news|fiction)
#   --title    / -t   文章標題
#   --content  / -f   內容檔案路徑（純文字，不含 front matter）
#   --draft    / -d   設為草稿（可選，預設 false）
#   --image    / -i   封面圖片 URL（可選）
#   --tags     / -T   標籤，逗號分隔（可選）

set -euo pipefail

# ── 顏色輸出 ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ── 預設值 ────────────────────────────────────────────────
CATEGORY=""
TITLE=""
CONTENT_FILE=""
DRAFT="false"
IMAGE=""
TAGS=""
REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || echo ".")"

# ── 解析參數 ──────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --category|-c) CATEGORY="$2"; shift 2 ;;
    --title|-t)    TITLE="$2";    shift 2 ;;
    --content|-f)  CONTENT_FILE="$2"; shift 2 ;;
    --draft|-d)    DRAFT="true";  shift ;;
    --image|-i)    IMAGE="$2";    shift 2 ;;
    --tags|-T)     TAGS="$2";     shift 2 ;;
    *) log_error "未知參數: $1"; exit 1 ;;
  esac
done

# ── 驗證必要參數 ──────────────────────────────────────────
[[ -z "$CATEGORY" ]] && { log_error "缺少 --category"; exit 1; }
[[ -z "$TITLE"    ]] && { log_error "缺少 --title";    exit 1; }
[[ -z "$CONTENT_FILE" ]] && { log_error "缺少 --content"; exit 1; }
[[ ! -f "$CONTENT_FILE" ]] && { log_error "內容檔案不存在: $CONTENT_FILE"; exit 1; }

VALID_CATEGORIES="tech economy entertainment news fiction"
if ! echo "$VALID_CATEGORIES" | grep -qw "$CATEGORY"; then
  log_error "無效分類: $CATEGORY（允許：$VALID_CATEGORIES）"
  exit 1
fi

# ── 產生 slug ─────────────────────────────────────────────
generate_slug() {
  local title="$1"
  # 轉小寫、移除特殊字元、空格換 -
  echo "$title" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9\u4e00-\u9fff ]/-/g' \
    | sed 's/ \+/-/g' \
    | sed 's/-\+/-/g' \
    | sed 's/^-//;s/-$//' \
    | cut -c1-60
}

# ── 計算閱讀時間 ──────────────────────────────────────────
estimate_reading_time() {
  local file="$1"
  local word_count
  word_count=$(wc -w < "$file")
  # 中文約 300 字/分鐘，英文約 200 字/分鐘
  echo $(( (word_count / 250) + 1 ))
}

# ── 設定變數 ──────────────────────────────────────────────
DATE=$(date +%Y-%m-%d)
DATETIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SLUG=$(generate_slug "$TITLE")
READING_TIME=$(estimate_reading_time "$CONTENT_FILE")

# 預設圖片（依分類）
if [[ -z "$IMAGE" ]]; then
  case "$CATEGORY" in
    tech)          IMAGE="https://images.unsplash.com/photo-1518770660439-4636190af475?w=800" ;;
    economy)       IMAGE="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800" ;;
    entertainment) IMAGE="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800" ;;
    news)          IMAGE="https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800" ;;
    fiction)       IMAGE="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800" ;;
  esac
fi

# 標籤格式轉換（逗號分隔 → YAML 陣列）
format_tags() {
  local tags="$1"
  if [[ -z "$tags" ]]; then
    echo '[]'
  else
    echo -n '['
    IFS=',' read -ra tag_arr <<< "$tags"
    for i in "${!tag_arr[@]}"; do
      tag="${tag_arr[$i]// /}"
      [[ $i -gt 0 ]] && echo -n ', '
      echo -n "\"$tag\""
    done
    echo ']'
  fi
}

TAGS_YAML=$(format_tags "$TAGS")

# ── 目標路徑 ──────────────────────────────────────────────
CONTENT_DIR="$REPO_ROOT/content/$CATEGORY"
OUTPUT_FILE="$CONTENT_DIR/${DATE}-${SLUG}.md"

mkdir -p "$CONTENT_DIR"

# ── 寫入文章 ──────────────────────────────────────────────
log_info "建立文章：$OUTPUT_FILE"

cat > "$OUTPUT_FILE" << FRONTMATTER
---
title: "$TITLE"
date: $DATETIME
description: ""
categories: ["$CATEGORY"]
tags: $TAGS_YAML
image: "$IMAGE"
readingTime: $READING_TIME
draft: $DRAFT
slug: "$SLUG"
---

FRONTMATTER

# 附加內容
cat "$CONTENT_FILE" >> "$OUTPUT_FILE"

log_ok "文章已建立：$OUTPUT_FILE"

# ── Git 操作 ──────────────────────────────────────────────
cd "$REPO_ROOT"

log_info "執行 git add..."
git add "content/$CATEGORY/${DATE}-${SLUG}.md"

log_info "執行 git commit..."
git commit -m "feat($CATEGORY): 新增文章《$TITLE》

自動發佈 | $(date +'%Y-%m-%d %H:%M %Z')
分類：$CATEGORY
Slug：$SLUG"

log_info "執行 git push..."
git push origin main

log_ok "文章已推送！CI/CD pipeline 已觸發。"
log_info "預計 2-3 分鐘後可在網站查看：https://ai-content-hub.pages.dev/$CATEGORY/$SLUG/"

echo ""
echo "📄 文章資訊"
echo "   分類：$CATEGORY"
echo "   標題：$TITLE"
echo "   Slug：$SLUG"
echo "   路徑：content/$CATEGORY/${DATE}-${SLUG}.md"
echo "   日期：$DATE"
echo "   閱讀時間：${READING_TIME} 分鐘"
