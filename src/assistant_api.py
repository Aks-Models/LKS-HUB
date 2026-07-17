"""
LKS HUB Assistant API v2

Production-ready HTTP API for the LKS HUB AI Assistant.

Endpoints:
    GET  /
    GET  /health
    POST /ask

Local command:
    python src/assistant_api.py

Production behavior:
    The server listens on 0.0.0.0.
    The port is read from the PORT environment variable when available.
"""

import sys
from http.server import ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api_config import (  # noqa: E402
    API_VERSION,
    ASSISTANT_VERSION,
    HOST,
    PORT,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from api_handler import LKSAssistantHandler  # noqa: E402


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
    print(
        f"Health check      : "
        f"http://127.0.0.1:{PORT}/health"
    )
    print("Question endpoint : POST /ask")
    print(
        "Rate limit        : "
        f"{RATE_LIMIT_REQUESTS} questions per "
        f"{RATE_LIMIT_WINDOW_SECONDS // 60} minutes"
    )
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