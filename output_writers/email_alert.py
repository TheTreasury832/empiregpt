import smtplib
import os

def alert_strong_deal(deal):
    msg = f"Subject: 🚨 EmpireGPT Deal Alert\n\n{deal}"

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("EMAIL_FROM")
    receiver_email = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASS")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg)
    except Exception as e:
        print("Alert email failed:", e)