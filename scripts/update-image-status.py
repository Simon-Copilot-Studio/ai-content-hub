#!/usr/bin/env python3
"""Update image-prompts.json and article front matter for a generated image."""
import json
import sys
import time
import re
from pathlib import Path

PROJECT = Path(__file__).parent.parent
PROMPTS_FILE = PROJECT / "data" / "image-prompts.json"

def update(slug, category, image_path):
    with open(PROMPTS_FILE, 'r') as f:
        data = json.load(f)
    
    updated = 0
    for p in data:
        if p['slug'] == slug and p['status'] == 'pending':
            p['status'] = 'done'
            p['generated_image'] = image_path
            p['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            
            # Update front matter
            filepath = Path(p['filepath'])
            if filepath.exists():
                content = filepath.read_text(encoding='utf-8')
                # Replace image line in front matter
                content = re.sub(
                    r'^image:\s*"[^"]*"',
                    f'image: "{image_path}"',
                    content,
                    count=1,
                    flags=re.MULTILINE
                )
                filepath.write_text(content, encoding='utf-8')
                print(f"✅ Updated: {filepath.name}")
            updated += 1
    
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Total entries updated: {updated}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: update-image-status.py <slug> <category> <image_path>")
        sys.exit(1)
    update(sys.argv[1], sys.argv[2], sys.argv[3])
