"""Create the clearly-labelled seed JSON used before the first successful live run."""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent.analyzer import build_daily_report
from agent.processor import summarize_sectors

BASE = {
    "^IXIC": 23031.21, "^GSPC": 7266.99, "^SOX": 6681.12, "^N225": 50115.6, "^TOPX": 3011.5,
    "^KS11": 2747.95, "^KQ11": 892.78, "^VIX": 18.42, "^TNX": 4.21, "DX-Y.NYB": 98.74,
    "JPY=X": 146.52, "KRW=X": 1378.4, "CL=F": 73.18, "GC=F": 3342.6, "SPCX": 282.54,
    "RKLB": 83.35, "ASTS": 71.92, "LUNR": 14.86, "MU": 148.8, "SNDK": 91.43, "STX": 154.19,
    "WDC": 83.82, "005930.KS": 78600, "000660.KS": 284500, "285A.T": 8120, "LIN": 485.62,
    "DOW": 31.44, "DD": 91.28, "APD": 308.74, "4063.T": 6070, "051910.KS": 324500,
    "NVDA": 188.42, "AMD": 212.6, "AVGO": 388.69, "MSFT": 528.12, "GOOGL": 201.74,
    "AMZN": 231.48, "META": 694.16, "AAPL": 226.38,
}
CHANGES = [0.82, 0.46, 1.18, -0.18, 0.31, 0.56, 0.39, -2.11, 0.24, -0.16, 0.12, -0.21, 0.64, 0.32]


def business_dates(end: date, count: int = 12) -> list[date]:
    dates: list[date] = []
    current = end
    while len(dates) < count:
        if current.weekday() < 5:
            dates.append(current)
        current -= timedelta(days=1)
    return list(reversed(dates))


def make_quote(item: dict[str, Any], index: int, trade_date: date) -> dict[str, Any]:
    close = BASE[item["symbol"]]
    change_pct = CHANGES[index % len(CHANGES)]
    previous = close / (1 + change_pct / 100)
    history = []
    for position, day in enumerate(business_dates(trade_date)):
        factor = 0.96 + position * 0.0037
        history.append({"date": day.isoformat(), "open": round(close * factor, 4), "high": round(close * (factor + .012), 4), "low": round(close * (factor - .01), 4), "close": round(close * (factor + .004), 4), "volume": 1_000_000 + position * 72_000})
    history[-1]["close"] = close
    return {**{key: item[key] for key in ("symbol", "name", "market", "category", "currency")}, "trade_date": trade_date.isoformat(), "close": close, "previous_close": round(previous, 4), "change": round(close - previous, 4), "change_pct": change_pct, "trend_5d": round((close / history[-6]["close"] - 1) * 100, 4), "status": "demo", "source": "演示数据（等待首次自动采集）", "history": history}


def main() -> None:
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    last_weekday = now.date() - timedelta(days=1)
    while last_weekday.weekday() >= 5:
        last_weekday -= timedelta(days=1)
    config = json.loads((ROOT / "config" / "markets.json").read_text(encoding="utf-8"))
    groups = {group: [make_quote(item, index, last_weekday) for index, item in enumerate(config[group])] for group in ("indices", "macro", "stocks")}
    sectors = summarize_sectors(groups["stocks"])
    for sector in sectors:
        sector["status"] = "demo"
    news = [{"id": "system-demo", "title": "等待首次自动采集，真实新闻会在任务成功后替换此提示", "url": "#", "source": "系统", "published_at": now.isoformat(timespec="seconds"), "category": "system", "symbols": [], "is_official": True}]
    output = {"meta": {"generated_at": now.isoformat(timespec="seconds"), "report_date": now.date().isoformat(), "timezone": "Asia/Shanghai", "status": "demo", "status_message": "当前为明确标记的演示数据，等待首次 GitHub Actions 自动采集", "next_update": "每天北京时间 09:47 首次尝试；10:07、10:27、10:47、11:07 自动补偿", "version": "1.0.0", "collector_issues": 0}, **groups, "sectors": sectors, "news": news, "report": build_daily_report(groups["indices"], groups["macro"], sectors, news)}
    output["report"]["overview"] = "当前为界面演示数据，不代表真实市场。首次自动任务成功后将替换为最近完整收盘数据。"
    for target in (ROOT / "data" / "latest" / "dashboard.json", ROOT / "frontend" / "public" / "data" / "dashboard.json"):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Created clearly-labelled seed dashboard JSON.")


if __name__ == "__main__":
    main()
