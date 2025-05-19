import streamlit as st
import json
from scrapers.zillow_scraper import scrape_zillow_data
from calculators.financial_model import calculate_financials
from calculators.offer_logic import generate_offers
from calculators.deal_grader import grade_deal
from output_writers.markdown_generator import generate_markdown_summary
from output_writers.pdf_writer import export_pdf

st.title("EmpireGPT Real Estate Underwriter")

if 'sample_data' not in st.session_state:
    with open("sample_input.json", "r") as f:
        st.session_state.sample_data = json.load(f)

address = st.text_input("Enter Property Address", value=st.session_state.sample_data.get("address", ""))

if address:
    data = scrape_zillow_data(address)
    arv = sum(c["price"] for c in data["sold_comps"]) / len(data["sold_comps"])
    offers = generate_offers(arv, rehab_cost=30000)
    offer = offers["low"]
    fin = calculate_financials(offer, data["rent_zestimate"], 2400, 950, rehab_cost=30000)
    grade, verdict = grade_deal(fin["IRR"], fin["DSCR"], fin["CoC Return"])
    summary_data = {
        "address": address,
        "arv": arv,
        "strategy": "Cash",
        "cash_flow": fin["NOI"] / 12 - fin["Monthly Payment"],
        "irr": fin["IRR"],
        "cap_rate": fin["Cap Rate"],
        "dscr": fin["DSCR"],
        "grade": verdict
    }
    st.markdown(generate_markdown_summary(summary_data))

    if st.button("Export as PDF"):
        export_pdf(summary_data)
        st.success("PDF export complete.")