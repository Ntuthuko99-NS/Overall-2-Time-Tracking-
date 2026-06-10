from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional


class ClockInMethod(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    MANUAL = "manual"


class TimeEntryStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    AUTO_CLOSED = "auto_closed"
    CORRECTED = "corrected"


@dataclass
class Location:
    latitude: float
    longitude: float
    address: Optional[str] = None


@dataclass
class TimeEntry:
    # Required fields
    employee_id: str
    clock_in_time: datetime
    date: date

    # Optional fields
    employee_name: Optional[str] = None

    clock_out_time: Optional[datetime] = None

    clock_in_location: Optional[Location] = None
    clock_out_location: Optional[Location] = None

    clock_in_method: ClockInMethod = ClockInMethod.WEB

    status: TimeEntryStatus = TimeEntryStatus.ACTIVE

    total_hours: float = 0.0
    overtime_hours: float = 0.0

    notes: Optional[str] = None

    is_late: bool = False

    shift_id: Optional[str] = None
