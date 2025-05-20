
import streamlit as st
import pandas as pd
from scrapers.zillow_scraper import scrape_zillow_data

st.set_page_config(page_title="EmpireGPT", layout="wide")
st.title("🏠 EmpireGPT - Investor Dashboard")

address = st.text_input("Enter property address:", "21309 W Memorial Dr, Porter, TX 77365")

def compute_arv(comps, sqft):
    return round(sum(c['price'] / c['sqft'] for c in comps) / len(comps) * sqft, -2)

def calc_rehab(year):
    return 25000 if 2025 - year < 30 else 35000

def offers_by_tier(arv, rehab):
    tiers = []
    for i, pct in enumerate([0.75, 0.80, 0.85]):
        offer = arv * pct - rehab
        down = offer * (0.05 + 0.03 * i)
        total = rehab + offer * 0.02 + offer * 0.03 + down
        tiers.append({
            "Tier": ["Low", "Medium", "High"][i],
            "Offer ($)": round(offer, -2),
            "Down Payment": int(down),
            "Total Cost": int(total)
        })
    return pd.DataFrame(tiers)

def analyze_deal(data):
    comps = data["sold_comps"]
    details = data["property_details"]
    arv = compute_arv(comps, details["sqft"])
    rehab = calc_rehab(details["year_built"])
    offers = offers_by_tier(arv, rehab)

    rent = data["rent_zestimate"]
    net = rent - 250 - (0.05 * rent)
    annual_net = net * 12
    dscr = round(annual_net / (offers.iloc[0]["Offer ($)"] * 0.08), 2)
    coc = round(annual_net / offers.iloc[0]["Total Cost"], 2)
    irr = 0.18 if coc >= 0.15 else 0.13

    if irr >= 0.18 and dscr >= 1.5:
        grade = "A – Strong"
    elif irr >= 0.14:
        grade = "B – Review"
    elif irr >= 0.10:
        grade = "C – Weak"
    else:
        grade = "D – Reject"

    return {
        "ARV": arv,
        "Rehab": rehab,
        "DSCR": dscr,
        "IRR": irr,
        "CoC": coc,
        "Grade": grade,
        "Offers": offers
    }

if address:
    data = scrape_zillow_data(address)
    result = analyze_deal(data)

    st.markdown("### 🔍 Property Overview")
    st.write(data["property_details"])

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### 🏷 Comps (Last 3)")
        st.dataframe(pd.DataFrame(data["sold_comps"]))
        st.markdown("### 💰 Offer Tiers")
        st.dataframe(result["Offers"])
    with col2:
        st.markdown("### 📊 Financial Metrics")
        st.metric("ARV", f"${result['ARV']}")
        st.metric("Rehab", f"${result['Rehab']}")
        st.metric("IRR", f"{result['IRR']:.0%}")
        st.metric("DSCR", result["DSCR"])
        st.metric("CoC Return", f"{result['CoC']:.0%}")
        st.success(f"Verdict: {result['Grade']}")

    st.markdown("### 📋 Investor Summary")
    st.markdown(f"""
**Address:** `{address}`  
**ARV:** `${result['ARV']}`  
**Rehab:** `${result['Rehab']}`  
**IRR:** `{result['IRR']:.0%}`  
**DSCR:** `{result['DSCR']}`  
**CoC Return:** `{result['CoC']:.0%}`  
**Grade:** **{result['Grade']}**
""")
