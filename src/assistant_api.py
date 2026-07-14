"""
LKS HUB Assistant API v2

Production-ready HTTP API for the LKS AI Assistant.

Endpoints:
    GET  /
    GET  /health
    POST /ask

Local command:
    py src/assistant_api.py

Production behavior:
    The server listens on 0.0.0.0.
    The port is read from the PORT environment variable when available.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lks_ai import answer  # noqa: E402


HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))

API_VERSION = "2.0"
ASSISTANT_VERSION = "v7"

MAX_QUESTION_LENGTH = 2000
MAX_REQUEST_BODY_BYTES = 50_000


def build_json_response(payload: dict[str, Any]) -> bytes:
    """Convert a dictionary into UTF-8 encoded JSON."""

    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")


class LKSAssistantHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the LKS HUB Assistant API."""

    server_version = f"LKSHUBAssistantAPI/{API_VERSION}"

    def send_json(
        self,
        status_code: int,
        payload: dict[str, Any],
    ) -> None:
        """Send a JSON response with development CORS headers."""

        response_body = build_json_response(payload)

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(response_body)),
        )

        # Development-friendly CORS.
        # Before public deployment, restrict this to approved domains.
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
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
            "Cache-Control",
            "no-store",
        )

        self.end_headers()
        self.wfile.write(response_body)

    def do_OPTIONS(self) -> None:
        """Handle browser CORS preflight requests."""

        self.send_response(204)

        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
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
            "Cache-Control",
            "no-store",
        )

        self.end_headers()

    def do_GET(self) -> None:
        """Handle API information and health-check requests."""

        request_path = self.path.split("?", maxsplit=1)[0]

        if request_path == "/health":
            self.send_json(
                200,
                {
                    "status": "ok",
                    "service": "LKS HUB Assistant API",
                    "version": API_VERSION,
                    "assistant_version": ASSISTANT_VERSION,
                },
            )
            return

        if request_path == "/":
            self.send_json(
                200,
                {
                    "service": "LKS HUB Assistant API",
                    "version": API_VERSION,
                    "assistant_version": ASSISTANT_VERSION,
                    "status": "running",
                    "endpoints": {
                        "health": "GET /health",
                        "ask": "POST /ask",
                    },
                },
            )
            return

        self.send_json(
            404,
            {
                "error": "Endpoint not found.",
                "path": request_path,
            },
        )

    def do_POST(self) -> None:
        """Process questions submitted to the assistant."""

        request_path = self.path.split("?", maxsplit=1)[0]

        if request_path != "/ask":
            self.send_json(
                404,
                {
                    "error": "Endpoint not found.",
                    "path": request_path,
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
            self.send_json(
                400,
                {
                    "error": "Invalid Content-Length header.",
                },
            )
            return

        if content_length <= 0:
            self.send_json(
                400,
                {
                    "error": "Request body is required.",
                },
            )
            return

        if content_length > MAX_REQUEST_BODY_BYTES:
            self.send_json(
                413,
                {
                    "error": (
                        "Request body is too large. "
                        f"Maximum size is {MAX_REQUEST_BODY_BYTES} bytes."
                    ),
                },
            )
            return

        try:
            raw_body = self.rfile.read(content_length)

            request_data = json.loads(
                raw_body.decode("utf-8")
            )

        except UnicodeDecodeError:
            self.send_json(
                400,
                {
                    "error": "Request body must use UTF-8 encoding.",
                },
            )
            return

        except json.JSONDecodeError:
            self.send_json(
                400,
                {
                    "error": "Request body must contain valid JSON.",
                },
            )
            return

        if not isinstance(request_data, dict):
            self.send_json(
                400,
                {
                    "error": "JSON body must be an object.",
                },
            )
            return

        question_value = request_data.get("question", "")

        if not isinstance(question_value, str):
            self.send_json(
                400,
                {
                    "error": "The 'question' field must be text.",
                },
            )
            return

        question = question_value.strip()

        if not question:
            self.send_json(
                400,
                {
                    "error": "The 'question' field is required.",
                },
            )
            return

        if len(question) > MAX_QUESTION_LENGTH:
            self.send_json(
                400,
                {
                    "error": (
                        "Question is too long. "
                        f"Maximum length is "
                        f"{MAX_QUESTION_LENGTH} characters."
                    ),
                },
            )
            return

        try:
            assistant_answer = answer(question)

        except Exception as error:
            print(
                "Assistant error: "
                f"{type(error).__name__}: {error}"
            )

            self.send_json(
                500,
                {
                    "error": (
                        "The assistant could not process the question."
                    ),
                },
            )
            return

        self.send_json(
            200,
            {
                "question": question,
                "answer": assistant_answer,
                "assistant": "LKS HUB AI",
                "assistant_version": ASSISTANT_VERSION,
                "api_version": API_VERSION,
            },
        )

    def log_message(
        self,
        message_format: str,
        *args: Any,
    ) -> None:
        """Write compact request information to the terminal."""

        print(
            f"{self.client_address[0]} - "
            f"{message_format % args}"
        )


def main() -> None:
    """Start the LKS HUB Assistant API server."""

    try:
        server = ThreadingHTTPServer(
            (HOST, PORT),
            LKSAssistantHandler,
        )

    except OSError as error:
        print("=" * 70)
        print("LKS HUB ASSISTANT API COULD NOT START")
        print("=" * 70)
        print(f"Host  : {HOST}")
        print(f"Port  : {PORT}")
        print(f"Error : {error}")
        print("")
        print(
            "Another process may already be using this port."
        )
        return

    print("=" * 70)
    print("LKS HUB ASSISTANT API")
    print("=" * 70)
    print(f"API version       : {API_VERSION}")
    print(f"Assistant version : {ASSISTANT_VERSION}")
    print(f"Host              : {HOST}")
    print(f"Port              : {PORT}")
    print(f"Local server      : http://127.0.0.1:{PORT}")
    print(f"Health check      : http://127.0.0.1:{PORT}/health")
    print("Question endpoint : POST /ask")
    print("Press Ctrl+C to stop.")
    print("=" * 70)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping LKS HUB Assistant API...")

    finally:
        server.server_close()
        print("API stopped.")


if __name__ == "__main__":
    main()