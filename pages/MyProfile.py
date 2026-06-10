import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def my_profile_page(
    current_user,
    employees,
    time_entries,
    leave_requests
):
    """
    My Profile Page
    """

    # Find employee profile
    current_employee = next(
        (
            emp
            for emp in employees
            if emp["email"] == current_user["email"]
        ),
        None
    )

    if not current_employee:
        st.error(
            "Profile not found. Contact administrator."
        )
        return

    # Employee records
    my_entries = [
        e for e in time_entries
        if e["employee_id"]
        == current_employee["employee_id"]
    ]

    my_leave = [
        r for r in leave_requests
        if r["employee_id"]
        == current_employee["employee_id"]
    ]

    # Date calculations
    today = datetime.today().date()

    week_start = today - timedelta(
        days=today.weekday()
    )

    week_end = week_start + timedelta(days=6)

    month_start = today.replace(day=1)

    # Weekly entries
    weekly_entries = []

    for entry in my_entries:

        entry_date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        ).date()

        if week_start <= entry_date <= week_end:
            weekly_entries.append(entry)

    # Monthly entries
    monthly_entries = []

    for entry in my_entries:

        entry_date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        ).date()

        if (
            entry_date.month == today.month
            and entry_date.year == today.year
        ):
            monthly_entries.append(entry)

    # Stats
    weekly_hours = sum(
        e.get("total_hours", 0)
        for e in weekly_entries
    )

    monthly_hours = sum(
        e.get("total_hours", 0)
        for e in monthly_entries
    )

    monthly_overtime = sum(
        e.get("overtime_hours", 0)
        for e in monthly_entries
    )

    expected_weekly_hours = (
        current_employee.get(
            "expected_daily_hours",
            8
        ) * 5
    )

    # Leave calculations
    approved_leave = [
        r for r in my_leave
        if r.get("status") == "approved"
    ]

    used_annual = sum(
        r.get("total_days", 0)
        for r in approved_leave
        if r.get("leave_type") == "annual"
    )

    used_sick = sum(
        r.get("total_days", 0)
        for r in approved_leave
        if r.get("leave_type") == "sick"
    )

    pending_leave = len([
        r for r in my_leave
        if r.get("status") == "pending"
    ])

    # --------------------------------------------------
    # PROFILE HEADER
    # --------------------------------------------------

    st.title("👤 My Profile")

    col1, col2 = st.columns([1, 5])

    with col1:

        initials = "".join(
            [
                n[0]
                for n in current_employee[
                    "full_name"
                ].split()
            ]
        )[:2]

        st.markdown(
            f"""
            <div style="
                width:80px;
                height:80px;
                border-radius:50%;
                background:#2563eb;
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:28px;
                font-weight:bold;">
                {initials}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.subheader(
            current_employee["full_name"]
        )

        st.write(
            current_employee.get(
                "department",
                "N/A"
            )
        )

        if current_employee.get(
            "is_clocked_in",
            False
        ):
            st.success("Currently Working")

    st.divider()

    # Employee Info
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.caption("Email")
        st.write(
            current_employee.get(
                "email",
                "-"
            )
        )

    with c2:
        st.caption("Phone")
        st.write(
            current_employee.get(
                "phone",
                "-"
            )
        )

    with c3:
        st.caption("Department")
        st.write(
            current_employee.get(
                "department",
                "-"
            )
        )

    with c4:
        st.caption("Employee ID")
        st.write(
            current_employee.get(
                "employee_id",
                "-"
            )
        )

    st.divider()

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    left, right = st.columns([1, 2])

    # LEFT COLUMN
    with left:

        st.subheader("⏰ Clock Status")

        if current_employee.get(
            "is_clocked_in"
        ):
            st.success("Clocked In")
        else:
            st.warning("Clocked Out")

        st.subheader("📈 Weekly Progress")

        progress = min(
            weekly_hours /
            expected_weekly_hours,
            1
        )

        st.progress(progress)

        st.write(
            f"{weekly_hours:.1f} / "
            f"{expected_weekly_hours} hrs"
        )

        st.subheader("🏖 Leave Balance")

        annual_remaining = (
            current_employee.get(
                "annual_leave_balance",
                21
            ) - used_annual
        )

        sick_remaining = (
            current_employee.get(
                "sick_leave_balance",
                30
            ) - used_sick
        )

        st.metric(
            "Annual Leave",
            f"{annual_remaining} days"
        )

        st.metric(
            "Sick Leave",
            f"{sick_remaining} days"
        )

        st.metric(
            "Pending Requests",
            pending_leave
        )

    # RIGHT COLUMN
    with right:

        st.subheader("📊 Statistics")

        a, b, c, d = st.columns(4)

        a.metric(
            "Week",
            f"{weekly_hours:.1f}h"
        )

        b.metric(
            "Month",
            f"{monthly_hours:.1f}h"
        )

        c.metric(
            "Overtime",
            f"{monthly_overtime:.1f}h"
        )

        d.metric(
            "Days Worked",
            len(monthly_entries)
        )

        st.divider()

        tab1, tab2 = st.tabs(
            ["Week", "Month"]
        )

        with tab1:

            st.subheader(
                "Weekly Timesheet"
            )

            if weekly_entries:
                st.dataframe(
                    pd.DataFrame(
                        weekly_entries
                    ),
                    use_container_width=True
                )
            else:
                st.info(
                    "No entries this week."
                )

        with tab2:

            st.subheader(
                "Monthly Timesheet"
            )

            if monthly_entries:
                st.dataframe(
                    pd.DataFrame(
                        monthly_entries
                    ),
                    use_container_width=True
                )
            else:
                st.info(
                    "No entries this month."
                )
