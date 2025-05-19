import streamlit as st
from scrapers.zillow_scraper import scrape_zillow_data

st.set_page_config(page_title="EmpireGPT", layout="wide")
st.title("🏠 EmpireGPT Underwriter")

address = st.text_input("Enter a property address", "123 Main St")

def compute_average_ppsqft(sold_comps):
    return sum(c["price"] / c["sqft"] for c in sold_comps) / len(sold_comps)

def estimate_arv(avg_ppsqft, subject_sqft):
    return round(avg_ppsqft * subject_sqft, -2)

def calculate_rehab_cost(year_built):
    age = 2025 - year_built
    base = 20000
    if age > 30:
        base += 10000
    return base

def estimate_offers(arv, rehab):
    low = arv * 0.75 - rehab
    med = arv * 0.80 - rehab
    high = arv * 0.85 - rehab
    return {
        "Low Offer": round(low, -2),
        "Medium Offer": round(med, -2),
        "High Offer": round(high, -2)
    }

def grade_deal(irr, dscr, coc):
    if irr >= 0.18 and dscr >= 1.5 and coc >= 0.12:
        return "A – Strong"
    elif irr >= 0.14 and dscr >= 1.25:
        return "B – Review"
    elif irr >= 0.10 and dscr >= 1.1:
        return "C – Weak"
    else:
        return "D – Reject"

if address:
    data = scrape_zillow_data(address)
    st.subheader("📊 Property Summary")
    st.json(data["property_details"])

    avg_ppsqft = compute_average_ppsqft(data["sold_comps"])
    arv = estimate_arv(avg_ppsqft, data["property_details"]["sqft"])
    rehab = calculate_rehab_cost(data["property_details"]["year_built"])
    offers = estimate_offers(arv, rehab)

    st.subheader("💰 Offer Tiers")
    st.write(offers)

    # Fake IRR logic for example
    rent = data["rent_zestimate"]
    net = rent * 12 - 2400 - 950 - (0.05 * rent * 12)
    dscr = round(net / (offers["Low Offer"] * 0.08), 2)
    coc = round((net / offers["Low Offer"]), 2)
    irr = 0.17  # Mock

    grade = grade_deal(irr, dscr, coc)

    st.subheader("📈 Financial Metrics")
    st.write({
        "ARV": arv,
        "Rehab Estimate": rehab,
        "IRR (mock)": f"{irr:.2%}",
        "DSCR": dscr,
        "CoC Return": f"{coc:.2%}",
        "Grade": grade
    })

    st.subheader("📝 Verdict Summary")
    st.markdown(f"""
**Address**: `{address}`  
**ARV**: `${arv}`  
**Rehab**: `${rehab}`  
**IRR**: `{irr:.2%}`  
**DSCR**: `{dscr}`  
**CoC Return**: `{coc:.2%}`  
**Verdict**: **{grade}**
""")