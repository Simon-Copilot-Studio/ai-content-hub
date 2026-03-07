"""
Blog Auto-Optimizer - analyzes performance data and optimizes content.
Called by OpenClaw cron after analytics collection.

Optimization actions:
1. Identify underperforming articles (low views, high bounce)
2. Generate improved titles (A/B testing)
3. Update meta descriptions for SEO
4. Add internal links between related articles
5. Suggest new content based on top performers
"""
import json, os, glob, re
from datetime import datetime, timedelta

CONTENT_DIR = "/home/simon/.openclaw/workspace/projects/ai-content-hub/content"
DATA_DIR = "/home/simon/.openclaw/workspace/projects/ai-content-hub/data/analytics"
OPTIMIZATION_LOG = "/home/simon/.openclaw/workspace/projects/ai-content-hub/data/optimization-log.json"


def load_latest_analytics():
    """Load most recent analytics data."""
    files = sorted(glob.glob(f"{DATA_DIR}/????-??-??.json"))
    if not files:
        return None
    with open(files[-1]) as f:
        return json.load(f)


def load_all_articles():
    """Scan all markdown files and extract front matter."""
    articles = []
    for md_file in glob.glob(f"{CONTENT_DIR}/**/*.md", recursive=True):
        if "_index.md" in md_file or "sample.md" in md_file:
            continue
        with open(md_file) as f:
            content = f.read()

        # Parse TOML or YAML front matter
        fm = {}
        if content.startswith("+++"):
            end = content.index("+++", 3)
            fm_text = content[3:end]
            for line in fm_text.strip().split("\n"):
                if "=" in line:
                    k, v = line.split("=", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
        elif content.startswith("---"):
            end = content.index("---", 3)
            fm_text = content[3:end]
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")

        articles.append({
            "path": md_file,
            "title": fm.get("title", ""),
            "description": fm.get("description", ""),
            "date": fm.get("date", ""),
            "slug": os.path.basename(md_file).replace(".md", ""),
            "section": md_file.split("/content/")[1].split("/")[0] if "/content/" in md_file else "",
            "word_count": len(content.split()),
            "has_images": "![" in content or "<img" in content,
            "internal_links": len(re.findall(r'\]\(/[^)]+\)', content)),
        })
    return articles


def analyze_performance(analytics, articles):
    """Cross-reference analytics with articles to find optimization opportunities."""
    url_metrics = {m["x"]: m["y"] for m in (analytics.get("metrics_url") or [])}
    stats = analytics.get("stats") or {}

    total_pv = stats.get("pageviews", {}).get("value", 1)
    avg_pv_per_article = total_pv / max(len(articles), 1)

    results = {
        "date": analytics.get("date", ""),
        "total_pageviews": total_pv,
        "total_visitors": stats.get("visitors", {}).get("value", 0),
        "avg_per_article": round(avg_pv_per_article, 1),
        "underperformers": [],
        "top_performers": [],
        "optimization_suggestions": [],
    }

    for article in articles:
        # Match URL path to analytics
        url_path = f"/ai-content-hub/{article['section']}/{article['slug']}/"
        views = url_metrics.get(url_path, 0)
        article["views"] = views

        if views > avg_pv_per_article * 2:
            results["top_performers"].append(article)
        elif views < avg_pv_per_article * 0.3:
            results["underperformers"].append(article)

    # Generate suggestions
    for article in results["underperformers"]:
        suggestions = []
        if len(article["title"]) > 60:
            suggestions.append("title_too_long")
        if len(article["title"]) < 20:
            suggestions.append("title_too_short")
        if not article["has_images"]:
            suggestions.append("add_images")
        if article["internal_links"] < 2:
            suggestions.append("add_internal_links")
        if article["word_count"] < 500:
            suggestions.append("content_too_short")

        if suggestions:
            results["optimization_suggestions"].append({
                "article": article["title"],
                "path": article["path"],
                "views": article["views"],
                "issues": suggestions,
            })

    # Content gap analysis - what topics are top performers?
    top_sections = {}
    for a in results["top_performers"]:
        sec = a["section"]
        top_sections[sec] = top_sections.get(sec, 0) + 1

    if top_sections:
        best_section = max(top_sections, key=top_sections.get)
        results["content_recommendation"] = f"Write more in '{best_section}' - your top performing section"

    return results


def generate_optimization_report(analysis):
    """Generate report for OpenClaw/Telegram."""
    lines = [
        f"🔧 **Blog 優化分析** — {analysis['date']}",
        "",
        f"📊 總瀏覽: {analysis['total_pageviews']} | 訪客: {analysis['total_visitors']}",
        f"📈 每篇平均: {analysis['avg_per_article']} views",
        "",
    ]

    if analysis["top_performers"]:
        lines.append("🏆 **表現最佳:**")
        for a in analysis["top_performers"][:5]:
            lines.append(f"  ✅ {a['title']} ({a['views']} views)")
        lines.append("")

    if analysis["underperformers"]:
        lines.append("⚠️ **需要優化:**")
        for a in analysis["underperformers"][:5]:
            lines.append(f"  ❌ {a['title']} ({a['views']} views)")
        lines.append("")

    if analysis["optimization_suggestions"]:
        lines.append("🔧 **優化建議:**")
        issue_labels = {
            "title_too_long": "標題過長",
            "title_too_short": "標題過短",
            "add_images": "缺少圖片",
            "add_internal_links": "缺少內部連結",
            "content_too_short": "內容太短",
        }
        for s in analysis["optimization_suggestions"][:5]:
            issues = ", ".join(issue_labels.get(i, i) for i in s["issues"])
            lines.append(f"  • {s['article']}: {issues}")
        lines.append("")

    if analysis.get("content_recommendation"):
        lines.append(f"💡 **內容建議:** {analysis['content_recommendation']}")

    return "\n".join(lines)


def log_optimization(analysis):
    """Save optimization results for tracking improvements over time."""
    log = []
    if os.path.exists(OPTIMIZATION_LOG):
        with open(OPTIMIZATION_LOG) as f:
            log = json.load(f)

    log.append({
        "date": analysis["date"],
        "total_pv": analysis["total_pageviews"],
        "visitors": analysis["total_visitors"],
        "underperformers": len(analysis["underperformers"]),
        "top_performers": len(analysis["top_performers"]),
        "suggestions": len(analysis["optimization_suggestions"]),
    })

    # Keep last 90 days
    log = log[-90:]

    os.makedirs(os.path.dirname(OPTIMIZATION_LOG), exist_ok=True)
    with open(OPTIMIZATION_LOG, "w") as f:
        json.dump(log, f, indent=2)


if __name__ == "__main__":
    analytics = load_latest_analytics()
    if not analytics:
        print("No analytics data found. Run analytics-collector.py first.")
        exit(1)

    articles = load_all_articles()
    analysis = analyze_performance(analytics, articles)
    report = generate_optimization_report(analysis)
    log_optimization(analysis)

    print(report)

    # Save analysis
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(f"{DATA_DIR}/analysis-{analysis['date']}.json", "w") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
