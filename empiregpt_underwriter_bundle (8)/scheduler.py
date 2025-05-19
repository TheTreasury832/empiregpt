from apscheduler.schedulers.blocking import BlockingScheduler
from output_writers.summary_email import send_summary_email

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='sun', hour=9)
def weekly_report():
    print("Sending weekly summary email...")
    send_summary_email(format="html")

if __name__ == "__main__":
    scheduler.start()