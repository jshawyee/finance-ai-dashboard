from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from notification.feishu import send_feishu, send_feishu_text
from notification.feishu.formatter import build_card

webhook = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()
if not webhook or not secret:
    raise SystemExit("FEISHU_WEBHOOK_URL and FEISHU_WEBHOOK_SECRET are required.")
data = json.loads((ROOT / "data" / "latest" / "dashboard.json").read_text(encoding="utf-8"))
try:
    send_feishu(webhook, secret, build_card(data, os.environ.get("DASHBOARD_URL", "")))
    print("Feishu daily card sent successfully.")
except Exception as card_error:
    report = data["report"]
    indices = "\n".join(f"{item['name']} {item['change_pct']:+.2f}%" for item in data["indices"])
    dashboard_url = os.environ.get("DASHBOARD_URL", "")
    fallback = f"Market Pulse 金融日报 · {data['meta']['report_date']}\n{report['headline']}\n\n{indices}\n\n{report['disclaimer']}\n{dashboard_url}"
    print(f"Interactive card failed ({type(card_error).__name__}); trying plain text fallback.")
    send_feishu_text(webhook, secret, fallback)
    print("Feishu plain text fallback sent successfully.")
