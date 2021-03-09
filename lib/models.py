from datetime import datetime
from typing_extensions import TypedDict
from typing import List, Optional
import iso8601
import random
import string
import pytz


def date(date_time: str or float or int) -> datetime:
    """Parses a date string into a datetime object."""
    if isinstance(date_time, float) or isinstance(date_time, int):
        return datetime.fromtimestamp(max(date_time, 100000)).astimezone(pytz.utc)
    else:
        return iso8601.parse_date(date_time)


def format_date(date: datetime) -> str:
    """Converts date to format compatible with JS"""
    return date.astimezone(pytz.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def random_id(length: int = 32) -> str:
    """Generates a random id of 32 symbols."""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class ValidationDetails(TypedDict):
    """Object to supply additional information for validation exceptions."""
    parameter: str
    """Name of invalid parameter."""
    value: Optional[str]
    """Entered invalid value."""
    message: str
    """Error message."""


class ExceptionMessage(TypedDict):
    """A REST API response that contains an exception message"""
    id: int
    """Error id"""
    error: str
    """Error name"""
    numericCode: Optional[int]
    """Numeric error code"""
    stringCode: Optional[str]
    """String error code"""
    message: str
    """Human-readable error message"""
    details: Optional[List[ValidationDetails]]
    """Additional information about error. Used to supply validation error details."""
