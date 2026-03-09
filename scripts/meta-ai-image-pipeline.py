#!/usr/bin/env python3
"""
Meta AI Image Generation Pipeline for AI Content Hub
=====================================================
Phase 1: Scan articles → generate prompts
Phase 2: Batch generate images via Meta AI (browser automation)
Phase 3: Download & distribute to article directories
Phase 4: Update front matter with local image paths
Phase 5: Browser-based visual QA verification

Usage:
  # Phase 1: Generate prompts for all articles
  python3 scripts/meta-ai-image-pipeline.py --scan

  # Phase 2+3: Generate & download images (requires Chrome relay ON)
  python3 scripts/meta-ai-image-pipeline.py --generate [--max N] [--category recipes]

  # Phase 4: Update article front matter
  python3 scripts/meta-ai-image-pipeline.py --update-frontmatter

  # Phase 5: Visual QA
  python3 scripts/meta-ai-image-pipeline.py --verify

  # All-in-one
  python3 scripts/meta-ai-image-pipeline.py --all [--max N]
"""

import os
import sys
import json
import re
import glob
import hashlib
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
STATIC_DIR = PROJECT_ROOT / "static" / "images"
PROMPTS_FILE = PROJECT_ROOT / "data" / "image-prompts.json"
STATUS_FILE = PROJECT_ROOT / "data" / "image-pipeline-status.json"
QA_REPORT_FILE = PROJECT_ROOT / "data" / "image-qa-report.json"

# Image specs
IMAGE_WIDTH = 1200  # px target for blog hero
IMAGE_QUALITY = 85  # JPEG quality

# Categories and their visual style guides
STYLE_GUIDES = {
    "recipes": {
        "style": "professional food photography, top-down overhead shot, natural lighting, "
                 "rustic wooden table background, garnished beautifully, appetizing colors, "
                 "shallow depth of field, 4K quality",
        "negative": "text, watermark, logo, cartoon, illustration, low quality",
    },
    "tech": {
        "style": "modern minimalist tech illustration, clean design, gradient background, "
                 "futuristic elements, professional, corporate style, subtle glow effects",
        "negative": "text, watermark, cluttered, low quality",
    },
    "economy": {
        "style": "professional business photography, clean modern office, data visualization, "
                 "abstract financial concept, blue and green tones, corporate style",
        "negative": "text, watermark, cartoon, low quality",
    },
    "entertainment": {
        "style": "vibrant colorful illustration, dynamic composition, eye-catching, "
                 "pop culture aesthetic, energetic mood, bold colors",
        "negative": "text, watermark, low quality, blurry",
    },
    "news": {
        "style": "photojournalistic style, dramatic lighting, documentary feel, "
                 "high contrast, cinematic composition, editorial quality",
        "negative": "text, watermark, cartoon, low quality",
    },
    "fiction": {
        "style": "cinematic digital art, atmospheric, dramatic lighting, concept art quality, "
                 "story-telling composition, rich color palette, fantasy/sci-fi elements",
        "negative": "text, watermark, low quality, blurry",
    },
}


