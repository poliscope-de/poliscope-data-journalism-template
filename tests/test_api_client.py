import unittest
from unittest.mock import patch

from api_client import ApiRateLimitError, poliscope_request


class FakeResponse:
    def __init__(self, status_code, headers=None, json_data=None):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data or {}

    def json(self):
        return self._json_data


@patch("api_client.time.sleep")
@patch("api_client.requests.request")
class PoliscopeRequestTests(unittest.TestCase):
    def test_retries_after_retry_after_header(self, request_mock, sleep_mock):
        request_mock.side_effect = [FakeResponse(429, {"Retry-After": "0.2"}), FakeResponse(200)]

        response = poliscope_request("GET", "https://example.test/api", headers={}, max_retries=2, sleep_after_request=0.0)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request_mock.call_count, 2)
        sleep_mock.assert_any_call(0.2)

    def test_uses_x_ratelimit_reset_when_retry_after_is_missing(self, request_mock, sleep_mock):
        request_mock.side_effect = [FakeResponse(429, {"x-ratelimit-reset": "1.5"}), FakeResponse(200)]

        response = poliscope_request("GET", "https://example.test/api", headers={}, max_retries=2, sleep_after_request=0.0)

        self.assertEqual(response.status_code, 200)
        sleep_mock.assert_any_call(1.5)

    def test_raises_after_exhausting_retries(self, request_mock, sleep_mock):
        request_mock.return_value = FakeResponse(429, {"Retry-After": "0.1"})

        with self.assertRaises(ApiRateLimitError):
            poliscope_request("GET", "https://example.test/api", headers={}, max_retries=1, sleep_after_request=0.0)

        self.assertEqual(request_mock.call_count, 2)

    def test_raises_readable_error_on_http_error(self, request_mock, sleep_mock):
        request_mock.return_value = FakeResponse(401)

        with self.assertRaisesRegex(RuntimeError, "401"):
            poliscope_request("GET", "https://example.test/api", headers={}, sleep_after_request=0.0)

    def test_relative_path_is_joined_with_base_url(self, request_mock, sleep_mock):
        request_mock.return_value = FakeResponse(200)

        with patch("api_client._get_setup_defaults", return_value=("https://api.test/v2/", {"Authorization": "Bearer x"})):
            poliscope_request("GET", "/entities", sleep_after_request=0.0)

        self.assertEqual(request_mock.call_args.kwargs["url"], "https://api.test/v2/entities")
        self.assertEqual(request_mock.call_args.kwargs["headers"], {"Authorization": "Bearer x"})


if __name__ == "__main__":
    unittest.main()
