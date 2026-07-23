import base64
import hashlib
import hmac
import unittest

from notification.feishu.client import _signature


class FeishuSignatureTests(unittest.TestCase):
    def test_matches_documented_algorithm(self) -> None:
        timestamp = "1700000000"
        secret = "test-secret"
        expected = base64.b64encode(hmac.new(f"{timestamp}\n{secret}".encode(), digestmod=hashlib.sha256).digest()).decode()
        self.assertEqual(_signature(timestamp, secret), expected)


if __name__ == "__main__":
    unittest.main()
