from __future__ import annotations

import os
from urllib.parse import urlparse

webhook = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
secret = os.environ.get("FEISHU_WEBHOOK_SECRET", "").strip()
if not webhook:
    raise SystemExit("FEISHU_WEBHOOK_URL is missing from repository Actions secrets.")
if not secret:
    raise SystemExit("FEISHU_WEBHOOK_SECRET is missing from repository Actions secrets.")
parsed = urlparse(webhook)
allowed_hosts = {"open.feishu.cn", "open.larksuite.com"}
if parsed.scheme != "https" or parsed.hostname not in allowed_hosts or "/open-apis/bot/v2/hook/" not in parsed.path:
    raise SystemExit("FEISHU_WEBHOOK_URL is not a valid Feishu/Lark custom bot webhook URL.")
if len(secret) < 10:
    raise SystemExit("FEISHU_WEBHOOK_SECRET appears incomplete.")
print("Feishu secrets are present and their formats are valid; values remain masked.")
