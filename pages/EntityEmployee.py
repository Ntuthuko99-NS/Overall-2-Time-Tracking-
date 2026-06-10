from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class EmployeeRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


@dataclass
class AllowedLocation:
    name: str
    latitude: float
    longitude: float
    radius_meters: float


@dataclass
class Employee:
    # Required fields
    employee_id: str
    full_name: str
    email: str

    # Optional fields
    phone: Optional[str] = None

    role: EmployeeRole = EmployeeRole.EMPLOYEE

    department: Optional[str] = None
    position: Optional[str] = None

    expected_daily_hours: float = 8

    is_active: bool = True
    is_clocked_in: bool = False

    current_session_id: Optional[str] = None

    allowed_locations: List[AllowedLocation] = field(default_factory=list)

    annual_leave_balance: float = 21
    sick_leave_balance: float = 30

    profile_image: Optional[str] = None
