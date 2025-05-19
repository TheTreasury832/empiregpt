import os
import requests

def push_to_airtable(deal):
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE")
    api_key = os.getenv("AIRTABLE_API_KEY")

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"fields": deal}

    try:
        r = requests.post(url, json=payload, headers=headers)
        print("Airtable response:", r.status_code)
    except Exception as e:
        print("Airtable push failed:", e)