import streamlit as st
import requests
import pandas as pd
import datetime

API_URL = "http://127.0.0.1:8000"  # FastAPI backend


# ---------------------------
# Auth Pages
# ---------------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["page"] = "dashboard"
        else:
            st.error(res.json().get("detail", "Invalid credentials"))

    if st.button("Go to Signup"):
        st.session_state["page"] = "signup"


def signup_page():
    st.title("📝 Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        res = requests.post(
            f"{API_URL}/add_user/",
            json={"username": username, "email": email, "password": password}
        )
        if res.status_code == 200:
            st.success("✅ Account created! Please log in.")
            st.session_state["page"] = "login"
        else:
            st.error(res.json().get("detail", "Signup failed"))

    if st.button("Back to Login"):
        st.session_state["page"] = "login"


# ---------------------------
# App Pages
# ---------------------------
def dashboard_page():
    st.title(f"🏠 Dashboard - Welcome {st.session_state['username']}!")

    st.write("Choose an action:")

    if st.button("➕ Add Habit"):
        st.session_state["page"] = "add_habit"

    if st.button("🗓️ Log Habit"):
        st.session_state["page"] = "log_habit"

    if st.button("📊 View Analytics"):
        st.session_state["page"] = "analytics"

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.session_state["page"] = "login"


def add_habit_page():
    st.title("➕ Add a New Habit")

    habit_name = st.text_input("Habit Name")
    description = st.text_area("Description")

    if st.button("Save Habit"):
        res = requests.post(
            f"{API_URL}/add_habit/",
            json={"user": str(st.session_state["username"]), "habit_name": str(habit_name), "description": str(description)}
        )
        if res.status_code == 200:
            st.success("Habit added successfully!")
            st.session_state["page"] = "dashboard"
        else:
            st.error(res.json().get("detail", "Failed to add habit"))

    if st.button("⬅️ Back"):
        st.session_state["page"] = "dashboard"


def log_habit_page():
    st.title("🗓️ Log Habit Progress")

    habit_name = st.text_input("Habit Name")
    status = st.selectbox("Status", ["done", "missed"])
    date = st.date_input("Date", datetime.date.today())

    if st.button("Save Log"):
        res = requests.post(
            f"{API_URL}/add_log/",
            json={"user": st.session_state["username"], "habit_name": habit_name, "status": status, "date": str(date)}
        )
        if res.status_code == 200:
            st.success("Log saved successfully!")
            st.session_state["page"] = "dashboard"
        else:
            st.error(res.json().get("detail", "Failed to save log"))

    if st.button("⬅️ Back"):
        st.session_state["page"] = "dashboard"


def analytics_page():
    st.title("📊 Analytics Dashboard")
    habit_name = st.text_input('Habit Name')

    # Example data from backend
    if(habit_name):
        res = requests.get(f"{API_URL}/logs/{st.session_state['username']}/{habit_name}")
        if res.status_code == 200:
            logs = res.json().get("logs", [])
            if logs:
                df = pd.DataFrame(logs)
                df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
                st.line_chart(df.set_index("date")["status"].apply(lambda x: 1 if x == "done" else 0))
            else:
                st.info("No logs yet. Start logging your habits!")
    else:
        st.error("Could not fetch analytics.")

    if st.button("⬅️ Back"):
        st.session_state["page"] = "dashboard"


# ---------------------------
# Router
# ---------------------------
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
        st.session_state["logged_in"] = False

    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "signup":
        signup_page()
    elif st.session_state["page"] == "dashboard":
        dashboard_page()
    elif st.session_state["page"] == "add_habit":
        add_habit_page()
    elif st.session_state["page"] == "log_habit":
        log_habit_page()
    elif st.session_state["page"] == "analytics":
        analytics_page()


if __name__ == "__main__":
    main()
