from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, time, timedelta, timezone
from typing import Any
from urllib.parse import quote
from zoneinfo import ZoneInfo

from agent.http_client import get_json

YAHOO_CHARTS = [
    "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=3mo&interval=1d&events=history",
    "https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range=3mo&interval=1d&events=history",
]


def _closed(timestamp: int, instrument: dict[str, Any], now: datetime) -> bool:
    zone = ZoneInfo(instrument["timezone"])
    bar_date = datetime.fromtimestamp(timestamp, timezone.utc).astimezone(zone).date()
    hour, minute = (int(part) for part in instrument["close"].split(":"))
    close_at = datetime.combine(bar_date, time(hour, minute), zone) + timedelta(minutes=20)
    return now.astimezone(zone) >= close_at


def _fetch_one(instrument: dict[str, Any], now: datetime) -> dict[str, Any]:
    symbols = instrument.get("aliases", [instrument["symbol"]])
    last_error: Exception | None = None
    for source_symbol in symbols:
        for endpoint in YAHOO_CHARTS:
            try:
                payload = get_json(endpoint.format(symbol=quote(source_symbol, safe="")), timeout=8, retries=1)
                result = payload["chart"]["result"][0]
                timestamps = result.get("timestamp", [])
                series = result["indicators"]["quote"][0]
                history: list[dict[str, Any]] = []
                for index, stamp in enumerate(timestamps):
                    values = {key: series.get(key, [None] * len(timestamps))[index] for key in ("open", "high", "low", "close", "volume")}
                    if any(values[key] is None for key in ("open", "high", "low", "close")) or not _closed(stamp, instrument, now):
                        continue
                    trade_date = datetime.fromtimestamp(stamp, timezone.utc).astimezone(ZoneInfo(instrument["timezone"])).date().isoformat()
                    history.append({"date": trade_date, **{key: round(float(value or 0), 4) for key, value in values.items()}})
                if len(history) < 2:
                    raise ValueError("not enough completed daily bars")
                latest, previous = history[-1], history[-2]
                change = latest["close"] - previous["close"]
                trend_base = history[-6]["close"] if len(history) >= 6 else history[0]["close"]
                age = (now.astimezone(ZoneInfo(instrument["timezone"])).date() - datetime.fromisoformat(latest["date"]).date()).days
                return {
                    "symbol": instrument["symbol"], "name": instrument["name"], "market": instrument["market"],
                    "category": instrument["category"], "currency": instrument["currency"], "trade_date": latest["date"],
                    "close": latest["close"], "previous_close": previous["close"], "change": round(change, 4),
                    "change_pct": round(change / previous["close"] * 100, 4),
                    "trend_5d": round((latest["close"] / trend_base - 1) * 100, 4),
                    "status": "fresh" if age <= 5 else "stale",
                    "source": f"Yahoo Finance ({source_symbol}{' · TOPIX ETF proxy' if source_symbol == '1306.T' else ''})",
                    "history": history[-60:],
                }
            except (RuntimeError, KeyError, IndexError, TypeError, ValueError) as error:
                last_error = error
    raise RuntimeError(f"all sources failed for {instrument['symbol']}") from last_error


def collect_markets(groups: dict[str, list[dict[str, Any]]], *, now: datetime | None = None) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    now = now or datetime.now(timezone.utc)
    jobs = [(group, item) for group in ("indices", "macro", "stocks") for item in groups[group]]
    results: dict[str, list[dict[str, Any]]] = {"indices": [], "macro": [], "stocks": []}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_fetch_one, item, now): (group, item) for group, item in jobs}
        for future in as_completed(futures):
            group, item = futures[future]
            try:
                results[group].append(future.result())
            except RuntimeError as error:
                errors.append(f"{item['symbol']}: {error}")
    order = {group: {item["symbol"]: index for index, item in enumerate(groups[group])} for group in results}
    for group in results:
        results[group].sort(key=lambda item: order[group][item["symbol"]])
    return results, errors
