from __future__ import annotations

from html import escape
from typing import Any


def _line(item: dict[str, Any]) -> str:
    arrow = "🟢" if item["change_pct"] >= 0 else "🟠"
    sign = "+" if item["change_pct"] >= 0 else ""
    return f"{arrow} **{escape(item['name'])}**  {item['close']:,.2f}  {sign}{item['change_pct']:.2f}%"


def build_card(data: dict[str, Any], dashboard_url: str = "") -> dict[str, Any]:
    report = data["report"]
    index_lines = "\n".join(_line(item) for item in data["indices"])
    sector_lines = "\n".join(f"• **{item['name']}** {item['average_change_pct']:+.2f}% · 领涨 {item['leader']}" for item in data["sectors"])
    risk_lines = "\n".join(f"• {escape(item)}" for item in report["risks"][:3])
    elements: list[dict[str, Any]] = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**{escape(report['headline'])}**\n{escape(report['overview'])}"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**全球指数 · 最近完整收盘**\n{index_lines}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**主题板块 · 等权表现**\n{sector_lines}"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**风险提示**\n{risk_lines}\n\n_{escape(report['disclaimer'])}_"}},
    ]
    if dashboard_url:
        elements.append({"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "打开金融驾驶舱"}, "url": dashboard_url, "type": "primary"}]})
    return {
        "config": {"wide_screen_mode": True, "enable_forward": True},
        "header": {"template": "green" if report["market_bias"] == "risk-on" else "orange" if report["market_bias"] == "risk-off" else "turquoise", "title": {"tag": "plain_text", "content": f"Market Pulse 金融日报 · {data['meta']['report_date']}"}},
        "elements": elements,
    }
