import datetime

from fastapi import HTTPException, status


def add_timezone_to_datetime(dt: datetime.datetime) -> datetime.datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.UTC)
    return dt

def parse_date_or_error(date_str: str) -> datetime.datetime:
    try:
        dt = datetime.datetime.fromisoformat(date_str)
        return add_timezone_to_datetime(dt)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {date_str}. Expected ISO format.",
        )
