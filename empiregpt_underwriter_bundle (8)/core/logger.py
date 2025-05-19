import os
import json
import csv

def log_deal_all(deal):
    os.makedirs("logs", exist_ok=True)

    # JSON log
    with open("logs/deal_history.json", "a") as f:
        f.write(json.dumps(deal) + "\n")

    # CSV log
    csv_path = "logs/deal_history.csv"
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=deal.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(deal)