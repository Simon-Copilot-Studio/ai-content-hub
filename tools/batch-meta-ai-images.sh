#!/bin/bash
# batch-meta-ai-images.sh — Generate missing recipe images via Meta AI Imagine
# Uses mcporter → meta-ai MCP server (Playwright browser automation)
# Each call generates 4 images, we pick the first one
set -uo pipefail

MCPORTER_CONFIG="$HOME/.openclaw/workspace/config/mcporter.json"
CONTENT_DIR="$HOME/blog/content/en/recipes"
STATIC_DIR="$HOME/blog/static/images/recipes"
LOG="/tmp/batch-meta-ai-images.log"
PROGRESS="/tmp/batch-meta-ai-images-progress.txt"

mkdir -p "$STATIC_DIR"

SUCCESS=0
FAIL=0
TOTAL=0
CONSECUTIVE_FAIL=0

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting Meta AI batch image generation" | tee "$LOG"

# Build list of missing images
MISSING_LIST=$(mktemp)
for f in $(find "$CONTENT_DIR" -name "*.md" | sort); do
  img=$(grep -m1 'image:' "$f" | sed 's/.*image:\s*["]*//;s/["]*$//')
  title=$(grep -m1 'title:' "$f" | sed 's/.*title:\s*["]*//;s/["]*$//')
  if [ -n "$img" ] && [ ! -f "$HOME/blog/static/$img" ]; then
    slug=$(basename "$img" .jpg)
    echo "${slug}|${title}" >> "$MISSING_LIST"
    TOTAL=$((TOTAL+1))
  fi
done

echo "Total missing: $TOTAL" | tee -a "$LOG"
echo "0/$TOTAL" > "$PROGRESS"

generate_image() {
  local slug="$1"
  local title="$2"
  local outpath="${STATIC_DIR}/${slug}.jpg"
  local prompt="Professional food photography of ${title}, beautifully plated on elegant dinnerware, warm natural lighting, shallow depth of field, top-down angle, restaurant quality, appetizing colors, clean background, 4K quality"
  
  # Escape quotes in prompt for JSON
  local escaped_prompt=$(echo "$prompt" | sed 's/"/\\"/g')
  
  for attempt in 1 2 3; do
    local result
    result=$(mcporter --config "$MCPORTER_CONFIG" call meta-ai.generate_image \
      --args "{\"prompt\": \"${escaped_prompt}\", \"aspect_ratio\": \"16:9\"}" 2>&1)
    
    # Extract first image path
    local img_path
    img_path=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['images'][0]['path'])" 2>/dev/null)
    
    if [ -n "$img_path" ] && [ -f "$img_path" ]; then
      # Convert PNG to JPG and copy to destination
      if command -v convert &>/dev/null; then
        convert "$img_path" -quality 85 "$outpath" 2>/dev/null
      else
        cp "$img_path" "${outpath%.jpg}.png"
        # Fallback: use python PIL if available
        python3 -c "from PIL import Image; Image.open('${img_path}').convert('RGB').save('${outpath}', 'JPEG', quality=85)" 2>/dev/null || cp "$img_path" "$outpath"
      fi
      
      if [ -f "$outpath" ] && [ "$(stat -c%s "$outpath" 2>/dev/null || echo 0)" -gt 5000 ]; then
        return 0
      fi
    fi
    
    echo "    Attempt $attempt failed, retrying..." | tee -a "$LOG"
    sleep $((attempt * 5))
  done
  
  return 1
}

while IFS='|' read -r slug title; do
  CURRENT=$((SUCCESS + FAIL + 1))
  echo "$(date '+%H:%M:%S') [$CURRENT/$TOTAL] Generating: $title" | tee -a "$LOG"
  
  if generate_image "$slug" "$title"; then
    SUCCESS=$((SUCCESS+1))
    CONSECUTIVE_FAIL=0
    echo "  ✅ $slug.jpg" | tee -a "$LOG"
  else
    FAIL=$((FAIL+1))
    CONSECUTIVE_FAIL=$((CONSECUTIVE_FAIL+1))
    echo "  ❌ Failed: $slug" | tee -a "$LOG"
  fi
  
  echo "${SUCCESS}/${TOTAL} (fail:${FAIL})" > "$PROGRESS"
  
  # Cooldown on consecutive failures
  if [ $CONSECUTIVE_FAIL -ge 5 ]; then
    echo "$(date '+%H:%M:%S') ⚠️ 5 consecutive failures, cooling down 3 min..." | tee -a "$LOG"
    sleep 180
    CONSECUTIVE_FAIL=0
  fi
  
  # Auto git commit every 30 successes
  if [ $((SUCCESS % 30)) -eq 0 ] && [ $SUCCESS -gt 0 ]; then
    cd ~/blog
    git add static/images/recipes/
    git commit -m "🖼️ Add recipe images via Meta AI (batch ${SUCCESS}/${TOTAL})" --no-verify 2>/dev/null || true
    echo "$(date '+%H:%M:%S') 📦 Git commit at $SUCCESS images" | tee -a "$LOG"
  fi
  
  # Delay between requests to avoid rate limiting
  sleep 5
done < "$MISSING_LIST"

# Final commit + push
cd ~/blog
git add static/images/recipes/
git commit -m "🖼️ Recipe images complete via Meta AI: ${SUCCESS}/${TOTAL}" --no-verify 2>/dev/null || true
git push origin main 2>/dev/null || true

echo "$(date '+%Y-%m-%d %H:%M:%S') DONE: ${SUCCESS}/${TOTAL} success, ${FAIL} failed" | tee -a "$LOG"
rm -f "$MISSING_LIST"
