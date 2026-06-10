import streamlit as st
from datetime import datetime


def leave_balance_card(employee, leave_requests):
    """
    Display employee leave balances.
    """

    current_year = datetime.now().year

    approved_this_year = [
        r for r in leave_requests
        if r.get("status") == "approved"
        and r.get("employee_id") == employee.get("employee_id")
        and datetime.strptime(
            r["start_date"],
            "%Y-%m-%d"
        ).year == current_year
    ]

    def get_used_days(leave_type):
        return sum(
            r.get("total_days", 0)
            for r in approved_this_year
            if r.get("leave_type") == leave_type
        )

    balances = [
        {
            "icon": "🏖️",
            "label": "Annual Leave",
            "type": "annual",
            "total": employee.get(
                "annual_leave_balance",
                21
            ),
            "used": get_used_days("annual")
        },
        {
            "icon": "🤒",
            "label": "Sick Leave",
            "type": "sick",
            "total": employee.get(
                "sick_leave_balance",
                30
            ),
            "used": get_used_days("sick")
        },
        {
            "icon": "🏠",
            "label": "Family Responsibility",
            "type": "family_responsibility",
            "total": 3,
            "used": get_used_days(
                "family_responsibility"
            )
        },
        {
            "icon": "🎓",
            "label": "Study Leave",
            "type": "study",
            "total": 5,
            "used": get_used_days("study")
        }
    ]

    st.subheader("📋 Leave Balances")

    for balance in balances:

        remaining = max(
            balance["total"] - balance["used"],
            0
        )

        percentage = (
            balance["used"] / balance["total"]
        ) * 100 if balance["total"] else 0

        st.markdown(
            f"### {balance['icon']} {balance['label']}"
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            st.progress(
                min(int(percentage), 100)
            )

        with col2:
            st.metric(
                "Remaining",
                f"{remaining}/{balance['total']}"
            )

        st.caption(
            f"Used: {balance['used']} days | "
            f"Available: {remaining} days"
        )

        st.divider()
