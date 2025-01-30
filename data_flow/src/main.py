import logging
import uvicorn
import time

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
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


app = FastAPI()

@app.get("/health")
def health_check():
    """Returns Prometheus-compatible health metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

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
    except Exception as e:
        logging.error(f"Error during scraping and sending data: {e}")

def start_scheduler():
    """
    Run the scheduler to scrape data every 5 minutes.
    """
    logging.info("Starting scheduler for scraping every 1 minutes.")
    schedule_task(run_scraper, interval=1) 
    
def start_uvicorn():
    """Start Uvicorn server in a separate thread."""
    uvicorn.run(app, host="0.0.0.0", port=5000)

def main():
    """
    Run both producer (scraper) and consumer concurrently using threads.
    """
    init_db()

    ochestrator = [
        (start_scheduler, ()),  
        (run_consumer, (process_data,)),
        (start_uvicorn, ()) 

    ]

    run_in_threads(ochestrator, timeout=None)



if __name__ == "__main__":
    init_db()
    main()
