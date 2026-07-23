from __future__ import annotations

import json
import http.client
import time
import urllib.error
import urllib.request
from typing import Any

USER_AGENT = "finance-ai-dashboard/1.0 (+https://github.com/jshawyee/finance-ai-dashboard)"


def get_json(url: str, *, timeout: int = 8, retries: int = 1) -> dict[str, Any]:
    last_error: Exception | None = None
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, http.client.HTTPException, OSError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(0.7 * (attempt + 1))
    raise RuntimeError(f"request failed: {url}") from last_error
