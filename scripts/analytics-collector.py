"""
Blog Analytics Collector - queries Umami API and saves daily reports.
Run via OpenClaw cron or manually.
"""
import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timedelta

UMAMI_URL = "http://localhost:3100"
WEBSITE_ID = "eef023a2-ea1f-40fb-b0c2-23ec694d3dc3"
DATA_DIR = "/home/simon/blog/data/analytics"
CREDS_FILE = "/home/simon/blog/docker/umami/.admin-password"

def get_token():
    """Login to Umami and get auth token."""
    with open(CREDS_FILE) as f:
        password = f.read().strip()
    data = json.dumps({"username": "admin", "password": password}).encode()
    req = urllib.request.Request(
        f"{UMAMI_URL}/api/auth/login",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())["token"]
    except Exception as e:
        print(f"Auth failed: {e}")
        return None

def api_get(token, endpoint, params=None):
    """Make authenticated GET request to Umami API."""
    url = f"{UMAMI_URL}/api/websites/{WEBSITE_ID}/{endpoint}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())
    except Exception as e:
        print(f"API error ({endpoint}): {e}")
        return None

def collect_daily(token, date=None):
    """Collect analytics for a specific date."""
    if date is None:
        date = datetime.now()

    start_at = int(datetime(date.year, date.month, date.day).timestamp() * 1000)
    end_at = start_at + 86400000  # +24hr

    params = {"startAt": str(start_at), "endAt": str(end_at)}

    report = {
        "date": date.strftime("%Y-%m-%d"),
        "collected_at": datetime.now().isoformat(),
        "stats": api_get(token, "stats", params),
        "pageviews": api_get(token, "pageviews", {**params, "unit": "hour"}),
        "metrics_url": api_get(token, "metrics", {**params, "type": "url"}),
        "metrics_referrer": api_get(token, "metrics", {**params, "type": "referrer"}),
        "metrics_browser": api_get(token, "metrics", {**params, "type": "browser"}),
        "metrics_os": api_get(token, "metrics", {**params, "type": "os"}),
        "metrics_device": api_get(token, "metrics", {**params, "type": "device"}),
        "metrics_country": api_get(token, "metrics", {**params, "type": "country"}),
        "metrics_language": api_get(token, "metrics", {**params, "type": "language"}),
    }

    return report

def save_report(report):
    """Save daily analytics report."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{report['date']}.json"
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"📊 Saved: {filepath}")
    return filepath

def generate_summary(report):
    """Generate human-readable summary for Telegram."""
    stats = report.get("stats") or {}
    urls = report.get("metrics_url") or []
    referrers = report.get("metrics_referrer") or []
    countries = report.get("metrics_country") or []

    pv = stats.get("pageviews", {}).get("value", 0)
    visitors = stats.get("visitors", {}).get("value", 0)
    bounces = stats.get("bounces", {}).get("value", 0)
    avg_time = stats.get("totaltime", {}).get("value", 0)

    bounce_rate = (bounces / pv * 100) if pv > 0 else 0

    lines = [
        f"📊 **Blog 日報** — {report['date']}",
        "",
        f"👁️ 瀏覽量: {pv}",
        f"👤 訪客數: {visitors}",
        f"📈 跳出率: {bounce_rate:.1f}%",
        f"⏱️ 平均停留: {avg_time // 1000}s" if avg_time else "",
        "",
        "🏆 **熱門頁面 Top 5:**",
    ]

    for i, u in enumerate(urls[:5], 1):
        lines.append(f"  {i}. {u.get('x', '?')} ({u.get('y', 0)} views)")

    if referrers:
        lines.append("")
        lines.append("🔗 **來源 Top 3:**")
        for r in referrers[:3]:
            lines.append(f"  • {r.get('x', 'direct')} ({r.get('y', 0)})")

    if countries:
        lines.append("")
        lines.append("🌍 **國家 Top 3:**")
        for c in countries[:3]:
            lines.append(f"  • {c.get('x', '?')} ({c.get('y', 0)})")

    return "\n".join(lines)

def collect_weekly(token):
    """Collect 7-day analytics for weekly review."""
    now = datetime.now()
    start_at = int((now - timedelta(days=7)).timestamp() * 1000)
    end_at = int(now.timestamp() * 1000)
    params = {"startAt": str(start_at), "endAt": str(end_at)}

    report = {
        "period": "weekly",
        "start": (now - timedelta(days=7)).strftime("%Y-%m-%d"),
        "end": now.strftime("%Y-%m-%d"),
        "collected_at": now.isoformat(),
        "stats": api_get(token, "stats", params),
        "pageviews": api_get(token, "pageviews", {**params, "unit": "day"}),
        "metrics_url": api_get(token, "metrics", {**params, "type": "url"}),
        "metrics_referrer": api_get(token, "metrics", {**params, "type": "referrer"}),
        "metrics_country": api_get(token, "metrics", {**params, "type": "country"}),
    }

    filepath = f"{DATA_DIR}/weekly-{now.strftime('%Y-%m-%d')}.json"
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"📊 Weekly saved: {filepath}")
    return report

if __name__ == "__main__":
    token = get_token()
    if not token:
        sys.exit(1)

    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"

    if mode == "daily":
        report = collect_daily(token)
        save_report(report)
        print(generate_summary(report))
    elif mode == "weekly":
        collect_weekly(token)
    elif mode == "summary":
        report = collect_daily(token)
        print(generate_summary(report))
