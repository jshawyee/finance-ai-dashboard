from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import urllib.request
from typing import Any


def _signature(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def _post(webhook_url: str, secret: str, message: dict[str, Any]) -> None:
    timestamp = int(time.time())
    payload = {"timestamp": timestamp, "sign": _signature(str(timestamp), secret), **message}
    request = urllib.request.Request(
        webhook_url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "finance-ai-dashboard/1.0"}, method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        result = json.loads(response.read().decode("utf-8"))
    if result.get("code", result.get("StatusCode", 0)) != 0:
        raise RuntimeError(f"Feishu rejected the message: {result}")


def send_feishu(webhook_url: str, secret: str, card: dict[str, Any]) -> None:
    _post(webhook_url, secret, {"msg_type": "interactive", "card": card})


def send_feishu_text(webhook_url: str, secret: str, text: str) -> None:
    _post(webhook_url, secret, {"msg_type": "text", "content": {"text": text}})
