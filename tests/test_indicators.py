import unittest

from agent.processor.indicators import summarize_sectors


class SectorSummaryTests(unittest.TestCase):
    def test_tracks_leader_and_laggard(self) -> None:
        rows = [
            {"symbol": "A", "category": "space", "change_pct": 2.0, "status": "fresh"},
            {"symbol": "B", "category": "space", "change_pct": -1.0, "status": "fresh"},
        ]
        result = summarize_sectors(rows)[0]
        self.assertEqual(result["average_change_pct"], 0.5)
        self.assertEqual(result["leader"], "A")
        self.assertEqual(result["laggard"], "B")
        self.assertEqual(result["advancing"], 1)
        self.assertEqual(result["declining"], 1)


if __name__ == "__main__":
    unittest.main()
