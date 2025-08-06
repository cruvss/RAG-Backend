import streamlit as st
import requests
import os
from datetime import datetime

API_URL = "http://localhost:8000"  

st.set_page_config(page_title="RAG Chat with Upload + Booking", layout="wide")

st.title("📄 RAG Document Chat + Interview Booking")

# --- SIDEBAR FILE UPLOAD ---
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF or Text File", type=["pdf", "txt"])
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{API_URL}/api/upload-document", files=files)
    if response.status_code == 200:
        st.sidebar.success("✅ File uploaded & processed!")
    else:
        st.sidebar.error("❌ Upload failed.")

# --- SESSION STATE ---
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{datetime.now().timestamp()}"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN CHAT INTERFACE ---
st.subheader("💬 Ask Questions")
user_query = st.text_input("Your question:", placeholder="Ask about the uploaded document...")
if st.button("Send") and user_query:
    st.session_state.chat_history.append(("You", user_query))
    payload = {
        "session_id": st.session_state.session_id,
        "query": user_query
    }
    response = requests.post(f"{API_URL}/api/chat", json=payload)
    if response.status_code == 200:
        bot_reply = response.json().get("response", "No response")
        st.session_state.chat_history.append(("Bot", bot_reply))
    else:
        st.session_state.chat_history.append(("Bot", "Error from API"))

# --- DISPLAY CHAT HISTORY ---
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 {speaker}:** {message}")
    else:
        st.markdown(f"**🤖 {speaker}:** {message}")

# --- INTERVIEW BOOKING ---
st.subheader("📅 Book an Interview")
with st.form("booking_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    date = st.date_input("Preferred Date")
    time = st.time_input("Preferred Time")
    submit_booking = st.form_submit_button("Book Interview")

    if submit_booking:
        payload = {
            "name": name,
            "email": email,
            "date": str(date),
            "time": str(time)
        }
        response = requests.post(f"{API_URL}/api/book-interview", json=payload)
        if response.status_code == 200:
            st.success("✅ Interview booked! Confirmation email sent.")
        else:
            st.error("❌ Failed to book interview.")
