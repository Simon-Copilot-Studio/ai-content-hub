#!/usr/bin/env python3
"""Generate placeholder images for blog posts using PIL"""

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

import os
import hashlib

IMAGE_DIR = "/home/simon/.openclaw/workspace/static/images"

articles = [
    ("tech", "2026-03-12-gogoro-lu-xuesen-debt", "Gogoro 陸學森\n欠款失聯事件"),
    ("tech", "2026-03-12-innolux-silicon-photonics", "群創光電\n矽光子轉型"),
    ("tech", "2026-03-12-ai-server-boom-2026", "AI 伺服器\n需求大爆發"),
    ("tech", "2026-03-12-us-301-investigation-taiwan", "美國 301 調查\n台灣入列"),
    ("economy", "2026-03-12-polaris-pharma-capital-reduction", "北極星藥業\n減資 50%"),
    ("economy", "2026-03-12-pegatron-earnings-dividend", "和碩法說會\nAI 伺服器佈局"),
    ("economy", "2026-03-12-innolux-record-volume", "群創成交量\n破 130 萬張"),
    ("economy", "2026-03-12-taiwan-stock-market-outlook", "台股反攻\nAI Capex 續增"),
    ("entertainment", "2026-03-12-lin-chia-cheng-nippon-ham", "林家正\n加盟日本火腿"),
    ("entertainment", "2026-03-12-wbc-2026-quarterfinals", "WBC 2026\n八強出爐"),
    ("entertainment", "2026-03-12-wbc-2026-bracket-schedule", "WBC 複賽\n賽程全攻略"),
    ("entertainment", "2026-03-12-lai-ya-yan-concert-2026", "賴雅妍\n首場演唱會"),
    ("entertainment", "2026-03-12-nba-march-highlights", "NBA 三月\n精彩對決"),
    ("entertainment", "2026-03-12-chen-fang-yu-comeback", "陳芳語\n2026 回歸"),
    ("news", "2026-03-12-xiao-jing-yan-kmt-primary", "蕭敬嚴\n參選遭圍剿"),
    ("news", "2026-03-12-dai-xiang-yi-retire", "戴湘儀\n宣布不連任"),
    ("news", "2026-03-12-arbor-day-taiwan-2026", "植樹節 2026\n全民種樹"),
    ("news", "2026-03-12-train-accident-yingge", "台鐵鶯歌\n平交道事故"),
    ("news", "2026-03-12-flesh-eating-bacteria-prevention", "食人菌\n預防全攻略"),
    ("news", "2026-03-12-xiluan-mountain-hiking", "西巒大山\n登山攻略"),
    ("news", "2026-03-12-wang-zha-jie-social-media", "王炸姐\n網路文化觀察"),
    ("news", "2026-03-12-premier-cho-japan-controversy", "卓榮泰赴日\n朝野攻防"),
]

# Category color schemes (gradient start, gradient end)
cat_colors = {
    "tech":          ((30, 60, 114), (0, 150, 136)),     # Deep blue to teal
    "economy":       ((142, 68, 173), (44, 62, 80)),     # Purple to dark
    "entertainment": ((255, 94, 98), (255, 165, 0)),     # Coral to orange
    "news":          ((52, 73, 94), (44, 62, 80)),       # Dark blue-gray
}

if not HAS_PIL:
    print("PIL not available. Creating minimal SVG placeholders instead...")
    for cat, slug, title in articles:
        outdir = os.path.join(IMAGE_DIR, cat)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"{slug}.webp")
        # Create a tiny 1x1 placeholder
        img = Image.new("RGB", (1200, 630), cat_colors.get(cat, ((100,100,100),(50,50,50)))[0])
        img.save(outpath, "WEBP", quality=80)
        print(f"✅ {cat}/{slug}.webp (minimal)")
else:
    for cat, slug, title in articles:
        outdir = os.path.join(IMAGE_DIR, cat)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"{slug}.webp")
        
        W, H = 1200, 630
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)
        
        c1, c2 = cat_colors.get(cat, ((100,100,100),(50,50,50)))
        
        # Draw gradient
        for y in range(H):
            r = int(c1[0] + (c2[0] - c1[0]) * y / H)
            g = int(c1[1] + (c2[1] - c1[1]) * y / H)
            b = int(c1[2] + (c2[2] - c1[2]) * y / H)
            draw.line([(0, y), (W, y)], fill=(r, g, b))
        
        # Add semi-transparent overlay
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 80))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # Try to find a font
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 64)
                    break
                except:
                    pass
        
        if font is None:
            font = ImageFont.load_default()
        
        # Draw title text centered
        lines = title.split("\n")
        total_h = len(lines) * 80
        y_start = (H - total_h) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (W - tw) // 2
            y = y_start + i * 80
            # Shadow
            draw.text((x+3, y+3), line, fill=(0, 0, 0, 180), font=font)
            # Text
            draw.text((x, y), line, fill=(255, 255, 255, 255), font=font)
        
        # Category label
        cat_label = {"tech": "科技", "economy": "財經", "entertainment": "娛樂", "news": "時事"}
        label = cat_label.get(cat, cat)
        try:
            small_font = ImageFont.truetype(font_paths[0] if os.path.exists(font_paths[0]) else font_paths[-1], 28)
        except:
            small_font = font
        draw.text((40, 30), f"AI 趨勢觀察站 | {label}", fill=(255, 255, 255, 200), font=small_font)
        
        img = img.convert("RGB")
        img.save(outpath, "WEBP", quality=85)
        print(f"✅ {cat}/{slug}.webp")

print(f"\n🎉 Total: {len(articles)} images generated!")
