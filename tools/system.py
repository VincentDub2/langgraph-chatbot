from datetime import datetime, timezone


def get_current_time() -> str:
    """Return current time in ISO 8601 UTC."""
    return datetime.now(timezone.utc).isoformat()


