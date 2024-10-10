import schedule
import time
import logging

def run_scheduler(job, interval):
    """
    Runs a scheduler that executes a job at fixed intervals.
    
    :param job: The function to run.
    :param interval: The interval in minutes at which the job should be run.
    """
    schedule.every(interval).minutes.do(job)  # Schedule the job
    logging.info(f"Scheduler set to run job every {interval} minutes.")

    try:
        while True:
            schedule.run_pending()  # Run scheduled jobs
            logging.info("Waiting for the next scheduled job...")
            time.sleep(1) 
    except KeyboardInterrupt:
        logging.info("Scheduler stopped.")
    except Exception as e:
        logging.error(f"Error in scheduler: {e}")
