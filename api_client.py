"""HTTP wrapper for Poliscope API requests."""

from __future__ import annotations

import time
from typing import Any

import requests


class ApiRateLimitError(RuntimeError):
    """Raised when the API keeps responding with rate-limit errors."""


ERROR_MESSAGES = {
    400: "Ungültige Parameter oder Validierungsfehler",
    401: "API-Schlüssel fehlt oder ist ungültig",
    403: "Schlüssel hat keinen Zugriff auf die angefragte Ressource",
    404: "Ressource nicht gefunden",
    409: "Ressource ist nicht in einem Zustand für diesen Request (z. B. OCR noch nicht fertig)",
    429: "Rate-Limit überschritten — siehe https://docs.poliscope.de/api/rate-limits",
    500: "Interner Fehler",
}


def _parse_positive_float(value: str | None) -> float:
    if not value:
        return 0.0

    try:
        return max(float(value), 0.0)
    except (TypeError, ValueError):
        return 0.0


def _get_wait_time(response: requests.Response) -> float:
    retry_after = _parse_positive_float(response.headers.get("Retry-After"))
    if retry_after > 0:
        return retry_after

    rate_limit_reset = _parse_positive_float(response.headers.get("x-ratelimit-reset"))
    if rate_limit_reset > 0:
        return rate_limit_reset

    return 1.0


def _get_setup_defaults() -> tuple[str | None, dict[str, str] | None]:
    try:
        from setup import poliscope_api_url, poliscope_headers  # type: ignore
    except Exception:
        return None, None

    return poliscope_api_url, poliscope_headers


def _resolve_request_target(
    url: str,
    headers: dict[str, str] | None,
) -> tuple[str, dict[str, str] | None]:
    setup_url, setup_headers = _get_setup_defaults()

    if headers is None and setup_headers is not None:
        headers = dict(setup_headers)

    if not url:
        if setup_url:
            return setup_url, headers
        raise ValueError("No API URL configured")

    if setup_url and not url.startswith(("http://", "https://")):
        base = setup_url.rstrip("/")
        path = url.lstrip("/")
        return f"{base}/{path}", headers

    return url, headers


def poliscope_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    max_retries: int = 5,
    sleep_after_request: float = 0.1,
    timeout: float = 10.0,
    require_success: bool = True,
    **kwargs: Any,
) -> requests.Response:
    """Send a request and honor API rate-limit headers.

    The wrapper sleeps for the value from the Retry-After header when the API
    responds with HTTP 429. It also waits a short period after each successful
    request to reduce burst traffic.
    """

    resolved_url, request_headers = _resolve_request_target(url, headers)
    request_headers = dict(request_headers or {})
    request_params = dict(params or {})

    for attempt in range(max_retries + 1):
        response = requests.request(
            method=method,
            url=resolved_url,
            headers=request_headers,
            params=request_params,
            timeout=timeout,
            **kwargs,
        )

        if response.status_code == 429:
            if attempt >= max_retries:
                raise ApiRateLimitError(
                    f"Rate limit exceeded after {max_retries} retries: {response.status_code}"
                )

            wait_time = _get_wait_time(response)
            time.sleep(wait_time)
            continue

        if sleep_after_request > 0:
            time.sleep(sleep_after_request)

        if require_success and not 200 <= response.status_code < 300:
            message = ERROR_MESSAGES.get(response.status_code, f"Unbekannter Fehler ({response.status_code})")
            raise RuntimeError(
                f"API request failed with status {response.status_code}: {message}"
            )

        return response

    raise ApiRateLimitError("Unexpected end of retry loop")


def get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    **kwargs: Any,
) -> Any:
    response = poliscope_request("GET", url, headers=headers, params=params, **kwargs)
    response.raise_for_status()
    return response.json()
