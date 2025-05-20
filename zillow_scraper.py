
def scrape_zillow_data(address):
    return {
        "rent_zestimate": 1650,
        "sold_comps": [
            {"address": "123 Elm St", "price": 190000, "sqft": 1430},
            {"address": "125 Oak St", "price": 198000, "sqft": 1450},
            {"address": "127 Pine St", "price": 185000, "sqft": 1400}
        ],
        "property_details": {
            "beds": 3,
            "baths": 2,
            "sqft": 1432,
            "lot_size": 8500,
            "year_built": 1985,
            "condition": "Fair"
        }
    }
