import unittest
from unittest.mock import patch

from api_client import ApiRateLimitError, poliscop_request


class FakeResponse:
    def __init__(self, status_code, headers=None, json_data=None):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data or {}

    def json(self):
        return self._json_data


class PoliscopRequestTests(unittest.TestCase):
    @patch("api_client.requests.request")
    @patch("api_client.time.sleep")
    def test_retries_after_retry_after_header(self, sleep_mock, request_mock):
        request_mock.side_effect = [
            FakeResponse(429, {"Retry-After": "0.2"}),
            FakeResponse(200, {}),
        ]

        response = poliscop_request(
            "GET",
            "https://example.test/api",
            headers={},
            max_retries=2,
            sleep_after_request=0.0,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request_mock.call_count, 2)
        sleep_mock.assert_any_call(0.2)

    @patch("api_client.requests.request")
    @patch("api_client.time.sleep")
    def test_uses_x_ratelimit_reset_when_retry_after_is_missing(self, sleep_mock, request_mock):
        request_mock.side_effect = [
            FakeResponse(429, {"x-ratelimit-reset": "1.5"}),
            FakeResponse(200, {}),
        ]

        response = poliscop_request(
            "GET",
            "https://example.test/api",
            headers={},
            max_retries=2,
            sleep_after_request=0.0,
        )

        self.assertEqual(response.status_code, 200)
        sleep_mock.assert_any_call(1.5)

    @patch("api_client.requests.request")
    @patch("api_client.time.sleep")
    def test_raises_after_exhausting_retries(self, sleep_mock, request_mock):
        request_mock.return_value = FakeResponse(429, {"Retry-After": "0.1"})

        with self.assertRaises(ApiRateLimitError):
            poliscop_request(
                "GET",
                "https://example.test/api",
                headers={},
                max_retries=1,
                sleep_after_request=0.0,
            )

        self.assertEqual(request_mock.call_count, 2)
        self.assertGreaterEqual(sleep_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main()
