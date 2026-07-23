from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
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
    try:
        send_feishu_text(webhook, secret, fallback)
        print("Feishu plain text fallback sent successfully.")
    except Exception as final_error:
        diagnostic = ROOT / "data" / "system" / "feishu-diagnostic.json"
        diagnostic.parent.mkdir(parents=True, exist_ok=True)
        diagnostic.write_text(json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "failure",
            "error_type": type(final_error).__name__,
            "message": str(final_error)[:500],
            "note": "This file never contains the webhook URL or signing secret.",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
