import schedule
import time

def job():
    print("Scheduled task running...")

def run_scheduler():
    """
    Runs a scheduler that executes a job at fixed intervals.
    """
    schedule.every(10).minutes.do(job) 

    while True:
        schedule.run_pending()
        time.sleep(1)
