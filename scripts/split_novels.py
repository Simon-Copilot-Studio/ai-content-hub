#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小說拆分腳本 - 將小說拆分成 Blog 連載格式
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 配置
NOVELS_DIR = Path("/mnt/c/Users/Simon/novels")
OUTPUT_DIR = Path.home() / "blog/content/fiction"
BASE_DATE = "2026-03-24"

# 小說 metadata 配置
NOVEL_META = {
    "novel_01_星際迷航.md": {
        "slug": "star-voyage",
        "title": "星際迷航",
        "tags": ["小說", "科幻", "連載"],
        "image": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1200&h=630&fit=crop",
    },
    "novel_02_江湖夢.md": {
        "slug": "jianghu-dream",
        "title": "江湖夢",
        "tags": ["小說", "武俠", "連載"],
        "image": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=1200&h=630&fit=crop",
    },
    "novel_03_末日倖存者.md": {
        "slug": "doomsday-survivor",
        "title": "末日倖存者",
        "tags": ["小說", "末日", "生存", "連載"],
        "image": "https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=1200&h=630&fit=crop",
    },
    "novel_04_時光書店.md": {
        "slug": "time-bookstore",
        "title": "時光書店",
        "tags": ["小說", "奇幻", "文學", "連載"],
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200&h=630&fit=crop",
    },
    "novel_05_深海密碼.md": {
        "slug": "deep-sea-code",
        "title": "深海密碼",
        "tags": ["小說", "懸疑", "冒險", "連載"],
        "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1200&h=630&fit=crop",
    },
    "novel_06_帝國崛起.md": {
        "slug": "empire-rise",
        "title": "帝國崛起",
        "tags": ["小說", "歷史", "權謀", "連載"],
        "image": "https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=1200&h=630&fit=crop",
    },
    "novel_07_AI覺醒.md": {
        "slug": "ai-awakening",
        "title": "AI覺醒",
        "tags": ["小說", "科幻", "AI", "連載"],
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630&fit=crop",
    },
    "novel_08_山城往事.md": {
        "slug": "mountain-city-tales",
        "title": "山城往事",
        "tags": ["小說", "文學", "鄉土", "連載"],
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&h=630&fit=crop",
    },
    "novel_09_暗影獵人.md": {
        "slug": "shadow-hunter",
        "title": "暗影獵人",
        "tags": ["小說", "奇幻", "動作", "連載"],
        "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=1200&h=630&fit=crop",
    },
    "novel_10_星塵女巫.md": {
        "slug": "stardust-witch",
        "title": "星塵女巫",
        "tags": ["小說", "奇幻", "魔法", "連載"],
        "image": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1200&h=630&fit=crop",
    },
    "novel_11_龍族後裔.md": {
        "slug": "dragon-descendants",
        "title": "龍族後裔",
        "tags": ["小說", "奇幻", "龍族", "連載"],
        "image": "https://images.unsplash.com/photo-1572586425006-f60c10f8f4d5?w=1200&h=630&fit=crop",
    },
    "novel_12_量子迷宮.md": {
        "slug": "quantum-maze",
        "title": "量子迷宮",
        "tags": ["小說", "科幻", "懸疑", "連載"],
        "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop",
    },
    "novel_13_戰火餘生.md": {
        "slug": "war-survivors",
        "title": "戰火餘生",
        "tags": ["小說", "戰爭", "歷史", "連載"],
        "image": "https://images.unsplash.com/photo-1526066801842-6ccf0a23d59c?w=1200&h=630&fit=crop",
    },
    "novel_14_極地密令.md": {
        "slug": "arctic-mission",
        "title": "極地密令",
        "tags": ["小說", "冒險", "諜報", "連載"],
        "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=1200&h=630&fit=crop",
    },
    "novel_15_靈魂交易所.md": {
        "slug": "soul-exchange",
        "title": "靈魂交易所",
        "tags": ["小說", "都市奇幻", "暗黑", "連載"],
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200&h=630&fit=crop",
    },
    "novel_16_鬼市奇譚.md": {
        "slug": "ghost-market-tales",
        "title": "鬼市奇譚",
        "tags": ["小說", "靈異", "民俗", "連載"],
        "image": "https://images.unsplash.com/photo-1509266272358-7701da638078?w=1200&h=630&fit=crop",
    },
    "novel_17_雲端帝國.md": {
        "slug": "cloud-empire",
        "title": "雲端帝國",
        "tags": ["小說", "科幻", "賽博龐克", "連載"],
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&h=630&fit=crop",
    },
    "novel_18_荒野獵人.md": {
        "slug": "wilderness-hunter",
        "title": "荒野獵人",
        "tags": ["小說", "冒險", "生存", "連載"],
        "image": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1200&h=630&fit=crop",
    },
    "novel_19_千年棋局.md": {
        "slug": "millennium-chess",
        "title": "千年棋局",
        "tags": ["小說", "歷史", "懸疑", "連載"],
        "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=1200&h=630&fit=crop",
    },
    "novel_20_異界藥師.md": {
        "slug": "otherworld-pharmacist",
        "title": "異界藥師",
        "tags": ["小說", "奇幻", "穿越", "連載"],
        "image": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=1200&h=630&fit=crop",
    },
    "novel_21_都市仙人.md": {
        "slug": "urban-immortal",
        "title": "都市仙人",
        "tags": ["小說", "都市", "修仙", "連載"],
        "image": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1200&h=630&fit=crop",
    },
    "novel_22_深淵之門.md": {
        "slug": "abyss-gate",
        "title": "深淵之門",
        "tags": ["小說", "恐怖", "冒險", "連載"],
        "image": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1200&h=630&fit=crop",
    },
    "novel_23_機甲風暴.md": {
        "slug": "mecha-storm",
        "title": "機甲風暴",
        "tags": ["小說", "科幻", "機甲", "連載"],
        "image": "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1200&h=630&fit=crop",
    },
    "novel_24_食神之路.md": {
        "slug": "culinary-god-path",
        "title": "食神之路",
        "tags": ["小說", "美食", "勵志", "連載"],
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=630&fit=crop",
    },
    "novel_25_血族黎明.md": {
        "slug": "vampire-dawn",
        "title": "血族黎明",
        "tags": ["小說", "吸血鬼", "暗黑", "連載"],
        "image": "https://images.unsplash.com/photo-1511988617509-a57c8a288659?w=1200&h=630&fit=crop",
    },
    "novel_26_天空之城.md": {
        "slug": "sky-city",
        "title": "天空之城",
        "tags": ["小說", "科幻", "冒險", "連載"],
        "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=630&fit=crop",
    },
    "novel_27_記憶商人.md": {
        "slug": "memory-merchant",
        "title": "記憶商人",
        "tags": ["小說", "科幻", "哲學", "連載"],
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=630&fit=crop",
    },
    "novel_28_九州風雲錄.md": {
        "slug": "jiuzhou-chronicles",
        "title": "九州風雲錄",
        "tags": ["小說", "武俠", "歷史", "連載"],
        "image": "https://images.unsplash.com/photo-1451906278231-17b2df0a5c41?w=1200&h=630&fit=crop",
    },
    "novel_29_末日方舟.md": {
        "slug": "doomsday-ark",
        "title": "末日方舟",
        "tags": ["小說", "末日", "科幻", "連載"],
        "image": "https://images.unsplash.com/photo-1454789548928-9efd52dc4031?w=1200&h=630&fit=crop",
    },
    "novel_30_夢境偵探.md": {
        "slug": "dream-detective",
        "title": "夢境偵探",
        "tags": ["小說", "懸疑", "奇幻", "連載"],
        "image": "https://images.unsplash.com/photo-1502139214982-d0ad755818d8?w=1200&h=630&fit=crop",
    },
}


