import streamlit as st
from scrapers.zillow_scraper import scrape_zillow_data

st.title("EmpireGPT")

address = st.text_input("Enter a property address:", "123 Main St")

if address:
    data = scrape_zillow_data(address)
    st.subheader("Zillow Data (Mocked)")
    st.json(data)