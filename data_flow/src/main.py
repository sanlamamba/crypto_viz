import logging
import time
from prometheus_client import Counter, Gauge, start_http_server
from scrapers.coingecko_scraper import scrape_coingecko
from scrapers.coinmarketcap_scraper import scrape_coinmarketcap
from scrapers.normalize import DataNormalizer
from kafka_helper.producer import send_to_kafka
from kafka_helper.consumer import run_consumer
from kafka_helper.process_data import process_data
from utils.retry import retry_on_failure
from utils.data_validation import validate_data
from config.logging_config import setup_logging
from utils.scheduler import run_scheduler as schedule_task
from utils.threading import run_in_threads
from dbConfig import init_db

# Prometheus Metrics
SCRAPING_SUCCESS_COUNT = Counter('scraping_success_count', 'Number of successful scraping operations')
SCRAPING_FAILURE_COUNT = Counter('scraping_failure_count', 'Number of failed scraping operations')
KAFKA_SEND_SUCCESS_COUNT = Counter('kafka_send_success_count', 'Number of messages successfully sent to Kafka')
KAFKA_SEND_FAILURE_COUNT = Counter('kafka_send_failure_count', 'Number of messages failed to send to Kafka')
ACTIVE_THREADS = Gauge('active_threads', 'Number of active threads')

def run_scraper():
    """
    Main entry point for the scraper. Scrapes, normalizes, validates, and sends data to Kafka.
    """
    setup_logging()
    logging.info("Starting scrapers...")

    try:
        coingecko_data = retry_on_failure(scrape_coingecko)
        coinmarketcap_data = retry_on_failure(scrape_coinmarketcap)

        combined_data = coinmarketcap_data + coingecko_data

        normalizer = DataNormalizer(combined_data)
        normalized_data = normalizer.normalize_data()
        
        validate_data(normalized_data)
        send_to_kafka(normalized_data)
        logging.info("Data successfully sent to Kafka.")
        
        # Update Prometheus metrics
        SCRAPING_SUCCESS_COUNT.inc()
        KAFKA_SEND_SUCCESS_COUNT.inc()
    except Exception as e:
        logging.error(f"Error during scraping and sending data: {e}")
        # Update Prometheus metrics
        SCRAPING_FAILURE_COUNT.inc()
        KAFKA_SEND_FAILURE_COUNT.inc()

def start_scheduler():
    """
    Run the scheduler to scrape data every 1 minute.
    """
    logging.info("Starting scheduler for scraping every 1 minute.")
    schedule_task(run_scraper, interval=1) 

def main():
    """
    Run both producer (scraper) and consumer concurrently using threads.
    """
    init_db()
    
    # Start Prometheus HTTP server for metrics on port 5000
    start_http_server(5000)
    logging.info("Prometheus metrics server started on port 5000")

    ochestrator = [
        (start_scheduler, ()),  
        (run_consumer, (process_data,)) 
    ]

    # Update active threads metric in real-time
    ACTIVE_THREADS.set(len(ochestrator))
    
    run_in_threads(ochestrator)

if __name__ == "__main__":
    init_db()
    main()
