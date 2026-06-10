import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


def reports_page(employees, time_entries):
    st.title("📊 Reports")
    st.caption("Attendance and performance overview")

    # -----------------------------
    # Month Selector
    # -----------------------------
    months = []

    for i in range(12):
        d = datetime.today() - relativedelta(months=i)

        months.append({
            "value": d.strftime("%Y-%m"),
            "label": d.strftime("%B %Y")
        })

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_month = st.selectbox(
            "Select Month",
            options=[m["value"] for m in months],
            format_func=lambda x: next(
                m["label"]
                for m in months
                if m["value"] == x
            )
        )

    with col2:
        export = st.button("📥 Export")

    # -----------------------------
    # Date Range
    # -----------------------------
    year, month = map(
        int,
        selected_month.split("-")
    )

    start_date = date(year, month, 1)

    last_day = calendar.monthrange(
        year,
        month
    )[1]

    end_date = date(
        year,
        month,
        last_day
    )

    # -----------------------------
    # Filter Entries
    # -----------------------------
    filtered_entries = []

    for entry in time_entries:

        entry_date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        ).date()

        if start_date <= entry_date <= end_date:
            filtered_entries.append(entry)

    # -----------------------------
    # Attendance Summary
    # -----------------------------
    workdays = pd.bdate_range(
        start=start_date,
        end=end_date
    )

    total_workdays = len(workdays)

    attendance_summary = []

    for emp in employees:

        emp_entries = [
            e for e in filtered_entries
            if e["employee_id"]
            == emp["employee_id"]
        ]

        days_worked = len(
            set(
                e["date"]
                for e in emp_entries
            )
        )

        total_hours = sum(
            e.get("total_hours", 0)
            for e in emp_entries
        )

        overtime = sum(
            e.get("overtime_hours", 0)
            for e in emp_entries
        )

        attendance_rate = (
            round(
                (
                    days_worked /
                    total_workdays
                ) * 100,
                1
            )
            if total_workdays > 0
            else 0
        )

        attendance_summary.append({
            "employee_id":
                emp["employee_id"],
            "Employee":
                emp["full_name"],
            "Department":
                emp.get(
                    "department",
                    "-"
                ),
            "Days Worked":
                days_worked,
            "Hours":
                total_hours,
            "Overtime":
                overtime,
            "Attendance %":
                attendance_rate
        })

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    total_employees = len(employees)

    total_hours_worked = sum(
        e["Hours"]
        for e in attendance_summary
    )

    total_overtime = sum(
        e["Overtime"]
        for e in attendance_summary
    )

    avg_attendance = round(
        (
            sum(
                e["Attendance %"]
                for e in attendance_summary
            )
            / len(attendance_summary)
        ),
        1
    ) if attendance_summary else 0

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Employees",
            total_employees
        )

    with m2:
        st.metric(
            "Total Hours",
            f"{total_hours_worked:.0f}"
        )

    with m3:
        st.metric(
            "Overtime",
            f"{total_overtime:.1f}h"
        )

    with m4:
        st.metric(
            "Avg Attendance",
            f"{avg_attendance}%"
        )

    st.divider()

    # -----------------------------
    # Tabs
    # -----------------------------
    attendance_tab, overtime_tab = st.tabs(
        [
            "Attendance",
            "Overtime"
        ]
    )

    # -----------------------------
    # Attendance Tab
    # -----------------------------
    with attendance_tab:

        st.subheader(
            "Attendance Report"
        )

        if attendance_summary:

            attendance_df = pd.DataFrame(
                [
                    {
                        "Employee":
                            e["Employee"],
                        "Department":
                            e["Department"],
                        "Days Worked":
                            e["Days Worked"],
                        "Hours":
                            round(
                                e["Hours"],
                                1
                            ),
                        "Attendance %":
                            e["Attendance %"]
                    }
                    for e
                    in attendance_summary
                ]
            )

            st.dataframe(
                attendance_df,
                use_container_width=True
            )

        else:
            st.info(
                "No attendance data available."
            )

    # -----------------------------
    # Overtime Tab
    # -----------------------------
    with overtime_tab:

        st.subheader(
            "Overtime Report"
        )

        if attendance_summary:

            overtime_df = pd.DataFrame(
                [
                    {
                        "Employee":
                            e["Employee"],
                        "Overtime Hours":
                            round(
                                e["Overtime"],
                                1
                            )
                    }
                    for e
                    in attendance_summary
                ]
            )

            st.dataframe(
                overtime_df,
                use_container_width=True
            )

        else:
            st.info(
                "No overtime data available."
            )

    # -----------------------------
    # Export CSV
    # -----------------------------
    if export and attendance_summary:

        csv = pd.DataFrame(
            attendance_summary
        ).to_csv(
            index=False
        )

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name=f"attendance_report_{selected_month}.csv",
            mime="text/csv"
        )
