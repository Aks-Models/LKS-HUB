"""
HTTP request handler for the LKS HUB Assistant API.
"""

import json
import re
from http.server import BaseHTTPRequestHandler
from typing import Any

from api_config import (
    API_VERSION,
    ASSISTANT_NAME,
    ASSISTANT_VERSION,
    DEVELOPER_MODE,
    MAX_QUESTION_LENGTH,
    MAX_REQUEST_BODY_BYTES,
    SERVICE_NAME,
)
from api_rate_limit import check_rate_limit
from api_responses import send_json
from api_security import (
    get_allowed_cors_origin,
    get_client_ip,
    has_unapproved_origin,
    send_security_headers,
)
from lks_ai import answer


def clean_public_answer(raw_answer: str) -> str:
    """
    Convert an internal assistant response into polished public text.

    Developer-only elements removed from public output include:
        - response banners
        - repeated question labels
        - knowledge-route information
        - verification notes
        - internal separators
        - assistant and API metadata
    """

    if not isinstance(raw_answer, str):
        return str(raw_answer)

    normalized_answer = raw_answer.replace(
        "\r\n",
        "\n",
    ).replace(
        "\r",
        "\n",
    )

    lines = normalized_answer.split("\n")
    public_lines: list[str] = []

    verification_section_started = False

    for original_line in lines:
        stripped_line = original_line.strip()

        if stripped_line.upper() == "VERIFICATION NOTE":
            verification_section_started = True
            continue

        if verification_section_started:
            continue

        if not stripped_line:
            public_lines.append("")
            continue

        upper_line = stripped_line.upper()

        if upper_line in {
            "LKS HUB AI RESPONSE",
            "LKS-HUB AI RESPONSE",
        }:
            continue

        if stripped_line.startswith("Question:"):
            continue

        if stripped_line.startswith("Knowledge route:"):
            continue

        if stripped_line.startswith("Knowledge Route:"):
            continue

        if re.fullmatch(
            r"[=\-_]{3,}",
            stripped_line,
        ):
            continue

        if re.match(
            r"^(assistant|assistant_version|api_version)\s*:",
            stripped_line,
            flags=re.IGNORECASE,
        ):
            continue

        public_lines.append(
            original_line.rstrip()
        )

    public_answer = "\n".join(public_lines)

    public_answer = re.sub(
        r"\n{3,}",
        "\n\n",
        public_answer,
    )

    public_answer = public_answer.strip()

    if not public_answer:
        return (
            "I could not prepare a complete answer at this time. "
            "Please try again shortly."
        )

    return public_answer


class LKSAssistantHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the LKS HUB Assistant API."""

    server_version = "LKS-HUB"
    sys_version = ""

    def do_OPTIONS(self) -> None:
        """Handle browser CORS preflight requests."""

        allowed_origin = get_allowed_cors_origin(self)

        if allowed_origin is None:
            self.send_response(403)

            self.send_header(
                "Content-Length",
                "0",
            )

            send_security_headers(self)

            self.end_headers()
            return

        self.send_response(204)

        self.send_header(
            "Access-Control-Allow-Origin",
            allowed_origin,
        )

        self.send_header(
            "Vary",
            "Origin",
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS",
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )

        self.send_header(
            "Access-Control-Max-Age",
            "600",
        )

        self.send_header(
            "Content-Length",
            "0",
        )

        send_security_headers(self)

        self.end_headers()

    def do_GET(self) -> None:
        """Handle API information and health-check requests."""

        request_path = self.path.split(
            "?",
            maxsplit=1,
        )[0]

        if request_path == "/health":
            if DEVELOPER_MODE:
                health_payload = {
                    "status": "ok",
                    "service": SERVICE_NAME,
                    "version": API_VERSION,
                    "assistant_version": ASSISTANT_VERSION,
                    "developer_mode": True,
                }
            else:
                health_payload = {
                    "status": "ok",
                    "service": SERVICE_NAME,
                }

            send_json(
                self,
                200,
                health_payload,
            )
            return

        if request_path == "/":
            if DEVELOPER_MODE:
                root_payload = {
                    "service": SERVICE_NAME,
                    "version": API_VERSION,
                    "assistant_version": ASSISTANT_VERSION,
                    "status": "running",
                    "developer_mode": True,
                    "endpoints": {
                        "health": "GET /health",
                        "ask": "POST /ask",
                    },
                }
            else:
                root_payload = {
                    "service": SERVICE_NAME,
                    "status": "running",
                }

            send_json(
                self,
                200,
                root_payload,
            )
            return

        send_json(
            self,
            404,
            {
                "error": "Endpoint not found.",
            },
        )

    def do_POST(self) -> None:
        """Process questions submitted to the assistant."""

        request_path = self.path.split(
            "?",
            maxsplit=1,
        )[0]

        if request_path != "/ask":
            send_json(
                self,
                404,
                {
                    "error": "Endpoint not found.",
                },
            )
            return

        if has_unapproved_origin(self):
            send_json(
                self,
                403,
                {
                    "error": "Origin is not permitted.",
                },
            )
            return

        client_ip = get_client_ip(self)

        request_allowed, retry_after = check_rate_limit(
            client_ip
        )

        if not request_allowed:
            send_json(
                self,
                429,
                {
                    "error": (
                        "Too many questions were submitted. "
                        "Please wait before trying again."
                    ),
                    "retry_after_seconds": retry_after,
                },
                extra_headers={
                    "Retry-After": str(retry_after),
                },
            )
            return

        try:
            content_length = int(
                self.headers.get(
                    "Content-Length",
                    "0",
                )
            )

        except ValueError:
            send_json(
                self,
                400,
                {
                    "error": "Invalid request.",
                },
            )
            return

        if content_length <= 0:
            send_json(
                self,
                400,
                {
                    "error": "Request body is required.",
                },
            )
            return

        if content_length > MAX_REQUEST_BODY_BYTES:
            send_json(
                self,
                413,
                {
                    "error": "Request body is too large.",
                },
            )
            return

        try:
            raw_body = self.rfile.read(content_length)

            request_data = json.loads(
                raw_body.decode("utf-8")
            )

        except UnicodeDecodeError:
            send_json(
                self,
                400,
                {
                    "error": (
                        "Request body must use UTF-8 encoding."
                    ),
                },
            )
            return

        except json.JSONDecodeError:
            send_json(
                self,
                400,
                {
                    "error": (
                        "Request body must contain valid JSON."
                    ),
                },
            )
            return

        if not isinstance(request_data, dict):
            send_json(
                self,
                400,
                {
                    "error": "JSON body must be an object.",
                },
            )
            return

        question_value = request_data.get(
            "question",
            "",
        )

        if not isinstance(question_value, str):
            send_json(
                self,
                400,
                {
                    "error": (
                        "The question field must contain text."
                    ),
                },
            )
            return

        question = question_value.strip()

        if not question:
            send_json(
                self,
                400,
                {
                    "error": "A question is required.",
                },
            )
            return

        if len(question) > MAX_QUESTION_LENGTH:
            send_json(
                self,
                400,
                {
                    "error": (
                        "The question is too long. "
                        f"Maximum length is "
                        f"{MAX_QUESTION_LENGTH} characters."
                    ),
                },
            )
            return

        try:
            internal_answer = answer(question)

        except Exception as error:
            print(
                "Assistant error: "
                f"{type(error).__name__}: {error}"
            )

            send_json(
                self,
                500,
                {
                    "error": (
                        "The assistant is temporarily unavailable. "
                        "Please try again shortly."
                    ),
                },
            )
            return

        if DEVELOPER_MODE:
            response_payload = {
                "question": question,
                "answer": internal_answer,
                "assistant": ASSISTANT_NAME,
                "assistant_version": ASSISTANT_VERSION,
                "api_version": API_VERSION,
                "developer_mode": True,
            }
        else:
            response_payload = {
                "answer": clean_public_answer(
                    internal_answer
                ),
            }

        send_json(
            self,
            200,
            response_payload,
        )

    def log_message(
        self,
        message_format: str,
        *args: Any,
    ) -> None:
        """Write compact request information to the terminal."""

        print(
            f"{get_client_ip(self)} - "
            f"{message_format % args}"
        )