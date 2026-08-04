# Report generation service.

import logging
import time
from typing import Any

from shared.http_client import get

logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_SECONDS = 1.0


def fetch_with_retry(
    url: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
    **kwargs: Any,
) -> dict[str, Any]:
    """GET a URL via the shared HTTP client, retrying transient failures with backoff."""
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            response = get(url, **kwargs)
            return response.json()
        except Exception as exc:
            last_error = exc
            logger.warning("Attempt %d/%d failed for %s: %s", attempt, max_retries, url, exc)
            if attempt < max_retries:
                time.sleep(backoff_seconds * attempt)

    assert last_error is not None
    raise last_error
