import streamlit as st
import requests

BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="GenAI Healthcare Copilot", layout="wide")
st.title("🏥 GenAI Healthcare Copilot")

tabs = st.tabs(["AI Diagnostics", "Treatment Agent", "Mental Health", "Hospital Ops"])

# ------------------ TAB 1 ------------------
with tabs[0]:
    st.header("🩺 AI Diagnostics")
    file = st.file_uploader("Upload medical image")

    if st.button("Run Diagnosis") and file:
        files = {"file": file.getvalue()}
        res = requests.post(BASE + "/diagnose", files={"file": file})
        st.json(res.json())

# ------------------ TAB 2 ------------------
with tabs[1]:
    st.header("💊 Personalized Treatment")

    age = st.number_input("Age", 20, 90, 40)
    weight = st.number_input("Weight", 40, 120, 70)
    conditions = st.text_input("Conditions (comma separated)", "pneumonia")
    allergies = st.text_input("Allergies (comma separated)", "penicillin")

    if st.button("Get Treatment"):
        data = {
            "age": age,
            "weight": weight,
            "conditions": conditions.split(","),
            "allergies": allergies.split(",")
        }
        res = requests.post(BASE + "/treatment", json=data)
        st.json(res.json())

# ------------------ TAB 3 ------------------
with tabs[2]:
    st.header("🧘 Mental Health Companion")

    msg = st.text_input("How are you feeling today?")

    if st.button("Send"):
        res = requests.post(BASE + "/mental-health/chat", json={"message": msg})
        st.json(res.json())

# ------------------ TAB 4 ------------------
with tabs[3]:
    st.header("🏨 Hospital Workflow Optimization")

    if st.button("Optimize Hospital"):
        res = requests.get(BASE + "/hospital/optimize")
        st.json(res.json())
