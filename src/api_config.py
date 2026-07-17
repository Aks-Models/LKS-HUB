"""
Configuration for the LKS HUB Assistant API.
"""

import os


HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))

API_VERSION = "2.0"
ASSISTANT_VERSION = "v7"

SERVICE_NAME = "LKS HUB Assistant API"
ASSISTANT_NAME = "LKS HUB AI"

MAX_QUESTION_LENGTH = 2000
MAX_REQUEST_BODY_BYTES = 50_000

RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 300

ALLOWED_CORS_ORIGINS = {
    "https://lks.wh.sk",
    "https://www.lks.wh.sk",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
}


def read_boolean_environment_variable(
    variable_name: str,
    default: bool = False,
) -> bool:
    """
    Read a boolean environment variable safely.

    Accepted true values:
        1
        true
        yes
        on

    Accepted false values:
        0
        false
        no
        off
    """

    raw_value = os.environ.get(variable_name)

    if raw_value is None:
        return default

    normalized_value = raw_value.strip().lower()

    if normalized_value in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if normalized_value in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    return default


DEVELOPER_MODE = read_boolean_environment_variable(
    "LKS_DEVELOPER_MODE",
    default=False,
)