import streamlit as st
from datetime import date


LEAVE_TYPES = {
    "annual": "Annual Leave",
    "sick": "Sick Leave",
    "unpaid": "Unpaid Leave",
    "family_responsibility": "Family Responsibility",
    "maternity": "Maternity Leave",
    "paternity": "Paternity Leave",
    "study": "Study Leave",
    "other": "Other"
}


def leave_request_form(employee):
    """
    Leave Request Form

    Returns:
        dict | None
    """

    with st.form("leave_request_form"):

        st.subheader("📅 Request Leave")

        leave_type = st.selectbox(
            "Leave Type",
            options=list(LEAVE_TYPES.keys()),
            format_func=lambda x: LEAVE_TYPES[x]
        )

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=date.today()
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=date.today(),
                min_value=start_date
            )

        total_days = (
            (end_date - start_date).days + 1
        )

        if total_days > 0:
            st.info(
                f"Total: {total_days} "
                f"day{'s' if total_days != 1 else ''} requested"
            )

        reason = st.text_area(
            "Reason (Optional)",
            placeholder="Please provide a reason for your leave request...",
            height=100
        )

        submitted = st.form_submit_button(
            "Submit Request"
        )

        if submitted:

            leave_request = {
                "employee_id": employee["employee_id"],
                "employee_name": employee["full_name"],
                "leave_type": leave_type,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "total_days": total_days,
                "reason": reason,
                "status": "pending"
            }

            return leave_request

    return None
