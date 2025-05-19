# Mock Zillow scraper
def scrape_zillow_data(address):
    return {
        "sold_comps": [
            {"address": "123 Elm St", "price": 190000, "sqft": 1430, "date": "2024-03"},
            {"address": "125 Oak St", "price": 198000, "sqft": 1450, "date": "2024-01"},
            {"address": "127 Pine St", "price": 185000, "sqft": 1400, "date": "2023-12"}
        ],
        "rent_zestimate": 1650,
        "property_details": {
            "sqft": 1432,
            "beds": 3,
            "baths": 2,
            "lot_size": 8500,
            "year_built": 1985,
            "condition": "Fair"
        }
    }