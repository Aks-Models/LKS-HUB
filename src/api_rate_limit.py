"""
In-memory request rate limiting for the LKS HUB Assistant API.
"""

import threading
import time
from collections import deque

from api_config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)


_RATE_LIMIT_LOCK = threading.Lock()
_RATE_LIMIT_RECORDS: dict[str, deque[float]] = {}


def check_rate_limit(client_ip: str) -> tuple[bool, int]:
    """
    Check whether a client may submit another assistant request.

    Returns:
        A tuple containing:
        - True and 0 when the request is allowed.
        - False and the retry delay when the request is blocked.
    """

    current_time = time.monotonic()
    cutoff_time = current_time - RATE_LIMIT_WINDOW_SECONDS

    with _RATE_LIMIT_LOCK:
        request_times = _RATE_LIMIT_RECORDS.setdefault(
            client_ip,
            deque(),
        )

        while request_times and request_times[0] <= cutoff_time:
            request_times.popleft()

        if len(request_times) >= RATE_LIMIT_REQUESTS:
            oldest_request = request_times[0]

            retry_after = int(
                RATE_LIMIT_WINDOW_SECONDS
                - (current_time - oldest_request)
            )

            retry_after = max(retry_after, 1)

            return False, retry_after

        request_times.append(current_time)

    return True, 0