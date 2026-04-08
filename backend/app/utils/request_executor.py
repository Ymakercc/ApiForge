from dataclasses import dataclass
from time import perf_counter
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


DEFAULT_TIMEOUT = 30
ERROR_MESSAGE_MAX_LENGTH = 512


@dataclass
class RequestExecutionResult:
    success: bool
    status_code: int | None
    duration_ms: int
    data: Any | None
    error_message: str | None
    request_url: str
    request_headers: dict[str, Any] | None
    request_body: Any | None
    response_body: str | None


def _truncate_error_message(message: str | None) -> str | None:
    if not message:
        return None

    return message[:ERROR_MESSAGE_MAX_LENGTH]


def _parse_response_data(response: requests.Response) -> Any | None:
    if not response.content:
        return None

    content_type = response.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        try:
            return response.json()
        except ValueError:
            return response.text

    return response.text


def _build_error_message(response: requests.Response) -> str | None:
    if response.ok:
        return None

    parts = [f"HTTP {response.status_code}"]
    if response.reason:
        parts.append(response.reason)

    return _truncate_error_message(" ".join(parts))


def _merge_auth_config(
    headers: dict[str, Any] | None,
    params: dict[str, Any] | None,
    auth_type: str | None,
    auth_config: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, HTTPBasicAuth | None]:
    merged_headers = dict(headers or {}) or None
    merged_params = dict(params or {}) or None
    basic_auth = None
    config = auth_config or {}

    if auth_type == "bearer":
        token = config.get("token") or config.get("access_token")
        if token:
            merged_headers = merged_headers or {}
            merged_headers.setdefault("Authorization", f"Bearer {token}")
    elif auth_type == "basic":
        username = config.get("username") or config.get("user")
        password = config.get("password") or config.get("pass")
        if username is not None and password is not None:
            basic_auth = HTTPBasicAuth(str(username), str(password))
    elif auth_type == "apikey":
        key = config.get("key")
        value = config.get("value")
        location = str(config.get("in") or config.get("location") or "header").lower()
        if key and value is not None:
            if location == "query":
                merged_params = merged_params or {}
                merged_params.setdefault(str(key), value)
            else:
                merged_headers = merged_headers or {}
                merged_headers.setdefault(str(key), value)

    return merged_headers, merged_params, basic_auth


def execute_http_request(
    method: str,
    url: str,
    headers: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any | None = None,
    auth_type: str | None = None,
    auth_config: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> RequestExecutionResult:
    method = method.upper()
    merged_headers, merged_params, basic_auth = _merge_auth_config(
        headers=headers,
        params=params,
        auth_type=auth_type,
        auth_config=auth_config,
    )
    request_body = None if method in {"GET", "HEAD"} else json_body

    session = requests.Session()
    prepared_request = session.prepare_request(
        requests.Request(
            method=method,
            url=url,
            headers=merged_headers,
            params=merged_params,
            json=request_body,
            auth=basic_auth,
        )
    )
    started_at = perf_counter()

    try:
        response = session.send(prepared_request, timeout=timeout)
        duration_ms = int((perf_counter() - started_at) * 1000)
        response_body = response.text

        return RequestExecutionResult(
            success=response.ok,
            status_code=response.status_code,
            duration_ms=duration_ms,
            data=_parse_response_data(response),
            error_message=_build_error_message(response),
            request_url=prepared_request.url,
            request_headers=dict(prepared_request.headers),
            request_body=request_body,
            response_body=response_body,
        )
    except requests.RequestException as exc:
        duration_ms = int((perf_counter() - started_at) * 1000)

        return RequestExecutionResult(
            success=False,
            status_code=None,
            duration_ms=duration_ms,
            data=None,
            error_message=_truncate_error_message(str(exc)),
            request_url=prepared_request.url,
            request_headers=dict(prepared_request.headers),
            request_body=request_body,
            response_body=None,
        )
    finally:
        session.close()
