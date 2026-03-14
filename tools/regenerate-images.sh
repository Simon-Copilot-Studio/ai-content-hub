#!/bin/bash
# Regenerate 13 images with improved prompts (English text, avoid flags/faces)
set -euo pipefail

HF_API="https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_KEY="${HUGGINGFACE_API_KEY}"
BASE_DIR=~/blog/static/images

generate() {
  local category="$1"
  local slug="$2"
  local prompt="$3"
  local outpath="${BASE_DIR}/${category}/${slug}.jpg"
  
  echo "[$(date +%H:%M:%S)] Generating: ${category}/${slug}"
  
  # Backup old image
  if [ -f "$outpath" ]; then
    cp "$outpath" "${outpath}.bak"
  fi
  
  local status
  status=$(curl -s -o "$outpath" -w "%{http_code}" \
    -X POST "$HF_API" \
    -H "Authorization: Bearer $HF_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"inputs\":\"${prompt}\",\"parameters\":{\"width\":1024,\"height\":576}}")
  
  if [ "$status" = "200" ]; then
    local size=$(stat -c%s "$outpath")
    if [ "$size" -gt 10000 ]; then
      echo "  ✅ OK (${size} bytes)"
      rm -f "${outpath}.bak"
      return 0
    else
      echo "  ❌ Too small (${size} bytes), restoring backup"
      mv "${outpath}.bak" "$outpath" 2>/dev/null || true
      return 1
    fi
  else
    echo "  ❌ HTTP ${status}, restoring backup"
    mv "${outpath}.bak" "$outpath" 2>/dev/null || true
    return 1
  fi
}

echo "Starting regeneration at $(date)"
echo "================================"

# 1. 戴湘儀不連任 (Score 2) - Taiwan female politician stepping down
generate "news" "2026-03-12-dai-xiang-yi-retire" \
  "Elegant Asian woman in professional business suit standing at a modern podium with microphones, warm lighting, press conference setting, wooden panel backdrop, bouquet of flowers on the podium suggesting farewell ceremony, photorealistic editorial photography, no text no logos"

sleep 4

# 2. 蕭敬嚴藍營內鬥 (Score 3) - KMT internal conflict
generate "news" "2026-03-12-xiao-jing-yan-kmt-primary" \
  "Dramatic split image of two opposing groups of Asian politicians in suits arguing across a conference table, tense body language, modern government meeting room, blue and white color scheme, dramatic side lighting, photorealistic editorial photography, no text no banners"

sleep 4

# 3. 卓榮泰赴日爭議 (Score 3) - Premier's Japan trip controversy
generate "news" "2026-03-12-premier-cho-japan-controversy" \
  "Private luxury jet on airport tarmac at dusk, baseball stadium visible in background with bright stadium lights, dramatic contrast between the airplane and the sports venue, photorealistic editorial photography, no text no logos no flags"

sleep 4

# 4. Gogoro欠款 (Score 5) - Founder's debt scandal
generate "tech" "2026-03-12-gogoro-lu-xuesen-debt" \
  "Sleek electric scooter parked in front of a closed corporate office with dim lighting, legal documents and court gavel on a desk in foreground, dramatic noir lighting, concept of business dispute, photorealistic editorial photography, no text"

sleep 4

# 5. 301調查 (Score 5) - US trade investigation
generate "tech" "2026-03-12-us-301-investigation-taiwan" \
  "Container cargo ship at a busy port with stacked colorful shipping containers, dramatic cloudy sky suggesting trade tensions, industrial cranes in background, wide angle photorealistic editorial photography, no text no flags"

sleep 4

# 6. 陳芳語回歸 (Score 5) - Singer comeback
generate "entertainment" "2026-03-12-chen-fang-yu-comeback" \
  "Asian female singer performing on stage with colorful concert lights, holding a microphone, energetic pose, confetti falling, packed audience in background, vibrant purple and gold stage lighting, photorealistic concert photography, no text"

sleep 4

# 7. 王炸姐爆紅 (Score 5) - Viral social media phenomenon
generate "news" "2026-03-12-wang-zha-jie-social-media" \
  "Smartphone screen showing viral video content with thousands of heart and like notifications floating around the phone, neon pink and blue glow, social media icons scattered, shallow depth of field, photorealistic product photography, no readable text"

sleep 4

# 8. 群創成交量 (Score 6) - Record trading volume
generate "economy" "2026-03-12-innolux-record-volume" \
  "Dramatic close-up of electronic stock market trading screen showing green and red numbers and candlestick charts with massive volume bars, reflection of excited traders visible in the screen, photorealistic financial photography, no readable text"

sleep 4

# 9. 賴雅妍演唱會 (Score 6) - Female actress first concert
generate "entertainment" "2026-03-12-lai-ya-yan-concert-2026" \
  "Beautiful Asian woman in elegant concert dress singing on intimate livehouse stage, warm spotlight, small venue with close audience, acoustic guitar on stand nearby, fairy lights decoration, photorealistic concert photography, no text"

sleep 4

# 10. 林家正火腿 (Score 6) - Baseball player joins Japan team
generate "entertainment" "2026-03-12-lin-chia-cheng-nippon-ham" \
  "Asian baseball player in white pinstripe uniform number 38 making a powerful batting swing at night game, Japanese baseball stadium with bright lights, dynamic action shot, photorealistic sports photography, no text on uniform except number 38"

sleep 4

# 11. 北極星藥業減資 (Score 6) - Pharma company crisis
generate "economy" "2026-03-12-polaris-pharma-capital-reduction" \
  "Empty pharmaceutical factory floor with idle machinery and turned off lights, padlock on gate, red downward arrow graphic overlaid suggesting stock crash, dramatic moody lighting, photorealistic industrial photography, no text"

sleep 4

# 12. 鶯歌平交道 (Score 6) - Taiwan railroad crossing accident
generate "news" "2026-03-12-train-accident-yingge" \
  "Railroad level crossing with red warning lights flashing and barrier gate down, approaching commuter train in background, Asian suburban setting with scooters and small buildings, overcast sky, photorealistic news photography, no text"

sleep 4

# 13. WBC賽程表 (Score 6) - WBC bracket schedule
generate "entertainment" "2026-03-12-wbc-2026-bracket-schedule" \
  "Baseball diamond from aerial view during international tournament, packed stadium with colorful crowd, multiple baseball teams warming up, dramatic golden hour lighting, wide angle photorealistic sports photography, no text no logos no flags"

echo ""
echo "================================"
echo "Regeneration complete at $(date)"
echo "Total: 13 images"
