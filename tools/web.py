from typing import Optional

import requests


def fetch_url(url: str, timeout_seconds: int = 10) -> str:
    """Fetch text content from a URL with a short timeout.

    Returns response text on 2xx, otherwise a brief error message.
    """
    try:
        resp = requests.get(url, timeout=timeout_seconds)
        if 200 <= resp.status_code < 300:
            # Truncate to avoid overwhelming the context
            text = resp.text
            if len(text) > 8000:
                text = text[:8000] + "\n...[truncated]"
            return text
        return f"HTTP {resp.status_code}: {resp.text[:500]}"
    except Exception as exc:  # noqa: BLE001
        return f"Request error: {exc}"


