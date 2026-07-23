import unittest

from agent.analyzer.rules import build_daily_report


def quote(symbol: str, name: str, market: str, value: float) -> dict:
    return {"symbol": symbol, "name": name, "market": market, "change_pct": value}


class RuleReportTests(unittest.TestCase):
    def test_uses_possible_factor_language(self) -> None:
        indices = [quote("^IXIC", "纳指", "美国", 1), quote("^N225", "日经", "日本", -0.2)]
        macro = [quote("^VIX", "VIX", "美国", -2), quote("^TNX", "美国十年期收益率", "美国", 0.5)]
        sectors = [{"name": "科技龙头", "average_change_pct": 1.2, "leader": "NVDA"}]
        report = build_daily_report(indices, macro, sectors, [])
        self.assertIn("可能", report["disclaimer"])
        self.assertTrue(any(section["title"] == "可能影响因素" for section in report["sections"]))
        self.assertEqual(report["market_bias"], "risk-on")


if __name__ == "__main__":
    unittest.main()