def parse_frontmatter(filepath):
    """Parse YAML front matter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    # Simple YAML parser for front matter
    fm = {}
    current_key = None
    for line in fm_text.split("\n"):
        if line.startswith("  ") and current_key:
            # continuation of list/multiline
            continue
        match = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip().strip('"').strip("'")
            fm[key] = value
            current_key = key

    return fm, body


def get_category(filepath):
    """Determine article category from file path."""
    parts = Path(filepath).parts
    for part in parts:
        if part in STYLE_GUIDES:
            return part
    # Check parent directory
    for part in parts:
        if part in ["en"]:
            continue
        if part in ["content", "static", "images"]:
            continue
        if part in STYLE_GUIDES:
            return part
    return "tech"  # default fallback


def generate_prompt(title, category, description="", is_recipe=False):
    """Generate an image prompt based on article metadata."""
    style = STYLE_GUIDES.get(category, STYLE_GUIDES["tech"])

    if is_recipe or category == "recipes":
        # For recipes, focus on the dish itself
        dish_name = title.split(":")[0].strip().strip('"')
        prompt = (
            f"A beautiful {dish_name}, {style['style']}. "
            f"The dish is the hero of the shot, perfectly plated and ready to serve."
        )
    else:
        # For other articles, create a conceptual image
        clean_title = re.sub(r'["\'\[\]:：]', '', title)
        prompt = (
            f"Visual concept for article about '{clean_title}'. "
            f"{style['style']}."
        )

    return prompt


def scan_articles():
    """Phase 1: Scan all articles and generate image prompts."""
    prompts = []
    articles = glob.glob(str(CONTENT_DIR / "**" / "*.md"), recursive=True)

    for filepath in sorted(articles):
        if "_index.md" in filepath:
            continue

        fm, body = parse_frontmatter(filepath)
        title = fm.get("title", Path(filepath).stem)
        description = fm.get("description", "")
        category = get_category(filepath)
        image = fm.get("image", "")

        # Determine relative path for image storage
        rel_path = Path(filepath).relative_to(CONTENT_DIR)
        slug = rel_path.stem
        lang = ""
        if str(rel_path).startswith("en/"):
            lang = "en"
            category_from_path = rel_path.parts[1] if len(rel_path.parts) > 2 else category
        else:
            category_from_path = rel_path.parts[0] if len(rel_path.parts) > 1 else category

        # Image output path
        img_dir = f"{category_from_path}"
        img_filename = f"{slug}.jpg"
        img_path = f"/images/{img_dir}/{img_filename}"
        img_full_path = str(STATIC_DIR / img_dir / img_filename)

        is_recipe = category_from_path == "recipes"
        prompt = generate_prompt(title, category_from_path, description, is_recipe)

        already_local = "images/" in image and "unsplash" not in image
        already_generated = os.path.exists(img_full_path)

        prompts.append({
            "filepath": filepath,
            "title": title,
            "category": category_from_path,
            "lang": lang,
            "slug": slug,
            "prompt": prompt,
            "current_image": image,
            "target_image_path": img_path,
            "target_full_path": img_full_path,
            "already_local": already_local,
            "already_generated": already_generated,
            "status": "done" if already_generated else "pending",
        })

    # Save prompts
    PROMPTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

    # Stats
    total = len(prompts)
    pending = sum(1 for p in prompts if p["status"] == "pending")
    done = sum(1 for p in prompts if p["status"] == "done")
    by_cat = {}
    for p in prompts:
        cat = p["category"]
        by_cat[cat] = by_cat.get(cat, 0) + 1

    print(f"\n📊 Image Pipeline Scan Results")
    print(f"{'='*50}")
    print(f"Total articles: {total}")
    print(f"  ✅ Already generated: {done}")
    print(f"  ⏳ Pending: {pending}")
    print(f"\nBy category:")
    for cat, count in sorted(by_cat.items()):
        cat_pending = sum(1 for p in prompts if p["category"] == cat and p["status"] == "pending")
        print(f"  {cat}: {count} total, {cat_pending} pending")
    print(f"\nPrompts saved to: {PROMPTS_FILE}")

    return prompts


def update_frontmatter(dry_run=False):
    """Phase 4: Update article front matter with local image paths."""
    if not PROMPTS_FILE.exists():
        print("❌ No prompts file found. Run --scan first.")
        return

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    updated = 0
    skipped = 0

    for p in prompts:
        if not os.path.exists(p["target_full_path"]):
            skipped += 1
            continue

        filepath = p["filepath"]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already using local image
        if p["target_image_path"] in content:
            continue

        # Replace image in front matter
        old_image = p.get("current_image", "")
        if old_image:
            new_content = content.replace(
                f'image: "{old_image}"',
                f'image: "{p["target_image_path"]}"'
            ).replace(
                f"image: '{old_image}'",
                f'image: "{p["target_image_path"]}"'
            )
        else:
            # Add image field after title
            new_content = re.sub(
                r'(title:.*\n)',
                f'\\1image: "{p["target_image_path"]}"\n',
                content,
                count=1
            )

        if new_content != content:
            if dry_run:
                print(f"  [DRY] Would update: {filepath}")
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  ✅ Updated: {filepath}")
            updated += 1

    print(f"\n📊 Front Matter Update: {updated} updated, {skipped} skipped (no image yet)")


def generate_qa_checklist():
    """Phase 5: Generate QA verification checklist."""
    if not PROMPTS_FILE.exists():
        print("❌ No prompts file found. Run --scan first.")
        return

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    qa_items = []
    for p in prompts:
        img_exists = os.path.exists(p["target_full_path"])
        img_size = 0
        if img_exists:
            img_size = os.path.getsize(p["target_full_path"])

        qa_items.append({
            "title": p["title"],
            "category": p["category"],
            "image_path": p["target_image_path"],
            "image_exists": img_exists,
            "image_size_kb": round(img_size / 1024, 1) if img_size else 0,
            "size_ok": 50 < (img_size / 1024) < 2000 if img_size else False,  # 50KB-2MB
            "checks": {
                "exists": img_exists,
                "size_reasonable": 50 < (img_size / 1024) < 2000 if img_size else False,
                "frontmatter_updated": False,  # Will be checked by browser
                "displays_correctly": None,  # Browser check
                "matches_content": None,  # Manual/AI check
            }
        })

    QA_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QA_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(qa_items, f, ensure_ascii=False, indent=2)

    total = len(qa_items)
    with_image = sum(1 for q in qa_items if q["image_exists"])
    good_size = sum(1 for q in qa_items if q["size_ok"])

    print(f"\n📊 QA Report")
    print(f"{'='*50}")
    print(f"Total articles: {total}")
    print(f"  ✅ Image exists: {with_image}")
    print(f"  ✅ Size OK (50KB-2MB): {good_size}")
    print(f"  ❌ Missing image: {total - with_image}")
    print(f"\nReport saved to: {QA_REPORT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Meta AI Image Generation Pipeline")
    parser.add_argument("--scan", action="store_true", help="Phase 1: Scan articles & generate prompts")
    parser.add_argument("--generate", action="store_true", help="Phase 2+3: Generate & download images")
    parser.add_argument("--update-frontmatter", action="store_true", help="Phase 4: Update front matter")
    parser.add_argument("--verify", action="store_true", help="Phase 5: QA verification")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    parser.add_argument("--max", type=int, default=0, help="Max images to generate (0=all)")
    parser.add_argument("--category", type=str, default="", help="Filter by category")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")

    args = parser.parse_args()

    if args.all:
        args.scan = True
        args.generate = True
        args.update_frontmatter = True
        args.verify = True

    if args.scan or not any([args.scan, args.generate, args.update_frontmatter, args.verify]):
        print("\n🔍 Phase 1: Scanning articles...")
        scan_articles()

    if args.generate:
        print("\n🎨 Phase 2+3: Image generation requires browser automation.")
        print("   Run this from OpenClaw with Chrome Relay ON:")
        print("   → OpenClaw will handle Meta AI interaction")
        print(f"\n   Prompts file: {PROMPTS_FILE}")

    if args.update_frontmatter:
        print("\n📝 Phase 4: Updating front matter...")
        update_frontmatter(dry_run=args.dry_run)

    if args.verify:
        print("\n🔎 Phase 5: QA Verification...")
        generate_qa_checklist()


if __name__ == "__main__":
    main()
