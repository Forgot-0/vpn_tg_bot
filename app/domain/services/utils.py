from datetime import UTC, datetime


def now_utc() -> datetime:
    return datetime.now(UTC)

def replace(date: datetime) -> datetime:
    return date.replace(tzinfo=UTC)
 
def fromtimestamp(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, UTC)