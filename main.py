import streamlit as st
import json
from scrapers.zillow_scraper import scrape_zillow_data

st.title("🏡 EmpireGPT Real Estate Underwriter")

address = st.text_input("Enter Property Address", "123 Main St, TX")

if address:
    data = scrape_zillow_data(address)
    st.subheader("Zillow Mock Data")
    st.json(data)