from __future__ import annotations

from statistics import fmean
from typing import Any

SECTOR_NAMES = {"space": "商业航天", "memory": "存储与内存", "chemicals": "化工与材料", "technology": "科技龙头"}


def summarize_sectors(stocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for key, name in SECTOR_NAMES.items():
        members = [item for item in stocks if item["category"] == key]
        if not members:
            continue
        leader = max(members, key=lambda item: item["change_pct"])
        laggard = min(members, key=lambda item: item["change_pct"])
        summaries.append({
            "key": key, "name": name, "average_change_pct": round(fmean(item["change_pct"] for item in members), 4),
            "advancing": sum(item["change_pct"] > 0.01 for item in members),
            "declining": sum(item["change_pct"] < -0.01 for item in members),
            "unchanged": sum(abs(item["change_pct"]) <= 0.01 for item in members),
            "leader": leader["symbol"], "laggard": laggard["symbol"],
            "status": "stale" if any(item["status"] == "stale" for item in members) else "fresh",
        })
    return summaries
