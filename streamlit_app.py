import streamlit as st

st.set_page_config(
    page_title="Time Tracking & Attendance",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ Time Tracking & Attendance System")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Employees", "Attendance", "Alerts"]
)

# Dashboard
if page == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Employees", 25)

    with col2:
        st.metric("Present Today", 20)

    with col3:
        st.metric("Absent Today", 5)

# Employees
elif page == "Employees":
    st.header("Employees")

    st.dataframe({
        "ID": [1, 2, 3],
        "Name": ["John", "Sarah", "Mike"],
        "Department": ["IT", "HR", "Finance"]
    })

# Attendance
elif page == "Attendance":
    st.header("Attendance")

    employee = st.selectbox(
        "Employee",
        ["John", "Sarah", "Mike"]
    )

    if st.button("Clock In"):
        st.success(f"{employee} clocked in successfully!")

    if st.button("Clock Out"):
        st.success(f"{employee} clocked out successfully!")

# Alerts
elif page == "Alerts":
    st.header("Alerts")

    st.warning("3 employees are late today.")
    st.info("Shift starts at 08:00.")
