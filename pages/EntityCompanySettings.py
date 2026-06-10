from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional


class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    UNPAID = "unpaid"
    FAMILY_RESPONSIBILITY = "family_responsibility"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    STUDY = "study"
    OTHER = "other"


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@dataclass
class LeaveRequest:
    # Required fields
    employee_id: str
    start_date: date
    end_date: date

    # Optional fields with defaults
    leave_type: LeaveType = LeaveType.ANNUAL
    employee_name: Optional[str] = None
    total_days: float = 0
    reason: Optional[str] = None

    status: LeaveStatus = LeaveStatus.PENDING

    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None

    supporting_document: Optional[str] = None
