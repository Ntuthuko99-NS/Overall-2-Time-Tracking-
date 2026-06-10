import streamlit as st
import time

DAY_LABELS = {
    "monday": "Mon",
    "tuesday": "Tue",
    "wednesday": "Wed",
    "thursday": "Thu",
    "friday": "Fri",
    "saturday": "Sat",
    "sunday": "Sun",
}


# -------------------------------------
# Session State
# -------------------------------------
if "shifts" not in st.session_state:
    st.session_state.shifts = []

if "employees" not in st.session_state:
    st.session_state.employees = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "editing_shift" not in st.session_state:
    st.session_state.editing_shift = None


# -------------------------------------
# Create / Update Shift
# -------------------------------------
def save_shift(data):

    editing_shift = st.session_state.editing_shift

    if editing_shift:
        for i, shift in enumerate(st.session_state.shifts):
            if shift["id"] == editing_shift["id"]:
                st.session_state.shifts[i].update(data)
                break
    else:
        data["id"] = int(time.time() * 1000)
        data["assigned_employees"] = []
        st.session_state.shifts.append(data)

    st.session_state.show_form = False
    st.session_state.editing_shift = None


# -------------------------------------
# Delete Shift
# -------------------------------------
def delete_shift(shift_id):
    st.session_state.shifts = [
        s for s in st.session_state.shifts
        if s["id"] != shift_id
    ]


# -------------------------------------
# Assign / Remove Employee
# -------------------------------------
def toggle_employee(shift_id, employee):

    for shift in st.session_state.shifts:

        if shift["id"] != shift_id:
            continue

        assigned = shift.get("assigned_employees", [])

        exists = any(
            e["employee_id"] == employee["employee_id"]
            for e in assigned
        )

        if exists:
            shift["assigned_employees"] = [
                e for e in assigned
                if e["employee_id"] != employee["employee_id"]
            ]
        else:
            assigned.append({
                "employee_id": employee["employee_id"],
                "employee_name": employee["full_name"]
            })

            shift["assigned_employees"] = assigned


# -------------------------------------
# Header
# -------------------------------------
st.title("📅 Shift Scheduling")
st.caption("Manage work shifts")

if st.button("➕ Create Shift"):
    st.session_state.editing_shift = None
    st.session_state.show_form = True


# -------------------------------------
# Shift Form
# -------------------------------------
if st.session_state.show_form:

    with st.form("shift_form"):

        shift = st.session_state.editing_shift or {}

        name = st.text_input(
            "Shift Name",
            value=shift.get("name", "")
        )

        col1, col2 = st.columns(2)

        with col1:
            start_time = st.text_input(
                "Start Time",
                value=shift.get("start_time", "09:00")
            )

        with col2:
            end_time = st.text_input(
                "End Time",
                value=shift.get("end_time", "17:00")
            )

        location = st.text_input(
            "Location",
            value=shift.get("location", "")
        )

        department = st.text_input(
            "Department",
            value=shift.get("department", "")
        )

        selected_days = st.multiselect(
            "Days of Week",
            list(DAY_LABELS.keys()),
            default=shift.get(
                "days_of_week",
                ["monday", "tuesday", "wednesday",
                 "thursday", "friday"]
            )
        )

        submitted = st.form_submit_button(
            "Update Shift"
            if st.session_state.editing_shift
            else "Create Shift"
        )

        if submitted:

            save_shift({
                "name": name,
                "start_time": start_time,
                "end_time": end_time,
                "days_of_week": selected_days,
                "location": location,
                "department": department,
            })

            st.rerun()


# -------------------------------------
# Empty State
# -------------------------------------
if len(st.session_state.shifts) == 0:

    st.info("⏰ No shifts yet")

# -------------------------------------
# Shift Cards
# -------------------------------------
else:

    cols = st.columns(3)

    for index, shift in enumerate(st.session_state.shifts):

        with cols[index % 3]:

            with st.container(border=True):

                st.subheader(shift["name"])

                st.caption(
                    f"{shift['start_time']} - {shift['end_time']}"
                )

                days = [
                    DAY_LABELS.get(day, day)
                    for day in shift.get("days_of_week", [])
                ]

                st.write("**Days:**", ", ".join(days))

                if shift.get("location"):
                    st.write(
                        f"📍 {shift['location']}"
                    )

                assigned_count = len(
                    shift.get(
                        "assigned_employees",
                        []
                    )
                )

                st.write(
                    f"👥 {assigned_count} assigned"
                )

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "Edit",
                        key=f"edit_{shift['id']}"
                    ):
                        st.session_state.editing_shift = shift
                        st.session_state.show_form = True
                        st.rerun()

                with c2:
                    if st.button(
                        "Delete",
                        key=f"delete_{shift['id']}"
                    ):
                        delete_shift(shift["id"])
                        st.rerun()
