
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="EmpireGPT", layout="wide")
st.title("🏠 EmpireGPT - Investor Dashboard")

address = st.text_input("Enter property address:", "21309 W Memorial Dr, Porter, TX 77365")
backend_url = "http://localhost:8000/api/underwrite"

if st.button("Run Underwriter"):
    with st.spinner("Analyzing..."):
        res = requests.post(backend_url, json={"address": address})
        if res.ok:
            data = res.json()
            st.subheader("📋 Summary")
            st.write(data["text"])
            st.subheader("💰 Offers")
            st.dataframe(pd.DataFrame(data["offers"]))
            st.subheader("📊 Financials")
            st.write({
                "ARV": f"${data['arv']}",
                "IRR": f"{data['irr']}%",
                "DSCR": data["dscr"],
                "CoC Return": f"{data['coc']}%",
                "Grade": data["grade"]
            })
        else:
            st.error("Failed to fetch underwriting data.")
