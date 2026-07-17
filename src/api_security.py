"""
Security and CORS utilities for the LKS HUB Assistant API.
"""

from http.server import BaseHTTPRequestHandler

from api_config import ALLOWED_CORS_ORIGINS


def get_client_ip(handler: BaseHTTPRequestHandler) -> str:
    """
    Return the best available client IP address.

    Render supplies the original client address through X-Forwarded-For.
    """

    forwarded_for = handler.headers.get(
        "X-Forwarded-For",
        "",
    )

    if forwarded_for:
        first_forwarded_ip = forwarded_for.split(
            ",",
            maxsplit=1,
        )[0].strip()

        if first_forwarded_ip:
            return first_forwarded_ip

    return handler.client_address[0]


def get_allowed_cors_origin(
    handler: BaseHTTPRequestHandler,
) -> str | None:
    """Return the request origin when it is approved."""

    request_origin = handler.headers.get("Origin")

    if request_origin in ALLOWED_CORS_ORIGINS:
        return request_origin

    return None


def has_unapproved_origin(
    handler: BaseHTTPRequestHandler,
) -> bool:
    """
    Check whether a browser explicitly supplied an unapproved origin.

    Requests without an Origin header are not automatically rejected because
    command-line and server-to-server clients normally omit that header.
    """

    request_origin = handler.headers.get("Origin")

    return bool(
        request_origin
        and request_origin not in ALLOWED_CORS_ORIGINS
    )


def send_security_headers(
    handler: BaseHTTPRequestHandler,
) -> None:
    """Send common security headers."""

    handler.send_header(
        "Cache-Control",
        "no-store",
    )

    handler.send_header(
        "X-Content-Type-Options",
        "nosniff",
    )

    handler.send_header(
        "X-Frame-Options",
        "DENY",
    )

    handler.send_header(
        "Referrer-Policy",
        "no-referrer",
    )

    handler.send_header(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )

    handler.send_header(
        "X-XSS-Protection",
        "0",
    )


def send_cors_headers(
    handler: BaseHTTPRequestHandler,
) -> None:
    """Send CORS response headers for an approved browser origin."""

    allowed_origin = get_allowed_cors_origin(handler)

    if allowed_origin is None:
        return

    handler.send_header(
        "Access-Control-Allow-Origin",
        allowed_origin,
    )

    handler.send_header(
        "Vary",
        "Origin",
    )

    handler.send_header(
        "Access-Control-Allow-Methods",
        "GET, POST, OPTIONS",
    )

    handler.send_header(
        "Access-Control-Allow-Headers",
        "Content-Type",
    )