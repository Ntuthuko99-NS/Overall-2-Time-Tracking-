import streamlit as st

# ----------------------------
# CONFIG
# ----------------------------

st.set_page_config(
    page_title="TimeTrack",
    page_icon="🕒",
    layout="wide"
)

# ----------------------------
# USER DATA
# ----------------------------

user = {
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

# ----------------------------
# NAVIGATION
# ----------------------------

NAVIGATION = {
    "Dashboard": "🏠",
    "My Profile": "👤",
    "Employees": "👥",
    "Timesheet": "⏰",
    "Shifts": "📅",
    "Leave": "📝",
    "Alerts": "🔔",
    "Reports": "📊",
    "Settings": "⚙️"
}

# ----------------------------
# SIDEBAR
# ----------------------------

def render_sidebar():

    st.sidebar.markdown("## 🕒 TimeTrack")
    st.sidebar.caption("Attendance System")

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        list(NAVIGATION.keys()),
        format_func=lambda x: f"{NAVIGATION[x]} {x}"
    )

    st.sidebar.divider()

    st.sidebar.markdown(
        f"""
        **{user['full_name']}**

        {user['role']}
        """
    )

    if st.sidebar.button("🚪 Sign Out"):
        st.sidebar.success("Logged out")

    return page


# ----------------------------
# PAGE CONTENT
# ----------------------------

selected_page = render_sidebar()

st.title(selected_page)

if selected_page == "Dashboard":
    st.write("Dashboard content goes here")

elif selected_page == "My Profile":
    st.write("Profile page")

elif selected_page == "Employees":
    st.write("Employees page")

elif selected_page == "Timesheet":
    st.write("Timesheet page")

elif selected_page == "Shifts":
    st.write("Shift management page")

elif selected_page == "Leave":
    st.write("Leave requests page")

elif selected_page == "Alerts":
    st.write("Alerts page")

elif selected_page == "Reports":
    st.write("Reports page")

elif selected_page == "Settings":
    st.write("Settings page")
