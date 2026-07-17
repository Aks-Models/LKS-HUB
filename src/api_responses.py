"""
JSON response utilities for the LKS HUB Assistant API.
"""

import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from api_security import (
    send_cors_headers,
    send_security_headers,
)


def build_json_response(
    payload: dict[str, Any],
) -> bytes:
    """Convert a dictionary into UTF-8 encoded JSON."""

    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")


def send_json(
    handler: BaseHTTPRequestHandler,
    status_code: int,
    payload: dict[str, Any],
    extra_headers: dict[str, str] | None = None,
) -> None:
    """Send a JSON response with security and CORS headers."""

    response_body = build_json_response(payload)

    handler.send_response(status_code)

    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8",
    )

    handler.send_header(
        "Content-Length",
        str(len(response_body)),
    )

    send_security_headers(handler)

    if extra_headers:
        for header_name, header_value in extra_headers.items():
            handler.send_header(
                header_name,
                header_value,
            )

    send_cors_headers(handler)

    handler.end_headers()
    handler.wfile.write(response_body)