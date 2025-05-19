import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from output_writers.airtable_push import push_to_airtable
from output_writers.gohighlevel_push import push_to_gohighlevel
from output_writers.email_alert import alert_strong_deal

# Auth
st.set_page_config(page_title="EmpireGPT Dashboard", layout="wide")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("🔐 Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username == os.getenv("DASHBOARD_USER", "admin") and password == os.getenv("DASHBOARD_PASS", "empire"):
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

st.title("📊 EmpireGPT Deal Dashboard")

# Load data
json_path = "logs/deal_history.json"
csv_path = "logs/deal_history.csv"
data = []

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except Exception as e:
                alert_strong_deal({"address": "unknown", "error": str(e)})

if not data and os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(data)

if df.empty:
    st.warning("No deals found.")
    st.stop()

# Filters
grade_filter = st.multiselect("Filter by Grade", options=df["grade"].unique(), default=df["grade"].unique())
df = df[df["grade"].isin(grade_filter)]

# CRM Push UI
selected = st.multiselect("Select Deals to Push to CRM", df["address"].tolist())

if st.button("Push Selected to Airtable"):
    for addr in selected:
        deal = df[df["address"] == addr].iloc[0].to_dict()
        try:
            push_to_airtable(deal)
            st.success(f"Pushed to Airtable: {addr}")
        except Exception as e:
            st.error(f"Failed Airtable push: {addr}")
            alert_strong_deal({"address": addr, "error": str(e)})

if st.button("Push Selected to GoHighLevel"):
    for addr in selected:
        deal = df[df["address"] == addr].iloc[0].to_dict()
        try:
            push_to_gohighlevel(deal)
            st.success(f"Pushed to GoHighLevel: {addr}")
        except Exception as e:
            st.error(f"Failed GoHighLevel push: {addr}")
            alert_strong_deal({"address": addr, "error": str(e)})

# Charts
st.subheader("IRR Distribution")
st.altair_chart(alt.Chart(df).mark_bar().encode(x=alt.X("irr:Q", bin=True), y='count()'), use_container_width=True)

st.subheader("DSCR Distribution")
st.altair_chart(alt.Chart(df).mark_bar().encode(x=alt.X("dscr:Q", bin=True), y='count()'), use_container_width=True)

st.subheader("CoC Return (Cash Flow Proxy)")
st.altair_chart(alt.Chart(df).mark_bar().encode(x=alt.X("cash_flow:Q", bin=True), y='count()'), use_container_width=True)

st.subheader("Grade Distribution")
st.altair_chart(alt.Chart(df).mark_bar().encode(x='grade:N', y='count()'), use_container_width=True)