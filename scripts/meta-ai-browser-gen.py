#!/usr/bin/env python3
"""
Meta AI Browser Automation - Image Generator
=============================================
Uses OpenClaw Browser Relay (Chrome profile) to:
1. Open Meta AI
2. Send image generation prompts one by one
3. Download generated images
4. Save to correct article directories

Designed to be called by OpenClaw's browser automation,
NOT run standalone (needs browser tool access).

This script outputs JSON commands for OpenClaw to execute.
"""

import json
import os
import sys
import time
import base64
import re
from pathlib import Path
from urllib.parse import quote

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_FILE = PROJECT_ROOT / "data" / "image-prompts.json"
STATUS_FILE = PROJECT_ROOT / "data" / "image-gen-status.json"
STATIC_DIR = PROJECT_ROOT / "static" / "images"
DOWNLOAD_DIR = PROJECT_ROOT / "tmp" / "meta-ai-downloads"


def load_pending(max_count=0, category=""):
    """Load pending prompts."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    pending = [p for p in prompts if p["status"] == "pending"]

    if category:
        pending = [p for p in pending if p["category"] == category]

    if max_count > 0:
        pending = pending[:max_count]

    return pending


def save_status(prompt_item, status, image_path="", error=""):
    """Update status for a single prompt."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    for p in prompts:
        if p["filepath"] == prompt_item["filepath"]:
            p["status"] = status
            if image_path:
                p["generated_image"] = image_path
            if error:
                p["error"] = error
            p["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            break

    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)


def ensure_dirs():
    """Create output directories."""
    for cat in ["recipes", "tech", "economy", "entertainment", "news", "fiction"]:
        (STATIC_DIR / cat).mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def generate_openclaw_commands(pending):
    """
    Generate a sequence of OpenClaw browser commands.
    Output as JSON for OpenClaw to consume.
    """
    commands = []

    # Step 1: Navigate to Meta AI
    commands.append({
        "action": "navigate",
        "url": "https://www.meta.ai/",
        "wait": 3000,
        "description": "Open Meta AI"
    })

    for i, p in enumerate(pending):
        prompt_text = f"Generate an image: {p['prompt']}"

        # Step 2: Type prompt
        commands.append({
            "action": "type_prompt",
            "text": prompt_text,
            "article": p["title"],
            "category": p["category"],
            "target_path": p["target_full_path"],
            "index": i + 1,
            "total": len(pending),
            "description": f"[{i+1}/{len(pending)}] {p['title'][:40]}..."
        })

        # Step 3: Wait for generation
        commands.append({
            "action": "wait_for_image",
            "timeout": 30000,
            "description": "Wait for image generation"
        })

        # Step 4: Download image
        commands.append({
            "action": "download_image",
            "target_path": p["target_full_path"],
            "slug": p["slug"],
            "category": p["category"],
            "description": f"Download image for {p['slug']}"
        })

        # Brief pause between generations
        if i < len(pending) - 1:
            commands.append({
                "action": "pause",
                "duration": 2000,
                "description": "Brief pause between generations"
            })

    return commands


def print_batch_summary(pending):
    """Print what will be generated."""
    print(f"\n🎨 Meta AI Image Generation Batch")
    print(f"{'='*60}")
    print(f"Total images to generate: {len(pending)}")
    print(f"\nBreakdown:")

    by_cat = {}
    for p in pending:
        cat = p["category"]
        by_cat[cat] = by_cat.get(cat, 0) + 1

    for cat, count in sorted(by_cat.items()):
        print(f"  {cat}: {count}")

    print(f"\nArticles:")
    for i, p in enumerate(pending):
        print(f"  [{i+1}] [{p['category']}] {p['title'][:60]}")

    print(f"\n💡 Estimated time: ~{len(pending) * 20}s ({len(pending)} × 20s per image)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=10)
    parser.add_argument("--category", type=str, default="")
    parser.add_argument("--output-commands", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    pending = load_pending(max_count=args.max, category=args.category)

    if not pending:
        print("✅ No pending images to generate!")
        sys.exit(0)

    print_batch_summary(pending)

    if args.output_commands:
        commands = generate_openclaw_commands(pending)
        cmd_file = PROJECT_ROOT / "data" / "meta-ai-commands.json"
        with open(cmd_file, "w") as f:
            json.dump(commands, f, indent=2)
        print(f"\n📋 Commands saved to: {cmd_file}")
