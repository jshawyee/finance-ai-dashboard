from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent.analyzer import build_daily_report
from agent.market_collector import collect_markets
from agent.news_collector import collect_news
from agent.processor import summarize_sectors

LATEST = ROOT / "data" / "latest" / "dashboard.json"
MARKER = ROOT / ".daily-generated"


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _merge(group: str, config: dict[str, Any], live: dict[str, list[dict[str, Any]]], previous: dict[str, Any] | None) -> list[dict[str, Any]]:
    fresh = {item["symbol"]: item for item in live[group]}
    cached = {item["symbol"]: item for item in (previous or {}).get(group, [])}
    merged: list[dict[str, Any]] = []
    for instrument in config[group]:
        symbol = instrument["symbol"]
        if symbol in fresh:
            merged.append(fresh[symbol])
        elif symbol in cached:
            fallback = cached[symbol] | {"status": "stale", "source": f"缓存 · {cached[symbol].get('source', '上次成功数据')}"}
            merged.append(fallback)
    return merged


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect completed closes and generate the zero-cost daily report.")
    parser.add_argument("--skip-if-fresh", action="store_true")
    args = parser.parse_args()
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    previous = _read_json(LATEST)
    if args.skip_if_fresh and previous and previous.get("meta", {}).get("report_date") == now.date().isoformat() and previous.get("meta", {}).get("status") == "fresh":
        print("A fresh report already exists for today; compensation run skipped.")
        MARKER.unlink(missing_ok=True)
        return 0

    config = json.loads((ROOT / "config" / "markets.json").read_text(encoding="utf-8"))
    live, market_errors = collect_markets(config, now=now)
    merged = {group: _merge(group, config, live, previous) for group in ("indices", "macro", "stocks")}
    if not merged["indices"] or not merged["stocks"]:
        raise RuntimeError("No usable index or stock data was available, including cache; existing website remains untouched.")

    news, news_errors = collect_news()
    if not news and previous:
        news = previous.get("news", [])
    sectors = summarize_sectors(merged["stocks"])
    expected = sum(len(config[group]) for group in ("indices", "macro", "stocks"))
    actual = sum(len(merged[group]) for group in ("indices", "macro", "stocks"))
    stale_count = sum(item["status"] == "stale" for group in merged.values() for item in group)
    status = "fresh" if actual == expected and stale_count == 0 and not market_errors else "partial"
    issue_count = len(market_errors) + len(news_errors)
    message = "所有行情已取得最近完整收盘数据" if status == "fresh" else f"使用了 {stale_count} 项缓存，{expected - actual} 项暂不可用；保留可验证数据"
    data: dict[str, Any] = {
        "meta": {"generated_at": now.isoformat(timespec="seconds"), "report_date": now.date().isoformat(), "timezone": "Asia/Shanghai", "status": status, "status_message": message, "next_update": "每天北京时间 09:47 首次尝试；10:07、10:27、10:47、11:07 自动补偿", "version": "1.0.0", "collector_issues": issue_count},
        **merged, "sectors": sectors, "news": news,
        "report": build_daily_report(merged["indices"], merged["macro"], sectors, news),
    }
    _write_json(LATEST, data)
    _write_json(ROOT / "data" / "history" / f"{now.date().isoformat()}.json", data)
    history = sorted((ROOT / "data" / "history").glob("*.json"))
    for old_file in history[:-120]:
        old_file.unlink()
    MARKER.write_text(now.isoformat(), encoding="utf-8")
    print(f"Generated {status} dashboard: {actual}/{expected} quotes, {len(news)} news, {issue_count} collector issues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
