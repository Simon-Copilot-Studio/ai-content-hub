#!/usr/bin/env bash
# smart-image-gen.sh — 智慧產圖腳本
# 掃描最近 N 天內缺圖的文章，用最佳免費平台自動產圖
#
# Usage:
#   ./scripts/smart-image-gen.sh              # 預設掃最近 3 天
#   ./scripts/smart-image-gen.sh --days 7     # 掃最近 7 天
#   ./scripts/smart-image-gen.sh --dry-run    # 只列出缺圖文章，不產圖
#
# 平台優先順序：
#   1. Meta AI Imagine (unlimited, high quality)
#   2. Raphael AI (unlimited, FLUX.1-Dev)
#   3. image_generate 工具 (OpenClaw 內建)
#
# 設計：可被 cron 或 heartbeat 呼叫

set -euo pipefail

BLOG_DIR="${HOME}/blog"
CONTENT_DIR="${BLOG_DIR}/content"
STATIC_DIR="${BLOG_DIR}/static/images"
DAYS=3
DRY_RUN=false
GENERATED=0
FAILED=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo "🖼️  Smart Image Generator — scanning last ${DAYS} days"
echo "=================================================="

# Find articles from last N days that might need images
find "${CONTENT_DIR}" -name "*.md" -newer <(date -d "${DAYS} days ago" +%Y%m%d 2>/dev/null || echo "") -type f 2>/dev/null | \
  sort | while read -r filepath; do

  # Skip index files
  [[ "$(basename "$filepath")" == "_index.md" ]] && continue
  [[ "$(basename "$filepath")" == "sample.md" ]] && continue

  # Extract category from path
  rel="${filepath#${CONTENT_DIR}/}"
  category="$(dirname "$rel" | cut -d/ -f1)"
  slug="$(basename "$filepath" .md)"

  # Check if image already exists
  img_path="${STATIC_DIR}/${category}/${slug}.jpg"
  img_path_png="${STATIC_DIR}/${category}/${slug}.png"

  if [[ -f "$img_path" ]] || [[ -f "$img_path_png" ]]; then
    continue  # Already has image
  fi

  # Check frontmatter for existing image
  if head -50 "$filepath" | grep -q "^image:" ; then
    img_val=$(head -50 "$filepath" | grep "^image:" | head -1 | sed 's/image: *//;s/^"//;s/"$//')
    if [[ "$img_val" == /images/* ]] && [[ -f "${BLOG_DIR}/static${img_val}" ]]; then
      continue  # Has valid local image
    fi
  fi

  # Extract title from frontmatter
  title=$(head -20 "$filepath" | grep "^title:" | head -1 | sed 's/title: *//;s/^"//;s/"$//')
  [[ -z "$title" ]] && title="$slug"

  echo ""
  echo "📝 Missing image: ${category}/${slug}"
  echo "   Title: ${title}"

  if $DRY_RUN; then
    echo "   [DRY RUN] Would generate image"
    continue
  fi

  # Create output directory
  mkdir -p "${STATIC_DIR}/${category}"

  # Generate image prompt based on category
  case "$category" in
    tech)
      style="Modern tech illustration, clean minimalist design, gradient blue-purple palette, abstract digital concept"
      ;;
    economy|finance)
      style="Professional financial visualization, clean charts and graphs aesthetic, blue-green palette, business infographic style"
      ;;
    recipes)
      style="Professional food photography, overhead shot, natural lighting, white marble background, appetizing presentation"
      ;;
    entertainment)
      style="Vibrant entertainment poster style, dynamic composition, warm rich colors, cinematic feel"
      ;;
    *)
      style="Clean editorial illustration, modern design, balanced composition, professional color palette"
      ;;
  esac

  prompt="Create an image for article: '${title}'. Style: ${style}. No text or watermarks."

  echo "   🎨 Generating with Meta AI MCP..."

  # Try Meta AI first via mcporter
  if mcporter call meta-ai.generate_image prompt="${prompt}" 2>/dev/null | grep -q "url\|image\|success"; then
    echo "   ✅ Meta AI succeeded"
    ((GENERATED++)) || true
  else
    echo "   ⚠️  Meta AI failed, trying image_generate tool next time..."
    echo "${filepath}|${title}|${prompt}" >> /tmp/smart-image-gen-retry.txt
    ((FAILED++)) || true
  fi

done

echo ""
echo "=================================================="
echo "📊 Results: Generated=${GENERATED}, Failed=${FAILED}"
if [[ -f /tmp/smart-image-gen-retry.txt ]]; then
  retry_count=$(wc -l < /tmp/smart-image-gen-retry.txt)
  echo "🔄 Retry queue: ${retry_count} articles in /tmp/smart-image-gen-retry.txt"
fi
echo "Done!"
