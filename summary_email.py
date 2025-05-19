import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from datetime import datetime

def send_summary_email(format="plain"):
    path = "logs/deal_history.csv"
    if not os.path.exists(path):
        return "No log file found."

    df = pd.read_csv(path)
    count = len(df)
    avg_irr = df["irr"].mean()
    grade_counts = df["grade"].value_counts().to_dict()

    html = f"""
    <h3>EmpireGPT Weekly Deal Summary - {datetime.now().date()}</h3>
    <ul>
        <li>Total Deals: {count}</li>
        <li>Avg IRR: {avg_irr:.2%}</li>
        <li>Grade Breakdown: {grade_counts}</li>
    </ul>
    """
    plain = f"""
    EmpireGPT Weekly Deal Summary - {datetime.now().date()}
    ---------------------------------------
    Total Deals: {count}
    Avg IRR: {avg_irr:.2%}
    Grade Breakdown: {grade_counts}
    """

    body = html if format == "html" else plain
    msg = MIMEText(body, "html" if format == "html" else "plain")
    msg["Subject"] = "📊 EmpireGPT Deal Summary"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 587))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
            print("Summary email sent.")
    except Exception as e:
        print("Failed to send summary:", e)