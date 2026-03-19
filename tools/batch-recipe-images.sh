#!/bin/bash
# batch-recipe-images.sh — Generate missing recipe images via HF FLUX.1-schnell
# Runs in background (nohup), auto-retries, auto-commits every 50 images
set -uo pipefail

HF_API="https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_KEY="${HUGGINGFACE_API_KEY}"
BASE_DIR="${HOME}/blog/static/images/recipes"
CONTENT_DIR="${HOME}/blog/content/en/recipes"
LOG="/tmp/batch-recipe-images.log"
PROGRESS="/tmp/batch-recipe-images-progress.txt"

mkdir -p "$BASE_DIR"

SUCCESS=0
FAIL=0
TOTAL=0
CONSECUTIVE_FAIL=0

echo "$(date '+%Y-%m-%d %H:%M:%S') Starting batch recipe image generation" | tee "$LOG"

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
  local outpath="${BASE_DIR}/${slug}.jpg"
  # Create food photography prompt from title
  local prompt="Professional food photography of ${title}, beautifully plated on elegant dinnerware, warm natural lighting, shallow depth of field, top-down angle, restaurant quality, appetizing colors, clean background"
  
  for attempt in 1 2 3; do
    STATUS=$(curl -s -o "$outpath" -w "%{http_code}" --max-time 30 \
      -X POST "$HF_API" \
      -H "Authorization: Bearer $HF_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"inputs\":\"${prompt}\",\"parameters\":{\"width\":1024,\"height\":576}}")
    
    if [ "$STATUS" = "200" ] && [ -f "$outpath" ] && [ "$(stat -c%s "$outpath" 2>/dev/null || echo 0)" -gt 10000 ]; then
      return 0
    fi
    
    # Rate limit or server error - wait
    if [ "$STATUS" = "429" ] || [ "$STATUS" = "503" ]; then
      sleep $((attempt * 10))
    else
      sleep $((attempt * 3))
    fi
  done
  
  rm -f "$outpath"
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
  if [ $CONSECUTIVE_FAIL -ge 10 ]; then
    echo "$(date '+%H:%M:%S') ⚠️ 10 consecutive failures, cooling down 5 min..." | tee -a "$LOG"
    sleep 300
    CONSECUTIVE_FAIL=0
  fi
  
  # Auto git commit every 50 successes
  if [ $((SUCCESS % 50)) -eq 0 ] && [ $SUCCESS -gt 0 ]; then
    cd ~/blog
    git add static/images/recipes/
    git commit -m "🖼️ Add recipe images (batch ${SUCCESS}/${TOTAL})" --no-verify 2>/dev/null || true
    echo "$(date '+%H:%M:%S') 📦 Git commit at $SUCCESS images" | tee -a "$LOG"
  fi
  
  # Small delay between requests
  sleep 2
done < "$MISSING_LIST"

# Final commit + push
cd ~/blog
git add static/images/recipes/
git commit -m "🖼️ Recipe images complete: ${SUCCESS}/${TOTAL} generated" --no-verify 2>/dev/null || true
git push origin main 2>/dev/null || true

echo "$(date '+%Y-%m-%d %H:%M:%S') DONE: ${SUCCESS}/${TOTAL} success, ${FAIL} failed" | tee -a "$LOG"
rm -f "$MISSING_LIST"
