#!/bin/bash
# Fiction Genre Shared Images Generator
# Maps fiction tags to genre categories, generates one image per genre,
# then copies to all fiction articles in that genre.

BLOG_DIR=~/blog
MCPORTER_CONFIG=~/.openclaw/workspace/config/mcporter.json
IMG_DIR=$BLOG_DIR/static/images/fiction

mkdir -p "$IMG_DIR"

# Genre mapping: primary tag -> genre category -> prompt
declare -A GENRE_PROMPT
GENRE_PROMPT["科幻"]="Futuristic sci-fi cityscape with neon lights and floating vehicles, cyberpunk atmosphere, dramatic lighting, cinematic, 4K"
GENRE_PROMPT["武俠"]="Ancient Chinese martial arts hero on misty mountain cliff, traditional ink painting style mixed with dramatic lighting, sword and flowing robes, cinematic, 4K"
GENRE_PROMPT["奇幻"]="Fantasy magical world with glowing crystals and enchanted forest, mystical creatures, ethereal purple and blue atmosphere, cinematic, 4K"
GENRE_PROMPT["愛情"]="Romantic couple silhouette under cherry blossom trees at sunset, warm golden light, dreamy bokeh, cinematic, 4K"
GENRE_PROMPT["校園"]="Asian university campus with students, cherry blossoms and modern architecture, warm afternoon sunlight, nostalgic atmosphere, cinematic, 4K"
GENRE_PROMPT["職場"]="Modern office with city skyline view through floor-to-ceiling windows, dramatic lighting, corporate thriller atmosphere, cinematic, 4K"
GENRE_PROMPT["驚悚"]="Dark mysterious alley with fog and single street lamp, noir thriller atmosphere, shadows and suspense, cinematic, 4K"
GENRE_PROMPT["家庭"]="Warm family dinner scene in traditional Asian home, golden lamplight, multiple generations at table, heartwarming, cinematic, 4K"
GENRE_PROMPT["歷史"]="Ancient Chinese palace courtyard in morning mist, traditional architecture with red pillars and golden roof, dramatic sky, cinematic, 4K"
GENRE_PROMPT["商戰"]="Corporate boardroom with city skyline at night, chess pieces on mahogany table, power and strategy atmosphere, cinematic, 4K"
GENRE_PROMPT["青春"]="Group of young people at a beach at golden hour, carefree summer vibes, wind-blown hair, nostalgic warm tones, cinematic, 4K"
GENRE_PROMPT["社會"]="Urban streetscape showing contrast between old and new buildings, rain-wet streets reflecting neon signs, documentary feel, cinematic, 4K"
GENRE_PROMPT["靈異"]="Haunted traditional Asian temple at twilight, fog and mysterious lantern light, eerie atmosphere, cinematic, 4K"
GENRE_PROMPT["冒險"]="Explorer standing at edge of vast canyon overlooking uncharted territory, adventure and wonder, dramatic sky, cinematic, 4K"
GENRE_PROMPT["都市"]="Bustling Asian city at night with rain reflections, noodle shops and street vendors, urban atmosphere, cinematic, 4K"

# Categorize each fiction file
categorize_fiction() {
    local file=$1
    local tags=$(grep "^tags:" "$file" | head -1)
    
    # Check tags in priority order
    for genre in "科幻" "武俠" "奇幻" "驚悚" "靈異" "愛情" "校園" "商戰" "職場" "歷史" "家庭" "青春" "社會" "冒險" "都市"; do
        if echo "$tags" | grep -q "$genre"; then
            echo "$genre"
            return
        fi
    done
    echo "都市"  # default
}

# Step 1: Generate one image per genre
echo "=== Generating genre images ==="
for genre in "${!GENRE_PROMPT[@]}"; do
    prompt="${GENRE_PROMPT[$genre]}"
    outfile="$IMG_DIR/genre-${genre}.jpg"
    
    if [ -f "$outfile" ]; then
        echo "SKIP: $genre (already exists)"
        continue
    fi
    
    echo "GENERATING: $genre"
    result=$(mcporter --config "$MCPORTER_CONFIG" call meta-ai.generate_image \
        --timeout 120000 \
        --args "{\"prompt\": \"$prompt\", \"aspect_ratio\": \"16:9\"}" 2>&1)
    
    path=$(echo "$result" | grep '"path"' | head -1 | sed 's/.*"path": "//;s/".*//')
    
    if [ -n "$path" ] && [ -f "$path" ]; then
        cp "$path" "$outfile"
        echo "  -> $outfile"
    else
        echo "  FAILED: $genre"
    fi
    
    sleep 5  # Rate limit
done

# Step 2: Update fiction articles to use genre images
echo ""
echo "=== Updating fiction articles ==="
updated=0
skipped=0

for file in "$BLOG_DIR"/content/fiction/*.md; do
    # Check if image file exists on disk
    current_img=$(grep "^image:" "$file" | sed 's/image: "//;s/"//')
    
    if [ -f "$BLOG_DIR/static/$current_img" ]; then
        skipped=$((skipped+1))
        continue
    fi
    
    # Categorize and assign genre image
    genre=$(categorize_fiction "$file")
    genre_img="images/fiction/genre-${genre}.jpg"
    
    if [ -f "$BLOG_DIR/static/$genre_img" ]; then
        # Update the image path in the markdown
        sed -i "s|^image:.*|image: \"$genre_img\"|" "$file"
        updated=$((updated+1))
    fi
done

echo "Updated: $updated files"
echo "Skipped (already have image): $skipped files"
echo "Done!"
