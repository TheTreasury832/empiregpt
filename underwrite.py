
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class UnderwriteRequest(BaseModel):
    address: str

@app.post("/api/underwrite")
def underwrite_property(payload: UnderwriteRequest):
    address = payload.address
    sqft = random.randint(1300, 1600)
    arv = sqft * random.randint(120, 150)
    irr = round(random.uniform(0.14, 0.21), 2)
    dscr = round(random.uniform(1.2, 1.7), 2)
    coc = round(random.uniform(0.08, 0.18), 2)
    grade = "A – Strong" if irr > 0.18 else "B – Review" if irr > 0.14 else "C – Weak"

    offers = [
        {"tier": "Low", "offer": round(arv * 0.72), "total": round(arv * 0.75), "verdict": "Strong"},
        {"tier": "Medium", "offer": round(arv * 0.78), "total": round(arv * 0.80), "verdict": "Review"},
        {"tier": "High", "offer": round(arv * 0.83), "total": round(arv * 0.85), "verdict": "Caution"},
    ]

    return {
        "text": f"EmpireGPT analyzed {address} and estimated an ARV of ${arv}.",
        "arv": arv,
        "irr": irr * 100,
        "dscr": dscr,
        "coc": coc * 100,
        "grade": grade,
        "offers": offers
    }
