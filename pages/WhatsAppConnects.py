import streamlit as st

# Mock function (replace with your real API/client)
def get_whatsapp_connect_url(agent_name: str):
    return f"https://wa.me/setup?agent={agent_name}"


def whatsapp_connect():
    whatsapp_url = get_whatsapp_connect_url("shift_reminder")

    st.title("📱 WhatsApp Notifications")

    st.write("Get shift reminders and alerts on WhatsApp")

    st.markdown("### What you'll receive:")
    st.write("🔔 Shift reminders 30 min before start")
    st.write("⏰ Clock in/out reminders")
    st.write("⚠️ Schedule changes and updates")

    st.link_button(
        "Connect WhatsApp 📲",
        whatsapp_url
    )

    st.caption("You'll be redirected to WhatsApp to complete the setup")


if __name__ == "__main__":
    whatsapp_connect()
