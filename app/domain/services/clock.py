from datetime import UTC, datetime


def now_utc() -> datetime:
    return datetime.now(UTC)
