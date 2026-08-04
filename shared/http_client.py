# Shared HTTP client wrapper.
# CLAUDE.md requires all external HTTP calls to go through this wrapper instead
# of calling requests/httpx directly, so timeouts are always enforced.

import os
from typing import Any

import requests

DEFAULT_TIMEOUT_SECONDS = 5

# Corporate proxies that perform TLS inspection re-sign traffic with their own
# CA. Point this at that CA bundle instead of disabling verification.
CA_BUNDLE_ENV_VAR = "CORPORATE_CA_BUNDLE"


def _verify_target() -> bool | str:
    ca_bundle = os.environ.get(CA_BUNDLE_ENV_VAR)
    return ca_bundle if ca_bundle else True


def get(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS, **kwargs: Any) -> requests.Response:
    """GET request with an enforced timeout. Raises for non-2xx responses."""
    kwargs.setdefault("verify", _verify_target())
    response = requests.get(url, timeout=timeout, **kwargs)
    response.raise_for_status()
    return response


def post(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS, **kwargs: Any) -> requests.Response:
    """POST request with an enforced timeout. Raises for non-2xx responses."""
    kwargs.setdefault("verify", _verify_target())
    response = requests.post(url, timeout=timeout, **kwargs)
    response.raise_for_status()
    return response