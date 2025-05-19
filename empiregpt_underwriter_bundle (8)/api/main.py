from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from pydantic import BaseModel
import pandas as pd
import io
import os
from scrapers.zillow_scraper import scrape_zillow_data
from calculators.financial_model import calculate_financials
from calculators.offer_logic import generate_offers
from calculators.deal_grader import grade_deal
from output_writers.email_alert import alert_strong_deal
from core.logger import log_deal_all

API_KEY = os.getenv("API_KEY", "changeme")

def check_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

app = FastAPI()

class PropertyRequest(BaseModel):
    address: str
    rehab_cost: float = 30000

@app.post("/underwrite")
def underwrite(request: PropertyRequest, x_api_key: str = Header(...)):
    check_key(x_api_key)
    data = scrape_zillow_data(request.address)
    arv = sum(c["price"] for c in data["sold_comps"]) / len(data["sold_comps"])
    offers = generate_offers(arv, rehab_cost=request.rehab_cost)
    offer = offers["low"]
    fin = calculate_financials(offer, data["rent_zestimate"], 2400, 950, rehab_cost=request.rehab_cost)
    grade, verdict = grade_deal(fin["IRR"], fin["DSCR"], fin["CoC Return"])
    result = {
        "address": request.address,
        "arv": arv,
        "strategy": "Cash",
        "cash_flow": fin["NOI"] / 12 - fin["Monthly Payment"],
        "irr": fin["IRR"],
        "cap_rate": fin["Cap Rate"],
        "dscr": fin["DSCR"],
        "grade": verdict
    }
    alert_strong_deal(result)
    log_deal_all(result)
    return result

@app.post("/batch")
def batch_underwrite(file: UploadFile = File(...), x_api_key: str = Header(...)):
    check_key(x_api_key)
    content = file.file.read().decode("utf-8")
    df = pd.read_csv(io.StringIO(content))
    results = []
    for addr in df["address"]:
        data = scrape_zillow_data(addr)
        arv = sum(c["price"] for c in data["sold_comps"]) / len(data["sold_comps"])
        offers = generate_offers(arv, rehab_cost=30000)
        offer = offers["low"]
        fin = calculate_financials(offer, data["rent_zestimate"], 2400, 950, rehab_cost=30000)
        grade, verdict = grade_deal(fin["IRR"], fin["DSCR"], fin["CoC Return"])
        result = {
            "address": addr,
            "arv": arv,
            "strategy": "Cash",
            "cash_flow": fin["NOI"] / 12 - fin["Monthly Payment"],
            "irr": fin["IRR"],
            "cap_rate": fin["Cap Rate"],
            "dscr": fin["DSCR"],
            "grade": verdict
        }
        alert_strong_deal(result)
        log_deal_all(result)
        results.append(result)
    return results