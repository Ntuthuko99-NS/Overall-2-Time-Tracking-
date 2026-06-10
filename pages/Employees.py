import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:5000/employees"

# -----------------------------
# API FUNCTIONS
# -----------------------------

def get_employees():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to load employees: {e}")
        return []


def create_employee(data):
    response = requests.post(API_URL, json=data)
    response.raise_for_status()


def update_employee(employee_id, data):
    response = requests.put(
        f"{API_URL}/{employee_id}",
        json=data
    )
    response.raise_for_status()


def delete_employee(employee_id):
    response = requests.delete(
        f"{API_URL}/{employee_id}"
    )
    response.raise_for_status()


# -----------------------------
# SESSION STATE
# -----------------------------

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "editing_employee" not in st.session_state:
    st.session_state.editing_employee = None

# -----------------------------
# LOAD EMPLOYEES
# -----------------------------

employees = get_employees()

# -----------------------------
# HEADER
# -----------------------------

col1, col2 = st.columns([4, 1])

with col1:
    st.title("Employees")
    st.caption(f"{len(employees)} total employees")

with col2:
    if st.button("➕ Add Employee"):
        st.session_state.editing_employee = None
        st.session_state.show_form = True

# -----------------------------
# FILTERS
# -----------------------------

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input(
        "Search Employees",
        placeholder="Search by name, email, employee ID"
    )

with col2:
    role = st.selectbox(
        "Role",
        ["all", "employee", "manager", "admin"]
    )

with col3:
    status = st.selectbox(
        "Status",
        ["all", "active", "inactive"]
    )

# -----------------------------
# FILTER LOGIC
# -----------------------------

filtered_employees = []

for emp in employees:

    matches_search = (
        search.lower() in str(emp.get("full_name", "")).lower()
        or search.lower() in str(emp.get("email", "")).lower()
        or search.lower() in str(emp.get("employee_id", "")).lower()
    )

    matches_role = (
        role == "all"
        or emp.get("role") == role
    )

    matches_status = (
        status == "all"
        or (status == "active" and emp.get("is_active"))
        or (status == "inactive" and not emp.get("is_active"))
    )

    if matches_search and matches_role and matches_status:
        filtered_employees.append(emp)

# -----------------------------
# EMPLOYEE LIST
# -----------------------------

if len(filtered_employees) == 0:
    st.info("No employees found.")

for emp in filtered_employees:

    with st.container(border=True):

        st.markdown(
            f"""
            ### {emp.get('full_name')}
            **Employee ID:** {emp.get('employee_id')}

            **Email:** {emp.get('email')}

            **Department:** {emp.get('department')}

            **Position:** {emp.get('position')}

            **Role:** {emp.get('role')}
            """
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "✏️ Edit",
                key=f"edit_{emp['id']}"
            ):
                st.session_state.editing_employee = emp
                st.session_state.show_form = True

        with col2:
            if st.button(
                "🗑 Delete",
                key=f"delete_{emp['id']}"
            ):
                delete_employee(emp["id"])
                st.success("Employee deleted")
                st.rerun()

# -----------------------------
# EMPLOYEE FORM
# -----------------------------

if st.session_state.show_form:

    st.divider()

    employee = (
        st.session_state.editing_employee
        or {}
    )

    title = (
        "Edit Employee"
        if employee
        else "Add Employee"
    )

    st.subheader(title)

    with st.form("employee_form"):

        employee_id = st.text_input(
            "Employee ID",
            value=employee.get("employee_id", "")
        )

        full_name = st.text_input(
            "Full Name",
            value=employee.get("full_name", "")
        )

        email = st.text_input(
            "Email",
            value=employee.get("email", "")
        )

        phone = st.text_input(
            "Phone",
            value=employee.get("phone", "")
        )

        department = st.text_input(
            "Department",
            value=employee.get("department", "")
        )

        position = st.text_input(
            "Position",
            value=employee.get("position", "")
        )

        role = st.selectbox(
            "Role",
            ["employee", "manager", "admin"],
            index=0
        )

        expected_hours = st.number_input(
            "Expected Daily Hours",
            min_value=1,
            max_value=24,
            value=int(
                employee.get(
                    "expected_daily_hours",
                    8
                )
            )
        )

        is_active = st.checkbox(
            "Active",
            value=employee.get(
                "is_active",
                True
            )
        )

        submitted = st.form_submit_button(
            "Save Employee"
        )

        if submitted:

            data = {
                "employee_id": employee_id,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "department": department,
                "position": position,
                "role": role,
                "expected_daily_hours": expected_hours,
                "is_active": is_active
            }

            try:

                if employee:
                    update_employee(
                        employee["id"],
                        data
                    )
                    st.success(
                        "Employee updated"
                    )
                else:
                    create_employee(data)
                    st.success(
                        "Employee created"
                    )

                st.session_state.show_form = False
                st.session_state.editing_employee = None
                st.rerun()

            except Exception as e:
                st.error(str(e))
