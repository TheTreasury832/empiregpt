def scrape_zillow_data(address):
    # Simulated Zillow data for testing
    return {
        "rent_zestimate": 1600,
        "sold_comps": [
            {"price": 195000, "sqft": 1400, "date": "2024-01"},
            {"price": 202000, "sqft": 1450, "date": "2024-03"},
            {"price": 188000, "sqft": 1390, "date": "2023-11"},
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