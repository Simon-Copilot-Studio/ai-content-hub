#!/usr/bin/env python3
"""
Recipe Image Generator — AI 食譜圖片自動生成系統
Reads recipe markdown files, generates step-by-step images via Gemini API,
saves them locally, and inserts image tags into articles.

Usage:
  python3 scripts/generate-recipe-images.py                    # All recipes
  python3 scripts/generate-recipe-images.py --file content/recipes/2026-03-08-fluffy-pancakes.md
  python3 scripts/generate-recipe-images.py --dry-run           # Preview prompts only
  python3 scripts/generate-recipe-images.py --max-per-run 10    # Limit images per run (rate limit friendly)
  python3 scripts/generate-recipe-images.py --skip-existing     # Skip recipes that already have images

Requires: GEMINI_API_KEY environment variable
"""

import os
import sys
import json
import glob
import re
import time
import base64
import urllib.request
import urllib.error
from pathlib import Path

# === Config ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = [
    PROJECT_ROOT / "content" / "recipes",
    PROJECT_ROOT / "content" / "en" / "recipes",
]
IMAGE_BASE = PROJECT_ROOT / "static" / "images" / "recipes"
SITE_IMAGE_PREFIX = "/images/recipes"
KEYS_FILE = Path.home() / ".openclaw" / "workspace" / "config" / "gemini-keys.json"

# Models to try in order (free tier rotation)
MODELS = [
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-image-preview",
    "gemini-2.0-flash-exp-image-generation",
    "nano-banana-pro-preview",
]

RATE_LIMIT_DELAY = 12  # seconds between requests (free tier: ~5 RPM)
MAX_RETRIES = 3
RETRY_DELAY = 30  # seconds after 429


def load_api_keys():
    """Load API keys from keys file + env var. Returns list of keys."""
    keys = []
    # From env
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        keys.append(env_key)
    # From keys file
    if KEYS_FILE.exists():
        try:
            with open(KEYS_FILE) as f:
                data = json.load(f)
            for k in data.get("keys", []):
                if k and k not in keys:
                    keys.append(k)
        except Exception:
            pass
    return keys


class KeyRotator:
    """Rotate through multiple API keys, skipping exhausted ones."""

    def __init__(self, keys):
        self.keys = keys
        self.exhausted = set()  # indices of exhausted keys
        self.current = 0

    def get_key(self):
        """Get next available key, or None if all exhausted."""
        if len(self.exhausted) >= len(self.keys):
            return None
        attempts = 0
        while attempts < len(self.keys):
            if self.current not in self.exhausted:
                return self.keys[self.current]
            self.current = (self.current + 1) % len(self.keys)
            attempts += 1
        return None

    def mark_exhausted(self):
        """Mark current key as exhausted (daily limit hit)."""
        print(f"  🔑 Key #{self.current + 1} exhausted, rotating...")
        self.exhausted.add(self.current)
        self.current = (self.current + 1) % len(self.keys)

    def advance(self):
        """Move to next key (for per-minute limits)."""
        self.current = (self.current + 1) % len(self.keys)

    @property
    def available(self):
        return len(self.keys) - len(self.exhausted)

# === Image Generation Plan ===
# Each recipe gets up to 5 images:
#   01-ingredients: Mise en place / ingredient layout
#   02-prep: Key preparation step (mixing, chopping, etc.)
#   03-cooking: Active cooking moment
#   04-final: Plated finished dish (hero shot)
#   05-serving: Serving suggestion / lifestyle shot


