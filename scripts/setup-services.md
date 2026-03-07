# Blog Auto-Optimization Services Setup

## Components
1. **Umami** (Docker) — Analytics backend on port 3100
2. **Cloudflare Tunnel** — Exposes Umami to public internet
3. **OpenClaw Cron** — Daily analytics + optimization cycle

## Quick Start
```
# Start Umami
cd docker/umami && docker compose up -d

# Start tunnel (gets new URL each time)
python3 scripts/umami-tunnel.py start

# Run daily cycle manually
python3 scripts/daily-blog-cycle.py
```

## Architecture
```
GitHub Pages (public) ──→ Umami JS (via tunnel) ──→ Umami (localhost:3100)
                                                          ↓
OpenClaw Cron (11:00) ──→ daily-blog-cycle.py ──→ Umami API (localhost:3100)
                                ↓
                    analytics-collector.py → data/analytics/*.json
                    auto-optimize.py → optimization suggestions
                    auto-add-internal-links → content updates
                    hugo build → git push → GitHub Pages redeploy
                                ↓
                    Telegram report → Simon
```

## Data Files
- `data/analytics/YYYY-MM-DD.json` — Daily analytics snapshots
- `data/analytics/weekly-*.json` — Weekly summaries
- `data/analytics/analysis-*.json` — AI analysis results
- `data/optimization-log.json` — Historical optimization tracking
- `data/tunnel_url.txt` — Current tunnel URL
- `data/reports/*.txt` — Daily reports

## Notes
- Quick tunnel URLs change on restart; hugo.toml is auto-updated
- Umami default creds changed; password stored in docker/umami/.admin-password
- Website ID: eef023a2-ea1f-40fb-b0c2-23ec694d3dc3
