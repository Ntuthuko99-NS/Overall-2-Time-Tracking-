import streamlit as st

DAYS_OF_WEEK = [
    ("monday", "Mon"),
    ("tuesday", "Tue"),
    ("wednesday", "Wed"),
    ("thursday", "Thu"),
    ("friday", "Fri"),
    ("saturday", "Sat"),
    ("sunday", "Sun"),
]

COLORS = [
    "#3b82f6",
    "#8b5cf6",
    "#ec4899",
    "#f97316",
    "#10b981",
    "#06b6d4",
    "#6366f1",
    "#84cc16",
]


def shift_form(shift=None):
    """Create/Edit Shift Form"""

    default_shift = {
        "name": "",
        "start_time": "09:00",
        "end_time": "17:00",
        "expected_hours": 8,
        "days_of_week": [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
        ],
        "location": "",
        "department": "",
        "color": "#3b82f6",
        "is_active": True,
    }

    if shift:
        default_shift.update(shift)

    title = "Edit Shift" if shift else "Create New Shift"

    st.subheader(title)

    with st.form("shift_form"):

        name = st.text_input(
            "Shift Name *",
            value=default_shift["name"],
            placeholder="Morning Shift, Night Shift"
        )

        col1, col2 = st.columns(2)

        with col1:
            start_time = st.time_input(
                "Start Time"
            )

        with col2:
            end_time = st.time_input(
                "End Time"
            )

        st.write("### Days of Week")

        selected_days = []

        cols = st.columns(7)

        for idx, (day_id, label) in enumerate(DAYS_OF_WEEK):
            with cols[idx]:
                if st.checkbox(
                    label,
                    value=day_id in default_shift["days_of_week"],
                    key=day_id
                ):
                    selected_days.append(day_id)

        col1, col2 = st.columns(2)

        with col1:
            location = st.text_input(
                "Location",
                value=default_shift["location"],
                placeholder="Main Office"
            )

        with col2:
            department = st.text_input(
                "Department",
                value=default_shift["department"],
                placeholder="Security"
            )

        color = st.selectbox(
            "Color",
            COLORS,
            index=COLORS.index(default_shift["color"])
        )

        expected_hours = st.number_input(
            "Expected Hours",
            min_value=0.0,
            value=float(default_shift["expected_hours"]),
            step=0.5
        )

        is_active = st.checkbox(
            "Active",
            value=default_shift["is_active"]
        )

        submitted = st.form_submit_button(
            "Update Shift" if shift else "Create Shift"
        )

        if submitted:

            form_data = {
                "name": name,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "expected_hours": expected_hours,
                "days_of_week": selected_days,
                "location": location,
                "department": department,
                "color": color,
                "is_active": is_active,
            }

            st.success("Shift saved successfully!")
            st.json(form_data)

            return form_data

    return None


# Example usage
st.title("Shift Management")

shift_form()
