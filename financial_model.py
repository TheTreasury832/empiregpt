import numpy_financial as npf

def calculate_financials(offer, rent, taxes, insurance, mgmt_pct=0.08, vacancy=0.05, rate=0.06, term=30, rehab_cost=0):
    loan_amount = offer
    monthly_pmt = npf.pmt(rate/12, term*12, -loan_amount)
    net_rent = rent - taxes/12 - insurance/12 - (rent * mgmt_pct) - (rent * vacancy)
    noi = net_rent * 12
    cap_rate = noi / offer
    annual_debt_service = monthly_pmt * 12
    dscr = noi / annual_debt_service
    cash_flow = net_rent - monthly_pmt
    coc_return = (cash_flow * 12) / (rehab_cost + offer * 0.1)
    irr = npf.irr([-rehab_cost - offer * 0.1] + [cash_flow * 12] * 5 + [offer * 1.25])
    return {
        "Monthly Payment": monthly_pmt,
        "NOI": noi,
        "Cap Rate": cap_rate,
        "DSCR": dscr,
        "IRR": irr,
        "CoC Return": coc_return
    }