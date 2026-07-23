from __future__ import annotations

from typing import Any


def _tone(value: float) -> str:
    return "positive" if value > 0.25 else "negative" if value < -0.25 else "neutral"


def _fmt(item: dict[str, Any]) -> str:
    sign = "+" if item["change_pct"] >= 0 else ""
    return f"{item['name']} {sign}{item['change_pct']:.2f}%"


def _find(items: list[dict[str, Any]], symbol: str) -> dict[str, Any] | None:
    return next((item for item in items if item["symbol"] == symbol), None)


def build_daily_report(indices: list[dict[str, Any]], macro: list[dict[str, Any]], sectors: list[dict[str, Any]], news: list[dict[str, Any]]) -> dict[str, Any]:
    us = [item for item in indices if item["market"] == "美国"]
    asia = [item for item in indices if item["market"] in {"日本", "韩国"}]
    us_average = sum(item["change_pct"] for item in us) / max(len(us), 1)
    asia_average = sum(item["change_pct"] for item in asia) / max(len(asia), 1)
    sector_average = sum(item["average_change_pct"] for item in sectors) / max(len(sectors), 1)
    vix, treasury, dollar, oil = (_find(macro, symbol) for symbol in ("^VIX", "^TNX", "DX-Y.NYB", "CL=F"))
    leader = max(sectors, key=lambda item: item["average_change_pct"], default=None)
    laggard = min(sectors, key=lambda item: item["average_change_pct"], default=None)

    positive_count = sum(item["change_pct"] > 0 for item in indices)
    negative_count = sum(item["change_pct"] < 0 for item in indices)
    bias = "risk-on" if us_average > 0.35 and (not vix or vix["change_pct"] < 0) else "risk-off" if us_average < -0.35 and (not vix or vix["change_pct"] > 0) else "mixed"
    headline = f"{leader['name'] if leader else '全球市场'}相对领先，指数呈现{'偏强' if positive_count > negative_count else '分化'}格局"

    possible_factors = []
    if vix:
        possible_factors.append(f"VIX {_fmt(vix)}，风险偏好可能受到{'支持' if vix['change_pct'] < 0 else '压制'}")
    if treasury:
        possible_factors.append(f"美国十年期收益率 {_fmt(treasury)}，可能影响成长股估值")
    if dollar:
        possible_factors.append(f"美元指数 {_fmt(dollar)}，需关注对日元、韩元和跨国企业的传导")
    if oil:
        possible_factors.append(f"WTI 原油 {_fmt(oil)}，可能影响化工成本与产品价差预期")

    return {
        "headline": headline,
        "overview": f"最近完整收盘数据显示，{positive_count} 个指数上涨、{negative_count} 个下跌。以下判断由固定规则生成，只描述同步变化与可能因素，不将新闻或宏观指标表述为已证实的涨跌原因。",
        "market_bias": bias,
        "sections": [
            {"title": "美国市场", "tone": _tone(us_average), "summary": f"美国三大观察指数平均变动 {us_average:+.2f}%。", "evidence": [_fmt(item) for item in us]},
            {"title": "日、韩市场", "tone": _tone(asia_average), "summary": f"日本、韩国指数最近完整交易日平均变动 {asia_average:+.2f}%。", "evidence": [_fmt(item) for item in asia]},
            {"title": "行业趋势", "tone": _tone(sector_average), "summary": f"四个关注板块等权平均 {sector_average:+.2f}%。", "evidence": [f"{item['name']} {item['average_change_pct']:+.2f}%（领涨 {item['leader']}）" for item in sectors]},
            {"title": "可能影响因素", "tone": "neutral", "summary": "宏观指标与股价同时变化不等于因果关系。", "evidence": possible_factors},
            {"title": "相关信息", "tone": "neutral", "summary": f"本期收集 {len(news)} 条可追溯链接，其中 {sum(item['is_official'] for item in news)} 条标记为官方来源。", "evidence": [item["title"] for item in news[:3]] or ["本期未取得可验证新闻，未进行原因归因"]},
        ],
        "highlights": [f"{leader['name']}领涨关注板块，等权变动 {leader['average_change_pct']:+.2f}%" if leader else "板块数据不足", f"指数涨跌家数为 {positive_count}:{negative_count}"],
        "risks": ["免费公共行情可能延迟、调整或短时不可用", "新闻标题不能单独证明价格波动原因", f"{laggard['name']}为相对落后板块，等权变动 {laggard['average_change_pct']:+.2f}%" if laggard else "板块数据不足"],
        "focus_next": ["美债收益率、美元与 VIX 的方向是否延续", "存储价格、产能与企业业绩指引", "商业航天发射、订单和监管进展", "化工原料成本及产品价差"],
        "disclaimer": "仅供个人信息整理，不构成投资建议。所有‘可能因素’均为规则推断，请结合原始公告核验。",
    }
