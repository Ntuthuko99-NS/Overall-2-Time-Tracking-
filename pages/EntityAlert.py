from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class AlertType(str, Enum):
    SHIFT_REMINDER = "shift_reminder"
    LATE_ARRIVAL = "late_arrival"
    MISSED_SHIFT = "missed_shift"
    OVERTIME_WARNING = "overtime_warning"
    FORGOT_CLOCK_OUT = "forgot_clock_out"
    LOCATION_WARNING = "location_warning"


class AlertStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    DISMISSED = "dismissed"


class AlertPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AlertChannel(str, Enum):
    APP = "app"
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class TargetAudience(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"
    ALL = "all"


@dataclass
class Alert:
    # Required fields
    type: AlertType
    message: str

    # Optional fields
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None

    shift_id: Optional[str] = None
    shift_name: Optional[str] = None

    status: AlertStatus = AlertStatus.PENDING
    priority: AlertPriority = AlertPriority.MEDIUM

    sent_via: List[AlertChannel] = field(default_factory=list)

    scheduled_time: Optional[datetime] = None
    sent_at: Optional[datetime] = None

    target_audience: TargetAudience = TargetAudience.EMPLOYEE
