import logging
from run_scrapers import run_all_scrapers
from scrapers.normalize import DataNormalizer
from kafka_helper.producer import send_to_kafka
from kafka_helper.consumer import run_consumer
from kafka_helper.process_data import process_data
from utils.data_validation import validate_data
from config.logging_config import setup_logging
from utils.scheduler import run_scheduler as schedule_task
from utils.threading import run_in_threads
from dbConfig import init_db

def run_scraper():
    """
    Main entry point for the scraper. Scrapes, normalizes, validates, and sends data to Kafka.
    """
    setup_logging()
    logging.info("Starting scrapers...")

    try:
        combined_data = run_all_scrapers()
        normalizer = DataNormalizer(combined_data)
        normalized_data = normalizer.normalize_data()
        validate_data(normalized_data)
        send_to_kafka(normalized_data)
    except Exception as e:
        logging.error(f"Error during scraping and sending data: {e}")

def start_scheduler():
    """
    Run the scheduler to scrape data every 1 minute.
    """
    schedule_task(run_scraper, interval=1) 

def main():
    """
    Run both producer (scraper) and consumer concurrently using threads.
    """
    init_db()

    orchestrator = [
        (start_scheduler, ()),
        (run_consumer, (process_data,))
    ]

    run_in_threads(orchestrator)


if __name__ == "__main__":
    run_scraper()
