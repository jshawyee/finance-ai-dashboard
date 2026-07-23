from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from notification.feishu import send_feishu
from notification.feishu.formatter import build_card

webhook = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()
if not webhook or not secret:
    raise SystemExit("FEISHU_WEBHOOK_URL and FEISHU_WEBHOOK_SECRET are required.")
data = json.loads((ROOT / "data" / "latest" / "dashboard.json").read_text(encoding="utf-8"))
send_feishu(webhook, secret, build_card(data, os.environ.get("DASHBOARD_URL", "")))
print("Feishu daily card sent successfully.")
