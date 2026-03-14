#!/bin/bash
# Generate featured images for 2026-03-12 articles using HuggingFace FLUX.1-schnell
set -euo pipefail

HF_API="https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_KEY="${HUGGINGFACE_API_KEY}"
STATIC_DIR="/home/simon/blog/static/images"
LOG="/tmp/image-gen.log"

echo "Starting image generation at $(date)" | tee "$LOG"

generate_image() {
  local category="$1"
  local slug="$2"
  local prompt="$3"
  local outfile="${STATIC_DIR}/${category}/${slug}.jpg"
  
  echo "[$(date +%H:%M:%S)] Generating: ${category}/${slug}" | tee -a "$LOG"
  
  # Generate image
  local http_code
  http_code=$(curl -s -X POST "$HF_API" \
    -H "Authorization: Bearer $HF_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"inputs\": \"${prompt}\"}" \
    -o "/tmp/gen_${slug}.jpg" \
    -w "%{http_code}" \
    --max-time 120)
  
  if [ "$http_code" = "200" ]; then
    local ftype
    ftype=$(file -b "/tmp/gen_${slug}.jpg" | head -1)
    if echo "$ftype" | grep -q "JPEG\|image"; then
      mv "/tmp/gen_${slug}.jpg" "$outfile"
      echo "  ✅ OK ($(stat -c%s "$outfile") bytes)" | tee -a "$LOG"
      return 0
    else
      echo "  ❌ Not an image: $ftype" | tee -a "$LOG"
      cat "/tmp/gen_${slug}.jpg" >> "$LOG"
      return 1
    fi
  else
    echo "  ❌ HTTP $http_code" | tee -a "$LOG"
    # Rate limit? Wait and retry
    if [ "$http_code" = "429" ] || [ "$http_code" = "503" ]; then
      echo "  ⏳ Rate limited, waiting 30s..." | tee -a "$LOG"
      sleep 30
      # Retry once
      http_code=$(curl -s -X POST "$HF_API" \
        -H "Authorization: Bearer $HF_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"inputs\": \"${prompt}\"}" \
        -o "/tmp/gen_${slug}.jpg" \
        -w "%{http_code}" \
        --max-time 120)
      if [ "$http_code" = "200" ]; then
        mv "/tmp/gen_${slug}.jpg" "$outfile"
        echo "  ✅ Retry OK" | tee -a "$LOG"
        return 0
      fi
    fi
    return 1
  fi
}

# Tech articles
generate_image "tech" "2026-03-12-ai-server-boom-2026" \
  "photorealistic modern data center server room with rows of AI computing racks, blue LED lights glowing, cables organized neatly, professional photography, wide angle shot"
sleep 3

generate_image "tech" "2026-03-12-gogoro-lu-xuesen-debt" \
  "photorealistic electric scooter parked on a Taipei city street at dusk, modern urban setting, dramatic lighting, editorial photography style"
sleep 3

generate_image "tech" "2026-03-12-innolux-silicon-photonics" \
  "photorealistic close-up of silicon photonics chip on circuit board, fiber optic cables connected, blue and green light traces, semiconductor technology photography"
sleep 3

generate_image "tech" "2026-03-12-us-301-investigation-taiwan" \
  "photorealistic photo of US and Taiwan flags side by side on a diplomatic conference table, trade documents scattered, serious atmosphere, editorial photography"
sleep 3

# Economy articles
generate_image "economy" "2026-03-12-innolux-record-volume" \
  "photorealistic LCD display panel manufacturing clean room with workers in bunny suits, automated production line, bright fluorescent lighting, industrial photography"
sleep 3

generate_image "economy" "2026-03-12-pegatron-earnings-dividend" \
  "photorealistic modern electronics factory assembly line with robotic arms, circuit boards being assembled, corporate industrial photography"
sleep 3

generate_image "economy" "2026-03-12-polaris-pharma-capital-reduction" \
  "photorealistic pharmaceutical laboratory with scientist examining test tubes, modern lab equipment, dramatic lighting, medical research photography"
