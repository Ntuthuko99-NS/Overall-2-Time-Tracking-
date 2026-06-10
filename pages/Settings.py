import streamlit as st

# Default settings
if "settings" not in st.session_state:
    st.session_state.settings = {
        "company_name": "",
        "default_daily_hours": 8,
        "default_weekly_hours": 40,
        "week_start_day": "monday",
        "overtime_multiplier": 1.5,
        "enable_geofencing": False,
        "geofence_radius_meters": 100,
        "office_locations": [],
        "auto_clock_out_hours": 12,
        "grace_period_minutes": 15,
        "currency": "ZAR",
        "timezone": "Africa/Johannesburg",
    }

settings = st.session_state.settings

st.set_page_config(page_title="Settings", layout="wide")

st.title("⚙️ Settings")
st.caption("Configure your system")

# -----------------------------
# Company Info
# -----------------------------
st.subheader("Company Info")

settings["company_name"] = st.text_input(
    "Company Name",
    value=settings["company_name"]
)

settings["currency"] = st.selectbox(
    "Currency",
    ["ZAR", "USD"],
    index=["ZAR", "USD"].index(settings["currency"])
)

st.divider()

# -----------------------------
# Working Hours
# -----------------------------
st.subheader("Working Hours")

col1, col2 = st.columns(2)

with col1:
    settings["default_daily_hours"] = st.number_input(
        "Daily Hours",
        min_value=0,
        value=settings["default_daily_hours"]
    )

with col2:
    settings["default_weekly_hours"] = st.number_input(
        "Weekly Hours",
        min_value=0,
        value=settings["default_weekly_hours"]
    )

st.divider()

# -----------------------------
# Location Settings
# -----------------------------
st.subheader("Location Settings")

settings["enable_geofencing"] = st.checkbox(
    "Enable Geofencing",
    value=settings["enable_geofencing"]
)

if settings["enable_geofencing"]:

    settings["geofence_radius_meters"] = st.number_input(
        "Radius (meters)",
        min_value=0,
        value=settings["geofence_radius_meters"]
    )

    st.markdown("### Locations")

    if st.button("➕ Add Location"):
        settings["office_locations"].append({
            "name": "",
            "address": "",
            "latitude": 0.0,
            "longitude": 0.0
        })

    remove_index = None

    for i, loc in enumerate(settings["office_locations"]):

        st.markdown(f"#### Location {i + 1}")

        loc["name"] = st.text_input(
            f"Name {i}",
            value=loc["name"],
            key=f"name_{i}"
        )

        loc["address"] = st.text_input(
            f"Address {i}",
            value=loc["address"],
            key=f"address_{i}"
        )

        col1, col2 = st.columns(2)

        with col1:
            loc["latitude"] = st.number_input(
                f"Latitude {i}",
                value=float(loc["latitude"]),
                key=f"lat_{i}"
            )

        with col2:
            loc["longitude"] = st.number_input(
                f"Longitude {i}",
                value=float(loc["longitude"]),
                key=f"lng_{i}"
            )

        if st.button("🗑 Remove", key=f"remove_{i}"):
            remove_index = i

    if remove_index is not None:
        settings["office_locations"].pop(remove_index)
        st.rerun()

st.divider()

# -----------------------------
# Save
# -----------------------------
if st.button("💾 Save Settings"):
    st.success("Settings saved!")

    # Replace with database/API call
    print(settings)

    st.json(settings)