def extract_chapters(content):
    """提取章節"""
    lines = content.split("\n")
    chapters = []
    current_chapter = {"title": "", "content": []}
    prologue = []
    in_prologue = True

    for line in lines:
        if line.startswith("## 第"):
            # 新章節開始
            if in_prologue:
                in_prologue = False
            elif current_chapter["title"]:
                # 保存上一章
                chapters.append(current_chapter)
                current_chapter = {"title": "", "content": []}

            current_chapter["title"] = line[3:].strip()  # 移除 "## "
        elif in_prologue:
            # 序言部分（## 之前的所有內容）
            if not line.startswith("# "):  # 跳過主標題
                prologue.append(line)
        else:
            # 章節內容
            current_chapter["content"].append(line)

    # 保存最後一章
    if current_chapter["title"]:
        chapters.append(current_chapter)

    return "\n".join(prologue).strip(), chapters


def group_chapters(chapters, chapters_per_post=3):
    """將章節分組，每組 2-3 章"""
    groups = []
    for i in range(0, len(chapters), chapters_per_post):
        group = chapters[i : i + chapters_per_post]
        groups.append(group)
    return groups


def create_index_md(meta, prologue, total_chapters, total_words):
    """建立 _index.md"""
    # 從 prologue 中提取簡介（取前 200 字）
    description = prologue[:200].replace("\n", " ").strip()
    if len(prologue) > 200:
        description += "..."

    front_matter = f"""---
title: "《{meta['title']}》"
description: "{description}"
author: "AI 小說工坊"
date: {BASE_DATE}
tags: {meta['tags']}
series: "{meta['title']}"
image: "{meta['image']}"
novel: true
chapters: {total_chapters}
words: {total_words}
status: "完結"
---

{prologue}
"""
    return front_matter