def parse_recipe_frontmatter(filepath):
    """Parse YAML front matter from a recipe markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split front matter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    fm_text = parts[1]
    body = parts[2]

    # Simple YAML parsing (no PyYAML dependency)
    fm = {}
    current_key = None
    current_list = None
    list_key = None

    for line in fm_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # List item
        if stripped.startswith('- ') and list_key:
            val = stripped[2:].strip().strip('"').strip("'")
            if list_key not in fm:
                fm[list_key] = []
            fm[list_key].append(val)
            continue

        # Key: value
        if ':' in stripped:
            indent = len(line) - len(line.lstrip())
            key_part, _, val_part = stripped.partition(':')
            key = key_part.strip()
            val = val_part.strip().strip('"').strip("'")

            if indent == 0 or indent == 2:
                if val:
                    fm[key] = val
                    list_key = None
                else:
                    list_key = key
                    fm[key] = []
            elif indent >= 4 and current_key:
                # Nested under recipe:
                if isinstance(fm.get(current_key), dict):
                    fm[current_key][key] = val
                elif current_key == 'recipe':
                    if 'recipe' not in fm or not isinstance(fm['recipe'], dict):
                        fm['recipe'] = {}
                    if val:
                        fm['recipe'][key] = val
                    else:
                        list_key = key
                        fm['recipe'][key] = []

            if indent == 0:
                current_key = key

    return fm, body


def extract_recipe_info(fm, body):
    """Extract structured recipe info for prompt generation."""
    info = {
        'title': fm.get('title', ''),
        'description': fm.get('description', ''),
        'lang': fm.get('lang', 'zh'),
        'tags': fm.get('tags', []),
        'categories': fm.get('categories', []),
    }

    # Extract recipe details
    recipe = fm.get('recipe', {})
    if isinstance(recipe, dict):
        info['ingredients'] = recipe.get('ingredients', [])
        info['steps'] = recipe.get('steps', [])
        info['cuisine'] = recipe.get('cuisine', '')
        info['category'] = recipe.get('category', '')
    else:
        info['ingredients'] = fm.get('ingredients', [])
        info['steps'] = fm.get('steps', [])
        info['cuisine'] = fm.get('cuisine', '')
        info['category'] = fm.get('category', '')

    # Extract key cooking methods from body
    cooking_keywords = []
    lower_body = body.lower()
    for kw in ['bake', 'fry', 'grill', 'boil', 'steam', 'sauté', 'roast',
                'simmer', 'whisk', 'knead', 'fold', 'chop', 'slice', 'dice',
                'stir', 'blend', 'marinate', 'broil', 'poach',
                '煎', '炒', '烤', '蒸', '煮', '滷', '燉', '炸', '拌', '切']:
        if kw in lower_body:
            cooking_keywords.append(kw)
    info['methods'] = cooking_keywords[:5]

    return info


def generate_prompts(info, slug):
    """Generate 5 image prompts tailored to this specific recipe."""
    title = info['title']
    ingredients = info.get('ingredients', [])
    steps = info.get('steps', [])
    cuisine = info.get('cuisine', '')
    methods = info.get('methods', [])
    tags = info.get('tags', [])

    # Determine visual style based on cuisine
    style_hint = "Clean, bright food photography style"
    if any(t in str(tags).lower() for t in ['japanese', '日式', '日本']):
        style_hint = "Japanese minimalist food photography, ceramic dishes, bamboo mat"
    elif any(t in str(tags).lower() for t in ['taiwanese', '台灣', '台式']):
        style_hint = "Taiwanese home-style food photography, warm lighting, traditional bowl"
    elif any(t in str(tags).lower() for t in ['korean', '韓式', '韓國']):
        style_hint = "Korean food photography, banchan style, colorful plates"
    elif any(t in str(tags).lower() for t in ['italian', '義式']):
        style_hint = "Rustic Italian food photography, wooden board, olive oil"
    elif any(t in str(tags).lower() for t in ['american', 'classic']):
        style_hint = "American comfort food photography, warm homey setting"

    base_style = (
        f"{style_hint}. Shot on a 50mm lens, f/2.8, natural window light from left side. "
        "Shallow depth of field. No text, no watermarks, no logos, no human hands visible. "
        "Professional food styling."
    )

    prompts = []

    # 01 - Ingredients mise en place
    if ingredients:
        ing_list = ', '.join(ingredients[:8])
        prompts.append({
            'id': '01-ingredients',
            'alt': f'{title} - Ingredients',
            'prompt': (
                f"Overhead food photography: mise en place for {title}. "
                f"Ingredients neatly arranged in small bowls and measuring cups on a clean surface: {ing_list}. "
                f"Everything measured and ready to cook. {base_style}"
            )
        })

    # 02 - Key preparation step
    if steps and len(steps) >= 2:
        prep_step = steps[0] if len(steps) > 0 else "preparing ingredients"
        prompts.append({
            'id': '02-preparation',
            'alt': f'{title} - Preparation',
            'prompt': (
                f"Food photography close-up: {prep_step} "
                f"for making {title}. Show the mixing bowl or cutting board with ingredients "
                f"in the process of being prepared. Action frozen mid-step. {base_style}"
            )
        })

    # 03 - Active cooking
    if steps and len(steps) >= 4:
        cook_step = steps[len(steps) // 2]  # Middle step is usually the cooking
        method_hint = f"using {methods[0]}" if methods else "being cooked"
        prompts.append({
            'id': '03-cooking',
            'alt': f'{title} - Cooking',
            'prompt': (
                f"Food photography: {cook_step} "
                f"Close-up of {title} {method_hint} in a pan/pot on the stove. "
                f"Steam or sizzle visible. Warm tones. {base_style}"
            )
        })
    elif methods:
        prompts.append({
            'id': '03-cooking',
            'alt': f'{title} - Cooking',
            'prompt': (
                f"Food photography: {title} being cooked, action shot showing the "
                f"{methods[0]}ing process. Warm kitchen lighting. {base_style}"
            )
        })

    # 04 - Finished dish (hero shot)
    prompts.append({
        'id': '04-finished',
        'alt': f'{title} - Finished Dish',
        'prompt': (
            f"Professional food photography hero shot: beautifully plated {title}. "
            f"The dish is perfectly cooked and garnished, served on an elegant plate. "
            f"45-degree angle. Appetizing and Instagram-worthy. {base_style}"
        )
    })

    # 05 - Serving / lifestyle
    desc = info.get('description', title)
    prompts.append({
        'id': '05-serving',
        'alt': f'{title} - Serving Suggestion',
        'prompt': (
            f"Lifestyle food photography: {title} served at a dining table setting. "
            f"Complete meal presentation with side dishes, utensils, napkin, and drink. "
            f"Warm, inviting atmosphere. Bird's eye view or 30-degree angle. {base_style}"
        )
    })

    return prompts


def generate_image(prompt, output_path, key_rotator, model_index=0):
    """Generate an image using Gemini API with key rotation. Returns True on success."""
    if model_index >= len(MODELS):
        # All models tried with current key, try next key
        key_rotator.mark_exhausted()
        if key_rotator.available > 0:
            print(f"  🔄 Trying next API key ({key_rotator.available} remaining)...")
            return generate_image(prompt, output_path, key_rotator, model_index=0)
        print(f"  ❌ All keys and models exhausted")
        return False

    api_key = key_rotator.get_key()
    if not api_key:
        print(f"  ❌ No available API keys")
        return False

    model = MODELS[model_index]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    for attempt in range(MAX_RETRIES):
        try:
            resp = urllib.request.urlopen(req, timeout=90)
            data = json.loads(resp.read())

            # Check for safety block
            candidates = data.get("candidates", [])
            if not candidates:
                reason = data.get("promptFeedback", {}).get("blockReason", "unknown")
                print(f"  ⚠️ Blocked ({reason}), trying softer prompt...")
                return False

            for part in candidates[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    size_kb = len(img_data) / 1024
                    key_num = key_rotator.current + 1
                    print(f"  ✅ Saved {output_path.name} ({size_kb:.0f} KB) via {model} [key#{key_num}]")
                    return True

            print(f"  ⚠️ No image in response from {model}")
            return False

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()[:500]
            if e.code == 429:
                is_daily = "PerDay" in error_body or "per_day" in error_body.lower()
                if is_daily:
                    # Daily limit - try next key first, then next model
                    print(f"  🔑 Daily limit hit on key#{key_rotator.current + 1}/{model}")
                    key_rotator.mark_exhausted()
                    if key_rotator.available > 0:
                        return generate_image(prompt, output_path, key_rotator, model_index=0)
                    else:
                        # All keys exhausted, try next model with reset keys
                        print(f"  🔄 All keys exhausted for {model}, trying next model...")
                        return generate_image(prompt, output_path, key_rotator, model_index + 1)

                # Per-minute limit - wait and retry
                if attempt < MAX_RETRIES - 1:
                    key_rotator.advance()  # Try different key while waiting
                    print(f"  ⏳ Per-minute limit, rotating key & waiting {RETRY_DELAY}s... (attempt {attempt + 1})")
                    time.sleep(RETRY_DELAY)
                    # Rebuild request with new key
                    new_key = key_rotator.get_key()
                    if new_key:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={new_key}"
                        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
                else:
                    print(f"  🔄 {model} rate limited after retries, trying next model...")
                    return generate_image(prompt, output_path, key_rotator, model_index + 1)
            else:
                print(f"  ❌ HTTP {e.code} from {model}: {error_body[:100]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False

    return False


def insert_images_into_markdown(filepath, slug, generated_images):
    """Insert image markdown tags into the recipe article."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    fm_section = parts[1]
    body = parts[2]

    # Check if images already inserted
    if f'{SITE_IMAGE_PREFIX}/{slug}/' in body:
        print(f"  ℹ️  Images already in article, skipping insertion")
        return False

    # Build image markdown snippets
    img_map = {}
    for img in generated_images:
        img_id = img['id']
        alt = img['alt']
        path = f"{SITE_IMAGE_PREFIX}/{slug}/{img_id}.png"
        img_map[img_id] = f'\n![{alt}]({path})\n'

    # Strategy: Insert images at logical positions in the body
    lines = body.split('\n')
    new_lines = []
    inserted = set()
    heading_count = 0

    # Insert ingredients image right after first paragraph
    for i, line in enumerate(lines):
        new_lines.append(line)

        # After first non-empty paragraph (first real content)
        if '01-ingredients' in img_map and '01-ingredients' not in inserted:
            if i > 0 and line.strip() == '' and new_lines[-2].strip() and not new_lines[-2].startswith('#'):
                # Check if previous line was actual content (not front matter artifacts)
                prev_content = new_lines[-2].strip()
                if len(prev_content) > 20 and not prev_content.startswith('!'):
                    new_lines.append(img_map['01-ingredients'])
                    inserted.add('01-ingredients')
                    continue

        # Track headings for other image placement
        if line.strip().startswith('## ') or line.strip().startswith('### '):
            heading_count += 1

            # Insert prep image after 2nd heading
            if heading_count == 2 and '02-preparation' in img_map and '02-preparation' not in inserted:
                new_lines.append(img_map['02-preparation'])
                inserted.add('02-preparation')

            # Insert cooking image after 3rd heading
            elif heading_count == 3 and '03-cooking' in img_map and '03-cooking' not in inserted:
                new_lines.append(img_map['03-cooking'])
                inserted.add('03-cooking')

    # Insert finished dish before the last section
    body_text = '\n'.join(new_lines)

    # Add finished dish image before "Storage" or "Variations" or last heading
    for marker in ['## Storage', '## Variations', '## Serving', '## 保存', '## 變化', '## 上桌']:
        if marker in body_text and '04-finished' in img_map and '04-finished' not in inserted:
            body_text = body_text.replace(marker, img_map['04-finished'] + '\n' + marker)
            inserted.add('04-finished')
            break

    # Add serving image at the very end
    if '05-serving' in img_map and '05-serving' not in inserted:
        body_text = body_text.rstrip() + '\n' + img_map['05-serving'] + '\n'
        inserted.add('05-serving')

    # If finished dish wasn't placed, add before serving
    if '04-finished' in img_map and '04-finished' not in inserted:
        # Insert before the last paragraph
        body_text = body_text.rstrip() + '\n' + img_map['04-finished'] + '\n'
        inserted.add('04-finished')

    # Reconstruct file
    new_content = '---' + fm_section + '---' + body_text
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  📝 Inserted {len(inserted)} images into article")
    return True


