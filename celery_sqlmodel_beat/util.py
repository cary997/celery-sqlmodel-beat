from datetime import datetime
from zoneinfo import ZoneInfo

NEVER_CHECK_TIMEOUT = 9999999999


def nowfun() -> datetime:
    return datetime.now(tz=ZoneInfo("UTC"))


def make_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=ZoneInfo("UTC"))
    else:
        return value.astimezone(ZoneInfo("UTC"))
