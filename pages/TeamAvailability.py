import streamlit as st
from datetime import datetime


def get_employee_status(employee, leave_requests):
    """
    Determine employee status:
    - on_leave
    - working
    - not_clocked_in
    """

    today = datetime.now().date()

    # Check approved leave
    for leave in leave_requests:
        if (
            leave["status"] == "approved"
            and leave["employee_id"] == employee["employee_id"]
        ):
            start = datetime.fromisoformat(
                leave["start_date"]
            ).date()

            end = datetime.fromisoformat(
                leave["end_date"]
            ).date()

            if start <= today <= end:
                return {
                    "status": "on_leave",
                    "leave_type": leave["leave_type"],
                }

    # Check attendance
    if employee.get("is_clocked_in"):
        return {"status": "working"}

    return {"status": "not_clocked_in"}


def render_team_availability(
    employees,
    leave_requests,
    time_entries=None,
):
    """
    Team Availability Widget
    """

    active_employees = [
        e for e in employees
        if e.get("is_active", True)
    ]

    working_count = sum(
        1
        for e in active_employees
        if get_employee_status(
            e,
            leave_requests
        )["status"]
        == "working"
    )

    on_leave_count = sum(
        1
        for e in active_employees
        if get_employee_status(
            e,
            leave_requests
        )["status"]
        == "on_leave"
    )

    st.subheader("👥 Team Availability")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"{working_count} Working")

    with col2:
        st.warning(f"{on_leave_count} On Leave")

    st.divider()

    if not active_employees:
        st.info("No active employees found.")
        return

    for employee in active_employees:

        status_info = get_employee_status(
            employee,
            leave_requests
        )

        status = status_info["status"]

        if status == "working":
            badge = "🟢 Working"

        elif status == "on_leave":

            leave_type = (
                status_info.get(
                    "leave_type",
                    "Leave"
                )
                .replace("_", " ")
                .title()
            )

            badge = f"🟡 {leave_type}"

        else:
            badge = "⚪ Not Clocked In"

        initials = "".join(
            [
                name[0]
                for name in employee.get(
                    "full_name",
                    ""
                ).split()
            ]
        )[:2].upper()

        position = (
            employee.get("position")
            or employee.get("department")
            or "Employee"
        )

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:
                st.markdown(
                    f"""
                    **{employee['full_name']}**  
                    {position}  
                    *({initials})*
                    """
                )

            with col2:
                st.write(badge)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

employees = [
    {
        "id": 1,
        "employee_id": 1001,
        "full_name": "John Smith",
        "position": "Security Officer",
        "is_active": True,
        "is_clocked_in": True,
    },
    {
        "id": 2,
        "employee_id": 1002,
        "full_name": "Sarah Jones",
        "department": "Operations",
        "is_active": True,
        "is_clocked_in": False,
    },
]

leave_requests = [
    {
        "employee_id": 1002,
        "status": "approved",
        "start_date": "2026-06-01",
        "end_date": "2026-06-15",
        "leave_type": "annual_leave",
    }
]

render_team_availability(
    employees,
    leave_requests
)
