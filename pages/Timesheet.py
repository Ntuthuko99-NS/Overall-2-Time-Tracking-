import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ----------------------------------
# Session State
# ----------------------------------
if "employees" not in st.session_state:
    st.session_state.employees = []

if "time_entries" not in st.session_state:
    st.session_state.time_entries = []


# ----------------------------------
# Date Helpers
# ----------------------------------
today = datetime.today()

def get_week_range(date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start.date(), end.date()

def get_month_range(date):
    start = date.replace(day=1)

    if start.month == 12:
        next_month = start.replace(
            year=start.year + 1,
            month=1
        )
    else:
        next_month = start.replace(
            month=start.month + 1
        )

    end = next_month - timedelta(days=1)

    return start.date(), end.date()


# ----------------------------------
# Filters
# ----------------------------------
st.title("📅 Timesheet")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    view_mode = st.selectbox(
        "View",
        ["week", "month"]
    )

if view_mode == "week":
    date_from, date_to = get_week_range(today)
else:
    date_from, date_to = get_month_range(today)

with col2:

    employee_options = {
        "All Employees": "all"
    }

    for emp in st.session_state.employees:
        employee_options[
            emp["full_name"]
        ] = emp["employee_id"]

    selected_label = st.selectbox(
        "Employee",
        list(employee_options.keys())
    )

selected_employee = employee_options[
    selected_label
]

with col3:
    st.write("")
    st.write("")
    st.button("⬇ Export")


st.caption(
    f"{date_from.strftime('%b %d')} - "
    f"{date_to.strftime('%b %d, %Y')}"
)

# ----------------------------------
# Filter Entries
# ----------------------------------
filtered_entries = []

for entry in st.session_state.time_entries:

    entry_date = datetime.strptime(
        entry["date"],
        "%Y-%m-%d"
    ).date()

    in_range = (
        date_from <= entry_date <= date_to
    )

    employee_match = (
        selected_employee == "all"
        or entry["employee_id"]
        == selected_employee
    )

    if in_range and employee_match:
        filtered_entries.append(entry)

# ----------------------------------
# Summary
# ----------------------------------
total_hours = sum(
    e.get("total_hours", 0)
    for e in filtered_entries
)

total_overtime = sum(
    e.get("overtime_hours", 0)
    for e in filtered_entries
)

days_worked = len(
    set(e["date"] for e in filtered_entries)
)

avg_hours = (
    total_hours / days_worked
    if days_worked > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Hours",
        f"{total_hours:.1f}h"
    )

with col2:
    st.metric(
        "Overtime",
        f"{total_overtime:.1f}h"
    )

with col3:
    st.metric(
        "Days Worked",
        days_worked
    )

with col4:
    st.metric(
        "Avg / Day",
        f"{avg_hours:.1f}h"
    )

# ----------------------------------
# Daily Chart Data
# ----------------------------------
daily_rows = []

current_day = date_from

while current_day <= date_to:

    day_string = current_day.strftime(
        "%Y-%m-%d"
    )

    entries = [
        e for e in filtered_entries
        if e["date"] == day_string
    ]

    hours = sum(
        e.get("total_hours", 0)
        for e in entries
    )

    overtime = sum(
        e.get("overtime_hours", 0)
        for e in entries
    )

    daily_rows.append({
        "Day": current_day.strftime("%a"),
        "Hours": hours,
        "Overtime": overtime
    })

    current_day += timedelta(days=1)

# ----------------------------------
# Chart
# ----------------------------------
st.subheader("Daily Hours")

if daily_rows:

    chart_df = pd.DataFrame(
        daily_rows
    ).set_index("Day")

    st.bar_chart(
        chart_df[["Hours"]]
    )

# ----------------------------------
# Timesheet Table
# ----------------------------------
st.subheader("Timesheet Entries")

if filtered_entries:

    df = pd.DataFrame(
        filtered_entries
    )

    if selected_employee != "all":
        columns = [
            c for c in df.columns
            if c != "employee_name"
        ]
        df = df[columns]

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info(
        "No timesheet entries found."
    )
