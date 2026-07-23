from __future__ import annotations

import os
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from notification.feishu import send_feishu

webhook = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()
if webhook and secret:
    card = {
        "header": {"template": "red", "title": {"tag": "plain_text", "content": "Market Pulse 今日自动更新失败"}},
        "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "网站将继续保留上次成功数据，不会用空数据覆盖。请打开 GitHub Actions 查看失败步骤。"}}],
    }
    send_feishu(webhook, secret, card)
    print("Feishu failure notice sent.")
else:
    print("Feishu secrets unavailable; failure notice skipped.")
