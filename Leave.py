import streamlit as st
import pandas as pd
from datetime import date

# ----------------------------------
# SESSION STATE
# ----------------------------------

if "leave_requests" not in st.session_state:
    st.session_state.leave_requests = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# ----------------------------------
# SAMPLE DATA
# ----------------------------------

current_user = {
    "email": "thabiso@example.com",
    "full_name": "Thabiso Mngomezulu",
    "role": "admin"
}

employees = [
    {
        "employee_id": 1,
        "email": "thabiso@example.com",
        "full_name": "Thabiso Mngomezulu",
        "role": "admin",
        "annual_leave_balance": 21,
        "sick_leave_balance": 30
    }
]

current_employee = next(
    (e for e in employees if e["email"] == current_user["email"]),
    None
)

is_manager = (
    current_user["role"] in ["admin", "manager"]
)

# ----------------------------------
# HELPERS
# ----------------------------------

def create_leave_request(data):
    data["id"] = len(st.session_state.leave_requests) + 1
    data["status"] = "pending"
    st.session_state.leave_requests.append(data)

def approve_request(request_id):
    for req in st.session_state.leave_requests:
        if req["id"] == request_id:
            req["status"] = "approved"

def reject_request(request_id):
    for req in st.session_state.leave_requests:
        if req["id"] == request_id:
            req["status"] = "rejected"

# ----------------------------------
# FILTERS
# ----------------------------------

leave_requests = st.session_state.leave_requests

my_requests = [
    r for r in leave_requests
    if r["employee_id"] == current_employee["employee_id"]
]

pending_requests = [
    r for r in leave_requests
    if r["status"] == "pending"
]

approved_requests = [
    r for r in leave_requests
    if r["status"] == "approved"
]

rejected_requests = [
    r for r in leave_requests
    if r["status"] == "rejected"
]

# ----------------------------------
# HEADER
# ----------------------------------

col1, col2 = st.columns([4, 1])

with col1:
    st.title("🏖 Leave Management")
    st.caption("Request and manage your leave")

with col2:
    if st.button("➕ Request Leave"):
        st.session_state.show_form = True

# ----------------------------------
# STATS
# ----------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Annual Leave",
        current_employee.get(
            "annual_leave_balance",
            21
        )
    )

with c2:
    st.metric(
        "Sick Leave",
        current_employee.get(
            "sick_leave_balance",
            30
        )
    )

with c3:
    st.metric(
        "Pending",
        len(pending_requests)
    )

with c4:
    st.metric(
        "Approved",
        len(approved_requests)
    )

# ----------------------------------
# TABS
# ----------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Pending",
    "My Requests",
    "Calendar",
    "Team"
])

# ----------------------------------
# PENDING
# ----------------------------------

with tab1:

    if not pending_requests:
        st.info("No pending requests")

    for req in pending_requests:

        with st.container(border=True):

            st.write(
                f"**Employee:** {req['employee_name']}"
            )

            st.write(
                f"**Leave Type:** {req['leave_type']}"
            )

            st.write(
                f"**Dates:** {req['start_date']} → {req['end_date']}"
            )

            st.write(
                f"**Reason:** {req['reason']}"
            )

            if is_manager:

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "✅ Approve",
                        key=f"approve_{req['id']}"
                    ):
                        approve_request(req["id"])
                        st.rerun()

                with c2:
                    if st.button(
                        "❌ Reject",
                        key=f"reject_{req['id']}"
                    ):
                        reject_request(req["id"])
                        st.rerun()

# ----------------------------------
# MY REQUESTS
# ----------------------------------

with tab2:

    if not my_requests:
        st.info("No requests submitted")

    for req in my_requests:

        with st.container(border=True):

            st.write(
                f"**Leave Type:** {req['leave_type']}"
            )

            st.write(
                f"**Status:** {req['status']}"
            )

            st.write(
                f"**Dates:** {req['start_date']} → {req['end_date']}"
            )

# ----------------------------------
# CALENDAR
# ----------------------------------

with tab3:

    st.subheader("Leave Calendar")

    if leave_requests:

        df = pd.DataFrame(leave_requests)

        st.dataframe(
            df[
                [
                    "employee_name",
                    "leave_type",
                    "start_date",
                    "end_date",
                    "status"
                ]
            ],
            use_container_width=True
        )

    else:
        st.info("No leave data available")

# ----------------------------------
# TEAM
# ----------------------------------

with tab4:

    if is_manager:

        st.subheader("Team Availability")

        employee_df = pd.DataFrame(employees)

        st.dataframe(
            employee_df[
                [
                    "employee_id",
                    "full_name",
                    "role"
                ]
            ],
            use_container_width=True
        )

    else:
        st.warning(
            "Manager access required"
        )

# ----------------------------------
# REQUEST FORM
# ----------------------------------

if st.session_state.show_form:

    st.divider()

    st.subheader("New Leave Request")

    with st.form("leave_request_form"):

        leave_type = st.selectbox(
            "Leave Type",
            [
                "annual",
                "sick",
                "unpaid",
                "family_responsibility",
                "maternity",
                "paternity",
                "study",
                "other"
            ]
        )

        start_date = st.date_input(
            "Start Date"
        )

        end_date = st.date_input(
            "End Date"
        )

        reason = st.text_area(
            "Reason"
        )

        submit = st.form_submit_button(
            "Submit Request"
        )

        if submit:

            create_leave_request({
                "employee_id":
                    current_employee["employee_id"],
                "employee_name":
                    current_user["full_name"],
                "leave_type":
                    leave_type,
                "start_date":
                    str(start_date),
                "end_date":
                    str(end_date),
                "reason":
                    reason
            })

            st.success(
                "Leave request submitted"
            )

            st.session_state.show_form = False

            st.rerun()