def create_chapter_md(meta, group, group_index, total_groups):
    """建立章節 md"""
    # 提取章節範圍
    first_ch = group[0]["title"]
    last_ch = group[-1]["title"]

    # 從章節標題提取數字
    first_num = re.search(r"第(\d+|[一二三四五六七八九十百千]+)章", first_ch)
    last_num = re.search(r"第(\d+|[一二三四五六七八九十百千]+)章", last_ch)

    if first_num and last_num:
        title_range = f"第 {first_num.group(1)}-{last_num.group(1)} 章"
    else:
        title_range = f"第 {group_index * 3 + 1}-{min((group_index + 1) * 3, group_index * 3 + len(group))} 章"

    # 從第一章內容中提取摘要（前 100 字）
    first_content = "\n".join(group[0]["content"][:10])
    description = first_content[:100].replace("\n", " ").strip()
    if len(first_content) > 100:
        description += "..."

    # 組合所有章節內容
    content_parts = []
    for ch in group:
        content_parts.append(f"## {ch['title']}\n")
        content_parts.append("\n".join(ch["content"]))
        content_parts.append("\n\n")

    front_matter = f"""---
title: "《{meta['title']}》{title_range}"
description: "{description}"
author: "AI 小說工坊"
date: {BASE_DATE}
tags: {meta['tags']}
series: "{meta['title']}"
weight: {group_index + 1}
---

{"".join(content_parts)}"""

    return front_matter


def process_novel(novel_file):
    """處理單部小說"""
    print(f"\n處理：{novel_file.name}")

    # 讀取小說內容
    with open(novel_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 獲取 metadata
    meta = NOVEL_META.get(novel_file.name)
    if not meta:
        print(f"  ⚠️  找不到 metadata，跳過")
        return

    # 建立輸出目錄
    output_dir = OUTPUT_DIR / f"novel-{meta['slug']}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 提取章節
    prologue, chapters = extract_chapters(content)
    total_chapters = len(chapters)
    total_words = len(content)

    print(f"  章節數：{total_chapters}")
    print(f"  總字數：{total_words}")

    # 建立 _index.md
    index_content = create_index_md(meta, prologue, total_chapters, total_words)
    index_file = output_dir / "_index.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"  ✓ 建立 _index.md")

    # 分組章節
    groups = group_chapters(chapters, chapters_per_post=3)
    print(f"  分成 {len(groups)} 篇文章")

    # 建立章節文章
    for i, group in enumerate(groups):
        chapter_content = create_chapter_md(meta, group, i, len(groups))

        # 檔名格式：chapter-01-03.md
        start = i * 3 + 1
        end = min((i + 1) * 3, total_chapters)
        chapter_file = output_dir / f"chapter-{start:02d}-{end:02d}.md"

        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(chapter_content)
        print(f"  ✓ 建立 {chapter_file.name}")

    print(f"  ✅ 完成：{meta['title']}")


def main():
    """主函數"""
    print("=" * 60)
    print("小說拆分腳本 - 開始處理")
    print("=" * 60)

    # 確保輸出目錄存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 優先處理的小說（最長的 5 部）
    priority = [
        "novel_15_靈魂交易所.md",
        "novel_25_血族黎明.md",
        "novel_24_食神之路.md",
        "novel_04_時光書店.md",
        "novel_16_鬼市奇譚.md",
    ]

    # 處理優先小說
    print("\n【第一階段】處理 Top 5 最長小說")
    for novel_name in priority:
        novel_file = NOVELS_DIR / novel_name
        if novel_file.exists():
            process_novel(novel_file)

    # 處理其餘小說
    print("\n【第二階段】處理其餘小說")
    for novel_file in sorted(NOVELS_DIR.glob("novel_*.md")):
        if novel_file.name not in priority:
            process_novel(novel_file)

    print("\n" + "=" * 60)
    print("✅ 全部完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