sleep 3

generate_image "economy" "2026-03-12-taiwan-stock-market-outlook" \
  "photorealistic Taiwan stock exchange trading floor with digital displays showing green numbers, traders watching screens, bustling atmosphere, financial photography"
sleep 3

# Entertainment articles
generate_image "entertainment" "2026-03-12-chen-fang-yu-comeback" \
  "photorealistic concert stage with dramatic spotlights, microphone in focus, colorful stage lighting, music performance photography, pop concert atmosphere"
sleep 3

generate_image "entertainment" "2026-03-12-lai-ya-yan-concert-2026" \
  "photorealistic intimate concert venue with warm stage lighting, acoustic setup, audience silhouettes, live music photography, cozy venue atmosphere"
sleep 3

generate_image "entertainment" "2026-03-12-lin-chia-cheng-nippon-ham" \
  "photorealistic baseball player in batting stance at a Japanese baseball stadium, night game under floodlights, action sports photography"
sleep 3

generate_image "entertainment" "2026-03-12-nba-march-highlights" \
  "photorealistic NBA basketball game action shot, player dunking the ball, packed arena with fans cheering, dynamic sports photography, dramatic lighting"
sleep 3

generate_image "entertainment" "2026-03-12-wbc-2026-bracket-schedule" \
  "photorealistic international baseball tournament scoreboard with flags of multiple nations, modern stadium background, sports event photography"
sleep 3

generate_image "entertainment" "2026-03-12-wbc-2026-quarterfinals" \
  "photorealistic baseball team celebrating victory on field, players hugging, confetti falling, stadium crowd cheering, dramatic sports moment photography"
sleep 3

# News articles
generate_image "news" "2026-03-12-arbor-day-taiwan-2026" \
  "photorealistic people planting young trees in a lush Taiwan park, green mountains in background, sunny day, environmental conservation photography"
sleep 3

generate_image "news" "2026-03-12-dai-xiang-yi-retire" \
  "photorealistic modern government press conference podium with microphones, official backdrop, formal political setting, editorial photography"
sleep 3

generate_image "news" "2026-03-12-flesh-eating-bacteria-prevention" \
  "photorealistic close-up of hands being washed thoroughly under running water, medical hygiene concept, clean bright bathroom, health awareness photography"
sleep 3

generate_image "news" "2026-03-12-premier-cho-japan-controversy" \
  "photorealistic diplomatic meeting room with country flags and conference table, formal international politics setting, editorial news photography"
sleep 3

generate_image "news" "2026-03-12-train-accident-yingge" \
  "photorealistic railroad crossing with warning lights and barrier arm, Taiwan countryside setting, railway safety concept, editorial photography"
sleep 3

generate_image "news" "2026-03-12-wang-zha-jie-social-media" \
  "photorealistic smartphone screen showing viral social media notifications and trending hashtags, colorful app interface, digital culture photography"
sleep 3

generate_image "news" "2026-03-12-xiao-jing-yan-kmt-primary" \
  "photorealistic political campaign rally stage with podium and supporters holding signs, indoor convention hall, political event photography"
sleep 3

generate_image "news" "2026-03-12-xiluan-mountain-hiking" \
  "photorealistic hikers on a misty mountain trail in Taiwan, lush green forest, dramatic mountain peaks in clouds, adventure outdoor photography"
sleep 3

echo ""
echo "=== Generation Complete ===" | tee -a "$LOG"
echo "Results:" | tee -a "$LOG"

# Count successes
SUCCESS=0
FAIL=0
for f in $(find "$STATIC_DIR" -name "2026-03-12-*.jpg" -newer /tmp/image-gen.log 2>/dev/null); do
  SUCCESS=$((SUCCESS+1))
done
echo "Generated: $SUCCESS images" | tee -a "$LOG"

# Also need to update frontmatter from .webp to .jpg
echo "Don't forget to update article frontmatter image paths from .webp to .jpg!" | tee -a "$LOG"
