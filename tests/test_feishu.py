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

    def test_signature_accepts_normalized_integer_timestamp(self) -> None:
        self.assertEqual(_signature(str(1_700_000_000), "secret-value"), _signature("1700000000", "secret-value"))


if __name__ == "__main__":
    unittest.main()
