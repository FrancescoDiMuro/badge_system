from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def now_with_timezone(tz: str = 'Europe/Rome'):
    return datetime.now(timezone(tz)).strftime('%Y-%m-%d %H:%M:%S%z')