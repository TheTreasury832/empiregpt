def generate_offers(arv, rehab_cost):
    return {
        "low": arv * 0.75 - rehab_cost,
        "medium": arv * 0.80 - rehab_cost,
        "high": arv * 0.85 - rehab_cost
    }