import os
import requests

def push_to_gohighlevel(deal):
    api_key = os.getenv("GOHIGHLEVEL_API_KEY")
    contact_url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    contact = {
        "firstName": deal.get("address"),
        "customField": {
            "grade": deal.get("grade"),
            "irr": deal.get("irr"),
            "dscr": deal.get("dscr")
        }
    }

    try:
        r = requests.post(contact_url, json=contact, headers=headers)
        print("GoHighLevel response:", r.status_code)
    except Exception as e:
        print("GoHighLevel push failed:", e)