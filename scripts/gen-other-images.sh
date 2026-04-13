#!/bin/bash
# Generate missing images for tech/news/economy/entertainment articles

BLOG_DIR=~/blog
MCPORTER_CONFIG=~/.openclaw/workspace/config/mcporter.json

process_article() {
    local file=$1
    local section=$2
    
    local current_img=$(grep "^image:" "$file" | sed 's/image: "//;s/"//')
    
    # Skip if image exists on disk
    if [ -f "$BLOG_DIR/static/$current_img" ]; then
        return 0
    fi
    
    # Skip external URLs
    if echo "$current_img" | grep -q "^http"; then
        return 0
    fi
    
    local title=$(grep "^title:" "$file" | sed 's/title: "//;s/"//')
    local basename=$(basename "$file" .md)
    local outfile="$BLOG_DIR/static/images/${section}/${basename}.jpg"
    
    mkdir -p "$BLOG_DIR/static/images/${section}"
    
    local prompt="Professional editorial illustration for article titled '${title}', modern tech aesthetic, clean design, professional, 4K"
    
    echo "GENERATING [$section]: $title"
    local result=$(mcporter --config "$MCPORTER_CONFIG" call meta-ai.generate_image \
        --timeout 120000 \
        --args "{\"prompt\": $(echo "$prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'), \"aspect_ratio\": \"16:9\"}" 2>&1)
    
    local path=$(echo "$result" | grep '"path"' | head -1 | sed 's/.*"path": "//;s/".*//')
    
    if [ -n "$path" ] && [ -f "$path" ]; then
        cp "$path" "$outfile"
        local rel_img="images/${section}/${basename}.jpg"
        sed -i "s|^image:.*|image: \"$rel_img\"|" "$file"
        echo "  -> $outfile"
        sleep 3
    else
        echo "  FAILED"
    fi
}

for section in tech news economy entertainment; do
    echo "=== $section ==="
    for file in "$BLOG_DIR"/content/${section}/*.md; do
        [ -f "$file" ] || continue
        process_article "$file" "$section"
    done
    echo ""
done

# Also handle 2026-03-14 old files if any
for file in "$BLOG_DIR"/content/2026-03-14/*.md 2>/dev/null; do
    [ -f "$file" ] || continue
    process_article "$file" "2026-03-14"
done

echo "=== Done! ==="
