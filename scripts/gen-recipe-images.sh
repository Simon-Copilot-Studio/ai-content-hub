#!/bin/bash
# Recipe Image Generator
# Reads recipe titles, generates food photography images via Meta AI

BLOG_DIR=~/blog
MCPORTER_CONFIG=~/.openclaw/workspace/config/mcporter.json
IMG_DIR_ZH=$BLOG_DIR/static/images/recipes
IMG_DIR_EN=$BLOG_DIR/static/images/recipes

mkdir -p "$IMG_DIR_ZH" "$IMG_DIR_EN"

process_recipe() {
    local file=$1
    local lang=$2
    
    # Get current image path
    local current_img=$(grep "^image:" "$file" | sed 's/image: "//;s/"//')
    
    # Skip if image already exists on disk
    if [ -f "$BLOG_DIR/static/$current_img" ]; then
        return 0
    fi
    
    # Skip if using external URL (unsplash etc)
    if echo "$current_img" | grep -q "^http"; then
        return 0
    fi
    
    # Get title for prompt
    local title=$(grep "^title:" "$file" | sed 's/title: "//;s/"//')
    local basename=$(basename "$file" .md)
    
    # Build food photography prompt
    local prompt
    if [ "$lang" = "zh" ]; then
        prompt="Professional food photography of ${title}, beautifully plated on elegant dishware, warm natural lighting, shallow depth of field, appetizing and delicious looking, top-down angle, 4K"
    else
        prompt="Professional food photography of ${title}, beautifully plated, warm natural lighting, shallow depth of field, appetizing, restaurant quality presentation, 4K"
    fi
    
    local outfile="$BLOG_DIR/static/images/recipes/${basename}.jpg"
    
    echo "GENERATING: $title"
    local result=$(mcporter --config "$MCPORTER_CONFIG" call meta-ai.generate_image \
        --timeout 120000 \
        --args "{\"prompt\": $(echo "$prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'), \"aspect_ratio\": \"16:9\"}" 2>&1)
    
    local path=$(echo "$result" | grep '"path"' | head -1 | sed 's/.*"path": "//;s/".*//')
    
    if [ -n "$path" ] && [ -f "$path" ]; then
        cp "$path" "$outfile"
        # Update markdown to point to local image
        local rel_img="images/recipes/${basename}.jpg"
        sed -i "s|^image:.*|image: \"$rel_img\"|" "$file"
        echo "  -> $outfile"
        return 1
    else
        echo "  FAILED: $title"
        return 0
    fi
}

# Process Chinese recipes
echo "=== Chinese Recipes ==="
count=0
for file in "$BLOG_DIR"/content/recipes/*.md; do
    [ -f "$file" ] || continue
    process_recipe "$file" "zh"
    if [ $? -eq 1 ]; then
        count=$((count+1))
        sleep 3  # Rate limit
    fi
done
echo "Generated: $count Chinese recipe images"

# Process English recipes
echo ""
echo "=== English Recipes ==="
count=0
for file in "$BLOG_DIR"/content/en/recipes/*.md; do
    [ -f "$file" ] || continue
    process_recipe "$file" "en"
    if [ $? -eq 1 ]; then
        count=$((count+1))
        sleep 3  # Rate limit
    fi
done
echo "Generated: $count English recipe images"

echo ""
echo "=== All done! ==="
