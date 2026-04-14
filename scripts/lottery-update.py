#!/usr/bin/env python3
"""
Taiwan Lottery Data Updater
抓取威力彩、大樂透、今彩539 開獎資料，存為 JSON。

Usage:
    python lottery-update.py                    # 抓當月資料
    python lottery-update.py --backfill 2025-01 # 抓指定年月
    python lottery-update.py --backfill 2025-01 --to 2025-06  # 抓範圍
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Handle both venv and system installs
try:
    from TaiwanLottery import TaiwanLotteryCrawler
except ImportError:
    # Try adding venv path
    venv_path = Path(__file__).resolve().parent.parent / ".venv/lib/python3.12/site-packages"
    if venv_path.exists():
        sys.path.insert(0, str(venv_path))
        from TaiwanLottery import TaiwanLotteryCrawler
    else:
        print("Error: taiwanlottery not installed. Run: pip install taiwanlottery")
        sys.exit(1)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "lottery"

# Lottery type configs
LOTTERY_TYPES = {
    "super_lotto": {
        "name": "威力彩",
        "method": "super_lotto",
        "file": "super_lotto.json",
    },
    "lotto649": {
        "name": "大樂透",
        "method": "lotto649",
        "file": "lotto649.json",
    },
    "daily_cash": {
        "name": "今彩539",
        "method": "lotto39m5",
        "file": "daily_cash_539.json",
    },
}

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def load_existing(filepath: Path) -> dict:
    """Load existing data, keyed by 期別 for dedup."""
    if not filepath.exists():
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["期別"]: item for item in data}


def save_data(filepath: Path, data_dict: dict):
    """Save data sorted by 期別 descending."""
    items = sorted(data_dict.values(), key=lambda x: x["期別"], reverse=True)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, default=str)


def fetch_with_retry(crawler, method_name: str, year: str, month: str) -> list:
    """Fetch data with retry logic."""
    method = getattr(crawler, method_name)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = method(back_time=[year, month])
            return result if result else []
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"  ⚠ Attempt {attempt} failed: {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"  ✗ All {MAX_RETRIES} attempts failed: {e}")
                return []


def generate_months(start_ym: str, end_ym: str) -> list[tuple[str, str]]:
    """Generate list of (year, month) tuples from start to end inclusive."""
    start = datetime.strptime(start_ym, "%Y-%m")
    end = datetime.strptime(end_ym, "%Y-%m")
    months = []
    current = start
    while current <= end:
        months.append((str(current.year), str(current.month).zfill(2)))
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return months


def update_lottery(months: list[tuple[str, str]], verbose: bool = True):
    """Main update logic."""
    crawler = TaiwanLotteryCrawler()
    summary = {}

    for key, config in LOTTERY_TYPES.items():
        filepath = DATA_DIR / config["file"]
        existing = load_existing(filepath)
        original_count = len(existing)
        new_count = 0

        if verbose:
            print(f"\n{'='*50}")
            print(f"📊 {config['name']} ({key})")
            print(f"   既有資料: {original_count} 期")

        for year, month in months:
            if verbose:
                print(f"   抓取 {year}-{month}...", end=" ", flush=True)

            results = fetch_with_retry(crawler, config["method"], year, month)

            added = 0
            for item in results:
                draw_id = item["期別"]
                if draw_id not in existing:
                    existing[draw_id] = item
                    added += 1
                    new_count += 1

            if verbose:
                print(f"取得 {len(results)} 期, 新增 {added} 期")

            # Be polite to the server
            time.sleep(1)

        save_data(filepath, existing)

        total = len(existing)
        summary[config["name"]] = {
            "original": original_count,
            "new": new_count,
            "total": total,
        }

        if verbose:
            print(f"   ✓ 儲存完成: {total} 期 (新增 {new_count})")

    return summary


def print_sample(limit: int = 3):
    """Print sample data from each file."""
    print(f"\n{'='*50}")
    print("📋 資料樣本")
    print(f"{'='*50}")

    for key, config in LOTTERY_TYPES.items():
        filepath = DATA_DIR / config["file"]
        if not filepath.exists():
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"\n--- {config['name']} (共 {len(data)} 期) ---")
        for item in data[:limit]:
            print(json.dumps(item, ensure_ascii=False, default=str))


def main():
    parser = argparse.ArgumentParser(description="台灣彩券開獎資料更新工具")
    parser.add_argument(
        "--backfill",
        type=str,
        help="起始年月 (YYYY-MM), e.g. 2025-01",
    )
    parser.add_argument(
        "--to",
        type=str,
        help="結束年月 (YYYY-MM), 搭配 --backfill 使用",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="顯示資料樣本",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="安靜模式",
    )

    args = parser.parse_args()

    now = datetime.now()

    if args.backfill:
        start_ym = args.backfill
        end_ym = args.to if args.to else args.backfill
        months = generate_months(start_ym, end_ym)
        print(f"🔄 回填模式: {start_ym} → {end_ym} ({len(months)} 個月)")
    else:
        year = str(now.year)
        month = str(now.month).zfill(2)
        months = [(year, month)]
        print(f"🔄 更新當月: {year}-{month}")

    summary = update_lottery(months, verbose=not args.quiet)

    print(f"\n{'='*50}")
    print("📈 更新摘要")
    print(f"{'='*50}")
    for name, stats in summary.items():
        print(f"  {name}: {stats['total']} 期 (新增 {stats['new']})")

    if args.sample or not args.quiet:
        print_sample()


if __name__ == "__main__":
    main()
