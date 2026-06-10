import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta


LEAVE_COLORS = {
    "annual": "🟦",
    "sick": "🟥",
    "unpaid": "⬜",
    "family_responsibility": "🟪",
    "maternity": "🩷",
    "paternity": "🟪",
    "study": "🟨",
    "other": "⬛"
}


def leave_calendar(leave_requests):
    # Initialize month in session state
    if "calendar_month" not in st.session_state:
        st.session_state.calendar_month = datetime.today().replace(day=1)

    current_month = st.session_state.calendar_month

    # Header
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("⬅ Previous"):
            year = current_month.year
            month = current_month.month - 1

            if month == 0:
                month = 12
                year -= 1

            st.session_state.calendar_month = datetime(
                year,
                month,
                1
            )
            st.rerun()

    with col2:
        st.markdown(
            f"## 📅 {current_month.strftime('%B %Y')}"
        )

    with col3:
        if st.button("Next ➡"):
            year = current_month.year
            month = current_month.month + 1

            if month == 13:
                month = 1
                year += 1

            st.session_state.calendar_month = datetime(
                year,
                month,
                1
            )
            st.rerun()

    # Approved requests only
    approved_requests = [
        r for r in leave_requests
        if r.get("status") == "approved"
    ]

    # Calendar generation
    cal = calendar.Calendar(firstweekday=0)

    month_days = cal.monthdatescalendar(
        current_month.year,
        current_month.month
    )

    weekday_names = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]

    # Weekday header
    cols = st.columns(7)

    for i, day in enumerate(weekday_names):
        cols[i].markdown(
            f"**{day}**"
        )

    # Calendar grid
    for week in month_days:

        cols = st.columns(7)

        for i, day in enumerate(week):

            leave_entries = []

            for leave in approved_requests:

                start = datetime.strptime(
                    leave["start_date"],
                    "%Y-%m-%d"
                ).date()

                end = datetime.strptime(
                    leave["end_date"],
                    "%Y-%m-%d"
                ).date()

                if start <= day <= end:

                    icon = LEAVE_COLORS.get(
                        leave["leave_type"],
                        "⬜"
                    )

                    leave_entries.append(
                        f"{icon} {leave['employee_name'].split()[0]}"
                    )

            day_text = f"**{day.day}**\n\n"

            if leave_entries:
                day_text += "\n".join(
                    leave_entries[:3]
                )

                if len(leave_entries) > 3:
                    day_text += (
                        f"\n+{len(leave_entries)-3} more"
                    )

            cols[i].markdown(day_text)

    # Legend
    st.divider()

    st.markdown("### Leave Types")

    legend_cols = st.columns(4)

    legend_items = [
        ("annual", "Annual Leave"),
        ("sick", "Sick Leave"),
        ("family_responsibility", "Family Leave"),
        ("study", "Study Leave")
    ]

    for idx, (leave_type, label) in enumerate(
        legend_items
    ):
        with legend_cols[idx]:
            st.write(
                f"{LEAVE_COLORS[leave_type]} {label}"
            )
