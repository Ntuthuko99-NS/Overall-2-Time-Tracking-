import streamlit as st
from datetime import datetime


LEAVE_TYPE_LABELS = {
    "annual": "Annual Leave",
    "sick": "Sick Leave",
    "unpaid": "Unpaid Leave",
    "family_responsibility": "Family Responsibility",
    "maternity": "Maternity Leave",
    "paternity": "Paternity Leave",
    "study": "Study Leave",
    "other": "Other"
}


def leave_request_card(
    request,
    show_actions=False,
    on_approve=None,
    on_reject=None
):
    """
    Display a leave request card.
    """

    status_icons = {
        "pending": "⏳",
        "approved": "✅",
        "rejected": "❌",
        "cancelled": "⚫"
    }

    employee_name = request.get(
        "employee_name",
        "Unknown Employee"
    )

    initials = "".join(
        [name[0] for name in employee_name.split()]
    )[:2].upper()

    leave_type = LEAVE_TYPE_LABELS.get(
        request.get("leave_type"),
        request.get("leave_type")
    )

    start_date = datetime.strptime(
        request["start_date"],
        "%Y-%m-%d"
    )

    end_date = datetime.strptime(
        request["end_date"],
        "%Y-%m-%d"
    )

    status = request.get(
        "status",
        "pending"
    )

    with st.container(border=True):

        # Header
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(
                f"""
                **👤 {employee_name}**

                {leave_type}
                """
            )

        with col2:
            st.write(
                f"{status_icons.get(status,'⏳')} "
                f"**{status.title()}**"
            )

        # Dates
        st.write(
            f"📅 {start_date.strftime('%b %d')} "
            f"→ "
            f"{end_date.strftime('%b %d, %Y')}"
        )

        total_days = request.get(
            "total_days",
            0
        )

        st.caption(
            f"🗓️ {total_days} day"
            f"{'s' if total_days != 1 else ''}"
        )

        # Reason
        if request.get("reason"):
            st.info(request["reason"])

        # Manager Actions
        if (
            show_actions
            and status == "pending"
        ):

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "✅ Approve",
                    key=f"approve_{request['id']}"
                ):
                    if on_approve:
                        on_approve(request)

            with col2:
                if st.button(
                    "❌ Reject",
                    key=f"reject_{request['id']}"
                ):
                    if on_reject:
                        on_reject(request)

        # Review Info
        if request.get("reviewed_by"):

            review_date = ""

            if request.get("reviewed_at"):
                review_date = datetime.strptime(
                    request["reviewed_at"],
                    "%Y-%m-%d"
                ).strftime("%b %d, %Y")

            action = (
                "Approved"
                if status == "approved"
                else "Rejected"
            )

            st.caption(
                f"{action} by "
                f"{request['reviewed_by']} "
                f"{review_date}"
            )