def get_slug(filepath):
    """Get URL slug from filename."""
    name = Path(filepath).stem
    # Remove date prefix if present
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    return slug


def process_recipe(filepath, key_rotator, dry_run=False, skip_existing=False):
    """Process a single recipe file: generate images and insert into article."""
    slug = get_slug(filepath)
    img_dir = IMAGE_BASE / slug

    print(f"\n{'='*60}")
    print(f"📖 {Path(filepath).name}")
    print(f"   slug: {slug}")

    # Skip if images already exist
    if skip_existing and img_dir.exists():
        existing = list(img_dir.glob("*.png"))
        if len(existing) >= 3:
            print(f"   ⏭️  Skipping: {len(existing)} images already exist")
            return 0

    # Parse recipe
    fm, body = parse_recipe_frontmatter(filepath)
    if not fm:
        print(f"   ❌ Could not parse front matter")
        return 0

    info = extract_recipe_info(fm, body)
    print(f"   title: {info['title']}")
    print(f"   ingredients: {len(info.get('ingredients', []))}")
    print(f"   steps: {len(info.get('steps', []))}")
    print(f"   methods: {info.get('methods', [])}")

    # Generate prompts
    prompts = generate_prompts(info, slug)
    print(f"   📸 {len(prompts)} images planned:")

    generated = []
    for p in prompts:
        print(f"\n   [{p['id']}] {p['alt']}")
        if dry_run:
            print(f"   PROMPT: {p['prompt'][:120]}...")
            continue

        output_path = img_dir / f"{p['id']}.png"

        # Skip if this specific image exists
        if output_path.exists():
            print(f"   ⏭️  Already exists, skipping")
            generated.append(p)
            continue

        if key_rotator.available == 0:
            print(f"  🛑 All API keys exhausted, stopping this recipe")
            break

        success = generate_image(p['prompt'], output_path, key_rotator)
        if success:
            generated.append(p)
            time.sleep(RATE_LIMIT_DELAY)
        else:
            print(f"   ⚠️ Failed, continuing...")
            # Don't break — try remaining images

    # Insert images into markdown
    if generated and not dry_run:
        insert_images_into_markdown(filepath, slug, generated)

    return len(generated)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate recipe images with Gemini AI")
    parser.add_argument('--file', help="Process single recipe file")
    parser.add_argument('--dry-run', action='store_true', help="Preview prompts without generating")
    parser.add_argument('--skip-existing', action='store_true', help="Skip recipes with existing images")
    parser.add_argument('--max-per-run', type=int, default=0, help="Max images to generate (0=unlimited)")
    parser.add_argument('--lang', choices=['all', 'en', 'zh'], default='all', help="Filter by language")
    args = parser.parse_args()

    api_keys = load_api_keys()
    if not api_keys and not args.dry_run:
        print("❌ No API keys found (set GEMINI_API_KEY or add to config/gemini-keys.json)")
        sys.exit(1)
    key_rotator = KeyRotator(api_keys) if api_keys else None

    # Collect recipe files
    files = []
    if args.file:
        files = [args.file]
    else:
        for content_dir in CONTENT_DIRS:
            if content_dir.exists():
                for f in sorted(content_dir.glob("*.md")):
                    if f.name == '_index.md':
                        continue
                    files.append(str(f))

    # Filter by language if needed
    if args.lang != 'all':
        filtered = []
        for f in files:
            with open(f, 'r', encoding='utf-8') as fh:
                head = fh.read(500)
            if args.lang == 'en' and ('lang: en' in head or '/en/' in f):
                filtered.append(f)
            elif args.lang == 'zh' and 'lang: en' not in head and '/en/' not in f:
                filtered.append(f)
        files = filtered

    print(f"🍳 Recipe Image Generator")
    print(f"   Found {len(files)} recipe files")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'GENERATE'}")
    print(f"   Max per run: {args.max_per_run or 'unlimited'}")
    if key_rotator:
        print(f"   API keys: {len(api_keys)} loaded")
    if args.skip_existing:
        print(f"   Skipping existing: YES")

    total_generated = 0
    for filepath in files:
        if args.max_per_run > 0 and total_generated >= args.max_per_run:
            print(f"\n⚡ Reached max {args.max_per_run} images, stopping.")
            break

        if key_rotator and key_rotator.available == 0:
            print(f"\n🛑 All API keys exhausted. Generated {total_generated} images before stopping.")
            break

        count = process_recipe(filepath, key_rotator, args.dry_run, args.skip_existing)
        total_generated += count

    print(f"\n{'='*60}")
    print(f"✅ Done! Generated {total_generated} images across {len(files)} recipes")
    if total_generated > 0 and not args.dry_run:
        print(f"📂 Images saved to: {IMAGE_BASE}")
        print(f"🔄 Run 'cd {PROJECT_ROOT} && git add -A && git push' to deploy")


if __name__ == '__main__':
    main()
