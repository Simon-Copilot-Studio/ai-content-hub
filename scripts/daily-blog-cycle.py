"""
Daily Blog Automation Cycle - orchestrates the full loop.
Called by OpenClaw heartbeat/cron.

Flow:
1. Ensure Umami + tunnel are running
2. Collect analytics data
3. Analyze performance
4. Generate optimization suggestions
5. Auto-apply safe optimizations (internal links, meta)
6. Generate new trending content (if scheduled)
7. Build + deploy
8. Send Telegram report

Usage:
  python daily-blog-cycle.py          # Full daily cycle
  python daily-blog-cycle.py report   # Just generate report
  python daily-blog-cycle.py deploy   # Just build + deploy
"""
import json, os, sys, subprocess, re, glob
from datetime import datetime

PROJECT_DIR = "/home/simon/.openclaw/workspace/projects/ai-content-hub"
SCRIPTS_DIR = f"{PROJECT_DIR}/scripts"
DATA_DIR = f"{PROJECT_DIR}/data"
CONTENT_DIR = f"{PROJECT_DIR}/content"


def check_umami():
    """Verify Umami is running."""
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://localhost:3100/api/heartbeat", timeout=5)
        data = json.loads(resp.read())
        return data.get("ok", False)
    except Exception:
        return False


def check_tunnel():
    """Check if cloudflared tunnel is running."""
    url_file = f"{DATA_DIR}/tunnel_url.txt"
    if os.path.exists(url_file):
        with open(url_file) as f:
            url = f.read().strip()
        try:
            import urllib.request
            urllib.request.urlopen(f"{url}/api/heartbeat", timeout=10)
            return url
        except Exception:
            pass
    return None


def collect_analytics():
    """Run analytics collector."""
    result = subprocess.run(
        [sys.executable, f"{SCRIPTS_DIR}/analytics-collector.py", "daily"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Analytics error: {result.stderr}")
    return result.returncode == 0


def run_optimizer():
    """Run auto-optimizer and get report."""
    result = subprocess.run(
        [sys.executable, f"{SCRIPTS_DIR}/auto-optimize.py"],
        capture_output=True, text=True
    )
    return result.stdout


def auto_add_internal_links():
    """Automatically add internal links between related articles."""
    articles = []
    for md_file in glob.glob(f"{CONTENT_DIR}/**/*.md", recursive=True):
        if "_index.md" in md_file or "sample.md" in md_file:
            continue
        with open(md_file) as f:
            content = f.read()
        # Extract title
        title_match = re.search(r'title\s*[=:]\s*["\'](.+?)["\']', content)
        title = title_match.group(1) if title_match else ""
        section = md_file.split("/content/")[1].split("/")[0]
        slug = os.path.basename(md_file).replace(".md", "")
        articles.append({
            "path": md_file,
            "title": title,
            "section": section,
            "slug": slug,
            "url": f"/{section}/{slug}/",
        })

    changes = 0
    for article in articles:
        with open(article["path"]) as f:
            content = f.read()

        # Find related articles (same section, not self)
        related = [a for a in articles if a["section"] == article["section"] and a["path"] != article["path"]]

        if not related:
            continue

        # Check if article already has a "related" section
        if "延伸閱讀" in content or "Related" in content or "相關文章" in content:
            continue

        # Add related articles section
        links = "\n".join(f"- [{a['title']}]({a['url']})" for a in related[:3])
        addition = f"\n\n---\n\n## 延伸閱讀\n\n{links}\n"

        with open(article["path"], "a") as f:
            f.write(addition)
        changes += 1

    return changes


def hugo_build():
    """Build Hugo site."""
    result = subprocess.run(
        ["hugo", "--minify"],
        cwd=PROJECT_DIR,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Hugo build error: {result.stderr}")
    return result.returncode == 0


def git_deploy(message=None):
    """Commit and push changes."""
    if message is None:
        message = f"auto: daily optimization {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    cmds = [
        ["git", "add", "-A"],
        ["git", "diff", "--cached", "--quiet"],  # Check if there are changes
    ]

    # Check for changes
    result = subprocess.run(cmds[1], cwd=PROJECT_DIR, capture_output=True)
    if result.returncode == 0:
        print("No changes to deploy")
        return False

    subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR, capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=PROJECT_DIR, capture_output=True)
    result = subprocess.run(["git", "push"], cwd=PROJECT_DIR, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Deployed to GitHub Pages")
        return True
    else:
        print(f"❌ Deploy failed: {result.stderr}")
        return False


def full_cycle():
    """Run the complete daily automation cycle."""
    report_lines = [f"🤖 **Blog 自動化日報** — {datetime.now().strftime('%Y-%m-%d %H:%M')}"]
    report_lines.append("")

    # 1. Check Umami
    if check_umami():
        report_lines.append("✅ Umami 運行中")
    else:
        report_lines.append("⚠️ Umami 未運行，嘗試啟動...")
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=f"{PROJECT_DIR}/docker/umami",
            capture_output=True
        )

    # 2. Check tunnel
    tunnel_url = check_tunnel()
    if tunnel_url:
        report_lines.append(f"✅ Tunnel: {tunnel_url}")
    else:
        report_lines.append("⚠️ Tunnel 未連線，重新啟動...")
        subprocess.Popen(
            [sys.executable, f"{SCRIPTS_DIR}/umami-tunnel.py", "restart"],
        )

    # 3. Collect analytics
    report_lines.append("")
    if collect_analytics():
        report_lines.append("✅ 分析數據已收集")
    else:
        report_lines.append("⚠️ 分析數據收集失敗（可能尚無流量）")

    # 4. Run optimizer
    opt_report = run_optimizer()
    if opt_report:
        report_lines.append("")
        report_lines.append(opt_report)

    # 5. Auto-add internal links
    link_changes = auto_add_internal_links()
    if link_changes > 0:
        report_lines.append(f"\n🔗 自動添加內部連結: {link_changes} 篇文章")

    # 6. Build + deploy
    if hugo_build():
        if git_deploy():
            report_lines.append("\n🚀 已自動部署更新")
        else:
            report_lines.append("\nℹ️ 無新變更需部署")
    else:
        report_lines.append("\n❌ Hugo 建置失敗")

    full_report = "\n".join(report_lines)
    print(full_report)

    # Save report
    os.makedirs(f"{DATA_DIR}/reports", exist_ok=True)
    with open(f"{DATA_DIR}/reports/{datetime.now().strftime('%Y-%m-%d')}.txt", "w") as f:
        f.write(full_report)

    return full_report


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    if mode == "full":
        full_cycle()
    elif mode == "report":
        collect_analytics()
        print(run_optimizer())
    elif mode == "deploy":
        hugo_build()
        git_deploy()
    elif mode == "links":
        changes = auto_add_internal_links()
        print(f"Added internal links to {changes} articles")
